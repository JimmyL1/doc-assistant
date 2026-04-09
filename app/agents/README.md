# agents/ — v2 LangGraph 擴充目錄

此目錄在 v1 為空，v2 升級時在這裡加入以下檔案：

- `state.py` — 定義 agent 狀態（TypedDict）
- `nodes.py` — 各個 LangGraph node 函式（retrieve, reason, search_web）
- `tools.py` — Tool 定義（網路搜尋、Python 計算器等）
- `graph.py` — LangGraph StateGraph 組裝

v2 的 agent 直接 import v1 的：
- `app.core.vector_store.as_retriever()`
- `app.rag.chain.query()`
- `app.core.llm.get_llm()`

不需要修改任何 v1 程式碼。
