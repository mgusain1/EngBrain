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

def local_fallback_answer(question, sources):
    if not sources:
        return "I do not have enough context to answer this question."

    source_lines = []

    for source in sources[:3]:
        source_lines.append(
            source["file_path"]
            + " lines "
            + str(source["start_line"])
            + "-"
            + str(source["end_line"])
        )

    return (
        "I could not use the LLM API, but I found relevant context for: "
        + question.rstrip(".?")
        + ". Check these sources: "
        + "; ".join(source_lines)
    )

def generate_answer(question,source):
    context = build_context(source)
    try:
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
    except Exception as e:
        print("OpenAI API failed:", str(e))
        return local_fallback_answer(question, source)

    