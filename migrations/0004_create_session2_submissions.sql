-- Migration: 0004_create_session2_submissions.sql
-- Description: 儲存自閉症教學第二節（Hanen 模式學習單）學生繳交之成果與評分

CREATE TABLE IF NOT EXISTS session2_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    total_score INTEGER NOT NULL,
    score_part1 INTEGER NOT NULL DEFAULT 0,
    score_part2 INTEGER NOT NULL DEFAULT 0,
    score_part3 INTEGER NOT NULL DEFAULT 0,
    score_part4 INTEGER NOT NULL DEFAULT 0,
    answers_json TEXT NOT NULL,
    feedback_examples TEXT,
    feedback_reflection TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_session2_submissions_student ON session2_submissions (student_id);
CREATE INDEX IF NOT EXISTS idx_session2_submissions_time ON session2_submissions (submitted_at);
