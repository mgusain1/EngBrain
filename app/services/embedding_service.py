from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2') 


def get_embedding(text:str):
    vec_text = model.encode(text)
    return vec_text.tolist()

if __name__ == "__main__":
    vec = get_embedding("hello world")
    print(len(vec))
    print(vec[:5])