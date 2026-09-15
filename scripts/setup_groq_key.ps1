# PowerShell 安全設定 Groq API Key 腳本
# 檔案位置：d:\2026ant線上教學網站\scripts\setup_groq_key.ps1

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🤖 自閉症與溝通障礙教學平台 - AI 蘇格拉底家教 (Groq Key 設定) " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "請直接在下方貼上您的 Groq API Key（以 gsk_ 開頭）：" -ForegroundColor Yellow

$key = Read-Host -Prompt "Groq API Key"

if (-not $key -or -not $key.Trim().StartsWith("gsk_")) {
    Write-Host ""
    Write-Host "❌ 警告：輸入的 API Key 格式似乎不正確（通常以 gsk_ 開頭），請確認後重新執行。" -ForegroundColor Red
    exit 1
}

$cleanKey = $key.Trim()

# 寫入專案環境變數檔 .dev.vars (UTF-8 無 BOM 格式，供 Cloudflare Wrangler 讀取)
$devVarsContent = "GROQ_API_KEY=$cleanKey`nAI_API_KEY=$cleanKey`nAI_MODEL=qwen/qwen3.8-27b`n"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText("d:\2026ant線上教學網站\.dev.vars", $devVarsContent, $utf8NoBom)

# 設定當前與使用者環境變數
[System.Environment]::SetEnvironmentVariable("GROQ_API_KEY", $cleanKey, "Process")
[System.Environment]::SetEnvironmentVariable("GROQ_API_KEY", $cleanKey, "User")

Write-Host ""
Write-Host "✅ 已安全寫入 d:\2026ant線上教學網站\.dev.vars" -ForegroundColor Green
Write-Host "✅ 已設定使用者環境變數 GROQ_API_KEY" -ForegroundColor Green
Write-Host "🔒 該檔案已列入 .gitignore，保證不會外洩或提交至 Git" -ForegroundColor Green
Write-Host ""
Write-Host "正在驗證 Groq API 連線狀態..." -ForegroundColor Gray

try {
    $headers = @{
        "Authorization" = "Bearer $cleanKey"
        "Content-Type" = "application/json"
    }
    $response = Invoke-RestMethod -Uri "https://api.groq.com/openai/v1/models" -Headers $headers -Method Get -TimeoutSec 10
    Write-Host "🎉 Groq API 連線驗證成功！可使用模型數: $($response.data.Count)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 連線至 Groq API 失敗，請確認網路連線或 Key 是否正確：$($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "設定完成！您可以關閉此視窗，回到網頁體驗 AI 蘇格拉底家教。" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan