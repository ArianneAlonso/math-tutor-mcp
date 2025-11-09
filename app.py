from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

system_prompt = """
Eres un profesor de matemáticas amable y paciente.
Explicas paso a paso las soluciones, con lenguaje sencillo y ejemplos claros.
Usa un tono educativo y amigable, sin tecnicismos innecesarios.
Responde en español, con pasos numerados y claros.
Evita usar notación LaTeX (no uses símbolos como $ o \\frac). 
Escribe todo en texto plano, por ejemplo: x = -3/2, x = -1.5.
Si haces operaciones, muéstralas de forma simple y legible.
"""


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    system_instruction=system_prompt
)

client = MultiServerMCPClient({
    "math-tutor": {
        "transport": "streamable_http",
        "url": "http://localhost:8000/mcp"
    }
})

async def chat():
    print("Tutor MCP listo. Escribí 'salir' para terminar.\n")

    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() == "salir":
            break
        response = await model.ainvoke(pregunta)
        print("Tutor:", response.content)

if __name__ == "__main__":
    asyncio.run(chat())
