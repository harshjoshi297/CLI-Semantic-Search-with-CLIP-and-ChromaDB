# CLI Semantic Search

Search your images and documents using natural language — powered by CLIP and ChromaDB.


Demo link - https://youtu.be/q9FBwY6K-PQ

```bash
sem-index --path ~/Pictures
sem-search --query "a dog running in a field" --type image
```

---

## What it does

**`sem-index`** recursively walks a directory, embeds every supported file using OpenAI's CLIP model, and stores the vectors in a persistent ChromaDB database on disk.

**`sem-search`** takes a natural language query, embeds it using the same CLIP model, and performs a similarity search against the indexed database — returning the most relevant files ranked by score.

Because CLIP is multimodal, the same text query can match both images and document content. Searching for `"vaccination certificate"` will surface a scanned PDF. Searching for `"a tiger in the jungle"` will surface the right photo.

---

## Supported file types

| Type | How it's handled |
|---|---|
| `.jpg`, `.jpeg`, `.png` | Embedded as image via CLIP image encoder |
| `.pdf` | Each page embedded as image + text extracted and embedded separately |

---

## Installation

**Requirements:** Python 3.10+

```bash
# Clone the repo
git clone https://github.com/harshjoshi297/CLI-Semantic-Search-with-CLIP-and-ChromaDB.git
cd CLI-Semantic-Search-with-CLIP-and-ChromaDB

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install CLI commands
pip install -e .
```

On first run, the CLIP model (~350MB) will be downloaded automatically.

---

## Usage

### Index a directory

```bash
sem-index --path /path/to/your/folder
```

Runs recursively. Skips files already indexed (duplicate detection via MD5 hash). The database is stored globally at `~/.semantic_search/chromadb` — index multiple folders and search across all of them.

```bash
# Index multiple folders over time
sem-index --path ~/Pictures
sem-index --path ~/Documents
sem-index --path ~/Downloads
```

### Search

```bash
# Search images
sem-search --query "a happy woman smiling" --type image

# Search document text
sem-search --query "machine learning engineer" --type text

# Return more results
sem-search --query "signature" --type image --top 10
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--query` | required | Natural language search query |
| `--type` | `image` | `image` or `text` |
| `--top` | `5` | Number of results to return |

### Example output

```
Searching for: 'a dog' (type: image)

Top 3 results:

  1. dog.png
     Type    : image
     Score   : 0.2662
     Path    : /home/harsh/Pictures/dog.png

  2. Tiger_HD.jpg
     Type    : image
     Score   : 0.1830
     Path    : /home/harsh/Pictures/Tiger_HD.jpg

  3. happywoman.png
     Type    : image
     Score   : 0.1825
     Path    : /home/harsh/Pictures/happywoman.png
```

---

## Project structure

```
CLI-Semantic-Search/
├── semantic_search/
│   ├── __init__.py
│   ├── index.py       # sem-index CLI command
│   ├── search.py      # sem-search CLI command
│   ├── loaders.py     # File loaders (images + PDFs)
│   ├── embedder.py    # CLIP model + embedding functions
│   └── db.py          # ChromaDB setup and storage
├── setup.py
├── requirements.txt
└── README.md
```

---

## How it works

```
sem-index --path ./docs
    │
    ├── Walk directory recursively
    ├── For each .jpg/.png → CLIP image encoder → 512d vector
    └── For each .pdf page → CLIP image encoder → 512d vector
                           → extract text → CLIP text encoder → 512d vector
                                    │
                                    ▼
                         ~/.semantic_search/chromadb
                         (persistent, global, grows over time)

sem-search --query "a dog" --type image
    │
    ├── Embed query → CLIP text encoder → 512d vector
    ├── Cosine similarity search in ChromaDB
    └── Return top-k results with score + metadata
```

---

## Tech stack

- [Click](https://click.palletsprojects.com/) — CLI framework
- [OpenCLIP](https://github.com/mlfoundations/open_clip) — CLIP model (ViT-B-32, OpenAI weights)
- [ChromaDB](https://www.trychroma.com/) — Vector database
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF text extraction and page rendering
- [Pillow](https://pillow.readthedocs.io/) — Image loading

---

## Requirements

```
click
chromadb
open-clip-torch
Pillow
pymupdf
torch
```

---

## Notes

- The CLIP model is downloaded once on first run and cached locally
- All vectors are stored at `~/.semantic_search/chromadb` — shared across all indexed folders
- Running `sem-index` on the same folder twice is safe — duplicates are skipped
- For best results use `--type image` for visual queries and `--type text` for document content queries

---

