import os 
from openai import OpenAI
import chromadb

class text_embedding():
    def __init__(self, file: str, model_config: dict):
        self.file = file
        self.model_config = model_config
        self.client = OpenAI(
                    api_key = self.model_config['api_key'],
                    base_url = self.model_config['base_url'],
                        )
        self.MODEL = self.model_config['model']
        # self.prompt = f"{self.model_config['instruction']}\n{self.model_config['query']}"
        self.chromadb_client = chromadb.PersistentClient("./chroma.db")
        self.chromadb_collection = self.chromadb_client.get_or_create_collection("Newton")


    def read_file(self) -> str:
        with open(self.file, 'r', encoding='utf-8') as f:
            return f.read()

    def get_chunks(self) -> list[str]:
        text = self.read_file()
        text_split = text.split("\n\n")
        
        chunks = []
        header = ''
        for c in text_split:
            if c.startswith("#"):
                header += f"{c}\n"
            else:
                chunks.append(f"{header}{c}")
                header = ''
        return chunks 
    
    def embed(self, text: str) -> list[float]:
        # embedding.data: list[Embedding]
        # embedding.data[0].embedding: list[float]
        embedding = self.client.embeddings.create(
            model = self.MODEL,
            input = text,
            dimensions = 1024,
            encoding_format='float'
        )
        assert embedding.data[0].embedding
        return embedding.data[0].embedding
    
    def create_db(self) -> None:
        for id, c in enumerate(self.get_chunks()):
            print(f"Processing:({id}:){c}")
            embedding = self.embed(c)
            self.chromadb_collection.upsert(
                ids = str(id),
                documents = c,
                embeddings = embedding
            )

    def search_db(self, query) -> list[str]:
        query_embedding = self.embed(query)
        result = self.chromadb_collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )
        assert result['documents']
        return result['documents'][0]
    



