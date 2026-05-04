import re

def clean_text(text):

    text = re.sub(r'\bi(?=[a-zA-Z])', '', text)
    text = re.sub(r'\d+(\.\d+)+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9., ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def split_text(text, chunk_size=3):

    sentences = text.split(".")
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        chunk = ". ".join(sentences[i:i+chunk_size]).strip()
        if len(chunk) > 50:
            chunks.append(chunk)

    return chunks