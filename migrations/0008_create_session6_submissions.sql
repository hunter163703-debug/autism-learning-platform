-- Migration: 0008_create_session6_submissions.sql
-- Description: 儲存自閉症教學 第六節 (It Takes Two to Talk Session 3 & Session 4: 雙向溝通與促進互動成長) 學生分組線上學習單之成果與評分

CREATE TABLE IF NOT EXISTS session6_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    group_name TEXT DEFAULT '',
    group_members TEXT DEFAULT '',
    total_score INTEGER NOT NULL DEFAULT 0,
    score_part1 INTEGER NOT NULL DEFAULT 0, -- Part A: Session 3 (50分)
    score_part2 INTEGER NOT NULL DEFAULT 0, -- Part B: Session 4 (50分)
    answers_json TEXT NOT NULL,
    ai_feedback TEXT,
    teacher_notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_session6_submissions_student ON session6_submissions (student_id);
CREATE INDEX IF NOT EXISTS idx_session6_submissions_group ON session6_submissions (group_name);
CREATE INDEX IF NOT EXISTS idx_session6_submissions_time ON session6_submissions (submitted_at);
