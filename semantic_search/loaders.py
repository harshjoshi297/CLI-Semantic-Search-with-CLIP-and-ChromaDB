import os
import fitz  # pymupdf
from PIL import Image

SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.pdf'}


def walk_directory(path):
    """Recursively walk directory and return supported files."""
    found_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, file)
                found_files.append(full_path)
    return found_files


def load_image(file_path):
    """Load an image file and return a PIL Image."""
    img = Image.open(file_path).convert("RGB")
    return [{"type": "image", "content": img, "source": file_path}]


def load_pdf(file_path):
    """Load a PDF and return text and images per page."""
    results = []
    doc = fitz.open(file_path)

    for page_num, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            results.append({
                "type": "text",
                "content": text,
                "source": file_path,
                "page": page_num + 1
            })

        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        results.append({
            "type": "image",
            "content": img,
            "source": file_path,
            "page": page_num + 1
        })

    doc.close()
    return results


def load_file(file_path):
    """Route file to the correct loader based on extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in {'.jpg', '.jpeg', '.png'}:
        return load_image(file_path)
    elif ext == '.pdf':
        return load_pdf(file_path)
    return []