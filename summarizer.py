import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_llm(prompt: str):

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    return response.json()["response"]


async def summarize(text: str):

    text = text[:4000]

    prompt = f"""
    You are a professional medical assistant.

    Analyze ONLY the provided report.

    Provide:
    1. Diagnosis
    2. Key Findings
    3. Severity
    4. Recommendations

    If information is missing, say "Not Mentioned".

    Report:
    {text}
    """

    return ask_llm(prompt)


async def answer_question(report: str, question: str):

    report = report[:4000]

    prompt = f"""
    You are a medical assistant.

    Use ONLY the provided report.

    Do NOT make assumptions.

    Report:
    {report}

    User Question:
    {question}
    """

    return ask_llm(prompt)


async def translate_report(text: str, language: str):

    prompt = f"""
    Translate the following medical text to {language}.

    Do NOT summarize.
    Keep medical meaning accurate.

    Text:
    {text}
    """

    return ask_llm(prompt)