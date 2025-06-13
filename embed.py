import os 
from openai import OpenAI
import chromadb
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document


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

    def get_chunks_bysection_md(self) -> list[Document]:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on)
        final_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        text = self.read_file()
        md_header_splits = markdown_splitter.split_text(text)
        final_docs = []
        for chunk in md_header_splits:
            sub_chunks = final_splitter.split_text(chunk)
            for sub_chunk in sub_chunks:
                final_docs.append(chunk.model_copy(update={"page_content": sub_chunk}))
        return final_docs
    
    def create_db_withmetadata(self) -> None:
        for id, c in enumerate(self.get_chunks_bysection_md()):
            print(f"Processing:({id}:){c}")
            doc_withmetadata = ' > '.join(list(c.metadata.values())) + '\n' + c.page_content 
            embedding = self.embed(doc_withmetadata)
            self.chromadb_collection.upsert(
                ids = str(id),
                document = doc_withmetadata,
                embeddings = embedding,
                metadatas = c.metadata
            )


    def search_db_withmetadata(self, query: str, where: dict = None) -> list[str]:
        query_embedding = self.embed(query)
        result = self.chromadb_collection.query(
            query_embeddings=query_embedding,
            n_results=5,
            where = where or {}
        )
        assert result['documents']
        return result['documents'][0]
    



    def search_db(self, query: str) -> list[str]:
        query_embedding = self.embed(query)
        result = self.chromadb_collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )
        assert result['documents']
        return result['documents'][0]
    



