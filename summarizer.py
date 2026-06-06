import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"

async def ask_llm(prompt: str):
    async with httpx.AsyncClient(timeout=800) as client:
        response = await client.post(
            OLLAMA_URL,
            json={"model": "llama3.2", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]


async def summarize(text: str):
    text = text[:3500]
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
    return await ask_llm(prompt)


async def answer_question(report: str, question: str) -> str:
    report = report[:3500]
    prompt = f"""You are a helpful medical AI assistant.

Answer the user's question based on the medical report below.

STRICT RULES:
- Do NOT mention any doctor names, patient names, or hospital names
- Do NOT say "according to Dr. X" or "Dr. X recommends"
- Give the answer directly and clearly
- If it is a health/diet/lifestyle question, give practical helpful advice
- Keep the answer concise and easy to understand

Medical Report:
{report}

Question: {question}

Answer:"""
    return await ask_llm(prompt)


async def translate_report(text: str, language: str):
    prompt = f"""
    Translate the following medical text to {language}.

    Do NOT summarize.
    Keep medical meaning accurate.

    Text:
    {text}
    """
    return await ask_llm(prompt)

async def extract_specialty(summary: str) -> str:
    prompt = f"""Based on this medical summary, what type of medical specialist should the patient see?
Reply with ONLY the specialist type (e.g. "cardiologist", "neurologist", "orthopedist", "pulmonologist", "gastroenterologist", "general physician").
One word or two words maximum. No explanation.

Summary:
{summary[:1000]}

Specialist:"""
    result = await ask_llm(prompt)
    return result.strip().split('\n')[0].strip()