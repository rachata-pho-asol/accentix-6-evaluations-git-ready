import chromadb
from google import genai
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
EMBEDDING_MODEL_ID = "gemini-embedding-001"

class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL_ID,
            contents=input,
            config=genai.types.EmbedContentConfig(
                task_type="retrieval_document",
            )
        )
        return response.embeddings[0].values # type: ignore

class AAXEvaluationDatabase:
    def __init__(self, path="./chromadb_data"):
        self.client = chromadb.PersistentClient(path=path)
        self.collections = {}
        # self.embedder = SentenceTransformer(model_name_or_path="intfloat/multilingual-e5-base")

    def add_collection(self, name):
        collection = self.client.get_or_create_collection(name=name, embedding_function=GeminiEmbeddingFunction())
        self.collections[name] = collection
        return collection

    def get_collection(self, name):
        return self.collections.get(name)

    def add_data(self, to_collection: str, from_csv: str):
        if to_collection not in self.collections:
            raise ValueError(f"Collection '{to_collection}' does not exist.")
        try:
            df = pd.read_csv(f'{from_csv}')
            df["document"] = df.apply(
                lambda row: f"หัวข้อ: {row['topic']}\n" +
                            f"ประเภทเจตนา: {row['intent_type']}\n" +
                            f"เนื้อหา: {row['text']}\n" +
                            f"สรุป: {row['conclude']}\n", axis=1
            )

            # embeddings = self.embedder.encode(df["document"].tolist(), convert_to_numpy=True, show_progress_bar=True)

            for i, d in enumerate(df["document"].tolist()):
                self.collections[to_collection].add(
                    ids=str(i),
                    documents=d
                )
            print(f"Data added to collection '{to_collection}' from '{from_csv}' successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to add data to collection '{to_collection}': {e}")

    def contains_data(self, collection_name: str) -> bool:
        if collection_name not in self.collections:
            return False
        try:
            count = self.collections[collection_name].count()
            return count > 0
        except Exception as e:
            raise RuntimeError(f"Failed to check data in collection '{collection_name}': {e}")

    def query_chroma(self, query_text: str, from_collection: str, n_results: int = 5):
        if from_collection not in self.collections:
            raise ValueError(f"Collection '{from_collection}' does not exist.")
        try:
            query_embeddings = client.models.embed_content(
                model=EMBEDDING_MODEL_ID,
                contents=query_text,
                config=genai.types.EmbedContentConfig(
                    task_type="retrieval_query",
                )
            )
            results = self.collections[from_collection].query(
                query_embeddings=query_embeddings.embeddings[0].values,
                n_results=n_results
            )
            return {
                "query": query_text,
                "results": [
                    {
                        "id": results["ids"][0][i],
                        "document": results["documents"][0][i],
                        "distance": results["distances"][0][i]
                    }
                    for i in range(len(results["ids"][0]))
                ]
            }
        except Exception as e:
            raise RuntimeError(f"Failed to query collection '{from_collection}': {e}")

