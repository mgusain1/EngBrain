import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_context(sources:str):
    context = ""
    for sou in sources:
        context+="File: "+ sou["file_path"]+"\n"
        context+="Line: "+str(sou["start_line"])+" - "+ str(sou["end_line"]) + "\n"
        context+="source Text: "+ sou["text"] + "\n\n"
    return context

def generate_answer(question,source):
    context = build_context(source)
    prompt = f"""
You are EngBrain, an AI assistant for understanding software repositories.

Answer the user's question using only the context below.
If the context does not contain enough information, say that you do not have enough context.
Mention relevant file paths when useful.

Context:
{context}

Question:
{question}
"""
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
    