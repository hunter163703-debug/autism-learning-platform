-- Migration: 0006_create_session4_submissions.sql
-- Description: 儲存自閉症教學 Session 2-3（跟隨孩子引導 - 影片觀察與臨床實務三大題）學生繳交之成果與評分

CREATE TABLE IF NOT EXISTS session4_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    total_score INTEGER NOT NULL DEFAULT 0,
    score_part1 INTEGER NOT NULL DEFAULT 0,
    score_part2 INTEGER NOT NULL DEFAULT 0,
    score_part3 INTEGER NOT NULL DEFAULT 0,
    answers_json TEXT NOT NULL,
    ai_feedback TEXT,
    teacher_notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_session4_submissions_student ON session4_submissions (student_id);
CREATE INDEX IF NOT EXISTS idx_session4_submissions_time ON session4_submissions (submitted_at);
