# -*- coding: utf-8 -*-
import os

session5_6_nav = '''
        <!-- 第五節：Session 1 學生分組學習單 -->
        <a href="session5.html" class="block p-3 rounded-xl border border-sky-200 bg-sky-50/60 hover:bg-sky-100/70 transition group shadow-sm">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-bold text-sky-700 bg-sky-100 px-2 py-0.5 rounded">第五節 · 學生分組</span>
            <i class="fa-solid fa-arrow-right text-xs text-sky-500 group-hover:translate-x-0.5 transition"></i>
          </div>
          <h4 class="font-bold text-xs text-slate-900 group-hover:text-sky-700 transition">【Session 1 課堂學習單】Let Your Child Lead</h4>
          <p class="text-[11px] text-slate-600 mt-0.5">互動起點、溝通四階段、OWL策略與影片觀察（滿分100分）。</p>
        </a>

        <!-- 第六節：Session 3 & 4 學生分組學習單 -->
        <a href="session6.html" class="block p-3 rounded-xl border border-indigo-200 bg-indigo-50/60 hover:bg-indigo-100/70 transition group shadow-sm">
          <div class="flex items-center justify-between mb-1">
            <span class="text-[11px] font-bold text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">第六節 · 學生分組</span>
            <i class="fa-solid fa-arrow-right text-xs text-indigo-500 group-hover:translate-x-0.5 transition"></i>
          </div>
          <h4 class="font-bold text-xs text-slate-900 group-hover:text-indigo-700 transition">【Session 3 & 4 課堂學習單】雙向溝通與促進互動</h4>
          <p class="text-[11px] text-slate-600 mt-0.5">提示技巧、SPARK模型、加入語言四大策略與4S原則（滿分100分）。</p>
        </a>
'''

# 1. session2.html
with open(r'D:\2026ant線上教學網站\public\session2.html', 'r', encoding='utf-8') as f:
    c2 = f.read()
if 'session5.html' not in c2:
    target2 = '三大核心影片觀察、Jacob/Alicia/柏翔真實個案深入剖析（滿分100分）。</p>\n        </a>'
    if target2 in c2:
        c2 = c2.replace(target2, target2 + '\n' + session5_6_nav)
        with open(r'D:\2026ant線上教學網站\public\session2.html', 'w', encoding='utf-8') as f:
            f.write(c2)
        print('Updated session2.html')

# 2. session3.html
with open(r'D:\2026ant線上教學網站\public\session3.html', 'r', encoding='utf-8') as f:
    c3 = f.read()
if 'session5.html' not in c3:
    target2 = '三大核心影片觀察、Jacob/Alicia/柏翔真實個案深入剖析（滿分100分）。</p>\n        </a>'
    if target2 in c3:
        c3 = c3.replace(target2, target2 + '\n' + session5_6_nav)
        with open(r'D:\2026ant線上教學網站\public\session3.html', 'w', encoding='utf-8') as f:
            f.write(c3)
        print('Updated session3.html')

# 3. session4.html
with open(r'D:\2026ant線上教學網站\public\session4.html', 'r', encoding='utf-8') as f:
    c4 = f.read()
if 'session5.html' not in c4:
    target4 = '三大核心影片題型、臨床實務深度剖析（滿分100分）。</p>'
    pos = c4.find(target4)
    if pos != -1:
        end_div_pos = c4.find('</div>\n      </div>', pos)
        if end_div_pos != -1:
            insert_point = end_div_pos + len('</div>')
            c4 = c4[:insert_point] + '\n' + session5_6_nav + c4[insert_point:]
            with open(r'D:\2026ant線上教學網站\public\session4.html', 'w', encoding='utf-8') as f:
                f.write(c4)
            print('Updated session4.html')

print('All sidebars synced!')
