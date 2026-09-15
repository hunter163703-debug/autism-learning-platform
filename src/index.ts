export interface Env {
  autism_comm_disorders_db: D1Database;
  ASSETS?: Fetcher;
  AI_API_KEY?: string;
  GROQ_API_KEY?: string;
  AI_MODEL?: string;
}

const SOCRATIC_SYSTEM_PROMPT = `你是一位溫暖、專業且極富教育熱忱的「自閉症與溝通障礙」臨床教學助教。
你使用正體中文（台灣繁體習慣用語，如「自閉症類群障礙」、「語用」、「介入」、「共同注意力」）。
你的核心任務是採用「蘇格拉底啟發式提問法（Socratic Method）」，引導在測驗中答錯的學生主動思考、突破迷思與建立正確觀念。

【教育指導準則】：
1. 嚴禁直接向學生公佈或背誦標準答案。請扮演啟發者，提供引導式「思考鷹架（Scaffolding）」。
2. 語氣溫和親切、充滿同理與鼓勵，切勿有指責或嚴厲語氣。
3. 針對學生所選擇的錯誤選項，探詢其思考脈絡（例如：詢問學生是題目中的哪個情境或關鍵詞讓其做出這個判斷）。
4. 每次回覆請保持簡明扼要（約 100~200 字），提出 1~2 個具有引導性的思考問題，不要給予太長而令人產生負擔的大段說教。
5. 當學生在對話中成功說出正確關鍵邏輯或核心概念時，請給予熱情讚美，並在回覆文字的最後一行單獨標記：[STATUS: CLARIFIED]`;

async function callLLM(env: Env, messages: { role: string; content: string }[]): Promise<string> {
  const apiKey = env.GROQ_API_KEY || env.AI_API_KEY;
  if (!apiKey) {
    throw new Error('未配置 AI API Key，請在 .dev.vars 中設定 GROQ_API_KEY 或 AI_API_KEY');
  }

  const model = env.AI_MODEL || 'qwen/qwen3.8-27b';
  const apiUrl = 'https://api.groq.com/openai/v1/chat/completions';

  const res = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey.trim()}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: model,
      messages: messages,
      temperature: 0.7,
      max_tokens: 800
    })
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`AI 服務呼叫失敗 (${res.status}): ${errText}`);
  }

  const data: any = await res.json();
  const reply = data.choices?.[0]?.message?.content;
  if (!reply) {
    throw new Error('AI 未回傳有效內容');
  }
  return reply.trim();
}

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Max-Age': '86400'
};

