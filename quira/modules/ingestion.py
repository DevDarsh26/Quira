import time
import logging
import asyncio
import uuid
from typing import Any, List, Dict, Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

import numpy as np
import os
import csv

logger = logging.getLogger("quira.ingestion")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

from quira.providers.base import VectorStore

class DocumentIngestor:
    """
    quira Data Ingestion Module:
    Parses PDFs and raw text, chunks them intelligently with overlaps, 
    embeds them, and upserts them into the VectorStore for retrieval.
    """
    def __init__(self, vector_store: VectorStore, embed_func: Any):
        self.vector_store = vector_store
        self.embed_func = embed_func

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Splits text into chunks of `chunk_size` characters with `overlap` characters.
        """
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            # Break if this is the last chunk
            if end >= text_len:
                break
            start += chunk_size - overlap
            
        return chunks

    def extract_pdf_text(self, file_path: str) -> str:
        """
        Extracts all text from a PDF file using PyMuPDF.
        """
        if fitz is None:
            raise ImportError("PyMuPDF is not installed. Run `pip install pymupdf` to parse PDFs.")
            
        try:
            doc = fitz.open(file_path)
            full_text = []
            for page in doc:
                full_text.append(page.get_text())
            doc.close()
            return "\n".join(full_text)
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            raise

    def extract_docx_text(self, file_path: str) -> str:
        try:
            import docx  # type: ignore
        except ImportError:
            raise ImportError("python-docx is not installed. Run `pip install python-docx`")
        
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def extract_html_text(self, file_path: str) -> str:
        try:
            from bs4 import BeautifulSoup  # type: ignore
        except ImportError:
            raise ImportError("beautifulsoup4 is not installed. Run `pip install beautifulsoup4`")
        
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            return soup.get_text(separator="\n")

    def extract_csv_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return "\n".join([", ".join(row) for row in reader])

    def extract_markdown_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    async def ingest_text(self, user_id: str, text: str, chunk_size: int = 1000, overlap: int = 200) -> int:
        """
        Chunks text, generates embeddings, and upserts them to Qdrant.
        Returns the number of chunks processed.
        """
        if not text.strip():
            logger.warning(f"User {user_id}: Empty text provided for ingestion.")
            return 0

        chunks = self._chunk_text(text, chunk_size, overlap)
        logger.info(f"User {user_id}: Split text into {len(chunks)} chunks.")
        
        # We assume qdrant_client is either the official sync or async client
        # Create PointStructs
        try:
            from qdrant_client.models import PointStruct
        except ImportError:
            # Fallback if qdrant models are not available locally (e.g. mock mode)
            class PointStruct:
                def __init__(self, id, vector, payload):
                    self.id = id
                    self.vector = vector
                    self.payload = payload

        points = []
        for chunk in chunks:
            # Generate embedding
            emb = self.embed_func(chunk)
            if isinstance(emb, np.ndarray):
                emb_list = emb.tolist()
            else:
                emb_list = list(emb)
                
            chunk_id = str(uuid.uuid4())
            points.append(PointStruct(
                id=chunk_id,
                vector=emb_list,
                payload={
                    "text": chunk,
                    "embedding": emb_list,
                    "created_at": time.time(),
                    "source": "ingestion"
                }
            ))

        # Upsert into VectorStore
        collection_name = f"quira_{user_id}"
        logger.info(f"User {user_id}: Upserting {len(points)} chunks into collection '{collection_name}'...")
        
        try:
            points_to_upsert = [
                {
                    "id": p.id,
                    "vector": p.vector,
                    "payload": p.payload
                } for p in points
            ]
            await self.vector_store.upsert(
                collection_name=collection_name,
                points=points_to_upsert
            )
            logger.info(f"User {user_id}: Successfully ingested {len(points)} chunks.")
            return len(points)
        except Exception as e:
            logger.error(f"User {user_id}: Failed to upsert: {e}")
            raise

    async def ingest_pdf(self, user_id: str, file_path: str, chunk_size: int = 1000, overlap: int = 200) -> int:
        """
        Helper method to extract text from a PDF and ingest it in one go.
        """
        logger.info(f"User {user_id}: Extracting text from PDF '{file_path}'...")
        text = self.extract_pdf_text(file_path)
        return await self.ingest_text(user_id, text, chunk_size, overlap)

    async def ingest_file(self, user_id: str, file_path: str, chunk_size: int = 1000, overlap: int = 200) -> int:
        """
        Auto-detects file extension and routes it to the correct parser.
        """
        ext = os.path.splitext(file_path)[1].lower()
        logger.info(f"User {user_id}: Extracting text from '{file_path}'...")
        
        if ext == ".pdf":
            text = self.extract_pdf_text(file_path)
        elif ext == ".docx":
            text = self.extract_docx_text(file_path)
        elif ext in [".html", ".htm"]:
            text = self.extract_html_text(file_path)
        elif ext == ".csv":
            text = self.extract_csv_text(file_path)
        elif ext in [".md", ".markdown", ".txt"]:
            text = self.extract_markdown_text(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
            
        return await self.ingest_text(user_id, text, chunk_size, overlap)
