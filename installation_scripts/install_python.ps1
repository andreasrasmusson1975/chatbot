# install_python.ps1

$Url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
$InstallerPath = Join-Path $PSScriptRoot "python-3.10.0-amd64.exe"

cls
Write-Host "🔽 Downloading Python 3.10.0..."
Invoke-WebRequest -Uri $Url -OutFile $InstallerPath -ErrorAction Stop

Write-Host "📦 Launching Python installer (interactive)..."
Start-Process -FilePath $InstallerPath -Wait

Write-Host "🧹 Cleaning up installer..."
Remove-Item $InstallerPath -Force
