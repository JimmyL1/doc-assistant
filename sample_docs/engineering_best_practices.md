# 台灣科技集團股份有限公司 — 工程最佳實踐手冊

> 維護單位：技術長室 / 架構委員會
> 版本：v4.0 | 最後更新：2025-02-01 | 適用：全體工程師

---

## 1. 前言

本手冊定義 台灣科技集團股份有限公司 工程團隊的標準工作規範。所有工程師，無論資歷，均須遵守這些規範。規範的目的不是限制，而是讓我們能夠在快速成長的同時，保持程式碼品質與工程效率。

> 好的工程文化 = 自動化 + 清晰溝通 + 持續改善

---

## 2. Code Review 規範

### 2.1 提交前自我審查清單

在送出 PR 前，作者必須確認：
- [ ] 所有 Unit Test 通過（本地執行）
- [ ] 新功能有對應測試（覆蓋率不低於80%）
- [ ] 沒有 TODO / FIXME 留在主幹程式碼中
- [ ] 環境變數、密碼、API Key 未硬編碼
- [ ] PR Description 清楚說明「為什麼」要做這個改動
- [ ] 已更新相關文件（API文件、CHANGELOG）

### 2.2 Reviewer 守則

- **回應時限：** 24小時內開始審查，48小時內完成
- **評論類型標記：**
  - `[BLOCK]` — 必須修改才能合併
  - `[SUGGEST]` — 建議修改，但不強制
  - `[NIT]` — 細節問題，可忽略
  - `[QUESTION]` — 疑問，不要求改動
- **批准條件：** 至少1名 Senior Engineer 批准（核心模組需2名）
- **態度原則：** 批評程式碼，不批評人；提出問題，也給出建議

### 2.3 PR 大小規範

| PR 類型 | 最大行數 | 說明 |
|--------|---------|------|
| Bug Fix | 200行 | 盡量精準，影響範圍要小 |
| Feature | 500行 | 超過須拆分子 PR |
| Refactor | 800行 | 須有充分理由，事先與Lead討論 |
| 緊急修復 | 不限 | 但需事後補充測試 |

---

## 3. Git Flow 規範

### 3.1 分支命名規則

```
feature/JIRA-123-add-rag-document-upload
bugfix/JIRA-456-fix-embedding-timeout
hotfix/JIRA-789-patch-auth-bypass
release/v3.2.1
chore/update-dependencies-2025q1
```

### 3.2 Commit Message 規範

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**類型（type）：**
- `feat` — 新功能
- `fix` — Bug 修復
- `docs` — 文件更新
- `style` — 格式調整（不影響邏輯）
- `refactor` — 重構
- `test` — 測試相關
- `chore` — 建構、依賴更新

**範例：**
```
feat(rag): add multi-document query with source citation

Implement cross-document retrieval using Chroma vector store.
Returns top-5 relevant chunks with page reference and confidence score.

Closes JIRA-1234
```

### 3.3 主幹保護規則

- `main` 分支：禁止直接 push，只允許通過審查的 PR 合併
- `release/*` 分支：只接受來自 `develop` 的 merge，不接受 feature 直接 merge
- 所有 merge 使用 `Squash and Merge`（保持歷史乾淨）
- Tag 格式：`v{MAJOR}.{MINOR}.{PATCH}`（語義化版本）

---

## 4. 測試策略

### 4.1 測試金字塔

```
         /\
        /整合\
       / 測試  \    （20%）
      /----------\
     /   單元測試  \  （70%）
    /--------------\
   /   E2E / 冒煙   \  （10%）
  /------------------\
```

### 4.2 覆蓋率要求

| 層級 | 最低覆蓋率 | 說明 |
|------|-----------|------|
| 核心業務邏輯 | 90% | RAG chain、計費、認證 |
| API 端點 | 85% | 所有 HTTP 方法與錯誤路徑 |
| 工具函數 | 80% | |
| UI 元件 | 70% | 重要互動需有 E2E 補充 |

### 4.3 測試命名規範

```python
# Python 範例
def test_query_returns_answer_with_sources_when_documents_exist():
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...
```

規則：`test_[功能]_[場景]_[預期結果]`

---

## 5. 部署流程

### 5.1 環境架構

```
feature branch → dev（自動部署）
                  ↓ QA 驗證通過
                 staging（手動觸發）
                  ↓ PO + QA 簽核
                 production（手動觸發 + 值班確認）
```

### 5.2 部署檢查清單

**部署前：**
- [ ] CHANGELOG 已更新
- [ ] 資料庫 Migration 已審查（不可逆操作需特別標記）
- [ ] 環境變數已在目標環境設定
- [ ] 部署時間避開業務尖峰（09:00-11:00、13:30-17:30）

**部署中：**
- [ ] 監控 Error Rate（基準：<0.1%）
- [ ] 監控 P99 Latency（基準：<500ms）
- [ ] Canary 部署：先放5%流量觀察10分鐘

**部署後：**
- [ ] 執行 Smoke Test
- [ ] 確認 Alerting 正常運作
- [ ] 在 `#deployments` Slack 頻道發布部署通知

### 5.3 回滾程序

若部署後 Error Rate 超過 1% 或 P99 > 2秒，立即執行回滾：

```bash
# 透過 CI/CD 系統回滾
./scripts/rollback.sh production v3.1.5
```

---

## 6. 監控與告警

### 6.1 黃金訊號（Four Golden Signals）

所有服務必須監控以下四項指標：

1. **延遲（Latency）：** P50 / P95 / P99
2. **流量（Traffic）：** RPS、QPS
3. **錯誤率（Errors）：** 5xx 比率、業務錯誤
4. **飽和度（Saturation）：** CPU、記憶體、磁碟、連線數

### 6.2 告警規則

| 指標 | Warning 閾值 | Critical 閾值 |
|------|------------|--------------|
| Error Rate | >0.5% | >1% |
| P99 Latency | >800ms | >2,000ms |
| CPU | >70% | >85% |
| Memory | >75% | >90% |
| Disk | >70% | >85% |

### 6.3 值班制度

- 工作日值班：08:00-22:00（由各 team lead 輪值）
- 假日 On-Call：24小時（2週輪一次）
- PagerDuty 告警 → 15分鐘未響應 → 升報主管

---

## 7. 安全開發規範

- 絕對禁止在程式碼中硬編碼任何密鑰或密碼（使用 Vault 或環境變數）
- 所有外部輸入必須驗證與清理（防止 SQL Injection、XSS）
- 依賴套件定期更新（每月執行 `npm audit` / `pip-audit`）
- 敏感操作（帳號刪除、批量更新）必須有二次確認與稽核日誌
- 程式碼中的個資必須加密儲存，不得明文紀錄於 Log

---

## 8. 文件規範

- 每個服務必須有 `README.md`（涵蓋：用途、安裝、設定、開發、部署）
- API 變更必須同步更新 OpenAPI Spec（Swagger）
- 架構決策使用 ADR（Architecture Decision Record）記錄
- Confluence 內部文件每季審查，刪除過時內容

聯絡架構委員會：architecture@twtech.com.tw
