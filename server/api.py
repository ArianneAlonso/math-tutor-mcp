from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
Eres un profesor de matemáticas amable y paciente.
Explicas paso a paso las soluciones, con lenguaje sencillo y ejemplos claros.
Usa un tono educativo y amigable, sin tecnicismos innecesarios.
Responde en español, con pasos numerados y claros.
Evita usar notación LaTeX (no uses símbolos como $ o \\frac). 
Escribe todo en texto plano, por ejemplo: x = -3/2, x = -1.5.
Si haces operaciones, muéstralas de forma simple y legible.

IMPORTANTE: Solo debes responder preguntas relacionadas con matemáticas de nivel secundaria 
(ecuaciones lineales, ecuaciones cuadráticas, operaciones básicas).
Si te preguntan algo que NO esté relacionado con matemáticas, responde educadamente:
"Lo siento, soy un tutor especializado en matemáticas de secundaria. Solo puedo ayudarte con 
ecuaciones lineales, ecuaciones cuadráticas y operaciones matemáticas básicas. Tienes alguna 
pregunta de matemáticas?"
"""

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

client = MultiServerMCPClient({
    "math-tutor": {
        "transport": "streamable_http",
        "url": "http://localhost:8000/mcp"
    }
})

tools = []

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

class ChatResponse(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    global tools
    try:
        tools = await client.get_tools()
        print(f"Conectado al servidor MCP. Tools disponibles: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.name}")
    except Exception as e:
        print(f"Error conectando al servidor MCP: {e}")
        import traceback
        traceback.print_exc()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        llm_with_tools = model.bind_tools(tools)
        
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        for msg in request.messages:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
        
        response = await llm_with_tools.ainvoke(messages)
        
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                tool_to_use = None
                for tool in tools:
                    if tool.name == tool_name:
                        tool_to_use = tool
                        break
                
                if tool_to_use:
                    tool_result = await tool_to_use.ainvoke(tool_args)
                    
                    messages.append(response)
                    messages.append(HumanMessage(content=f"Resultado de {tool_name}: {tool_result}"))
                    
                    final_response = await llm_with_tools.ainvoke(messages)
                    return ChatResponse(message=final_response.content)
        
        return ChatResponse(message=response.content)
        
    except Exception as e:
        print(f"Error en chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error procesando el mensaje: {str(e)}"
        )

@app.get("/health")
async def health():
    try:
        tool_count = len(tools)
        return {
            "status": "ok", 
            "mcp_connected": tool_count > 0,
            "tools_count": tool_count
        }
    except:
        return {
            "status": "ok", 
            "mcp_connected": False,
            "tools_count": 0
        }

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)