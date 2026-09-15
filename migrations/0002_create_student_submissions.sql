-- Migration: 0002_create_student_submissions.sql
-- Description: 記錄學生作答成果（學號、姓名、分數、作答時間、錯題等）

CREATE TABLE IF NOT EXISTS student_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_id INTEGER NOT NULL DEFAULT 1,
    student_id TEXT NOT NULL,
    student_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    correct_count INTEGER NOT NULL,
    total_questions INTEGER NOT NULL DEFAULT 10,
    wrong_questions TEXT,
    duration_seconds INTEGER NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id)
);

CREATE INDEX IF NOT EXISTS idx_submissions_student ON student_submissions (student_id);
CREATE INDEX IF NOT EXISTS idx_submissions_chapter ON student_submissions (chapter_id);
