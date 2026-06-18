import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_context(sources):
    context = ""

    for source in sources:
        context += "File: " + source["file_path"] + "\n"
        context += "Lines: " + str(source["start_line"]) + "-" + str(source["end_line"]) + "\n"
        context += "Source Text:\n" + source["text"] + "\n\n"

    return context


def local_fallback_runbook(task, sources):
    if not sources:
        return "I do not have enough context to generate a runbook."

    steps = []
    steps.append("Runbook for: " + task)
    steps.append("")
    steps.append("1. Review the most relevant source files listed below.")
    steps.append("2. Start with the first source because it ranked highest in retrieval.")
    steps.append("3. Inspect the related functions and imports.")
    steps.append("4. Follow the flow across the remaining sources.")
    steps.append("5. Make the change or debug the issue, then retest the endpoint/script.")

    steps.append("")
    steps.append("Relevant sources:")

    for source in sources[:3]:
        steps.append(
            "- "
            + source["file_path"]
            + " lines "
            + str(source["start_line"])
            + "-"
            + str(source["end_line"])
        )

    return "\n".join(steps)


def generate_runbook(task, sources):
    context = build_context(sources)

    prompt = f"""
You are EngBrain, an AI assistant for software engineering runbooks.

Create a clear step-by-step engineering runbook for the task below.
Use only the provided context.
If the context is not enough, say what is missing.
Mention relevant file paths when useful.

Context:
{context}

Task:
{task}

Return the answer as:
Title:
Purpose:
Steps:
Verification:
Sources:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        print("OpenAI API failed:", str(e))
        return local_fallback_runbook(task, sources)