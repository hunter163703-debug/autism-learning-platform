-- Migration: 0007_create_session5_submissions.sql
-- Description: 儲存自閉症教學 第五節 (It Takes Two to Talk Session 1: Let Your Child Lead) 學生分組線上學習單之成果與評分

CREATE TABLE IF NOT EXISTS session5_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    group_name TEXT DEFAULT '',
    group_members TEXT DEFAULT '',
    total_score INTEGER NOT NULL DEFAULT 0,
    score_part1 INTEGER NOT NULL DEFAULT 0,
    score_part2 INTEGER NOT NULL DEFAULT 0,
    score_part3 INTEGER NOT NULL DEFAULT 0,
    score_part4 INTEGER NOT NULL DEFAULT 0,
    answers_json TEXT NOT NULL,
    ai_feedback TEXT,
    teacher_notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_session5_submissions_student ON session5_submissions (student_id);
CREATE INDEX IF NOT EXISTS idx_session5_submissions_group ON session5_submissions (group_name);
CREATE INDEX IF NOT EXISTS idx_session5_submissions_time ON session5_submissions (submitted_at);
