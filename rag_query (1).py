import os
import faiss
import numpy as np
import torch
from typing import List

from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer

ENCODER_PATH = "./CodeRAG_encoder"
INDEX_FILE = "sql_rag_faiss_index.bin"
CORPUS_MAP_FILE = "sql_rag_corpus_map.npy"

LLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

device = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if device == "cuda" else torch.float32


def load_rag_components(encoder_path, index_file, corpus_map_file, llm_name):
    """Loads the encoder, FAISS index, corpus, LLM, and tokenizer from disk."""
    print(f" Loading RAG Components onto {device}...")

    if not os.path.exists(index_file) or not os.path.exists(corpus_map_file):
        raise FileNotFoundError(
            f"Index files not found. Ensure {index_file} and {corpus_map_file} were successfully created by your indexing script."
        )

    encoder = SentenceTransformer(encoder_path)
    index = faiss.read_index(index_file)
    corpus = np.load(corpus_map_file, allow_pickle=True).tolist()

    llm_tokenizer = AutoTokenizer.from_pretrained(llm_name)

    llm_model = AutoModelForCausalLM.from_pretrained(
        llm_name,
        torch_dtype=DTYPE,
        device_map="auto" if device == "cuda" else None
    )
    if device == "cpu":
        llm_model.to(device)

    print(f" LLM loaded: {llm_name} | Index loaded with {index.ntotal} documents.")
    return encoder, index, corpus, llm_model, llm_tokenizer


def retrieve_context(query: str, encoder: SentenceTransformer, index: faiss.Index, corpus: List[str], top_k: int = 3) -> \
List[str]:
    """Encodes the query and searches the FAISS index for the top_k best documents."""

    query_emb = encoder.encode(query, convert_to_numpy=True, normalize_embeddings=True)
    query_emb = query_emb.astype(np.float32).reshape(1, -1)

    D, I = index.search(query_emb, top_k)

    retrieved_docs = [corpus[i] for i in I[0]]

    return retrieved_docs


def generate_answer(query: str, context: List[str], llm_model, llm_tokenizer) -> str:
    """Generates a final SQL query using the LLM based on the retrieved context."""

    context_str = "\n\n---\n\n".join([f"RETRIEVED CONTEXT {i + 1}:\n{doc}" for i, doc in enumerate(context)])

    prompt_template = f"""
    You are an expert Text-to-SQL code generator. Your goal is to generate a single, accurate SQL query.
    You MUST generate the SQL query ONLY using the tables and columns mentioned in the provided DATABASE CONTEXT.
    If the context is insufficient or irrelevant, state that you cannot generate the query.

    DATABASE CONTEXT:
    ---
    {context_str}
    ---

    USER QUESTION: {query}

    SQL QUERY:
    """

    formatted_prompt = f"<s>[INST] {prompt_template.strip()} [/INST]"

    inputs = llm_tokenizer(formatted_prompt, return_tensors="pt").to(device)

    with torch.no_grad(): 
        output = llm_model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,  
            num_beams=1,
            pad_token_id=llm_tokenizer.eos_token_id
        )

    generated_text = llm_tokenizer.decode(output[0], skip_special_tokens=True)

    answer_start = generated_text.rfind("[/INST]")
    if answer_start != -1:
        generated_text = generated_text[answer_start + len("[/INST]"):].strip()

    return generated_text


def main_rag_pipeline():
    user_query = "What is the average salary for all employees?"

    try:
        encoder, index, corpus, llm_model, llm_tokenizer = load_rag_components(
            ENCODER_PATH, INDEX_FILE, CORPUS_MAP_FILE, LLM_MODEL_NAME
        )

        print("\n" + "=" * 80)
        print(f"**RAG PIPELINE EXECUTION** | QUERY: {user_query}")

        retrieved_context = retrieve_context(user_query, encoder, index, corpus, top_k=3)
        print("\n🔍 Retrieval Complete. The following context was found for the LLM:")
        for doc in retrieved_context:
            print(f"  - Snippet: {doc.split('SQL QUERY:')[0].strip()[:100]}...")

        print("\n🧠 Generation in Progress...")
        final_sql_query = generate_answer(user_query, retrieved_context, llm_model, llm_tokenizer)

        print("\n" + "=" * 80)
        print("**FINAL RAG-AUGMENTED SQL QUERY:**")
        print("```sql")
        print(final_sql_query)
        print("```")
        print("Process complete. Now, run your evaluation against the baseline model!")

    except FileNotFoundError as e:
        print(f"\n[CRITICAL ERROR] {e}")
        print(
            "ACTION REQUIRED: Ensure 'CodeRAG_encoder', 'sql_rag_faiss_index.bin', and 'sql_rag_corpus_map.npy' are in the same directory.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        print(
            "ACTION REQUIRED: Check that all necessary libraries (PyTorch, FAISS, transformers) are installed correctly.")


if __name__ == "__main__":
    main_rag_pipeline()