function json(data: any, init?: { status?: number }) {
  return new Response(JSON.stringify(data), {
    status: init?.status || 200,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      ...CORS_HEADERS
    }
  });
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // 處理跨來源預檢請求 (CORS Preflight)
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS_HEADERS });
    }

    // API 路由：取得所有章節
    if (url.pathname === '/api/chapters') {
      try {
        const { results } = await env.autism_comm_disorders_db
          .prepare('SELECT id, slug, title, subtitle, description, sort_order FROM chapters ORDER BY sort_order ASC')
          .all();
        return json({ success: true, data: results });
      } catch (err: any) {
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // API 路由：取得特定章節的所有題目與選項逐項解析
    if (url.pathname.startsWith('/api/chapters/') && url.pathname.endsWith('/questions')) {
      const parts = url.pathname.split('/');
      const slug = parts[3]; // /api/chapters/:slug/questions

      try {
        const chapter = await env.autism_comm_disorders_db
          .prepare('SELECT id, slug, title, subtitle, description FROM chapters WHERE slug = ?')
          .bind(slug)
          .first();

        if (!chapter) {
          return json({ success: false, error: 'Chapter not found' }, { status: 404 });
        }

        const { results: questions } = await env.autism_comm_disorders_db
          .prepare('SELECT id, source_tag, question_text, correct_option, summary_explanation, sort_order FROM questions WHERE chapter_id = ? ORDER BY sort_order ASC')
          .bind(chapter.id)
          .all();

        const { results: options } = await env.autism_comm_disorders_db
          .prepare('SELECT question_id, option_key, option_text, explanation FROM question_options WHERE question_id IN (SELECT id FROM questions WHERE chapter_id = ?)')
          .bind(chapter.id)
          .all();

        // 組合題目與選項
        const questionsWithOpts = questions.map((q: any) => ({
          id: q.id,
          source: q.source_tag,
          text: q.question_text,
          correct: q.correct_option,
          summary: q.summary_explanation,
          sort_order: q.sort_order,
          options: options.filter((o: any) => o.question_id === q.id).map((o: any) => ({
            key: o.option_key,
            text: o.option_text,
            explanation: o.explanation
          }))
        }));

        return json({
          success: true,
          chapter,
          questions: questionsWithOpts
        });
      } catch (err: any) {
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // API 路由：提交學生作答成果並寫入 D1 資料庫
    if (url.pathname === '/api/submissions' && request.method === 'POST') {
      try {
        const body = await request.json() as any;
        const {
          chapter_id = 1,
          student_id,
          student_name,
          score = 0,
          correct_count = 0,
          total_questions = 10,
          wrong_questions = [],
          duration_seconds = 0
        } = body;

        if (!student_id || !student_name || typeof student_id !== 'string' || typeof student_name !== 'string') {
          return json({ success: false, error: '請輸入正確的學號與姓名' }, { status: 400 });
        }

        const wrongQuestionsJson = typeof wrong_questions === 'string' 
          ? wrong_questions 
          : JSON.stringify(wrong_questions);

        const result = await env.autism_comm_disorders_db
          .prepare(`
            INSERT INTO student_submissions (
              chapter_id, student_id, student_name, score, correct_count, total_questions, wrong_questions, duration_seconds
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
          `)
          .bind(
            Number(chapter_id) || 1,
            student_id.trim(),
            student_name.trim(),
            Number(score),
            Number(correct_count),
            Number(total_questions) || 10,
            wrongQuestionsJson,
            Number(duration_seconds) || 0
          )
          .run();

        return json({
          success: true,
          message: '作答紀錄已成功儲存至 Cloudflare D1 資料庫',
          submission_id: result.meta?.last_row_id || null
        });
      } catch (err: any) {
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // API 路由：查詢作答紀錄 (可依學號查詢或查詢最新紀錄)
    if (url.pathname === '/api/submissions' && request.method === 'GET') {
      try {
        const studentId = url.searchParams.get('student_id');
        let query = 'SELECT id, chapter_id, student_id, student_name, score, correct_count, total_questions, wrong_questions, duration_seconds, submitted_at FROM student_submissions ';
        let params: any[] = [];

        if (studentId) {
          query += 'WHERE student_id = ? ORDER BY submitted_at DESC LIMIT 50';
          params.push(studentId.trim());
        } else {
          query += 'ORDER BY submitted_at DESC LIMIT 50';
        }

        const stmt = env.autism_comm_disorders_db.prepare(query);
        const { results } = params.length > 0 ? await stmt.bind(...params).all() : await stmt.all();

        const parsedResults = results.map((row: any) => {
          let parsedWrong = [];
          try {
            parsedWrong = row.wrong_questions ? JSON.parse(row.wrong_questions) : [];
          } catch (e) {
            parsedWrong = row.wrong_questions;
          }
          return {
            ...row,
            wrong_questions: parsedWrong
          };
        });

        return json({ success: true, data: parsedResults });
      } catch (err: any) {
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // ==========================================
    // AI 蘇格拉底家教 API 路由
    // ==========================================

    // 1. 啟動 AI 家教對話會話 (Start Session)
    if (url.pathname === '/api/ai/tutor/start' && request.method === 'POST') {
      try {
        const body = await request.json() as any;
        const {
          student_id,
          student_name,
          chapter_id = 1,
          question_id,
          question_tag = '自閉症核心觀念',
          question_text,
          student_choice,
          student_choice_text = '',
          correct_choice,
          correct_choice_text = '',
          summary = ''
        } = body;

        const finalStudentId = (student_id && String(student_id).trim()) ? String(student_id).trim() : 'GUEST';
        const finalStudentName = (student_name && String(student_name).trim()) ? String(student_name).trim() : '同學';
        const finalQuestionId = Number(question_id || body.question_sort_order || 1);
        const finalQuestionText = (question_text && String(question_text).trim()) ? String(question_text).trim() : '自閉症與溝通障礙核心觀念題';

        const studentChoiceKey = (student_choice || body.selected_key || '').toString();
        const studentChoiceText = (student_choice_text || body.selected_text || '').toString();
        const correctChoiceKey = (correct_choice || body.correct_key || '').toString();
        const correctChoiceText = (correct_choice_text || body.correct_text || '').toString();

        // 建立 session 紀錄
        const insertRes = await env.autism_comm_disorders_db
          .prepare(`
            INSERT INTO ai_tutor_sessions (
              student_id, student_name, chapter_id, question_id, question_tag,
              question_text, student_choice, correct_choice, status, turn_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'in_progress', 1)
          `)
          .bind(
            finalStudentId,
            finalStudentName,
            Number(chapter_id) || 1,
            finalQuestionId,
            question_tag || '自閉症核心觀念',
            finalQuestionText,
            studentChoiceKey,
            correctChoiceKey
          )
          .run();

        const sessionId = insertRes.meta?.last_row_id;

        // 建構蘇格拉底開場提示詞
        const openingUserPrompt = `學生姓名：${finalStudentName}
討論題號：第 ${finalQuestionId} 題
概念主題：${question_tag || '自閉症核心觀念'}
題目內容：${finalQuestionText}
學生剛才選擇的錯誤選項：【${studentChoiceKey}】${studentChoiceText}
標準解答選項：【${correctChoiceKey}】${correctChoiceText}
核心概念歸納與解析重點：${summary}

任務：請以親切、同理的蘇格拉底家教語氣向 ${finalStudentName} 打招呼，安慰他這題確實容易混淆；接著提出你的第 1 個啟發式引導問題，詢問他當初為什麼會選【${studentChoiceKey}】，引導他開始梳理自己的思考盲點。`;

        const aiOpeningMessage = await callLLM(env, [
          { role: 'system', content: SOCRATIC_SYSTEM_PROMPT },
          { role: 'user', content: openingUserPrompt }
        ]);

        // 儲存 AI 第一則開場訊息
        if (sessionId) {
          await env.autism_comm_disorders_db
            .prepare('INSERT INTO ai_tutor_messages (session_id, sender, content) VALUES (?, "assistant", ?)')
            .bind(sessionId, aiOpeningMessage)
            .run();
        }

        return json({
          success: true,
          session_id: sessionId,
          message: aiOpeningMessage,
          greeting_message: aiOpeningMessage
        });
      } catch (err: any) {
        console.error('AI Tutor Start Error:', err);
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // 2. 進行後續蘇格拉底對話 (Chat in Session)
    if (url.pathname === '/api/ai/tutor/chat' && request.method === 'POST') {
      try {
        const body = await request.json() as any;
        const { session_id, student_message } = body;

        if (!session_id || !student_message || !student_message.trim()) {
          return json({ success: false, error: '缺少 session_id 或訊息內容' }, { status: 400 });
        }

        // 查詢會話資訊
        const session: any = await env.autism_comm_disorders_db
          .prepare('SELECT * FROM ai_tutor_sessions WHERE id = ?')
          .bind(session_id)
          .first();

        if (!session) {
          return json({ success: false, error: '找不到該對話會話' }, { status: 404 });
        }

        // 寫入學生新發言
        await env.autism_comm_disorders_db
          .prepare('INSERT INTO ai_tutor_messages (session_id, sender, content) VALUES (?, "student", ?)')
          .bind(session_id, student_message.trim())
          .run();

        // 取得完整對話歷史
        const { results: history } = await env.autism_comm_disorders_db
          .prepare('SELECT sender, content FROM ai_tutor_messages WHERE session_id = ? ORDER BY id ASC')
          .bind(session_id)
          .all();

        // 組合 LLM 訊息流
        const systemWithContext = `${SOCRATIC_SYSTEM_PROMPT}

【當前探討題目背景】：
學生姓名：${session.student_name}
題目：${session.question_text}
學生選錯的選項：【${session.student_choice}】
標準解答：【${session.correct_choice}】
主題標籤：${session.question_tag}`;

        const messagesForLLM = [
          { role: 'system', content: systemWithContext }
        ];

        history.forEach((m: any) => {
          messagesForLLM.push({
            role: m.sender === 'student' ? 'user' : 'assistant',
            content: m.content
          });
        });

        // 呼叫 AI
        const rawReply = await callLLM(env, messagesForLLM);

        const isClarified = rawReply.includes('[STATUS: CLARIFIED]');
        const cleanReply = rawReply.replace('[STATUS: CLARIFIED]', '').trim();

        // 儲存 AI 回覆
        await env.autism_comm_disorders_db
          .prepare('INSERT INTO ai_tutor_messages (session_id, sender, content) VALUES (?, "assistant", ?)')
          .bind(session_id, cleanReply)
          .run();

        // 更新 session 狀態與輪數
        await env.autism_comm_disorders_db
          .prepare(`
            UPDATE ai_tutor_sessions 
            SET turn_count = turn_count + 1,
                status = CASE WHEN ? = 1 THEN 'clarified' ELSE status END,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
          `)
          .bind(isClarified ? 1 : 0, session_id)
          .run();

        return json({
          success: true,
          reply: cleanReply,
          reply_message: cleanReply,
          message: cleanReply,
          is_clarified: isClarified
        });
      } catch (err: any) {
        console.error('AI Tutor Chat Error:', err);
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // 3. 查詢特定 Session 的訊息紀錄 (Get Messages)
    if (url.pathname === '/api/ai/tutor/messages' && request.method === 'GET') {
      try {
        const sessionId = url.searchParams.get('session_id');
        if (!sessionId) {
          return json({ success: false, error: '缺少 session_id' }, { status: 400 });
        }

        const { results } = await env.autism_comm_disorders_db
          .prepare('SELECT id, sender, content, created_at FROM ai_tutor_messages WHERE session_id = ? ORDER BY id ASC')
          .bind(sessionId)
          .all();

        return json({ success: true, data: results });
      } catch (err: any) {
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // 4. 查詢學生的 AI 家教討論會話列表 (Get Sessions)
    if (url.pathname === '/api/ai/tutor/sessions' && request.method === 'GET') {
      try {
        const studentId = url.searchParams.get('student_id');
        let query = 'SELECT id, student_id, student_name, chapter_id, question_id, question_tag, question_text, student_choice, correct_choice, status, turn_count, created_at, updated_at FROM ai_tutor_sessions ';
        let params: any[] = [];

        if (studentId) {
          query += 'WHERE student_id = ? ORDER BY id DESC LIMIT 50';
          params.push(studentId.trim());
        } else {
          query += 'ORDER BY id DESC LIMIT 50';
        }

        const stmt = env.autism_comm_disorders_db.prepare(query);
        const { results } = params.length > 0 ? await stmt.bind(...params).all() : await stmt.all();

        return json({ success: true, data: results });
      } catch (err: any) {
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // 5. 查詢所有 AI 家教對話歷程逐字稿 (Get All Transcript Messages for Excel Export)
    if (url.pathname === '/api/ai/tutor/all-messages' && request.method === 'GET') {
      try {
        const { results } = await env.autism_comm_disorders_db
          .prepare(`
            SELECT 
              m.id as message_id,
              m.session_id,
              m.sender,
              m.content,
              m.created_at,
              s.student_id,
              s.student_name,
              s.question_id,
              s.question_tag,
              s.question_text,
              s.student_choice,
              s.correct_choice,
              s.status as session_status
            FROM ai_tutor_messages m
            LEFT JOIN ai_tutor_sessions s ON m.session_id = s.id
            ORDER BY m.session_id ASC, m.id ASC
          `)
          .all();

        return json({ success: true, data: results });
      } catch (err: any) {
        return json({ success: false, error: err.message }, { status: 500 });
      }
    }

    // 靜態前端資源處理 (Cloudflare Assets)
    if (env.ASSETS) {
      return env.ASSETS.fetch(request);
    }

    return new Response('自閉症與溝通障礙教學平台 API 運作中。請訪問前端頁面或 /api/chapters', {
      headers: { 'content-type': 'text/plain; charset=utf-8' }
    });
  }
};
