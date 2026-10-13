# -*- coding: utf-8 -*-
"""
產生第六節 (Session 3 & Session 4) 線上互動學習單網站：public/session6.html
單元主題：雙向溝通與促進互動成長 (Take Turn to Keep the Interaction Going & The Hanen Program)
"""

html_content = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>【第六節 課堂學習單】Session 3 & 4：雙向溝通與促進互動成長 - 課堂線上互動學習單</title>
  <!-- SheetJS for Excel Export -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            autism: {
              50: '#f0f9ff',
              100: '#e0f2fe',
              500: '#0ea5e9',
              600: '#0284c7',
              700: '#0369a1',
              900: '#0c4a6e',
            },
            hanen: {
              50: '#fff7ed',
              100: '#ffedd5',
              200: '#fed7aa',
              500: '#f97316',
              600: '#ea580c',
              700: '#c2410c',
              800: '#9a3412',
              900: '#7c2d12',
            }
          }
        }
      }
    }
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600;700;900&display=swap');
    body {
      font-family: 'Noto Sans TC', sans-serif;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #f1f5f9;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 4px;
    }
    .answer-textarea {
      transition: all 0.2s ease-in-out;
      border: 1.5px solid #cbd5e1;
    }
    .answer-textarea:focus {
      outline: none;
      border-color: #6366f1;
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
      background-color: #f8fafc;
    }
    .blank-input {
      border-bottom: 2px solid #6366f1;
      background: transparent;
      outline: none;
      transition: border-color 0.2s;
    }
    .blank-input:focus {
      border-bottom-color: #ec4899;
      background-color: #eef2ff;
    }
    @media print {
      header, aside, .no-print, button, #toast, #scoreReportModalOverlay, #teacherDashboardModalOverlay, #aiReviewModal {
        display: none !important;
      }
      body {
        background: white !important;
        color: black !important;
      }
      .print-shadow-none {
        box-shadow: none !important;
        border: 1px solid #cbd5e1 !important;
      }
    }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- 頂部導航列 -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm no-print">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <button id="sidebarToggle" class="p-2 rounded-lg text-slate-600 hover:bg-slate-100 lg:hidden">
          <i class="fa-solid fa-bars text-xl"></i>
        </button>
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-600 flex items-center justify-center text-white shadow-md">
          <i class="fa-solid fa-comments text-lg"></i>
        </div>
        <div>
          <span class="text-xs font-semibold uppercase tracking-wider text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded">It Takes Two to Talk® · Session 3 & 4</span>
          <h1 class="text-base sm:text-lg font-bold text-slate-900 leading-tight">【第六節 課堂學習單】雙向溝通與促進互動成長（學生分組）</h1>
        </div>
      </div>

      <div class="flex items-center space-x-2 sm:space-x-3">
        <!-- 老師檢視成績 按鈕 -->
        <button id="teacherDashboardBtn" type="button" onclick="loadTeacherDashboard()" class="inline-flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black text-white bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-700 hover:from-emerald-700 hover:to-teal-800 shadow-md shadow-emerald-600/20 transition transform hover:-translate-y-0.5" title="檢視全班作答成果與歷程">
          <i class="fa-solid fa-chalkboard-user text-sm"></i>
          <span>老師檢視成績</span>
        </button>

        <!-- 學生身分與分組登記按鈕 -->
        <button id="studentProfileBtn" type="button" onclick="openStudentModal()" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-50 border border-indigo-200 text-indigo-700 hover:bg-indigo-100 transition shadow-sm">
          <i class="fa-solid fa-user-group"></i>
          <span id="studentProfileText">登記學號與姓名</span>
        </button>

        <!-- 暫存學習單 -->
        <button id="saveDraftBtn" type="button" onclick="saveDraft(true)" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 transition shadow-sm">
          <i class="fa-solid fa-floppy-disk"></i>
          <span class="hidden sm:inline">暫存</span>
        </button>

        <!-- 列印 / 匯出 PDF -->
        <button id="printBtn" type="button" onclick="window.print()" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 transition shadow-sm">
          <i class="fa-solid fa-print"></i>
          <span class="hidden sm:inline">列印</span>
        </button>

        <!-- 重新開始測驗 -->
        <button id="resetWorksheetHeaderBtn" type="button" onclick="confirmResetWorksheet()" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 hover:bg-rose-100 transition shadow-sm" title="清空當前作答並重新開始">
          <i class="fa-solid fa-rotate-left"></i>
          <span>重填</span>
        </button>
      </div>
    </div>
  </header>

  <!-- 主內容佈局 -->
  <div class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 flex gap-6">

    <!-- 左側章節選單 (Sidebar) -->
    <aside id="sidebar" class="fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-slate-200 transform -translate-x-full lg:translate-x-0 lg:static lg:z-auto transition-transform duration-300 ease-in-out flex flex-col shadow-xl lg:shadow-none rounded-2xl lg:border lg:h-[calc(100vh-6.5rem)] lg:sticky lg:top-20 no-print">
      <div class="p-4 border-b border-slate-100 flex items-center justify-between">
        <h2 class="font-bold text-slate-800 flex items-center space-x-2 text-sm">
          <i class="fa-solid fa-layer-group text-indigo-600"></i>
          <span>課程全單元選單</span>
        </h2>
        <button id="closeSidebar" class="p-1.5 text-slate-400 hover:text-slate-600 lg:hidden">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-2">
        <!-- 第一節 -->
        <a href="index.html" class="block p-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition group">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">第一節 · 核心測驗</span>
            <i class="fa-solid fa-arrow-right text-xs text-slate-400 group-hover:translate-x-0.5 transition"></i>
          </div>
          <h4 class="font-bold text-xs text-slate-900 group-hover:text-sky-700 transition">自閉症兒童診斷與臨床表現</h4>
          <p class="text-[11px] text-slate-500 mt-0.5">DSM-IV / DSM-5 鑑別檢測題庫與詳解</p>
        </a>

        <!-- 第二節 -->
        <a href="session2.html" class="block p-3 rounded-xl border border-orange-200 bg-orange-50/40 hover:bg-orange-100/60 transition group">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-bold text-orange-700 bg-orange-100 px-2 py-0.5 rounded">第二節 · 實證方案</span>
            <i class="fa-solid fa-arrow-right text-xs text-orange-400 group-hover:translate-x-0.5 transition"></i>
          </div>
          <h4 class="font-bold text-xs text-slate-900 group-hover:text-orange-700 transition">跟隨孩子的引導 (Follow Child's Lead)</h4>
          <p class="text-[11px] text-slate-500 mt-0.5">OWL 技巧、風格與父母角色線上學習單</p>
        </a>

        <!-- 第三節 -->
        <a href="session3.html" class="block p-3 rounded-xl border border-sky-200 bg-sky-50/40 hover:bg-sky-100/60 transition group">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-bold text-sky-700 bg-sky-100 px-2 py-0.5 rounded">第三節 (Session 2-2)</span>
            <i class="fa-solid fa-arrow-right text-xs text-sky-400 group-hover:translate-x-0.5 transition"></i>
          </div>
          <h4 class="font-bold text-xs text-slate-900 group-hover:text-sky-700 transition">跟隨孩子引導四大核心策略</h4>
          <p class="text-[11px] text-slate-500 mt-0.5">Hanens3 示範影片、參與＆遊戲、模仿、解讀、評論</p>
        </a>

        <!-- 第四節 -->
        <a href="session4.html" class="block p-3 rounded-xl border border-amber-200 bg-amber-50/40 hover:bg-amber-100/60 transition group">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded">第四節 (Session 2-3)</span>
            <i class="fa-solid fa-arrow-right text-xs text-amber-400 group-hover:translate-x-0.5 transition"></i>
          </div>
          <h4 class="font-bold text-xs text-slate-900 group-hover:text-amber-700 transition">跟隨孩子引導 (綜合實務篇)</h4>
          <p class="text-[11px] text-slate-500 mt-0.5">Jacob/Alicia/柏翔真實個案深入剖析</p>
        </a>

        <!-- 第五節 -->
        <a href="session5.html" class="block p-3 rounded-xl border border-sky-200 bg-sky-50/40 hover:bg-sky-100/60 transition group">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-bold text-sky-700 bg-sky-100 px-2 py-0.5 rounded">第五節 (Session 1)</span>
            <i class="fa-solid fa-arrow-right text-xs text-sky-400 group-hover:translate-x-0.5 transition"></i>
          </div>
          <h4 class="font-bold text-xs text-slate-900 group-hover:text-sky-700 transition">【Session 1】Let Your Child Lead</h4>
          <p class="text-[11px] text-slate-500 mt-0.5">學生分組學習單：互動概念、四階段與OWL應用</p>
        </a>

        <!-- 第六節：當前頁面 -->
        <div class="p-3 rounded-xl bg-indigo-600 text-white shadow-md relative">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-black uppercase tracking-wider bg-white/20 text-white px-2 py-0.5 rounded">
              當前單元 · 第六節
            </span>
            <i class="fa-solid fa-circle-check text-xs text-indigo-200"></i>
          </div>
          <h4 class="font-bold text-xs text-white">【Session 3 & 4】雙向溝通與促進互動</h4>
          <p class="text-[11px] text-indigo-100 mt-0.5">課堂學習單：輪替提示、SPARK模型、4S原則</p>
        </div>
      </div>

      <!-- 底部 D1 資料庫綁定提示 -->
      <div class="p-3 bg-slate-50 border-t border-slate-200 text-xs text-slate-500 rounded-b-2xl">
        <div class="flex items-center space-x-2 text-slate-700 font-medium">
          <i class="fa-solid fa-server text-indigo-600"></i>
          <span>D1 課程資料庫綁定</span>
        </div>
        <p class="mt-1 text-[11px] text-slate-500 truncate font-mono">autism-comm-disorders-db</p>
        <p class="text-[10px] text-emerald-600 mt-0.5 font-medium flex items-center">
          <i class="fa-solid fa-circle text-[6px] mr-1 text-emerald-500"></i>session6_submissions 雲端即時同步
        </p>
      </div>
    </aside>

    <!-- 右側學習單主體區 -->
    <main class="flex-1 min-w-0 flex flex-col space-y-6">

      <!-- 學生分組與身分登記橫幅 -->
      <div id="studentBanner" class="p-4 rounded-2xl border transition-all duration-300 bg-indigo-50/80 border-indigo-200 text-indigo-950 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-sm">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center flex-shrink-0 shadow-sm">
            <i class="fa-solid fa-people-group text-lg"></i>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <span id="studentBannerTitle" class="text-sm font-bold">尚未登記學生身分</span>
              <span id="studentBannerStatusBadge" class="text-[11px] px-2 py-0.5 rounded-full font-bold bg-amber-100 text-amber-800 border border-amber-300">尚未登記</span>
            </div>
            <p id="studentBannerDesc" class="text-xs text-indigo-700 mt-0.5">本單元為第六節雙單元合一學習單，請先登記「學號」與「姓名」，即時記錄作答成果。</p>
          </div>
        </div>

        <div class="flex items-center gap-2 w-full sm:w-auto">
          <button type="button" onclick="openStudentModal()" class="w-full sm:w-auto px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-700 text-xs font-bold rounded-xl shadow-sm transition flex items-center justify-center space-x-1.5">
            <i class="fa-solid fa-user-pen"></i>
            <span>登記 / 修改分組身分</span>
          </button>
        </div>
      </div>

      <!-- 單元頂部資訊卡 -->
      <div class="bg-gradient-to-r from-indigo-700 via-purple-700 to-pink-700 rounded-2xl p-6 sm:p-8 text-white shadow-lg relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-44 h-44 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
        <div class="relative z-10">
          <div class="flex items-center space-x-2 text-indigo-100 text-xs font-semibold mb-2">
            <span class="bg-white/20 px-2.5 py-0.5 rounded-full backdrop-blur-sm">It Takes Two to Talk® 核心雙單元</span>
            <span>·</span>
            <span>第六節 學生分組學習單</span>
            <span>·</span>
            <span class="bg-emerald-400/20 text-emerald-200 px-2 py-0.5 rounded-full">滿分 100 分 (各50分)</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-black tracking-tight">【Session 3 & 4】雙向溝通與促進互動成長</h2>
          <p class="text-indigo-100 text-xs sm:text-sm mt-2 max-w-3xl leading-relaxed">
            整合雙大核心單元：<strong>Part A【Session 3】</strong>跟隨孩子的引導，促進互動成長 (50分) ＋ <strong>Part B【Session 4】</strong>雙向溝通 - 家長漢能計畫 (50分)。包含 Emily 下午茶、Alicia 提問改變、Sean 肢體常規、Jack 盪鞦韆 SPARK、Tristan 球池擴充與 4S 原則完整剖析。
          </p>

          <!-- 單元錨點切換按鈕 -->
          <div class="mt-5 pt-4 border-t border-white/20 flex flex-wrap items-center justify-between gap-4 text-xs">
            <div class="flex items-center space-x-2">
              <a href="#partA" class="px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 font-bold text-white transition flex items-center space-x-1">
                <span>Part A：Session 3 促進互動 (11大題)</span>
                <i class="fa-solid fa-arrow-down text-[10px]"></i>
              </a>
              <a href="#partB" class="px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 font-bold text-white transition flex items-center space-x-1">
                <span>Part B：Session 4 雙向溝通與4S (三大篇)</span>
                <i class="fa-solid fa-arrow-down text-[10px]"></i>
              </a>
            </div>
            <span class="bg-white/10 px-3 py-1 rounded-lg text-white font-mono font-bold">
              進度：<span id="answeredProgressText">0 / 25 欄位</span>
            </span>
          </div>
        </div>
      </div>

      <!-- 表單本體 -->
      <form id="worksheetForm" onsubmit="event.preventDefault(); submitWorksheet();" class="space-y-8">

        <!-- ========================================================= -->
        <!-- PART A: Session 3 課堂學習單 (共 50 分) -->
        <!-- ========================================================= -->
        <section id="partA" class="bg-white border-2 border-indigo-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
          <div class="flex items-center justify-between pb-4 border-b border-indigo-100">
            <div class="flex items-center space-x-3">
              <div class="w-9 h-9 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-black text-sm shadow-sm">
                Part A
              </div>
              <div>
                <span class="text-[11px] font-bold text-indigo-600 uppercase tracking-wider">Session 3 課堂學習單</span>
                <h3 class="text-base sm:text-lg font-black text-slate-900">跟隨孩子的引導，促進互動成長（Take Turn to Keep the Interaction Going）</h3>
              </div>
            </div>
            <span class="text-xs font-bold text-indigo-700 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-200">
              Part A 配分：50 分
            </span>
          </div>

          <div class="space-y-6">
            <!-- 1. 對話保持平衡三項要素 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div class="flex items-start justify-between">
                <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">1. 【核心要素】對話保持平衡三要素 · 4分</span>
                <span class="text-xs text-slate-400">填空題</span>
              </div>
              <p class="text-sm font-semibold text-slate-800">
                為了讓對話保持平衡，家長需要配合孩子的哪三項要素？
              </p>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-slate-500 block mb-1">第一要素：</span>
                  <input type="text" id="s3_q1_1" class="blank-input font-bold text-indigo-700 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">（Length of turn）</span>
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-slate-500 block mb-1">第二要素：</span>
                  <input type="text" id="s3_q1_2" class="blank-input font-bold text-indigo-700 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">（Pace）</span>
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-slate-500 block mb-1">第三要素：</span>
                  <input type="text" id="s3_q1_3" class="blank-input font-bold text-indigo-700 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">（Interest）</span>
                </div>
              </div>
            </div>

            <!-- 2. 發出提示五大核心方法 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div class="flex items-start justify-between">
                <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">2. 【核心方法】大人發出提示（Cue）協助輪流五大核心方法 · 5分</span>
                <span class="text-xs text-slate-400">填空題 (各1分)</span>
              </div>
              <p class="text-sm font-semibold text-slate-800">
                當大人發出提示（Cue）協助孩子輪流時，投影片提出了五大核心方法，且每一個方法後都必須落實最重要的步驟：
              </p>
              <div class="space-y-2 text-sm bg-white p-4 rounded-xl border border-slate-200">
                <div class="flex items-center flex-wrap gap-1">
                  <span>1. 使用你的</span>
                  <input type="text" id="s3_q2_1" class="blank-input font-bold text-indigo-700 w-48 text-center" placeholder="" oninput="updateProgress()">
                  <span>與肢體語言</span>
                </div>
                <div class="flex items-center flex-wrap gap-1">
                  <span>2. 提供孩子</span>
                  <input type="text" id="s3_q2_2" class="blank-input font-bold text-indigo-700 w-48 text-center" placeholder="" oninput="updateProgress()">
                </div>
                <div class="flex items-center flex-wrap gap-1">
                  <span>3. 熟悉的常規：</span>
                  <input type="text" id="s3_q2_3" class="blank-input font-bold text-indigo-700 w-48 text-center" placeholder="" oninput="updateProgress()">
                  <span>熟悉的常規</span>
                </div>
                <div class="flex items-center flex-wrap gap-1">
                  <span>4. 提供</span>
                  <input type="text" id="s3_q2_4" class="blank-input font-bold text-indigo-700 w-48 text-center" placeholder="" oninput="updateProgress()">
                  <span>的協助（hand-over-hand help）</span>
                </div>
                <div class="flex items-center flex-wrap gap-1">
                  <span>5. 提出</span>
                  <input type="text" id="s3_q2_5" class="blank-input font-bold text-indigo-700 w-48 text-center" placeholder="" oninput="updateProgress()">
                </div>
              </div>
            </div>

            <!-- 3. 投影片 14 影片觀察 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">3. 【課堂影片討論觀察】(投影片14 · itttr3-04) 延續對話方法 · 4分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">請配合課堂現場投影影片（繪本閱讀情境），觀察媽媽使用了哪幾種延續對話的方法，並舉例說明：</h4>
                </div>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>

              

              <div class="space-y-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(1) 媽媽使用了哪幾種延續對話的方法？</span>
                  <input type="text" id="s3_q3_1" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(2) 請舉例說明具體對話語句：</span>
                  <input type="text" id="s3_q3_2" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
              </div>
              <div class="flex justify-end">
                <button type="button" onclick="requestAiReview('s3_q3_combined', '投影片14 延續對話方法與舉例', 4)" class="text-xs text-indigo-600 hover:text-indigo-800 font-bold inline-flex items-center space-x-1">
                  <i class="fa-solid fa-wand-magic-sparkles text-indigo-500"></i>
                  <span>AI 助教審閱本題</span>
                </button>
              </div>
            </div>

            <!-- 4. 避開 Conversation Stoppers -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div class="flex items-start justify-between">
                <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">4. 【對話技巧】避開 Conversation Stoppers · 4分</span>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>
              <p class="text-sm font-semibold text-slate-800">(1) 請列舉 2 種應避免的問句類型（Conversation Stoppers）：</p>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-slate-500 block mb-1">① 應避免的問句類型一：</span>
                  <input type="text" id="s3_q4_1" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-slate-500 block mb-1">② 應避免的問句類型二：</span>
                  <input type="text" id="s3_q4_2" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
              </div>
              <div class="bg-white p-3 rounded-lg border border-slate-200 mt-2">
                <span class="text-xs font-bold text-indigo-700 block mb-1">(2) 除了調整發問方式（如改用選擇題或是非題），家長還可以採取什麼技巧來減少連續發問，同時又能維持對話？</span>
                <textarea id="s3_q4_3" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
              </div>
            </div>

            <!-- 5. 二選一 vs 是非題 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div class="flex items-start justify-between">
                <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">5. 【臨床比較】二選一問題 vs 是非題 · 4分</span>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>
              <p class="text-sm font-semibold text-slate-800">
                在引導溝通能力較初階的孩子進行輪替時，比較「二選一問題」與「是非題」各自的優勢與適用情境：
              </p>
              <textarea id="s3_q5" rows="3" class="answer-textarea w-full p-3 rounded-xl text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
              <div class="flex justify-end">
                <button type="button" onclick="requestAiReview('s3_q5', '二選一與是非題比較分析', 4)" class="text-xs text-indigo-600 hover:text-indigo-800 font-bold inline-flex items-center space-x-1">
                  <i class="fa-solid fa-wand-magic-sparkles text-indigo-500"></i>
                  <span>AI 助教審閱本題</span>
                </button>
              </div>
            </div>

            <!-- 6. 影片觀察：Emily 與爸爸下午茶 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">6. 【課堂影片討論觀察】(投影片18 · itttr3-05b) Emily 與爸爸 · 5分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">請配合課堂現場投影觀看爸爸與 Emily 玩下午茶扮家家酒影片，回答下列問題：</h4>
                </div>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>

              

              <div class="space-y-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（1）在遊戲進行中，爸爸運用問句的技巧創造了什麼機會？</span>
                  <input type="text" id="s3_q6_1" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（2）爸爸和 Emily 說了什麼？（請列舉具體台詞）</span>
                  <input type="text" id="s3_q6_2" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（3）Emily 聽到爸爸的提問，給予什麼回覆？</span>
                  <input type="text" id="s3_q6_3" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
              </div>
            </div>

            <!-- 7. Alicia 與媽媽 提問與評論 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">7. 【課堂影片討論觀察】(投影片28 · itttr3-07) Alicia 與媽媽提問與評論 · 5分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">提問與評論的運用（Questions & Comments）- Alicia 與媽媽：</h4>
                </div>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>

              

              <div class="space-y-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(1) Alicia 的媽媽起初使用了哪些類型的問題？對 Alicia 產生什麼影響？</span>
                  <textarea id="s3_q7_1" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(2) 後來 Alicia 的媽媽改變了哪些互動方式？</span>
                  <textarea id="s3_q7_2" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(3) 改變互動方式後，Alicia 的反應或參與情形有什麼不同？</span>
                  <textarea id="s3_q7_3" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
              </div>
            </div>

            <!-- 8. Sean 與媽媽肢體遊戲 (投影片33) -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">8. 【課堂影片討論觀察】(投影片33 · itttr3-08a) Sean 與媽媽肢體互動遊戲 · 5分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">請配合課堂現場投影觀看 Sean 與媽媽進行的肢體互動遊戲，回答問題：</h4>
                </div>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>

              

              <div class="space-y-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（1）在遊戲進行中，媽媽如何運用「調整常規（Adjust the routine）」與「提示（Cue）」的技巧來創造讓 Sean 輪流的機會？</span>
                  <textarea id="s3_q8_1" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（2）當大人「暫停」常規並等待（Wait）後，如果孩子沒有做出任何回應，大人應該如何進一步使用提示（Cue）來協助孩子輪流？</span>
                  <textarea id="s3_q8_2" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
              </div>
            </div>

            <!-- 9. Jack 與媽媽 (投影片41) -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">9. 【課堂影片討論觀察】(投影片41 · itttr3-10a) Jack 盪鞦韆與 SPARK · 5分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">請配合課堂現場投影觀看 Jack 盪鞦韆影片，並回答下列問題：</h4>
                </div>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>

              

              <div class="space-y-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（1）媽媽與 Jack 的互動符合 SPARK 中的哪一個概念？</span>
                  <input type="text" id="s3_q9_1" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（2）媽媽可以以哪種方式提示，增加 Jack 參與互動的機會？</span>
                  <input type="text" id="s3_q9_2" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">（3）如果在遊戲過程中，孩子一直沒有給予回應我們可以怎麼做？</span>
                  <input type="text" id="s3_q9_3" class="blank-input w-full text-sm font-medium" placeholder="" oninput="updateProgress()">
                </div>
              </div>
            </div>

            <!-- 10. SPARK 模型五步驟 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div class="flex items-start justify-between">
                <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">10. 【核心模型】SPARK 五個步驟 · 5分</span>
                <span class="text-xs text-slate-400">填空題 (各1分)</span>
              </div>
              <p class="text-sm font-semibold text-slate-800">
                SPARK 是設計例行活動以促進孩子輪流互動的五個步驟，請依序填入中文意義：
              </p>
              <div class="grid grid-cols-1 sm:grid-cols-5 gap-2 text-xs">
                <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                  <span class="font-black text-indigo-700 block mb-1">S：</span>
                  <input type="text" id="s3_q10_1" class="blank-input font-bold text-slate-800 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">Start the same way</span>
                </div>
                <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                  <span class="font-black text-indigo-700 block mb-1">P：</span>
                  <input type="text" id="s3_q10_2" class="blank-input font-bold text-slate-800 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">Plan child turn</span>
                </div>
                <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                  <span class="font-black text-indigo-700 block mb-1">A：</span>
                  <input type="text" id="s3_q10_3" class="blank-input font-bold text-slate-800 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">Adjust routine</span>
                </div>
                <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                  <span class="font-black text-indigo-700 block mb-1">R：</span>
                  <input type="text" id="s3_q10_4" class="blank-input font-bold text-slate-800 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">Repeat words/actions</span>
                </div>
                <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                  <span class="font-black text-indigo-700 block mb-1">K：</span>
                  <input type="text" id="s3_q10_5" class="blank-input font-bold text-slate-800 w-full" placeholder="" oninput="updateProgress()">
                  <span class="text-[10px] text-slate-400 block mt-1">Keep the same end</span>
                </div>
              </div>
            </div>

            <!-- 11. SPARK 實務規劃 (開放題) -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">11. 【實務規劃設計】運用 SPARK 模型規劃輪流點 · 9分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">請選擇一個日常生活常規或互動遊戲，運用 SPARK 模型規劃孩子的輪流點：</h4>
                </div>
                <span class="text-xs text-slate-400">實務設計題 (無標準答案)</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(1) 【S】常規簡單名稱與視覺輔助：</span>
                  <input type="text" id="s3_q11_1" class="blank-input w-full text-xs font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(2) 【P】預計在常規的什麼時機讓孩子輪流？</span>
                  <input type="text" id="s3_q11_2" class="blank-input w-full text-xs font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(3) 【A】你會使用什麼提示（Cue）來等待孩子回應？</span>
                  <input type="text" id="s3_q11_3" class="blank-input w-full text-xs font-medium" placeholder="" oninput="updateProgress()">
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-indigo-700 block mb-1">(4) 【K】你會使用什麼固定詞彙或動作作為常規結束信號？</span>
                  <input type="text" id="s3_q11_4" class="blank-input w-full text-xs font-medium" placeholder="" oninput="updateProgress()">
                </div>
              </div>
              <div class="flex justify-end">
                <button type="button" onclick="requestAiReview('s3_q11_combined', 'SPARK 實務日常活動輪替規劃設計', 9)" class="text-xs text-indigo-600 hover:text-indigo-800 font-bold inline-flex items-center space-x-1">
                  <i class="fa-solid fa-wand-magic-sparkles text-indigo-500"></i>
                  <span>AI 助教審閱本題設計</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- ========================================================= -->
        <!-- PART B: Session 4 課堂學習單 (共 50 分) -->
        <!-- ========================================================= -->
        <section id="partB" class="bg-white border-2 border-purple-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
          <div class="flex items-center justify-between pb-4 border-b border-purple-100">
            <div class="flex items-center space-x-3">
              <div class="w-9 h-9 rounded-xl bg-purple-600 text-white flex items-center justify-center font-black text-sm shadow-sm">
                Part B
              </div>
              <div>
                <span class="text-[11px] font-bold text-purple-600 uppercase tracking-wider">Session 4 課堂學習單</span>
                <h3 class="text-base sm:text-lg font-black text-slate-900">雙向溝通 - 家長漢能計畫（It Takes Two to Talk - The Hanen Program for Parents）</h3>
              </div>
            </div>
            <span class="text-xs font-bold text-purple-700 bg-purple-50 px-3 py-1 rounded-full border border-purple-200">
              Part B 配分：50 分
            </span>
          </div>

          <div class="space-y-6">
            <!-- 壹、核心理念篇 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <span class="text-xs font-black text-purple-700 bg-purple-100 px-2 py-0.5 rounded">壹、核心理念篇：如何順應孩子的導引加入語言？（Slide 11、30） · 16分</span>
                <span class="text-xs text-slate-400">填空題</span>
              </div>

              <!-- 1. 加入語言四大策略 -->
              <div>
                <p class="text-sm font-semibold text-slate-800 mb-2">1. 投影片與課本指出，根據孩子發展加入語言有四大策略（各2分，共8分）：</p>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">① imitate</span>
                    <input type="text" id="s4_q1_1" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">② interpret</span>
                    <input type="text" id="s4_q1_2" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">③ comment</span>
                    <input type="text" id="s4_q1_3" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">④ ask a question</span>
                    <input type="text" id="s4_q1_4" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                </div>
              </div>

              <!-- 2. 突現語言四大技巧 4S 原則 -->
              <div class="pt-2">
                <p class="text-sm font-semibold text-slate-800 mb-2">2. 突現語言的四大技巧，4S 原則（各2分，共8分）：</p>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">① 少說</span>
                    <input type="text" id="s4_q2_1" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">② 強調</span>
                    <input type="text" id="s4_q2_2" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">③ 放慢</span>
                    <input type="text" id="s4_q2_3" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                  <div class="bg-white p-2.5 rounded-lg border border-slate-200">
                    <span class="text-slate-500 font-bold block mb-1">④ 展示</span>
                    <input type="text" id="s4_q2_4" class="blank-input font-bold text-purple-700 w-full" placeholder="" oninput="updateProgress()">
                  </div>
                </div>
              </div>
            </div>

            <!-- 貳、影片觀察：Tristan 與爸爸 -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-purple-700 bg-purple-100 px-2 py-0.5 rounded">貳、課堂影片討論觀察篇一：Tristan 與爸爸（Slide 18、24 · itttr4-04 & itttr4-06a） · 18分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">請仔細觀察影片 (itttr4-04 與 itttr4-06a)，深入分析爸爸的做法：</h4>
                </div>
                <span class="text-xs text-slate-400">簡答題 (各6分)</span>
              </div>

              

              <div class="space-y-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-purple-800 block mb-1">
                    (1) 【爸爸的位置與態度】爸爸採取什麼姿勢？展現出怎樣的情感態度？
                  </span>
                  <textarea id="s4_q3_1" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-purple-800 block mb-1">
                    (2) 【爸爸如何與Tristan互動】爸爸是直接拿走孩子的玩具，還是有其他巧妙做法？他是如何創造遊戲互動的？
                  </span>
                  <textarea id="s4_q3_2" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-purple-800 block mb-1">
                    (3) 【爸爸如何擴充訊息】找出爸爸擴充 Tristan 訊息的具體範例（Expand）：
                  </span>
                  <textarea id="s4_q3_3" rows="3" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>
              </div>
              <div class="flex justify-end">
                <button type="button" onclick="requestAiReview('s4_q3_combined', 'Tristan 與爸爸互動與擴充訊息分析', 18)" class="text-xs text-purple-600 hover:text-purple-800 font-bold inline-flex items-center space-x-1">
                  <i class="fa-solid fa-wand-magic-sparkles text-purple-500"></i>
                  <span>AI 助教審閱本大題</span>
                </button>
              </div>
            </div>

            <!-- 參、影片三：4S 原則 (Slide 31) -->
            <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-4">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-xs font-black text-purple-700 bg-purple-100 px-2 py-0.5 rounded">參、課堂影片討論觀察篇二：4S 原則（Slide 31 · itttr4-08a） · 16分</span>
                  <h4 class="text-sm font-bold text-slate-800 mt-2">請配合課堂現場投影觀看積木高塔影片，深入分析媽媽的做法：</h4>
                </div>
                <span class="text-xs text-slate-400">簡答題</span>
              </div>

              

              <div class="space-y-3">
                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-purple-800 block mb-1">
                    (1) 【吸引注意 (6分)】媽媽使用了什麼方法吸引孩子注意？你還有什麼方法可以吸引注意？
                  </span>
                  <textarea id="s4_q4_1" rows="2" class="answer-textarea w-full p-2.5 rounded-lg text-sm custom-scrollbar" placeholder="" oninput="updateProgress()"></textarea>
                </div>

                <div class="bg-white p-3 rounded-lg border border-slate-200">
                  <span class="text-xs font-bold text-purple-800 block mb-1">
                    (2) 【媽媽如何運用 4S 原則 (10分)】找出媽媽如何運用 4S 原則的具體範例與效果：
                  </span>
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs mt-2">
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="font-bold text-purple-700 block">① Say Less（簡短說）範例：</span>
                      <textarea id="s4_q4_2_1" rows="2" class="w-full mt-1 p-1.5 border rounded text-xs" placeholder="" oninput="updateProgress()"></textarea>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="font-bold text-purple-700 block">② Stress（強調重點字）範例：</span>
                      <textarea id="s4_q4_2_2" rows="2" class="w-full mt-1 p-1.5 border rounded text-xs" placeholder="" oninput="updateProgress()"></textarea>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="font-bold text-purple-700 block">③ Go Slow（慢慢說）範例：</span>
                      <textarea id="s4_q4_2_3" rows="2" class="w-full mt-1 p-1.5 border rounded text-xs" placeholder="" oninput="updateProgress()"></textarea>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="font-bold text-purple-700 block">④ Show（做給你看）範例：</span>
                      <textarea id="s4_q4_2_4" rows="2" class="w-full mt-1 p-1.5 border rounded text-xs" placeholder="" oninput="updateProgress()"></textarea>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <button type="button" onclick="requestAiReview('s4_q4_combined', '4S 原則運用範例深度剖析', 16)" class="text-xs text-purple-600 hover:text-purple-800 font-bold inline-flex items-center space-x-1">
                  <i class="fa-solid fa-wand-magic-sparkles text-purple-500"></i>
                  <span>AI 助教審閱 4S 原則剖析</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- 提交按鈕區域 -->
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="text-xs text-slate-500">
            <span class="font-bold text-slate-700">提交說明：</span>
            本卷包含 Part A (50分) 與 Part B (50分)，總分 100 分。送出後自動核對答案計算成績並儲存至 Cloudflare D1。
          </div>
          <div class="flex items-center space-x-3 w-full sm:w-auto">
            <button type="button" onclick="saveDraft(true)" class="flex-1 sm:flex-none px-4 py-2.5 rounded-xl text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 transition">
              <i class="fa-solid fa-floppy-disk mr-1.5"></i>暫存目前作答
            </button>
            <button type="submit" id="submitBtn" class="flex-1 sm:flex-none px-6 py-2.5 rounded-xl text-sm font-black text-white bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-700 hover:to-pink-700 shadow-md shadow-indigo-600/30 transition transform hover:-translate-y-0.5">
              <i class="fa-solid fa-paper-plane mr-2"></i>提交第六節學習單
            </button>
          </div>
        </div>
      </form>

      <!-- 頁腳 -->
      <footer class="pt-8 pb-12 border-t border-slate-200 text-center text-xs text-slate-500 space-y-2 no-print">
        <p class="font-bold text-slate-700">亞洲大學 聽力暨語言治療學系 自閉症溝通障礙與溝通互動技巧學習平台</p>
        <p class="text-[11px] text-slate-400">本教學平台由 亞洲大學 聽力暨語言治療學系 語言組 林樺鋒老師 製作</p>
        <p class="text-[10px] text-slate-400 font-mono">D1 Database: autism-comm-disorders-db | Table: session6_submissions</p>
      </footer>
    </main>
  </div>

  <!-- 學生與分組登記 Modal -->
  <div id="studentModalOverlay" class="fixed inset-y-0 inset-x-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-100 space-y-4">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center">
            <i class="fa-solid fa-id-card text-sm"></i>
          </div>
          <h3 class="text-base font-bold text-slate-900">登記學生身分</h3>
        </div>
        <button type="button" onclick="closeStudentModal()" class="text-slate-400 hover:text-slate-600">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <p class="text-xs text-slate-500">請輸入學生學號與姓名，送出學習單後成績將自動綁定並記錄至 Cloudflare D1 資料庫：</p>
        <div>
          <label class="block font-bold text-slate-700 mb-1">學生學號 <span class="text-rose-500">*</span>：</label>
          <input type="text" id="modalStudentId" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none text-sm font-medium" placeholder="例如：112018001">
        </div>

        <div>
          <label class="block font-bold text-slate-700 mb-1">學生姓名 <span class="text-rose-500">*</span>：</label>
          <input type="text" id="modalStudentName" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none text-sm font-medium" placeholder="例如：王小明">
        </div>
      </div>

      <div class="pt-3 flex items-center justify-end space-x-2">
        <button type="button" onclick="closeStudentModal()" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100">
          取消
        </button>
        <button type="button" onclick="saveModalStudentProfile()" class="px-4 py-1.5 rounded-lg text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm">
          確認儲存
        </button>
      </div>
    </div>
  </div>

  <!-- AI 助教審閱建議 Modal -->
  <div id="aiReviewModal" class="fixed inset-y-0 inset-x-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl border border-slate-100 flex flex-col max-h-[85vh]">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center">
            <i class="fa-solid fa-robot text-sm"></i>
          </div>
          <div>
            <h3 class="text-sm font-bold text-slate-900">AI 臨床督導助教 · 即時審閱回饋</h3>
            <p id="aiReviewTopicText" class="text-[11px] text-slate-500">審閱主題</p>
          </div>
        </div>
        <button type="button" onclick="closeAiModal()" class="text-slate-400 hover:text-slate-600">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <div id="aiReviewContent" class="flex-1 overflow-y-auto custom-scrollbar my-4 text-xs sm:text-sm text-slate-700 whitespace-pre-wrap leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200">
        正在連線臨床助教模型評析中，請稍候...
      </div>

      <div class="pt-3 border-t border-slate-100 flex items-center justify-end">
        <button type="button" onclick="closeAiModal()" class="px-4 py-1.5 rounded-lg text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700">
          關閉
        </button>
      </div>
    </div>
  </div>

  <!-- 成績報告 Modal -->
  <div id="scoreReportModalOverlay" class="fixed inset-y-0 inset-x-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-white rounded-2xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-5">
      <div class="text-center space-y-2">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-500 to-pink-600 text-white flex items-center justify-center text-2xl mx-auto shadow-lg">
          <i class="fa-solid fa-award"></i>
        </div>
        <h3 class="text-xl font-black text-slate-900">第六節學習單提交成功！</h3>
        <p class="text-xs text-slate-500">成績與完整作答已即時同步至 Cloudflare D1</p>
      </div>

      <div class="bg-indigo-50 p-4 rounded-2xl border border-indigo-200 text-center space-y-1">
        <span class="text-xs font-bold text-indigo-800">總成績評定</span>
        <div class="text-4xl font-black text-indigo-700 font-mono" id="scoreModalTotal">0 <span class="text-base font-normal">/ 100</span></div>
        <p class="text-xs text-indigo-600" id="scoreModalStudentInfo">學生：- (學號：-)</p>
      </div>

      <div class="grid grid-cols-2 gap-3 text-center text-xs">
        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <span class="text-slate-400 block text-[11px] mb-1">Part A：Session 3 (促進互動成長)</span>
          <span class="font-black text-indigo-700 text-base" id="scoreModalPartA">0 / 50</span>
        </div>
        <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
          <span class="text-slate-400 block text-[11px] mb-1">Part B：Session 4 (雙向溝通家長漢能)</span>
          <span class="font-black text-purple-700 text-base" id="scoreModalPartB">0 / 50</span>
        </div>
      </div>

      <div class="pt-3 flex items-center justify-center space-x-3">
        <button type="button" onclick="closeScoreModal()" class="px-5 py-2 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm">
          完成並查看作答內容
        </button>
      </div>
    </div>
  </div>

  <!-- 老師檢視成績儀表板 Modal -->
  <div id="teacherDashboardModalOverlay" class="fixed inset-y-0 inset-x-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-3 sm:p-6 hidden">
    <div class="bg-white rounded-2xl max-w-6xl w-full h-[90vh] flex flex-col shadow-2xl border border-slate-100 overflow-hidden">
      <!-- 頂部工具列 -->
      <div class="p-4 sm:p-5 border-b border-slate-200 bg-slate-50 flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center shadow-sm">
            <i class="fa-solid fa-chalkboard-user text-lg"></i>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h3 class="text-base sm:text-lg font-black text-slate-900">第六節 (Session 3 & 4) 教師總覽儀表板</h3>
              <span class="text-xs font-bold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full border border-emerald-300">D1 即時同步</span>
            </div>
            <p class="text-xs text-slate-500">掌握全班小組分組、個人成績、Part A/B 分項表現與課堂討論註記</p>
          </div>
        </div>

        <div class="flex items-center space-x-2">
          <!-- 匯出 Excel -->
          <button type="button" onclick="exportToExcel()" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm transition">
            <i class="fa-solid fa-file-excel"></i>
            <span>匯出 Excel 報表</span>
          </button>

          <!-- 清空資料庫紀錄 -->
          <button type="button" onclick="clearDatabaseRecords()" class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 hover:bg-rose-100 shadow-sm transition">
            <i class="fa-solid fa-trash-can"></i>
            <span>清空作答</span>
          </button>

          <!-- 關閉 -->
          <button type="button" onclick="closeTeacherDashboard()" class="p-2 text-slate-400 hover:text-slate-600">
            <i class="fa-solid fa-xmark text-xl"></i>
          </button>
        </div>
      </div>

      <!-- 統計指標條 -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 bg-slate-100/60 border-b border-slate-200 text-xs">
        <div class="bg-white p-3 rounded-xl border border-slate-200">
          <span class="text-slate-400 block text-[11px]">總提交份數</span>
          <span class="font-black text-slate-800 text-base" id="statTotalSubmissions">0</span>
        </div>
        <div class="bg-white p-3 rounded-xl border border-slate-200">
          <span class="text-slate-400 block text-[11px]">不重複學生數</span>
          <span class="font-black text-indigo-700 text-base" id="statUniqueStudents">0</span>
        </div>
        <div class="bg-white p-3 rounded-xl border border-slate-200">
          <span class="text-slate-400 block text-[11px]">全班平均總分</span>
          <span class="font-black text-emerald-700 text-base" id="statAverageScore">0</span>
        </div>
        <div class="bg-white p-3 rounded-xl border border-slate-200">
          <span class="text-slate-400 block text-[11px]">小組總組數</span>
          <span class="font-black text-purple-700 text-base" id="statTotalGroups">0</span>
        </div>
      </div>

      <!-- 篩選與搜尋工具列 -->
      <div class="p-4 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div class="flex items-center space-x-2">
          <button type="button" id="viewModeAllBtn" onclick="switchTeacherViewMode('all')" class="px-3 py-1.5 rounded-lg font-bold bg-indigo-600 text-white">全班最新成績</button>
          <button type="button" id="viewModeGroupBtn" onclick="switchTeacherViewMode('group')" class="px-3 py-1.5 rounded-lg font-bold bg-slate-100 text-slate-700 hover:bg-slate-200">依小組分組檢視</button>
          <button type="button" id="viewModeHistoryBtn" onclick="switchTeacherViewMode('history')" class="px-3 py-1.5 rounded-lg font-bold bg-slate-100 text-slate-700 hover:bg-slate-200">歷次作答軌跡</button>
        </div>

        <div class="flex items-center space-x-2 w-full sm:w-auto">
          <input type="text" id="teacherSearchInput" oninput="filterTeacherSubmissions()" placeholder="搜尋學號、姓名..." class="px-3 py-1.5 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none w-full sm:w-60">
        </div>
      </div>

      <!-- 列表主體區 -->
      <div class="flex-1 overflow-y-auto custom-scrollbar p-4">
        <div id="teacherLoadingIndicator" class="text-center py-12 text-slate-400 text-xs">
          <i class="fa-solid fa-spinner fa-spin text-2xl text-indigo-600 mb-2 block"></i>
          正在自 Cloudflare D1 載入全班作答紀錄...
        </div>

        <table id="teacherSubmissionsTable" class="w-full text-left text-xs border-collapse hidden">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-slate-500 font-bold">
              <th class="p-2.5">組別</th>
              <th class="p-2.5">學號</th>
              <th class="p-2.5">姓名</th>
              <th class="p-2.5 text-center">總分(100)</th>
              <th class="p-2.5 text-center">Part A Session 3(50)</th>
              <th class="p-2.5 text-center">Part B Session 4(50)</th>
              <th class="p-2.5">提交時間</th>
              <th class="p-2.5 text-center">操作</th>
            </tr>
          </thead>
          <tbody id="teacherSubmissionsTbody" class="divide-y divide-slate-100">
            <!-- 動態生成 rows -->
          </tbody>
        </table>

        <!-- 小組卡片視圖 (Group View) -->
        <div id="teacherGroupContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 hidden">
          <!-- 動態生成小組卡片 -->
        </div>

        <div id="teacherEmptyNotice" class="text-center py-16 text-slate-400 text-xs hidden">
          <i class="fa-regular fa-folder-open text-3xl mb-2 block"></i>
          目前尚無學生提交紀錄。
        </div>
      </div>
    </div>
  </div>

  <!-- 學生作答詳情 Modal -->
  <div id="studentDetailModalOverlay" class="fixed inset-y-0 inset-x-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-white rounded-2xl max-w-4xl w-full h-[85vh] flex flex-col shadow-2xl border border-slate-100 overflow-hidden">
      <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div>
          <h3 class="text-base font-black text-slate-900" id="detailModalTitle">學生作答明細</h3>
          <p class="text-xs text-slate-500" id="detailModalSubtitle">學號：- ｜ 姓名：-</p>
        </div>
        <button type="button" onclick="closeStudentDetailModal()" class="text-slate-400 hover:text-slate-600">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-4 text-xs leading-relaxed" id="detailModalContent">
        <!-- 動態渲染詳細答案 -->
      </div>

      <div class="p-4 border-t border-slate-200 bg-slate-50 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div class="w-full sm:flex-1">
          <input type="text" id="detailTeacherNoteInput" placeholder="輸入教師課堂評語或討論註記（即時儲存至 D1）..." class="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none">
        </div>
        <div class="flex items-center space-x-2">
          <button type="button" onclick="saveDetailTeacherNote()" class="px-4 py-1.5 rounded-lg text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700">
            儲存註記
          </button>
          <button type="button" onclick="closeStudentDetailModal()" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-200">
            關閉
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 提示 Toast -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 px-4 py-3 rounded-xl shadow-lg text-xs font-bold flex items-center space-x-2 pointer-events-none">
    <i id="toastIcon" class="fa-solid fa-circle-check"></i>
    <span id="toastMsg">操作成功</span>
  </div>

  <!-- JavaScript 核心功能邏輯 -->
  <script>
    const API_BASE_URL = window.location.origin;

    let currentStudentId = '';
    let currentStudentName = '';
    let currentGroupName = '';
    let currentGroupMembers = '';
    let teacherSubmissionsData = [];
    let currentTeacherView = 'all';
    let currentViewingSubmissionId = null;

    document.addEventListener('DOMContentLoaded', () => {
      loadSavedProfile();
      loadDraft();
      initSidebar();
      updateProgress();
    });

    function initSidebar() {
      const toggle = document.getElementById('sidebarToggle');
      const close = document.getElementById('closeSidebar');
      const sidebar = document.getElementById('sidebar');
      if (toggle && sidebar) {
        toggle.addEventListener('click', () => sidebar.classList.toggle('-translate-x-full'));
      }
      if (close && sidebar) {
        close.addEventListener('click', () => sidebar.classList.add('-translate-x-full'));
      }
    }

    // 學生身分與分組
    function loadSavedProfile() {
      currentStudentId = localStorage.getItem('hanen_s6_student_id') || localStorage.getItem('hanen_student_id') || '';
      currentStudentName = localStorage.getItem('hanen_s6_student_name') || localStorage.getItem('hanen_student_name') || '';
      currentGroupName = '';
      currentGroupMembers = '';

      if (document.getElementById('modalStudentId')) document.getElementById('modalStudentId').value = currentStudentId;
      if (document.getElementById('modalStudentName')) document.getElementById('modalStudentName').value = currentStudentName;

      updateStudentBadge();
    }

    function updateStudentBadge() {
      const badge = document.getElementById('studentBannerStatusBadge');
      const profileText = document.getElementById('studentProfileText');
      const title = document.getElementById('studentBannerTitle');

      if (currentStudentId && currentStudentName) {
        badge.className = 'text-[11px] px-2 py-0.5 rounded-full font-bold bg-emerald-100 text-emerald-800 border border-emerald-300';
        badge.textContent = `${currentStudentName} (${currentStudentId})`;
        profileText.textContent = `${currentStudentName}`;
        title.textContent = `已登記：${currentStudentName} (${currentStudentId})`;
      } else {
        badge.className = 'text-[11px] px-2 py-0.5 rounded-full font-bold bg-amber-100 text-amber-800 border border-amber-300';
        badge.textContent = '尚未登記';
        profileText.textContent = '登記學號與姓名';
        title.textContent = '尚未登記學生學號與姓名';
      }
    }

    function openStudentModal() {
      if (document.getElementById('modalStudentId')) document.getElementById('modalStudentId').value = currentStudentId;
      if (document.getElementById('modalStudentName')) document.getElementById('modalStudentName').value = currentStudentName;
      document.getElementById('studentModalOverlay').classList.remove('hidden');
    }

    function closeStudentModal() {
      document.getElementById('studentModalOverlay').classList.add('hidden');
    }

    function saveModalStudentProfile() {
      const id = document.getElementById('modalStudentId').value.trim();
      const name = document.getElementById('modalStudentName').value.trim();

      if (!id || !name) {
        showToast('請務必輸入學號與姓名！', 'warning');
        return;
      }

      currentStudentId = id;
      currentStudentName = name;
      currentGroupName = '';
      currentGroupMembers = '';

      localStorage.setItem('hanen_s6_student_id', id);
      localStorage.setItem('hanen_s6_student_name', name);
      localStorage.setItem('hanen_student_id', id);
      localStorage.setItem('hanen_student_name', name);

      updateStudentBadge();
      closeStudentModal();
      showToast('學生身分已登記儲存！', 'success');
    }

    // 取得所有表單數值
    function getFormValues() {
      return {
        // Part A: Session 3
        s3_q1_1: document.getElementById('s3_q1_1').value.trim(),
        s3_q1_2: document.getElementById('s3_q1_2').value.trim(),
        s3_q1_3: document.getElementById('s3_q1_3').value.trim(),

        s3_q2_1: document.getElementById('s3_q2_1').value.trim(),
        s3_q2_2: document.getElementById('s3_q2_2').value.trim(),
        s3_q2_3: document.getElementById('s3_q2_3').value.trim(),
        s3_q2_4: document.getElementById('s3_q2_4').value.trim(),
        s3_q2_5: document.getElementById('s3_q2_5').value.trim(),

        s3_q3_1: document.getElementById('s3_q3_1').value.trim(),
        s3_q3_2: document.getElementById('s3_q3_2').value.trim(),

        s3_q4_1: document.getElementById('s3_q4_1').value.trim(),
        s3_q4_2: document.getElementById('s3_q4_2').value.trim(),
        s3_q4_3: document.getElementById('s3_q4_3').value.trim(),

        s3_q5: document.getElementById('s3_q5').value.trim(),

        s3_q6_1: document.getElementById('s3_q6_1').value.trim(),
        s3_q6_2: document.getElementById('s3_q6_2').value.trim(),
        s3_q6_3: document.getElementById('s3_q6_3').value.trim(),

        s3_q7_1: document.getElementById('s3_q7_1').value.trim(),
        s3_q7_2: document.getElementById('s3_q7_2').value.trim(),
        s3_q7_3: document.getElementById('s3_q7_3').value.trim(),

        s3_q8_1: document.getElementById('s3_q8_1').value.trim(),
        s3_q8_2: document.getElementById('s3_q8_2').value.trim(),

        s3_q9_1: document.getElementById('s3_q9_1').value.trim(),
        s3_q9_2: document.getElementById('s3_q9_2').value.trim(),
        s3_q9_3: document.getElementById('s3_q9_3').value.trim(),

        s3_q10_1: document.getElementById('s3_q10_1').value.trim(),
        s3_q10_2: document.getElementById('s3_q10_2').value.trim(),
        s3_q10_3: document.getElementById('s3_q10_3').value.trim(),
        s3_q10_4: document.getElementById('s3_q10_4').value.trim(),
        s3_q10_5: document.getElementById('s3_q10_5').value.trim(),

        s3_q11_1: document.getElementById('s3_q11_1').value.trim(),
        s3_q11_2: document.getElementById('s3_q11_2').value.trim(),
        s3_q11_3: document.getElementById('s3_q11_3').value.trim(),
        s3_q11_4: document.getElementById('s3_q11_4').value.trim(),

        // Part B: Session 4
        s4_q1_1: document.getElementById('s4_q1_1').value.trim(),
        s4_q1_2: document.getElementById('s4_q1_2').value.trim(),
        s4_q1_3: document.getElementById('s4_q1_3').value.trim(),
        s4_q1_4: document.getElementById('s4_q1_4').value.trim(),

        s4_q2_1: document.getElementById('s4_q2_1').value.trim(),
        s4_q2_2: document.getElementById('s4_q2_2').value.trim(),
        s4_q2_3: document.getElementById('s4_q2_3').value.trim(),
        s4_q2_4: document.getElementById('s4_q2_4').value.trim(),

        s4_q3_1: document.getElementById('s4_q3_1').value.trim(),
        s4_q3_2: document.getElementById('s4_q3_2').value.trim(),
        s4_q3_3: document.getElementById('s4_q3_3').value.trim(),

        s4_q4_1: document.getElementById('s4_q4_1').value.trim(),
        s4_q4_2_1: document.getElementById('s4_q4_2_1').value.trim(),
        s4_q4_2_2: document.getElementById('s4_q4_2_2').value.trim(),
        s4_q4_2_3: document.getElementById('s4_q4_2_3').value.trim(),
        s4_q4_2_4: document.getElementById('s4_q4_2_4').value.trim()
      };
    }

    function saveDraft(manual = false) {
      const data = getFormValues();
      localStorage.setItem('hanen_session6_draft', JSON.stringify(data));
      if (manual) {
        showToast('學習單草稿已成功暫存於本機！', 'success');
      }
    }

    function loadDraft() {
      const draft = localStorage.getItem('hanen_session6_draft');
      if (!draft) return;
      try {
        const d = JSON.parse(draft);
        for (const k in d) {
          const el = document.getElementById(k);
          if (el) el.value = d[k];
        }
      } catch (e) {}
    }

    function confirmResetWorksheet() {
      if (confirm('確定要清空當前所有填寫內容並重新作答嗎？')) {
        document.getElementById('worksheetForm').reset();
        localStorage.removeItem('hanen_session6_draft');
        updateProgress();
        showToast('學習單已重置。', 'info');
      }
    }

    function updateProgress() {
      const data = getFormValues();
      let filled = 0;
      const keys = Object.keys(data);
      keys.forEach(k => {
        if (data[k]) filled++;
      });
      document.getElementById('answeredProgressText').textContent = `${filled} / ${keys.length} 欄位`;
    }

    // 自動計分 (滿分 100 分：Part A: 50分, Part B: 50分)
    function calculateSession6Scores() {
      const v = getFormValues();
      let pa = 0, pb = 0;

      // Part A: Session 3 (共 50分)
      // 1. 三要素 (4分)
      if (/長度|length/i.test(v.s3_q1_1)) pa += 1.5;
      if (/節奏|pace/i.test(v.s3_q1_2)) pa += 1.5;
      if (/興趣|interest/i.test(v.s3_q1_3)) pa += 1;

      // 2. 五大方法 (5分)
      if (/表情|面部|臉/.test(v.s3_q2_1)) pa += 1;
      if (/視覺/.test(v.s3_q2_2)) pa += 1;
      if (/暫停|改變/.test(v.s3_q2_3)) pa += 1;
      if (/手把手|肢體|協助/.test(v.s3_q2_4)) pa += 1;
      if (/問題|發問/.test(v.s3_q2_5)) pa += 1;

      // 3. 投影片14 (4分)
      if (/yes|no|wh|問句/i.test(v.s3_q3_1)) pa += 2;
      if (/什麼|直升機|書|圖片/.test(v.s3_q3_2)) pa += 2;

      // 4. Stoppers (4分)
      if (/多|追問|時間|考驗|太難|興趣|自問/.test(v.s3_q4_1)) pa += 1;
      if (/多|追問|時間|考驗|太難|興趣|自問/.test(v.s3_q4_2)) pa += 1;
      if (/評論|陳述|描述|情境|turn questions into comments/i.test(v.s3_q4_3)) pa += 2;

      // 5. 二選一 vs 是非題 (4分)
      let s5_score = 0;
      if (/二選一|選項|詞彙|模型/.test(v.s3_q5)) s5_score += 2;
      if (/是非|點頭|搖頭|門檻|初階/.test(v.s3_q5)) s5_score += 2;
      pa += Math.min(4, s5_score);

      // 6. Emily 下午茶 (5分)
      if (/維持|話題|keep the conversation|開口|說話|輪替/.test(v.s3_q6_1)) pa += 1.5;
      if (/tea|sugar|same|one|two|three|茶|糖/i.test(v.s3_q6_2)) pa += 2;
      if (/yeah|點頭|動作|好/i.test(v.s3_q6_3)) pa += 1.5;

      // 7. Alicia 提問與評論 (5分)
      if (/連續|測試|考試|限制/.test(v.s3_q7_1)) pa += 1.5;
      if (/評論|描述|結合|等待/.test(v.s3_q7_2)) pa += 2;
      if (/參與|自然|流暢|減少壓力/.test(v.s3_q7_3)) pa += 1.5;

      // 8. Sean 肢體常規 (5分)
      if (/暫停|pause|等待|表情|手勢|肢體/i.test(v.s3_q8_1)) pa += 2.5;
      if (/加大|手把手|視覺|提示|引導/.test(v.s3_q8_2)) pa += 2.5;

      // 9. Jack SPARK (5分)
      if (/例行|活動|spark|常規/.test(v.s3_q9_1)) pa += 1.5;
      if (/暫停|表情|眼神|問句|等待/.test(v.s3_q9_2)) pa += 2;
      if (/興趣|評論|等待|日常/.test(v.s3_q9_3)) pa += 1.5;

      // 10. SPARK 五步驟 (5分)
      if (/相同|開始|start/i.test(v.s3_q10_1)) pa += 1;
      if (/輪替|輪流|plan/i.test(v.s3_q10_2)) pa += 1;
      if (/調整|改變|adjust/i.test(v.s3_q10_3)) pa += 1;
      if (/重複|repeat/i.test(v.s3_q10_4)) pa += 1;
      if (/固定|結尾|結束|end/i.test(v.s3_q10_5)) pa += 1;

      // 11. SPARK 規劃開放題 (9分)
      let s11_score = 0;
      if (v.s3_q11_1.length >= 4) s11_score += 2.5;
      if (v.s3_q11_2.length >= 4) s11_score += 2;
      if (v.s3_q11_3.length >= 4) s11_score += 2.5;
      if (v.s3_q11_4.length >= 3) s11_score += 2;
      pa += Math.min(9, s11_score);

      // Part B: Session 4 (共 50分)
      // 1. 四大策略 (8分)
      if (/模仿|imitate/i.test(v.s4_q1_1)) pb += 2;
      if (/解釋|口譯|interpret/i.test(v.s4_q1_2)) pb += 2;
      if (/回應|評論|comment/i.test(v.s4_q1_3)) pb += 2;
      if (/提問|問|ask/i.test(v.s4_q1_4)) pb += 2;

      // 2. 4S 原則 (8分)
      if (/say less|少說/i.test(v.s4_q2_1)) pb += 2;
      if (/stress|強調|重音/i.test(v.s4_q2_2)) pb += 2;
      if (/go slow|放慢|慢說/i.test(v.s4_q2_3)) pb += 2;
      if (/show|展示|做給你看/i.test(v.s4_q2_4)) pb += 2;

      // 3. Tristan 與爸爸 (18分)
      let t1 = 0, t2 = 0, t3 = 0;
      if (/蹲|球池|平視|認真|增強/.test(v.s4_q3_1)) t1 += 6; else if (v.s4_q3_1.length >= 8) t1 += 3;
      if (/沒有|直接|搶|配合|製造|正向|回饋/.test(v.s4_q3_2)) t2 += 6; else if (v.s4_q3_2.length >= 8) t2 += 3;
      if (/shovel|鏟子|球|ball|plane|飛機|擴充|where/i.test(v.s4_q3_3)) t3 += 6; else if (v.s4_q3_3.length >= 10) t3 += 3;
      pb += (t1 + t2 + t3);

      // 4. 4S 影片 (16分: 6 + 10)
      let s4_1 = 0;
      if (/big|up|簡短|放慢|展示|重複|名字|表情/.test(v.s4_q4_1)) s4_1 += 6; else if (v.s4_q4_1.length >= 10) s4_1 += 3;

      let s4_2 = 0;
      if (/簡短|單詞|block|降低/i.test(v.s4_q4_2_1)) s4_2 += 2.5; else if (v.s4_q4_2_1.length >= 5) s4_2 += 1.5;
      if (/重讀|音調|加強|聲學|聚焦/i.test(v.s4_q4_2_2)) s4_2 += 2.5; else if (v.s4_q4_2_2.length >= 5) s4_2 += 1.5;
      if (/放慢|停頓|等待|ready|拉長/i.test(v.s4_q4_2_3)) s4_2 += 2.5; else if (v.s4_q4_2_3.length >= 5) s4_2 += 1.5;
      if (/展示|捧出|拍打|動作|視覺|連結/i.test(v.s4_q4_2_4)) s4_2 += 2.5; else if (v.s4_q4_2_4.length >= 5) s4_2 += 1.5;
      pb += (s4_1 + s4_2);

      pa = Math.min(50, Math.round(pa));
      pb = Math.min(50, Math.round(pb));
      return { total: pa + pb, pa, pb };
    }

    // 提交學習單
    async function submitWorksheet() {
      if (!currentStudentId || !currentStudentName) {
        openStudentModal();
        showToast('請先登記學號與姓名再提交！', 'warning');
        return;
      }

      const scores = calculateSession6Scores();
      const answers = getFormValues();
      const btn = document.getElementById('submitBtn');
      const originalText = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>提交中...';

      try {
        const payload = {
          student_id: currentStudentId,
          student_name: currentStudentName,
          group_name: currentGroupName,
          group_members: currentGroupMembers,
          total_score: scores.total,
          score_part1: scores.pa,
          score_part2: scores.pb,
          answers_json: answers,
          ai_feedback: ''
        };

        const res = await fetch(`${API_BASE_URL}/api/session6/submit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!data.success) throw new Error(data.error || '提交失敗');

        // 顯示成績彈窗
        document.getElementById('scoreModalTotal').innerHTML = `${scores.total} <span class="text-base font-normal">/ 100</span>`;
        document.getElementById('scoreModalStudentInfo').textContent = `${currentStudentName} (學號: ${currentStudentId})`;
        document.getElementById('scoreModalPartA').textContent = `${scores.pa} / 50`;
        document.getElementById('scoreModalPartB').textContent = `${scores.pb} / 50`;

        document.getElementById('scoreReportModalOverlay').classList.remove('hidden');
        showToast('第六節學習單提交成功，已儲存至 D1 資料庫！', 'success');
      } catch (err) {
        alert(`提交失敗：${err.message}`);
      } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
      }
    }

    function closeScoreModal() {
      document.getElementById('scoreReportModalOverlay').classList.add('hidden');
    }

    // AI 助教審閱
    async function requestAiReview(fieldId, topicName, maxScore) {
      const v = getFormValues();
      let text = '';

      if (fieldId === 's3_q3_combined') {
        text = `延續方法：${v.s3_q3_1}\n舉例：${v.s3_q3_2}`;
      } else if (fieldId === 's3_q11_combined') {
        text = `S名稱與視覺：${v.s3_q11_1}\nP輪流時機：${v.s3_q11_2}\nA提示等待：${v.s3_q11_3}\nK結束信號：${v.s3_q11_4}`;
      } else if (fieldId === 's4_q3_combined') {
        text = `爸爸位置與態度：${v.s4_q3_1}\n創造遊戲互動：${v.s4_q3_2}\n擴充訊息範例：${v.s4_q3_3}`;
      } else if (fieldId === 's4_q4_combined') {
        text = `吸引注意：${v.s4_q4_1}\n4S原則Say less：${v.s4_q4_2_1}\nStress：${v.s4_q4_2_2}\nGo slow：${v.s4_q4_2_3}\nShow：${v.s4_q4_2_4}`;
      } else {
        const el = document.getElementById(fieldId);
        text = el ? el.value.trim() : '';
      }

      if (!text) {
        showToast('請先輸入相關作答內容再請求 AI 助教審閱！', 'warning');
        return;
      }

      document.getElementById('aiReviewTopicText').textContent = topicName;
      document.getElementById('aiReviewContent').textContent = '正在連線臨床督導助教模型審閱中，請稍候（約 2~3 秒）...';
      document.getElementById('aiReviewModal').classList.remove('hidden');

      try {
        const res = await fetch(`${API_BASE_URL}/api/ai/review-session6`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            student_name: currentStudentName || '同學',
            student_id: currentStudentId,
            group_name: currentGroupName,
            question_topic: topicName,
            question_text: topicName,
            answer_text: text,
            max_score: maxScore
          })
        });

        const data = await res.json();
        if (!data.success) throw new Error(data.error || 'AI 審閱失敗');

        document.getElementById('aiReviewContent').textContent = data.feedback;
      } catch (err) {
        document.getElementById('aiReviewContent').textContent = `AI 助教審閱連線異常：${err.message}\n請確認網路連線或稍後再試。`;
      }
    }

    function closeAiModal() {
      document.getElementById('aiReviewModal').classList.add('hidden');
    }

    // 教師端儀表板
    async function loadTeacherDashboard() {
      document.getElementById('teacherDashboardModalOverlay').classList.remove('hidden');
      document.getElementById('teacherLoadingIndicator').classList.remove('hidden');
      document.getElementById('teacherSubmissionsTable').classList.add('hidden');
      document.getElementById('teacherGroupContainer').classList.add('hidden');
      document.getElementById('teacherEmptyNotice').classList.add('hidden');

      try {
        const res = await fetch(`${API_BASE_URL}/api/session6/submissions`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error || '讀取失敗');

        teacherSubmissionsData = json.data || [];
        updateTeacherStats();
        renderTeacherView();
      } catch (err) {
        alert(`無法載入作答資料：${err.message}`);
      } finally {
        document.getElementById('teacherLoadingIndicator').classList.add('hidden');
      }
    }

    function closeTeacherDashboard() {
      document.getElementById('teacherDashboardModalOverlay').classList.add('hidden');
    }

    function updateTeacherStats() {
      const total = teacherSubmissionsData.length;
      document.getElementById('statTotalSubmissions').textContent = total;

      const studentSet = new Set();
      const groupSet = new Set();
      let scoreSum = 0;

      teacherSubmissionsData.forEach(r => {
        studentSet.add(r.student_id);
        if (r.group_name) groupSet.add(r.group_name);
        scoreSum += Number(r.total_score) || 0;
      });

      document.getElementById('statUniqueStudents').textContent = studentSet.size;
      document.getElementById('statTotalGroups').textContent = groupSet.size;
      document.getElementById('statAverageScore').textContent = total > 0 ? (scoreSum / total).toFixed(1) : 0;
    }

    function switchTeacherViewMode(mode) {
      currentTeacherView = mode;
      document.getElementById('viewModeAllBtn').className = mode === 'all' ? 'px-3 py-1.5 rounded-lg font-bold bg-indigo-600 text-white' : 'px-3 py-1.5 rounded-lg font-bold bg-slate-100 text-slate-700 hover:bg-slate-200';
      document.getElementById('viewModeGroupBtn').className = mode === 'group' ? 'px-3 py-1.5 rounded-lg font-bold bg-indigo-600 text-white' : 'px-3 py-1.5 rounded-lg font-bold bg-slate-100 text-slate-700 hover:bg-slate-200';
      document.getElementById('viewModeHistoryBtn').className = mode === 'history' ? 'px-3 py-1.5 rounded-lg font-bold bg-indigo-600 text-white' : 'px-3 py-1.5 rounded-lg font-bold bg-slate-100 text-slate-700 hover:bg-slate-200';
      renderTeacherView();
    }

    function filterTeacherSubmissions() {
      renderTeacherView();
    }

    function getFilteredData() {
      const q = document.getElementById('teacherSearchInput').value.trim().toLowerCase();
      let list = teacherSubmissionsData;

      if (q) {
        list = list.filter(r => 
          (r.student_id && r.student_id.toLowerCase().includes(q)) ||
          (r.student_name && r.student_name.toLowerCase().includes(q)) ||
          (r.group_name && r.group_name.toLowerCase().includes(q))
        );
      }

      if (currentTeacherView === 'all') {
        const map = new Map();
        list.forEach(r => {
          if (!map.has(r.student_id)) {
            map.set(r.student_id, r);
          }
        });
        return Array.from(map.values());
      }

      return list;
    }

    function renderTeacherView() {
      const list = getFilteredData();
      const table = document.getElementById('teacherSubmissionsTable');
      const groupContainer = document.getElementById('teacherGroupContainer');
      const empty = document.getElementById('teacherEmptyNotice');

      if (!list || list.length === 0) {
        table.classList.add('hidden');
        groupContainer.classList.add('hidden');
        empty.classList.remove('hidden');
        return;
      }

      empty.classList.add('hidden');

      if (currentTeacherView === 'group') {
        table.classList.add('hidden');
        groupContainer.classList.remove('hidden');
        renderGroupCards(list);
      } else {
        groupContainer.classList.add('hidden');
        table.classList.remove('hidden');
        renderTableRows(list);
      }
    }

    function renderTableRows(list) {
      const tbody = document.getElementById('teacherSubmissionsTbody');
      tbody.innerHTML = list.map(r => `
        <tr class="hover:bg-slate-50 transition">
          <td class="p-2.5 font-bold text-indigo-700">${escapeHtml(r.group_name || '個人')}</td>
          <td class="p-2.5 font-mono text-slate-600">${escapeHtml(r.student_id)}</td>
          <td class="p-2.5 font-bold text-slate-900">${escapeHtml(r.student_name)}</td>
          <td class="p-2.5 text-center font-black text-indigo-600">${r.total_score}</td>
          <td class="p-2.5 text-center text-slate-600">${r.score_part1} / 50</td>
          <td class="p-2.5 text-center text-slate-600">${r.score_part2} / 50</td>
          <td class="p-2.5 text-slate-400 font-mono text-[11px]">${r.submitted_at || ''}</td>
          <td class="p-2.5 text-center">
            <button type="button" onclick="openStudentDetailModal(${r.id})" class="px-2.5 py-1 rounded-lg text-xs font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200">
              檢視作答
            </button>
          </td>
        </tr>
      `).join('');
    }

    function renderGroupCards(list) {
      const container = document.getElementById('teacherGroupContainer');
      const groupMap = new Map();

      list.forEach(r => {
        const g = r.group_name || '未分組';
        if (!groupMap.has(g)) groupMap.set(g, []);
        groupMap.get(g).push(r);
      });

      let html = '';
      groupMap.forEach((members, gName) => {
        const avg = (members.reduce((s, m) => s + Number(m.total_score || 0), 0) / members.length).toFixed(1);
        html += `
          <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-3">
            <div class="flex items-center justify-between pb-2 border-b border-slate-100">
              <span class="font-black text-sm text-indigo-800"><i class="fa-solid fa-users text-indigo-600 mr-1.5"></i>${escapeHtml(gName)}</span>
              <span class="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">平均分：${avg}</span>
            </div>
            <div class="space-y-1.5">
              ${members.map(m => `
                <div class="flex items-center justify-between text-xs p-1.5 rounded bg-slate-50">
                  <span class="font-medium text-slate-800">${escapeHtml(m.student_name)} (${escapeHtml(m.student_id)})</span>
                  <div class="flex items-center space-x-2">
                    <span class="font-black text-indigo-600">${m.total_score}分</span>
                    <button type="button" onclick="openStudentDetailModal(${m.id})" class="text-[11px] text-indigo-600 hover:underline">詳情</button>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    // 檢視作答細節
    function openStudentDetailModal(id) {
      const record = teacherSubmissionsData.find(r => r.id === id);
      if (!record) return;

      currentViewingSubmissionId = id;
      document.getElementById('detailModalTitle').textContent = `作答詳細卷 · ${record.student_name} (${record.student_id})`;
      document.getElementById('detailModalSubtitle').textContent = `組別：${record.group_name || '個人'} ｜ 總分：${record.total_score} (Part A: ${record.score_part1}/50, Part B: ${record.score_part2}/50) ｜ 時間：${record.submitted_at}`;
      document.getElementById('detailTeacherNoteInput').value = record.teacher_notes || '';

      const a = record.answers || {};
      let html = `
        <div class="space-y-4">
          <div class="p-3 bg-indigo-50 rounded-xl border border-indigo-200">
            <h4 class="font-bold text-indigo-800 mb-1">【Part A：Session 3 促進互動成長 (得分: ${record.score_part1} / 50)】</h4>
            <p><strong>1. 三要素：</strong> ${escapeHtml(a.s3_q1_1 || '')} ｜ ${escapeHtml(a.s3_q1_2 || '')} ｜ ${escapeHtml(a.s3_q1_3 || '')}</p>
            <p class="mt-1"><strong>2. 提示五大方法：</strong> ① ${escapeHtml(a.s3_q2_1 || '')} ② ${escapeHtml(a.s3_q2_2 || '')} ③ ${escapeHtml(a.s3_q2_3 || '')} ④ ${escapeHtml(a.s3_q2_4 || '')} ⑤ ${escapeHtml(a.s3_q2_5 || '')}</p>
            <p class="mt-1"><strong>3. 投影片14 (繪本延續對話)：</strong> (1) ${escapeHtml(a.s3_q3_1 || '')} ｜ (2) ${escapeHtml(a.s3_q3_2 || '')}</p>
            <p class="mt-1"><strong>4. 避開 Stoppers：</strong> 避免① ${escapeHtml(a.s3_q4_1 || '')} ｜ ② ${escapeHtml(a.s3_q4_2 || '')} ｜ 技巧：${escapeHtml(a.s3_q4_3 || '')}</p>
            <p class="mt-1"><strong>5. 二選一 vs 是非題：</strong> ${escapeHtml(a.s3_q5 || '')}</p>
            <p class="mt-1"><strong>6. Emily 下午茶：</strong> (1) ${escapeHtml(a.s3_q6_1 || '')} ｜ (2) ${escapeHtml(a.s3_q6_2 || '')} ｜ (3) ${escapeHtml(a.s3_q6_3 || '')}</p>
            <p class="mt-1"><strong>7. Alicia 提問與評論：</strong> (1) ${escapeHtml(a.s3_q7_1 || '')} ｜ (2) ${escapeHtml(a.s3_q7_2 || '')} ｜ (3) ${escapeHtml(a.s3_q7_3 || '')}</p>
            <p class="mt-1"><strong>8. Sean 肢體互動常規：</strong> (1) ${escapeHtml(a.s3_q8_1 || '')} ｜ (2) ${escapeHtml(a.s3_q8_2 || '')}</p>
            <p class="mt-1"><strong>9. Jack 盪鞦韆與 SPARK：</strong> (1) ${escapeHtml(a.s3_q9_1 || '')} ｜ (2) ${escapeHtml(a.s3_q9_2 || '')} ｜ (3) ${escapeHtml(a.s3_q9_3 || '')}</p>
            <p class="mt-1"><strong>10. SPARK 五步驟：</strong> S: ${escapeHtml(a.s3_q10_1 || '')} ｜ P: ${escapeHtml(a.s3_q10_2 || '')} ｜ A: ${escapeHtml(a.s3_q10_3 || '')} ｜ R: ${escapeHtml(a.s3_q10_4 || '')} ｜ K: ${escapeHtml(a.s3_q10_5 || '')}</p>
            <p class="mt-1"><strong>11. SPARK 實務設計：</strong> [S] ${escapeHtml(a.s3_q11_1 || '')} ｜ [P] ${escapeHtml(a.s3_q11_2 || '')} ｜ [A] ${escapeHtml(a.s3_q11_3 || '')} ｜ [K] ${escapeHtml(a.s3_q11_4 || '')}</p>
          </div>

          <div class="p-3 bg-purple-50 rounded-xl border border-purple-200">
            <h4 class="font-bold text-purple-800 mb-1">【Part B：Session 4 雙向溝通 - 家長漢能計畫 (得分: ${record.score_part2} / 50)】</h4>
            <p><strong>壹-1. 四大策略：</strong> ① ${escapeHtml(a.s4_q1_1 || '')} ｜ ② ${escapeHtml(a.s4_q1_2 || '')} ｜ ③ ${escapeHtml(a.s4_q1_3 || '')} ｜ ④ ${escapeHtml(a.s4_q1_4 || '')}</p>
            <p class="mt-1"><strong>壹-2. 4S 原則：</strong> ① ${escapeHtml(a.s4_q2_1 || '')} ｜ ② ${escapeHtml(a.s4_q2_2 || '')} ｜ ③ ${escapeHtml(a.s4_q2_3 || '')} ｜ ④ ${escapeHtml(a.s4_q2_4 || '')}</p>
            <p class="mt-1"><strong>貳. Tristan 與爸爸：</strong></p>
            <ul class="list-disc pl-5 space-y-0.5">
              <li>位置與態度：${escapeHtml(a.s4_q3_1 || '')}</li>
              <li>互動與創造：${escapeHtml(a.s4_q3_2 || '')}</li>
              <li>擴充訊息 (Expand)：${escapeHtml(a.s4_q3_3 || '')}</li>
            </ul>
            <p class="mt-1"><strong>參. 4S 原則影片觀察：</strong></p>
            <p class="pl-2">吸引注意：${escapeHtml(a.s4_q4_1 || '')}</p>
            <ul class="list-disc pl-5 space-y-0.5">
              <li>Say less: ${escapeHtml(a.s4_q4_2_1 || '')}</li>
              <li>Stress: ${escapeHtml(a.s4_q4_2_2 || '')}</li>
              <li>Go slow: ${escapeHtml(a.s4_q4_2_3 || '')}</li>
              <li>Show: ${escapeHtml(a.s4_q4_2_4 || '')}</li>
            </ul>
          </div>
        </div>
      `;
      document.getElementById('detailModalContent').innerHTML = html;
      document.getElementById('studentDetailModalOverlay').classList.remove('hidden');
    }

    function closeStudentDetailModal() {
      document.getElementById('studentDetailModalOverlay').classList.add('hidden');
    }

    async function saveDetailTeacherNote() {
      if (!currentViewingSubmissionId) return;
      const note = document.getElementById('detailTeacherNoteInput').value.trim();

      try {
        const res = await fetch(`${API_BASE_URL}/api/session6/update-notes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: currentViewingSubmissionId, teacher_notes: note })
        });
        const json = await res.json();
        if (!json.success) throw new Error(json.error || '儲存失敗');

        const rec = teacherSubmissionsData.find(r => r.id === currentViewingSubmissionId);
        if (rec) rec.teacher_notes = note;

        showToast('課堂討論註記已儲存至 D1 資料庫！', 'success');
      } catch (err) {
        alert(`儲存失敗：${err.message}`);
      }
    }

    // 匯出 Excel
    function exportToExcel() {
      if (!teacherSubmissionsData || teacherSubmissionsData.length === 0) {
        showToast('目前尚無資料可匯出！', 'warning');
        return;
      }

      // 1. 最新成績總表 (去重)
      const studentMap = new Map();
      teacherSubmissionsData.forEach(r => {
        if (!studentMap.has(r.student_id)) {
          studentMap.set(r.student_id, { ...r, count: 1 });
        } else {
          studentMap.get(r.student_id).count += 1;
        }
      });

      const sheet1Data = Array.from(studentMap.values()).map((r, idx) => ({
        '項次': idx + 1,
        '小組': r.group_name || '個人',
        '同組成員': r.group_members || '',
        '學號': r.student_id,
        '姓名': r.student_name,
        '總成績': r.total_score,
        'Part A: Session 3得分(50分)': r.score_part1,
        'Part B: Session 4得分(50分)': r.score_part2,
        '教師課堂註記': r.teacher_notes || '',
        '累計作答次數': r.count,
        '最後提交時間': r.submitted_at || ''
      }));

      // 2. 歷次完整作答軌跡
      const sheet2Data = teacherSubmissionsData.map((r, idx) => {
        const a = r.answers || {};
        return {
          '紀錄ID': r.id,
          '小組': r.group_name || '個人',
          '學號': r.student_id,
          '姓名': r.student_name,
          '總成績': r.total_score,
          '三要素': `${a.s3_q1_1 || ''} / ${a.s3_q1_2 || ''} / ${a.s3_q1_3 || ''}`,
          '提示五大方法': `${a.s3_q2_1 || ''} / ${a.s3_q2_2 || ''} / ${a.s3_q2_3 || ''} / ${a.s3_q2_4 || ''} / ${a.s3_q2_5 || ''}`,
          '投影片14延續對話': `${a.s3_q3_1 || ''} (${a.s3_q3_2 || ''})`,
          '避開Stoppers': `免: ${a.s3_q4_1 || ''}, ${a.s3_q4_2 || ''} / 技巧: ${a.s3_q4_3 || ''}`,
          '二選一vs是非題': a.s3_q5 || '',
          'Emily下午茶': `機會:${a.s3_q6_1 || ''} / 台詞:${a.s3_q6_2 || ''} / 回應:${a.s3_q6_3 || ''}`,
          'Alicia媽媽改變': `問題:${a.s3_q7_1 || ''} / 改變:${a.s3_q7_2 || ''} / 反應:${a.s3_q7_3 || ''}`,
          'Sean肢體常規': `常規:${a.s3_q8_1 || ''} / 進一步提示:${a.s3_q8_2 || ''}`,
          'Jack SPARK': `概念:${a.s3_q9_1 || ''} / 提示:${a.s3_q9_2 || ''} / 無回應:${a.s3_q9_3 || ''}`,
          'SPARK步驟': `${a.s3_q10_1 || ''} / ${a.s3_q10_2 || ''} / ${a.s3_q10_3 || ''} / ${a.s3_q10_4 || ''} / ${a.s3_q10_5 || ''}`,
          'SPARK實務設計': `[S]${a.s3_q11_1 || ''} [P]${a.s3_q11_2 || ''} [A]${a.s3_q11_3 || ''} [K]${a.s3_q11_4 || ''}`,
          '加入語言四大策略': `${a.s4_q1_1 || ''} / ${a.s4_q1_2 || ''} / ${a.s4_q1_3 || ''} / ${a.s4_q1_4 || ''}`,
          '4S原則': `${a.s4_q2_1 || ''} / ${a.s4_q2_2 || ''} / ${a.s4_q2_3 || ''} / ${a.s4_q2_4 || ''}`,
          'Tristan位置態度': a.s4_q3_1 || '',
          'Tristan遊戲互動': a.s4_q3_2 || '',
          'Tristan擴充訊息': a.s4_q3_3 || '',
          '4S吸引注意': a.s4_q4_1 || '',
          '4S原則SayLess': a.s4_q4_2_1 || '',
          '4S原則Stress': a.s4_q4_2_2 || '',
          '4S原則GoSlow': a.s4_q4_2_3 || '',
          '4S原則Show': a.s4_q4_2_4 || '',
          '提交時間': r.submitted_at || ''
        };
      });

      const wb = XLSX.utils.book_new();
      const ws1 = XLSX.utils.json_to_sheet(sheet1Data);
      const ws2 = XLSX.utils.json_to_sheet(sheet2Data);

      XLSX.utils.book_append_sheet(wb, ws1, '最新成績總表');
      XLSX.utils.book_append_sheet(wb, ws2, '歷次作答詳細清單');

      XLSX.writeFile(wb, `第六節_Session3_4_學生學習單成績總表_${new Date().toISOString().slice(0, 10)}.xlsx`);
      showToast('Excel 報表匯出成功！', 'success');
    }

    // 清空歷史紀錄
    async function clearDatabaseRecords() {
      const promptVal = prompt('【危險操作】請輸入 "CLEAR" 以確認清空第六節 (Session 3 & 4) 的所有學生作答紀錄：');
      if (promptVal !== 'CLEAR') {
        showToast('取消清空操作。', 'info');
        return;
      }

      try {
        const res = await fetch(`${API_BASE_URL}/api/session6/clear`, {
          method: 'POST'
        });
        const json = await res.json();
        if (!json.success) throw new Error(json.error || '清除失敗');

        teacherSubmissionsData = [];
        updateTeacherStats();
        renderTeacherView();
        showToast('已成功清空第六節所有歷史紀錄！', 'success');
      } catch (err) {
        alert(`清空失敗：${err.message}`);
      }
    }

    function showToast(msg, type = 'info') {
      const toast = document.getElementById('toast');
      const icon = document.getElementById('toastIcon');
      const text = document.getElementById('toastMsg');

      text.textContent = msg;
      if (type === 'success') {
        toast.className = 'fixed bottom-6 right-6 z-50 transform translate-y-0 opacity-100 transition-all duration-300 px-4 py-3 rounded-xl shadow-lg text-xs font-bold flex items-center space-x-2 bg-emerald-600 text-white';
        icon.className = 'fa-solid fa-circle-check';
      } else if (type === 'warning') {
        toast.className = 'fixed bottom-6 right-6 z-50 transform translate-y-0 opacity-100 transition-all duration-300 px-4 py-3 rounded-xl shadow-lg text-xs font-bold flex items-center space-x-2 bg-amber-500 text-white';
        icon.className = 'fa-solid fa-triangle-exclamation';
      } else {
        toast.className = 'fixed bottom-6 right-6 z-50 transform translate-y-0 opacity-100 transition-all duration-300 px-4 py-3 rounded-xl shadow-lg text-xs font-bold flex items-center space-x-2 bg-slate-800 text-white';
        icon.className = 'fa-solid fa-info-circle';
      }

      setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
      }, 3000);
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }
  </script>
</body>
</html>
'''

with open(r'D:\2026ant線上教學網站\public\session6.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('session6.html created successfully!')
