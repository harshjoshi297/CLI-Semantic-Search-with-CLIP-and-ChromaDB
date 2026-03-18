import torch
import open_clip

model, preprocess, tokenizer = None, None, None


def load_clip_model():
    """Load CLIP model once and reuse."""
    global model, preprocess, tokenizer
    if model is not None:
        return

    print("Loading CLIP model...")
    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-L-14', pretrained='openai'
    )
    tokenizer = open_clip.get_tokenizer('ViT-L-14')
    model.eval()
    print("CLIP model loaded.\n")


def embed_image(img):
    """Embed a PIL image using CLIP image encoder."""
    image_tensor = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        embedding = model.encode_image(image_tensor)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding[0].tolist()


def embed_text(text):
    """Embed a text string using CLIP text encoder."""
    tokens = tokenizer([text])
    with torch.no_grad():
        embedding = model.encode_text(tokens)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding[0].tolist()