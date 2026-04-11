# 台灣科技集團股份有限公司 — REST API 開發者指南

> 版本：v3.2.1 | 最後更新：2025-04-01 | 適用環境：Production / Staging

---

## 1. 簡介

台灣科技集團開放平台（TaiwanTech Open Platform）提供一套 RESTful API，讓開發者與合作夥伴能夠將台灣科技的核心功能整合至自有系統。本指南涵蓋認證、端點說明、請求格式、錯誤碼與完整範例。

API 基礎 URL：
- Production：`https://api.twtech.com.tw/v3`
- Staging：`https://api-staging.twtech.com.tw/v3`

所有 API 請求與回應皆使用 `application/json` 格式，並強制使用 HTTPS。

---

## 2. 認證方式

### 2.1 OAuth 2.0（推薦）

台灣科技 API 使用 OAuth 2.0 Client Credentials Flow 進行機器對機器（M2M）認證。

**取得 Access Token：**

```bash
curl -X POST https://auth.twtech.com.tw/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "scope=documents:read documents:write query:execute"
```

**回應範例：**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "documents:read documents:write query:execute"
}
```

Token 有效期為 3,600 秒（1小時），請在過期前自動刷新。

### 2.2 API Key（簡易模式）

適用於快速測試與低安全需求場景。在請求 Header 中帶入：

```
X-API-Key: hyt_live_xxxxxxxxxxxxxxxxxxxxxx
```

**注意：** API Key 不支援細粒度權限控制，正式環境建議使用 OAuth 2.0。

### 2.3 IP 白名單

生產環境建議設定 IP 白名單，請至開發者後台（https://developer.twtech.com.tw）設定。

---

## 3. 端點說明

### 3.1 文件管理

| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/documents/upload` | 上傳並解析文件 |
| GET | `/documents` | 列出所有文件（支援分頁） |
| GET | `/documents/{id}` | 取得單一文件詳情 |
| DELETE | `/documents/{id}` | 刪除文件 |

### 3.2 智能查詢

| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/query` | 對文件庫提問（RAG） |
| GET | `/query/history` | 查詢歷史紀錄 |
| POST | `/query/feedback` | 提交查詢結果回饋 |

### 3.3 使用者與組織

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/org/members` | 列出組織成員 |
| POST | `/org/members/invite` | 邀請新成員 |
| GET | `/usage` | 取得 API 使用量統計 |

---

## 4. 請求格式

### 4.1 上傳文件

```bash
curl -X POST https://api.twtech.com.tw/v3/documents/upload \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -F "file=@/path/to/document.pdf" \
  -F "metadata={\"tags\":[\"財務\",\"2025Q1\"],\"department\":\"finance\"}"
```

**回應（201 Created）：**

```json
{
  "id": "doc_7f3a9b2c1d4e5f6a",
  "filename": "document.pdf",
  "status": "processing",
  "page_count": 42,
  "created_at": "2025-04-01T08:30:00Z",
  "estimated_completion": "2025-04-01T08:31:30Z"
}
```

### 4.2 查詢問答

```bash
curl -X POST https://api.twtech.com.tw/v3/query \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Q1 2025年的總營收是多少？",
    "document_ids": ["doc_7f3a9b2c1d4e5f6a"],
    "options": {
      "language": "zh-TW",
      "max_tokens": 1024,
      "include_sources": true,
      "top_k": 5
    }
  }'
```

**回應（200 OK）：**

```json
{
  "answer": "根據Q1 2025業務回顧報告，台灣科技集團股份有限公司在2025年第一季的總營收為新台幣4.28億元，年增18.3%。",
  "confidence": 0.94,
  "sources": [
    {
      "document_id": "doc_7f3a9b2c1d4e5f6a",
      "page": 3,
      "chunk": "總營收：NT$4.28億（年增18.3%）",
      "relevance_score": 0.97
    }
  ],
  "query_id": "qry_abc123",
  "latency_ms": 842
}
```

---

## 5. 分頁與篩選

列表端點支援以下查詢參數：

| 參數 | 類型 | 說明 | 預設值 |
|------|------|------|--------|
| `page` | integer | 頁碼（從1開始） | 1 |
| `per_page` | integer | 每頁筆數（最大100） | 20 |
| `sort` | string | 排序欄位（`created_at`, `filename`） | `created_at` |
| `order` | string | 排序方向（`asc`, `desc`） | `desc` |
| `filter[status]` | string | 依狀態篩選（`ready`, `processing`, `error`） | — |
| `filter[tag]` | string | 依標籤篩選 | — |

---

## 6. 錯誤碼

| HTTP狀態碼 | 錯誤代碼 | 說明 | 解決方式 |
|-----------|---------|------|---------|
| 400 | `INVALID_REQUEST` | 請求格式錯誤 | 檢查請求 body 格式 |
| 401 | `UNAUTHORIZED` | Token 無效或過期 | 重新取得 Access Token |
| 403 | `FORBIDDEN` | 無此資源存取權限 | 確認 Token scope |
| 404 | `NOT_FOUND` | 資源不存在 | 確認 ID 是否正確 |
| 413 | `FILE_TOO_LARGE` | 檔案超過 100MB 限制 | 壓縮或拆分檔案 |
| 415 | `UNSUPPORTED_FORMAT` | 不支援的檔案格式 | 僅支援 PDF/DOCX/TXT/PPTX |
| 429 | `RATE_LIMIT_EXCEEDED` | 超過 API 速率限制 | 降低請求頻率，參考 Retry-After Header |
| 500 | `INTERNAL_ERROR` | 伺服器內部錯誤 | 重試，若持續發生請聯絡支援 |
| 503 | `SERVICE_UNAVAILABLE` | 服務暫時不可用 | 等待後重試 |

**錯誤回應格式：**

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "每分鐘 API 請求上限為 60 次，請稍後再試",
    "retry_after": 23,
    "request_id": "req_xyz789"
  }
}
```

---

## 7. SDK 與工具

官方提供以下語言的 SDK：

- **Python**：`pip install twtech-sdk`
- **Node.js**：`npm install @twtech/sdk`
- **Java**：`com.twtech:twtech-sdk:3.2.1`
- **Go**：`go get github.com/twtech/sdk-go`

詳細 SDK 文件請參考：https://docs.twtech.com.tw/sdk

---

## 8. 聯絡支援

- 技術問題：developer@twtech.com.tw
- API 狀態頁：https://status.twtech.com.tw
- 開發者論壇：https://community.twtech.com.tw
- 企業支援（Enterprise SLA）：enterprise-support@twtech.com.tw
