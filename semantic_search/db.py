import chromadb
import hashlib
import os

DB_PATH = os.path.expanduser("~/.semantic_search/chromadb")
COLLECTION_NAME = "semantic_search"

client = None
collection = None


def get_collection():
    """Initialize ChromaDB client and return collection."""
    global client, collection
    if collection is not None:
        return collection

    os.makedirs(DB_PATH, exist_ok=True)
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # cosine similarity
    )
    return collection


def file_hash(file_path):
    """Generate MD5 hash of a file for duplicate detection."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def is_already_indexed(file_path, chunk_id):
    """Check if a specific chunk is already in ChromaDB."""
    col = get_collection()
    result = col.get(ids=[chunk_id])
    return len(result["ids"]) > 0


def store_embedding(chunk_id, vector, metadata):
    """Store a single embedding with metadata into ChromaDB."""
    col = get_collection()
    col.add(
        ids=[chunk_id],
        embeddings=[vector],
        metadatas=[metadata]
    )


def build_chunk_id(file_path, chunk_type, page=None):
    """Build a unique ID for each chunk."""
    h = file_hash(file_path)
    if page:
        return f"{h}_{chunk_type}_page{page}"
    return f"{h}_{chunk_type}"