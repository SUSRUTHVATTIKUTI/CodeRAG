import os
import argparse
import time
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import torch
import sys


DEFAULT_CSV = "/mnt/data/CodeRAG_Dataset.csv" if os.path.exists("/mnt/data/CodeRAG_Dataset.csv") else "CodeRAG_Dataset.csv"
FALLBACK_PUBLIC_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def detect_encoding_bytes(bs: bytes) -> Optional[str]:
    """
    Try to detect encoding from raw bytes. Prefer chardet if installed.
    """
    try:
        import chardet
        det = chardet.detect(bs)
        enc = det.get("encoding")
        if enc:
            return enc
    except Exception:
        pass
    return None

def load_csv(csv_path: str) -> pd.DataFrame:
    """
    Loads CSV with robust encoding detection and fallbacks.
    Ensures required columns exist and drops rows with missing query/pos.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Read a chunk of bytes for detection
    with open(csv_path, "rb") as f:
        raw = f.read(65536)  # read first 64KB for detection

    enc = detect_encoding_bytes(raw)
    tried_encodings = []
    if enc:
        tried_encodings.append(enc)

    # common fallbacks (ordered)
    fallback_list = ["utf-8", "utf-8-sig", "cp1252", "latin1", "iso-8859-1"]
    for e in fallback_list:
        if e not in tried_encodings:
            tried_encodings.append(e)

    last_exc = None
    for enc_try in tried_encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc_try)
            print(f"[info] Detected/used CSV encoding: {enc_try}")
            break
        except Exception as e:
            last_exc = e
    else:
        raise UnicodeDecodeError("csv", b"", 0, 1, f"Unable to decode CSV with tried encodings: {tried_encodings}. Last error: {last_exc}")

    required = {"prompt", "query", "pos", "neg"}
    if not required.issubset(set(df.columns)):
        raise ValueError(f"CSV must include columns: {required}. Found columns: {list(df.columns)}")

    df = df.dropna(subset=["query", "pos"])  
    df = df.reset_index(drop=True)
    return df

def create_examples(df: pd.DataFrame, use_neg_pairs: bool = True) -> List[InputExample]:
    examples: List[InputExample] = []
    for _, row in df.iterrows():
        q = str(row["query"])
        pos = str(row["pos"])
        examples.append(InputExample(texts=[q, pos]))
        if use_neg_pairs and not pd.isna(row.get("neg")):
            neg = str(row["neg"])
            examples.append(InputExample(texts=[q, neg]))
    return examples

def sample_hard_negatives(model: SentenceTransformer, df: pd.DataFrame, num_neg_per_query: int = 1) -> Dict[int, List[str]]:
    """
    Mine hard negatives from 'pos' column across dataset using current model.
    Returns dict: row_index -> list of hard negative strings.
    NOTE: requires faiss installed.
    """
    corpus = list(df["pos"].astype(str).unique())
    corpus_embeddings = model.encode(corpus, normalize_embeddings=True, show_progress_bar=False)
    idx_map = {i: c for i, c in enumerate(corpus)}
    queries = [str(q) for q in df["query"].tolist()]
    q_emb = model.encode(queries, normalize_embeddings=True, show_progress_bar=False)
    hard_negatives = {}
    try:
        import faiss
    except Exception as e:
        raise RuntimeError("faiss is required for hard negative mining. Install faiss and retry.") from e
    d = int(corpus_embeddings.shape[1])
    index = faiss.IndexFlatIP(d)
    index.add(np.array(corpus_embeddings, dtype="float32"))
    k = min(len(corpus), 1 + num_neg_per_query + 1)
    scores, ids = index.search(np.array(q_emb, dtype="float32"), k=k)
    for i, row in enumerate(df.itertuples()):
        found = []
        for idx in ids[i]:
            cand = idx_map[int(idx)]
            if cand == str(row.pos):
                continue
            found.append(cand)
            if len(found) >= num_neg_per_query:
                break
        hard_negatives[i] = found
    return hard_negatives

def load_sentence_transformer(base_model: str, device: Optional[str] = None) -> SentenceTransformer:
    """
    Tries to load the requested base_model. If it fails (e.g., gated/private repo),
    falls back to a public model defined by FALLBACK_PUBLIC_MODEL.
    Uses HUGGINGFACE_HUB_TOKEN or HF_API_TOKEN env var if present.
    """
    hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_API_TOKEN") or None
    try:
        print(f"[info] Attempting to load base model: {base_model}")
        model = SentenceTransformer(base_model, use_auth_token=hf_token)
        if device:
            model.to(device)
        print(f"[info] Successfully loaded model: {base_model}")
        return model
    except Exception as e:
        print(f"[warning] Failed to load requested model '{base_model}': {e}", file=sys.stderr)
        print("[warning] This may mean the model is private/gated or you are not authenticated.", file=sys.stderr)
        print("[warning] If you have access, run `huggingface-cli login` or set env var HUGGINGFACE_HUB_TOKEN.", file=sys.stderr)
        print(f"[info] Falling back to public model: {FALLBACK_PUBLIC_MODEL}")
        try:
            model = SentenceTransformer(FALLBACK_PUBLIC_MODEL)
            if device:
                model.to(device)
            print(f"[info] Loaded fallback model: {FALLBACK_PUBLIC_MODEL}")
            return model
        except Exception as e2:
            print(f"[error] Failed to load fallback model '{FALLBACK_PUBLIC_MODEL}': {e2}", file=sys.stderr)
            raise RuntimeError("Unable to load any sentence-transformer model. Check internet / HF token.") from e2

def fine_tune_encoder(
    csv_path: str,
    base_model: str,
    output_dir: str,
    epochs: int = 2,
    batch_size: int = 8,
    lr: float = 2e-5,
    checkpoint_every_steps: int = 200,
    use_hard_negative_mining: bool = False,
    device: Optional[str] = None
):
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[info] device: {device}")

    df = load_csv(csv_path)
    print(f"[info] Loaded {len(df)} rows from {csv_path}; columns: {list(df.columns)}")
    print("[info] Sample rows (first 5):")
    print(df.head(5).to_string(index=False))

    examples = create_examples(df, use_neg_pairs=True)
    print(f"[info] Created {len(examples)} InputExamples (including negatives).")

    model = load_sentence_transformer(base_model, device=device)
    emb_dim = model.get_sentence_embedding_dimension()
    print(f"[info] Embedding dim: {emb_dim}")

    hard_negatives = {}
    if use_hard_negative_mining:
        print("[info] Mining hard negatives (this may take a while)...")
        hard_negatives = sample_hard_negatives(model, df, num_neg_per_query=1)
        for idx, neg_list in hard_negatives.items():
            q = str(df.loc[idx, "query"])
            for neg_txt in neg_list:
                examples.append(InputExample(texts=[q, neg_txt]))
        print(f"[info] Added {sum(len(v) for v in hard_negatives.values())} mined negatives.")

    train_dataloader = DataLoader(examples, shuffle=True, batch_size=batch_size)
    train_loss = losses.MultipleNegativesRankingLoss(model=model)

    steps_per_epoch = max(1, len(train_dataloader))
    total_steps = steps_per_epoch * epochs
    warmup_steps = max(10, int(0.1 * total_steps))
    print(f"[info] epochs={epochs}, batch_size={batch_size}, total_steps={total_steps}, warmup_steps={warmup_steps}")

    os.makedirs(output_dir, exist_ok=True)
    start_time = time.time()
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=warmup_steps,
        show_progress_bar=True,
        output_path=output_dir
    )
    elapsed = time.time() - start_time
    print(f"[info] Training completed in {elapsed:.1f}s. Model saved to {output_dir}")
    return model, df

def eval_recall_at_k(model: SentenceTransformer, df: pd.DataFrame, k_list=[1,3,5]):
    corpus = list(df["pos"].astype(str).unique())
    corpus_emb = model.encode(corpus, normalize_embeddings=True, show_progress_bar=False)
    queries = [str(q) for q in df["query"].tolist()]
    q_emb = model.encode(queries, normalize_embeddings=True, show_progress_bar=False)
    try:
        import faiss
    except Exception as e:
        raise RuntimeError("faiss is required for recall evaluation. Install faiss and retry.") from e
    d = int(corpus_emb.shape[1])
    index = faiss.IndexFlatIP(d)
    index.add(np.array(corpus_emb, dtype="float32"))
    scores, ids = index.search(np.array(q_emb, dtype="float32"), k=max(k_list))
    results = {}
    for k in k_list:
        hits = 0
        for i, row in df.iterrows():
            gt = str(row["pos"])
            retrieved = [corpus[idx] for idx in ids[i,:k] if idx < len(corpus)]
            if gt in retrieved:
                hits += 1
        results[k] = hits / len(df)
    return results

def parse_args():
    p = argparse.ArgumentParser(description="Train retrieval encoder (CodeRAG) from CSV named CodeRAG_Dataset.csv")
    p.add_argument("--base_model", type=str, default="BAAI/bge-code-large-en", help="Base SentenceTransformer model")
    p.add_argument("--output_dir", type=str, default="CodeRAG_encoder", help="Where to save the fine-tuned encoder")
    p.add_argument("--epochs", type=int, default=2)
    p.add_argument("--batch_size", type=int, default=8)
    p.add_argument("--lr", type=float, default=2e-5)
    p.add_argument("--checkpoint_every_steps", type=int, default=200)
    p.add_argument("--use_hard_negatives", action="store_true", help="Mine and use hard negatives before training (slow)")
    p.add_argument("--device", type=str, default=None, help="Device override, e.g. 'cpu' or 'cuda'")
    return p.parse_args()

def main():
    args = parse_args()
    csv_path = DEFAULT_CSV
    try:
        model, df = fine_tune_encoder(
            csv_path=csv_path,
            base_model=args.base_model,
            output_dir=args.output_dir,
            epochs=args.epochs,
            batch_size=args.batch_size,
            lr=args.lr,
            checkpoint_every_steps=args.checkpoint_every_steps,
            use_hard_negative_mining=args.use_hard_negatives,
            device=args.device
        )
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)

    print("[info] Running quick evaluation (Recall@1,3,5)...")
    try:
        results = eval_recall_at_k(model, df, k_list=[1,3,5])
        for k,v in results.items():
            print(f"Recall@{k}: {v*100:.2f}%")
    except Exception as e:
        print(f"[warning] Evaluation failed: {e}", file=sys.stderr)

    print("[info] Done. Fine-tuned model folder:", args.output_dir)

if __name__ == "__main__":
    main()
