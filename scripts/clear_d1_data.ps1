# PowerShell 清除 Cloudflare D1 學生作答與 AI 家教歷程工具
# 檔案路徑：d:\2026ant線上教學網站\scripts\clear_d1_data.ps1

Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host " 🧹 自閉症與溝通障礙教學平台 - Cloudflare D1 資料庫重設工具 " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "請選擇欲清除的資料庫項目：" -ForegroundColor Cyan
Write-Host "  [1] 僅清除【學生測驗作答成績】(student_submissions)"
Write-Host "  [2] 僅清除【AI 蘇格拉底對話歷程】(ai_tutor_sessions / messages)"
Write-Host "  [3] 清除【全部紀錄】(測驗成績 ＋ AI 家教歷程)"
Write-Host "  [Q] 放棄取消"
Write-Host ""

$choice = Read-Host "請輸入選項 (1 / 2 / 3 / Q)"

if ($choice -eq "1") {
    $cmd = "DELETE FROM student_submissions;"
    $desc = "學生測驗作答成績"
} elseif ($choice -eq "2") {
    $cmd = "DELETE FROM ai_tutor_messages; DELETE FROM ai_tutor_sessions;"
    $desc = "AI 蘇格拉底對話歷程"
} elseif ($choice -eq "3") {
    $cmd = "DELETE FROM student_submissions; DELETE FROM ai_tutor_messages; DELETE FROM ai_tutor_sessions;"
    $desc = "全部歷史紀錄（測驗成績 ＋ AI 家教歷程）"
} else {
    Write-Host "操作已取消。" -ForegroundColor Gray
    exit 0
}

Write-Host ""
Write-Host "⚠️ 警告：即將永久刪除 Cloudflare D1 雲端資料庫中的【$desc】！" -ForegroundColor Red
$confirm = Read-Host "請輸入「CLEAR」確認執行"

if ($confirm -ne "CLEAR") {
    Write-Host "確認碼不符，已取消清除作業。" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "正在連線 Cloudflare D1 執行清除作業..." -ForegroundColor Cyan

$wranglerPath = "C:\Users\Administrator\AppData\Roaming\npm\wrangler.cmd"
& $wranglerPath d1 execute autism-comm-disorders-db --remote --command $cmd

Write-Host ""
Write-Host "🎉 清除作業已順利完成！" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Yellow
