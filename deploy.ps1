# deploy.ps1 - One-Command Deployment Script

Write-Host "🚀 Deploying Portfolio-vite to GitHub Pages..." -ForegroundColor Cyan

# Navigate to Portfolio-vite and build
Set-Location Portfolio-vite
Write-Host "📦 Building project..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

# Go back to root
Set-Location ..

# Copy dist contents to root
Write-Host "📋 Copying build to root..." -ForegroundColor Yellow
Copy-Item -Recurse -Force Portfolio-vite\dist\* . -Exclude node_modules,*.git*

# Add all changes
Write-Host "➕ Staging changes..." -ForegroundColor Yellow
git add -A

# Check if there are changes
$status = git status --short
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "✅ No changes detected - already up to date!" -ForegroundColor Green
    exit 0
}

# Commit and push
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m "deploy: Update dashboard ($timestamp)"

Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your site will update in 1-2 minutes at:" -ForegroundColor Cyan
Write-Host "   https://dylanelo.github.io/Portfolio/dashboard.html" -ForegroundColor White
Write-Host ""
Write-Host "💡 Remember to hard refresh (Ctrl+Shift+R) to see changes!" -ForegroundColor Yellow
