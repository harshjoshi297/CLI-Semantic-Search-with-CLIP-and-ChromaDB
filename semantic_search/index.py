import click
from semantic_search.loaders import walk_directory, load_file
from semantic_search.embedder import load_clip_model, embed_image, embed_text
from semantic_search.db import get_collection, store_embedding, is_already_indexed, build_chunk_id

@click.command()
@click.option('--path', required=True, type=click.Path(exists=True), help='Directory to index')
def index(path):
    """Recursively index all supported files in a directory into ChromaDB."""

    load_clip_model()
    get_collection()

    click.echo(f"Scanning directory: {path}\n")
    files = walk_directory(path)

    if not files:
        click.echo("No supported files found.")
        return

    click.echo(f"Found {len(files)} file(s) to index:\n")

    for file_path in files:
        click.echo(f"Processing: {file_path}")
        chunks = load_file(file_path)

        for chunk in chunks:
            page = chunk.get("page")
            chunk_id = build_chunk_id(file_path, chunk["type"], page)

            # Skip if already indexed
            if is_already_indexed(file_path, chunk_id):
                click.echo(f"  [SKIP] already indexed")
                continue

            # Embed
            if chunk["type"] == "image":
                vector = embed_image(chunk["content"])
            elif chunk["type"] == "text":
                vector = embed_text(chunk["content"])

            # Build metadata
            metadata = {
                "source": file_path,
                "type": chunk["type"],
                "filename": click.format_filename(file_path).split("/")[-1],
            }
            if page:
                metadata["page"] = page

            # Store
            store_embedding(chunk_id, vector, metadata)

            page_info = f"page {page}" if page else "image"
            click.echo(f"  [STORED] {chunk['type'].upper()} {page_info}")

    click.echo("\nIndexing complete!")
    click.echo(f"Database location: ~/.semantic_search/chromadb")


if __name__ == '__main__':
    index()