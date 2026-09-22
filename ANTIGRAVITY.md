# 2026 線上教學網站 - 專案規則與架構標準 (ANTIGRAVITY.md)

## 📌 專案概述
本專案為線上專業教學平台，支援多門獨立課程與多頁面單元內容。

---

## 🗄️ 資料庫架構標準與規範

### 1. 課程資料庫標準：特定課程獨立資料庫
- 本專案採用 **「特定課程獨立資料庫（Per-Course Dedicated D1 Database）」** 架構。
- 每門專業課程擁有獨立的 Cloudflare D1 資料庫，課程內可包含多個單元網頁（Pages / Lessons）。

### 2. 課程主題自動判定規則
- **自閉症溝通障礙課程**：
  - 當對話或需求涉及「自閉症」、「自閉症溝通障礙」、「自閉症教學」或相關特教溝通議題時，**一律自動判定並使用此專屬資料庫**：
    - **資料庫名稱 (database_name)**：`autism-comm-disorders-db`
    - **資料庫 ID (database_id)**：`8475edc2-cda6-4db2-8b7d-218b25d223b1`
    - **專案綁定名稱 (binding)**：`autism_comm_disorders_db`

### 3. 🚨 新建資料庫硬性規範（紅線規則）
- **嚴格禁止擅自建立任何新的 D1 資料庫或雲端資源**。
- 未來若有新的課程主題需要建立獨立資料庫時，**必須先向使用者主動說明、提供建議名稱並取得明確同意授權後，方可執行建立指令**。

