import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_manim_code(user_prompt):
    system_prompt = (
        "You are a math visualization assistant. Generate Python Manim code for the given math prompt. "
        "Use ManimCE (Community Edition). Return only the code, no explanation."
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama3-70b-8192",
        temperature=0.4
    )
    return chat_completion.choices[0].message.content

def clean_code(code):
    # Remove Markdown-style code blocks (e.g., ```python\n...\n```)
    if code.strip().startswith("```"):
        code = code.strip().split("```")[1]
        if code.strip().startswith("python"):
            code = "\n".join(code.strip().split("\n")[1:])
    return code.strip()

def fix_code(code):
    fix_prompt = (
        "You are a Python expert familiar with ManimCE. "
        "Fix any syntax or structural errors in the following Manim code. "
        "Do not add explanations or comments. Return corrected code only.\n\n"
        f"{code}"
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You fix Manim Python code."},
            {"role": "user", "content": fix_prompt}
        ],
        model="llama3-70b-8192",
        temperature=0.2
    )
    return clean_code(response.choices[0].message.content)
