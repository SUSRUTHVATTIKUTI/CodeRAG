import os
import faiss
import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from typing import List

ENCODER_PATH = "./CodeRAG_encoder"
DATASET_NAME = "gretelai/synthetic_text_to_sql"
DATASET_SPLIT = "train"
INDEX_FILE = "sql_rag_faiss_index.bin"
CORPUS_MAP_FILE = "sql_rag_corpus_map.npy"

def load_encoder(path: str) -> SentenceTransformer:
    """Loads the fine-tuned encoder model."""
    print(f"Loading Sentence Transformer from: {path}")
    return SentenceTransformer(path)


def load_data(name: str, split: str):
    """Loads the Hugging Face dataset and extracts relevant columns."""
    print(f"Loading dataset: {name}, split: {split}")
    ds = load_dataset(name, split=split)

    required_cols = {'sql_prompt', 'sql_context', 'sql'}
    if not required_cols.issubset(set(ds.column_names)):
        raise ValueError(f"Dataset must contain columns: {required_cols}")

    return ds

def create_corpus(ds) -> List[str]:
    """
    Creates the document chunks (corpus) by combining the database context and the SQL query.

    The retriever will search this text.
    The query will be the 'sql_prompt' (the natural language question).
    """
    print("Preparing corpus documents...")
    corpus_documents = []
    for row in tqdm(ds, desc="Processing documents"):
        document = f"DATABASE CONTEXT:\n{row['sql_context']}\n---\nSQL QUERY:\n{row['sql']}"
        corpus_documents.append(document)

    print(f"Total documents prepared: {len(corpus_documents)}")
    return corpus_documents

def build_faiss_index(model: SentenceTransformer, corpus: List[str]):
    """
    Generates embeddings for the corpus and builds a FAISS index.
    """
    print("Generating embeddings (This may take a while)...")

    corpus_embeddings = model.encode(
        corpus,
        convert_to_numpy=True,
        normalize_embeddings=True,  # Critical for cosine similarity search
        show_progress_bar=True
    ).astype('float32') 
    emb_dim = corpus_embeddings.shape[1]
    print(f"Embedding dimension: {emb_dim}")

    print("Building FAISS Index (IndexFlatIP for Inner Product/Cosine Similarity)...")
    index = faiss.IndexFlatIP(emb_dim)
    index.add(corpus_embeddings)

    # Save the index and corpus mapping
    faiss.write_index(index, INDEX_FILE)
    np.save(CORPUS_MAP_FILE, np.array(corpus))

    print(f"FAISS index saved to: {INDEX_FILE}")
    print(f"Corpus map saved to: {CORPUS_MAP_FILE}")

def main():
    try:
        model = load_encoder(ENCODER_PATH)
        ds = load_data(DATASET_NAME, DATASET_SPLIT)

        corpus_documents = create_corpus(ds)

        build_faiss_index(model, corpus_documents)

        print("\n Retrieval Indexing Complete.")
        print("You can now proceed to the LLM generation step using these saved files.")

    except FileNotFoundError:
        print(f"\n[ERROR] Encoder not found at {ENCODER_PATH}. Please ensure your fine-tuned model is saved there.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()