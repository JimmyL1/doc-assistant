from langchain_core.prompts import ChatPromptTemplate

RAG_SYSTEM_PROMPT = """你是一個專業的文件助理。請根據以下提供的文件內容回答問題。

規則：
- 只根據提供的文件內容回答，不要使用外部知識
- 如果文件中找不到答案，請明確說「根據現有文件，無法找到相關資訊」
- 回答要簡潔、準確，並引用來源文件名稱
- 請用繁體中文回答

文件內容：
{context}"""

# Prompt template: system message carries the retrieved context,
# human message carries the user's question
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    ("human", "{question}"),
])
