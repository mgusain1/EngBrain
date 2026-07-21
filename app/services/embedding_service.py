import hashlib
import os
import random

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def local_hash_embedding(text: str, size: int = 1536):
    vector = [0.0] * size

    words = text.lower().split()

    for word in words:
        hashed = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
        index = hashed % size
        vector[index] += 1.0

    norm = sum(x * x for x in vector) ** 0.5

    if norm == 0:
        return vector

    return [x / norm for x in vector]


def get_embedding(text: str):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    except Exception as e:
        print("OpenAI embedding failed:", str(e))
        return local_hash_embedding(text)