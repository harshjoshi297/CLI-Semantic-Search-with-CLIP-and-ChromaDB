import click
from semantic_search.embedder import load_clip_model, embed_text
from semantic_search.db import get_collection


@click.command()
@click.option('--query', required=True, help='Search query in natural language')
@click.option('--top', default=5, help='Number of results to return')
@click.option('--type', 'search_type', 
              type=click.Choice(['all', 'image', 'text']), 
              default='all', 
              help='Filter by chunk type')
def search(query, top, search_type):
    """Search indexed files using a natural language query."""

    load_clip_model()
    collection = get_collection()

    click.echo(f"\nSearching for: '{query}' (type: {search_type})\n")

    query_vector = embed_text(query)

    # Build filter
    where = None
    if search_type != 'all':
        where = {"type": {"$eq": search_type}}

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top,
        where=where
    )

    ids       = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not ids:
        click.echo("No results found.")
        return

    click.echo(f"Top {len(ids)} results:\n")
    for i, (meta, distance) in enumerate(zip(metadatas, distances), 1):
        score    = 1 - distance
        filename = meta.get("filename", "unknown")
        source   = meta.get("source", "unknown")
        ftype    = meta.get("type", "unknown")
        page     = meta.get("page", None)

        click.echo(f"  {i}. {filename}")
        click.echo(f"     Type    : {ftype}")
        click.echo(f"     Score   : {score:.4f}")
        click.echo(f"     Path    : {source}")
        if page:
            click.echo(f"     Page    : {page}")
        click.echo()


if __name__ == '__main__':
    search()