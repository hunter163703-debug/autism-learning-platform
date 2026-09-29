-- Migration: 0005_create_session3_submissions.sql
-- Description: 儲存自閉症教學第三節（跟隨孩子引導四大核心策略）學生繳交之成果與評分

CREATE TABLE IF NOT EXISTS session3_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    total_score INTEGER NOT NULL DEFAULT 0,
    score_part1 INTEGER NOT NULL DEFAULT 0,
    score_part2 INTEGER NOT NULL DEFAULT 0,
    score_part3 INTEGER NOT NULL DEFAULT 0,
    score_part4 INTEGER NOT NULL DEFAULT 0,
    score_part5 INTEGER NOT NULL DEFAULT 0,
    score_part6 INTEGER NOT NULL DEFAULT 0,
    score_part7 INTEGER NOT NULL DEFAULT 0,
    answers_json TEXT NOT NULL,
    ai_feedback TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_session3_submissions_student ON session3_submissions (student_id);
CREATE INDEX IF NOT EXISTS idx_session3_submissions_time ON session3_submissions (submitted_at);