### 4. 學生作答與成績記錄標準資料表 (`student_submissions`)
自閉症課程資料庫中統一維護學生作答成果資料表，包含學號、姓名、作答時間、分數與錯題 JSON：
- 表名：`student_submissions`
- 欄位架構：
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `chapter_id` (INTEGER NOT NULL DEFAULT 1)
  - `student_id` (TEXT NOT NULL) — 學生學號
  - `student_name` (TEXT NOT NULL) — 學生姓名
  - `score` (INTEGER NOT NULL) — 測驗總分 (0-100)
  - `correct_count` (INTEGER NOT NULL) — 答對題數
  - `total_questions` (INTEGER NOT NULL DEFAULT 10) — 總題數
  - `wrong_questions` (TEXT) — 錯題清單（含題號、題目、所選項與正確解析 JSON）
  - `duration_seconds` (INTEGER NOT NULL) — 總作答秒數
  - `submitted_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) — 提交時間
- 支援 API 端點：
  - `POST /api/submissions`：接收前端作答數據並寫入 D1 資料庫
  - `GET /api/submissions?student_id={id}`：查詢學生或全班歷史作答紀錄

### 4-2. 第二節：Hanen 方案學習單資料表 (session2_submissions)
自閉症第二節（跟隨孩子的引導 Follow Your Child's Lead）學習單作答數據記錄：
- 表名：session2_submissions
- 欄位架構：
  - id (INTEGER PRIMARY KEY AUTOINCREMENT)
  - student_id (TEXT NOT NULL) — 學生學號
  - student_name (TEXT NOT NULL) — 學生姓名
  - 	otal_score (INTEGER NOT NULL DEFAULT 0) — 總成績 (0-100)
  - score_part1 (INTEGER NOT NULL DEFAULT 0) — 壹、Let Your Child Lead (15分)
  - score_part2 (INTEGER NOT NULL DEFAULT 0) — 貳、創造主動溝通機會 (30分)
  - score_part3 (INTEGER NOT NULL DEFAULT 0) — 參、兒童溝通風格配對 (25分)
  - score_part4 (INTEGER NOT NULL DEFAULT 0) — 肆、父母角色配對與反思 (30分)
  - nswers_json (TEXT) — 完整作答內容 (含文字與配對卡片 JSON)
  - eedback_examples (TEXT) — 0~2歲生活例子五大向度 AI 評分回饋
  - eedback_reflection (TEXT) — 思考題反思評析
  - submitted_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- 支援 API 端點：
  - POST /api/session2/submit：提交學習單成績與答案至 D1
  - GET /api/session2/submissions：教師總覽與 Excel 匯出 (全班紀錄)
  - POST /api/session2/clear：教師專屬一鍵清除第二節歷史作答
  - POST /api/ai/review-examples：AI 臨床督導助教 0~2 歲實例評閱 (滿分16分)
- **報表匯出防重複規範**：
  - 第一頁籤【全班最新成績總表】：依學號嚴格去重，每人僅列最新一筆，並標註「累計測驗次數」。
  - 第二頁籤【歷次作答軌跡總覽】：保留所有作答歷程，便於分析學生進步軌跡。

### 5. AI 蘇格拉底家教（方案三：錯題破障微對話）架構規範
- **核心定位**：採用反詰問引導（Socratic Method），不直接提供答案，透過逐步階梯式提問引導學生自行推導並突破認知盲點。
- **後端模型**：Groq API (`qwen/qwen3.8-27b`)，以高敏捷（<1.5秒/回合）、全繁體中文（台灣特教臨床語彙）進行引導。
- **資料表規範**：
  - `ai_tutor_sessions`：記錄每次啟動的破障對話階段、學生學號、姓名、題號、所選錯誤、標準答案、對話輪數與突破狀態（`in_progress` / `clarified`）。
  - `ai_tutor_messages`：記錄每回合對話訊息內容、角色（`student` / `assistant` / `system`）。
- **支援 API 端點**：
  - `POST /api/ai/tutor/start`：建立破障家教階段並生成專屬引導開場詰問
  - `POST /api/ai/tutor/chat`：進行階梯詰問互動，當學生推導出關鍵時標記 `[STATUS: CLARIFIED]`
  - `GET /api/ai/tutor/sessions`：查詢 AI 家教歷程紀錄
  - `GET /api/ai/tutor/messages?session_id={id}`：查詢特定對話明細
  - `GET /api/ai/tutor/all-messages`：匯出所有學生 AI 家教完整逐字對話歷程

### 6. Excel 完整教學分析報表架構規範 (`學生作答成績與錯題報表.xlsx`)
- **檔案路徑**：`d:\2026ant線上教學網站\學生作答成績與錯題報表.xlsx`
- **匯出指令**：`python d:\2026ant線上教學網站\scripts\export_excel.py`
- **五大專業工作表設計**：
  1. **學生測驗總表**（深藍色系）：學生基本資料、作答時間、總分、正確率與錯題清單。
  2. **錯題深度剖析**（天藍色系）：每題學生所選錯誤選項、標準正解、逐項詳解與核心歸納。
  3. **全班難點與教學鑑別**（墨綠色系）：各題答錯率、錯誤選項分佈、高頻盲點標記與教師授課補強建議。
  4. **AI家教破障總覽**（深紫色系）：家教階段 Session ID、學生、題目、初選錯誤、正解、對話輪數與突破狀態。
  5. **AI逐字對話歷程**（靛青色系）：**完整保留每一回合對話逐字稿**（學生發言以淡藍標記、AI發言以淡紫標記、觀念突破關鍵點以淡綠標記），讓教師完全掌握學生思維卡點與概念演進。

### 7. 資料庫資料清除規範與安全防護 (Clear Data)
- **原則**：只清空資料列（`DELETE FROM`），**嚴格禁止刪除資料表結構（`DROP TABLE`）**。
- **清除途徑**：
  1. **線上網頁 UI**：歷史紀錄儀表板 ➔ 點擊「🧹 清除資料庫紀錄」按鈕，具備雙重防呆驗證。
  2. **PowerShell 腳本**：`powershell -ExecutionPolicy Bypass -File d:\2026ant線上教學網站\scripts\clear_d1_data.ps1`
  3. **後端 API**：`POST /api/admin/clear-data`（帶 `confirmation: "CLEAR"`）。
- **保留內容**：考題（`questions`、`question_options`）與章節資料永久保留，僅清除學生作答卷與對話紀錄。

### 8. 教學平台製作聲明與版權規範
- **製作者標註**：所有線上頁面頁腳、全卷檢視彈窗與對外說明文件，均需清楚標明：
  > **本教學平台由 亞洲大學 聽力暨語言治療學系 語言組 林樺鋒老師 製作**

---

## 🌐 線上發布與遠端儲存庫資訊

- **Cloudflare 全球主站（首選）**：[`https://autism-learning-platform.2026ant.workers.dev`](https://autism-learning-platform.2026ant.workers.dev)
- **GitHub Pages 靜態鏡像站**：[`https://hunter163703-debug.github.io/autism-learning-platform/`](https://hunter163703-debug.github.io/autism-learning-platform/)
- **GitHub 專案原始碼儲存庫**：[`https://github.com/hunter163703-debug/autism-learning-platform`](https://github.com/hunter163703-debug/autism-learning-platform)

---

## 📋 已登記課程資料庫清單

| 課程主題 | 資料庫名稱 | Database ID (UUID) | Binding 名稱 | 建立日期 |
| :--- | :--- | :--- | :--- | :--- |
| **自閉症溝通障礙** | `autism-comm-disorders-db` | `8475edc2-cda6-4db2-8b7d-218b25d223b1` | `autism_comm_disorders_db` | 2026-09-15 |

---

## ⚙️ 專案與 Cloudflare 綁定設定

### 常用管理指令（PowerShell）
```powershell
# 設定或更新 Groq API Key（安全無外洩引導）
powershell -ExecutionPolicy Bypass -File d:\2026ant線上教學網站\scripts\setup_groq_key.ps1

# 清除學生作答成績或 AI 對話歷程（新學期/班級重設）
powershell -ExecutionPolicy Bypass -File d:\2026ant線上教學網站\scripts\clear_d1_data.ps1

# 查詢自閉症溝通障礙資料庫資訊
& "C:\Users\Administrator\AppData\Roaming\npm\wrangler.cmd" d1 info autism-comm-disorders-db

# 查詢學生作答提交紀錄 (D1)
& "C:\Users\Administrator\AppData\Roaming\npm\wrangler.cmd" d1 execute autism-comm-disorders-db --command "SELECT id, student_id, student_name, score, duration_seconds, submitted_at FROM student_submissions ORDER BY submitted_at DESC LIMIT 10;"

# 查詢 AI 蘇格拉底家教對話歷程 (D1)
& "C:\Users\Administrator\AppData\Roaming\npm\wrangler.cmd" d1 execute autism-comm-disorders-db --command "SELECT id, student_name, question_id, status, turn_count FROM ai_tutor_sessions ORDER BY created_at DESC LIMIT 10;"

# 匯出 5 大工作表完整 Excel 學習歷程與教學診斷分析報表
python d:\2026ant線上教學網站\scripts\export_excel.py

# 部署更新至 Cloudflare Workers
& "C:\Users\Administrator\AppData\Roaming\npm\wrangler.cmd" deploy
```
