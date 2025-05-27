# install_tesseract.ps1

$Url = "https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe"
$InstallerPath = "$PSScriptRoot\tesseract-ocr-setup.exe"
cls
Write-Host "🔽 Downloading Tesseract..."
Invoke-WebRequest -Uri $Url -OutFile $InstallerPath -ErrorAction Stop

Write-Host "🛠 Installing ..."
$process = Start-Process -FilePath $InstallerPath -PassThru -Wait
$exitCode = $process.ExitCode

if ($exitCode -eq 0) {
    Write-Host "✅ Tesseract installed successfully!"
} else {
    Write-Host "❌ Installation failed with exit code $exitCode"
    exit 1
}

Write-Host "🧹 Cleaning up installer..."
Remove-Item $InstallerPath -Force
