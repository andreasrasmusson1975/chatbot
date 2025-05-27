# install_vcredist.ps1

$Url = "https://download.visualstudio.microsoft.com/download/pr/453680ea-b88a-411f-80fd-5db37fdc9dbb/5D9999036F2B3A930F83B7FE3E2186B12E79AE7C007D538F52E3582E986A37C3/VC_redist.x64.exe"
$InstallerPath = Join-Path $PSScriptRoot "VC_redist.x64.exe"

cls
Write-Host "🔽 Downloading Visual C++ Redistributable..."
Invoke-WebRequest -Uri $Url -OutFile $InstallerPath -ErrorAction Stop

Write-Host "🛠 Installing..."
$process = Start-Process -FilePath $InstallerPath -ArgumentList "/install", "/norestart" -PassThru -Wait
$exitCode = $process.ExitCode

if ($exitCode -eq 0) {
    Write-Host "✅ Visual C++ Redistributable installed successfully!"
} else {
    Write-Host "❌ Installation failed with exit code $exitCode"
    exit 1
}

Write-Host "🧹 Cleaning up installer..."
Remove-Item $InstallerPath -Force
