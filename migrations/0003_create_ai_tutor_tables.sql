-- Migration: 0003_create_ai_tutor_tables.sql
-- Description: AI 蘇格拉底家教對話歷程與訊息紀錄資料表

CREATE TABLE IF NOT EXISTS ai_tutor_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    chapter_id INTEGER NOT NULL DEFAULT 1,
    question_id INTEGER NOT NULL,
    question_tag TEXT,
    question_text TEXT NOT NULL,
    student_choice TEXT,
    correct_choice TEXT,
    status TEXT DEFAULT 'in_progress',
    turn_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_tutor_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    sender TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES ai_tutor_sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_ai_sessions_student ON ai_tutor_sessions(student_id);
CREATE INDEX IF NOT EXISTS idx_ai_messages_session ON ai_tutor_messages(session_id);
