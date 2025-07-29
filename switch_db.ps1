param ([string]$envTarget)

if ($envTarget -eq "prod") {
    Copy-Item ".env.production" ".env" -Force
    Write-Host "✅ Switched to Cloud PostgreSQL"
}
elseif ($envTarget -eq "local") {
    Copy-Item ".env.local" ".env" -Force
    Write-Host "✅ Switched to Local SQLite"
}
else {
    Write-Host "❌ Usage: .\switch_db.ps1 local | prod"
}