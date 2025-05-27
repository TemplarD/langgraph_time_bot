from datetime import datetime
from fastapi import FastAPI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessageGraph
from langchain_community.chat_models import ChatOllama
from langgraph.prebuilt import ToolNode

app = FastAPI()

# 1. Реализация инструмента времени (единственный требуемый инструмент)
def get_current_time() -> dict:
    """Возвращает текущее UTC время в ISO-8601 формате"""
    return {"utc": datetime.utcnow().isoformat() + "Z"}

# 2. Создание графа
def create_app():
    # Инициализация модели (Ollama)
    model = ChatOllama(model="llama3")
    
    # Узел для инструмента времени
    tools = [get_current_time]
    tool_node = ToolNode(tools)
    
    # Настройка графа
    workflow = MessageGraph()
    workflow.add_node("model", model)
    workflow.add_node("tools", tool_node)
    
    # Логика маршрутизации
    def router(state):
        last_msg = state[-1]
        if isinstance(last_msg, HumanMessage):
            if "time" in last_msg.content.lower() or "время" in last_msg.content.lower():
                return "tools"  # Запрос времени -> к инструменту
            return "model"  # Остальное -> к модели
        return "model"  # Ответ инструмента -> к модели
    
    workflow.add_conditional_edges("model", router)
    workflow.add_edge("tools", "model")
    workflow.set_entry_point("model")
    
    return workflow.compile()

# 3. API endpoint
@app.post("/chat")
async def chat_endpoint(message: dict):
    app = create_app()
    result = app.invoke(HumanMessage(content=message["messages"][0]["content"]))
    return {"response": result[-1].content}

# 4. Запуск через langgraph dev
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)