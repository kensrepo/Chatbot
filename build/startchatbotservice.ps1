param (
    [Parameter(Mandatory = $true)]
    [string]$Port,
  
    [Parameter(Mandatory = $true)]
    [string]$serviceName
)
Write-Host "startchatbotservice.ps1 invoked"

Start-Service -Name $serviceName
# Get the parent directory of the script's location
$ProjectPath = Split-Path $PSScriptRoot -Parent

# Change to that directory
Set-Location $ProjectPath

# Set environment variables
$env:VIRTUAL_ENV = Join-Path $ProjectPath "venv"
$env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"

# Define log paths
$logDir = Join-Path $ProjectPath "logs"
if (!(Test-Path $logDir)) {
    New-Item -Path $logDir -ItemType Directory | Out-Null
}

$logFile = Join-Path $logDir "service-stdout.log"
$errFile = Join-Path $logDir "service-stderr.log"

# Check if Python is installed
if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Installing..."
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pythonInstallerPath = "$env:TEMP\python_installer.exe"
    
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Write-Host "Python installed successfully!"
}

# Verify Python installation
python --version

# Create virtual environment if it doesn't exist
if (!(Test-Path "$ProjectPath\venv")) {
    Write-Host "Creating virtual environment invoked"
    python -m venv venv
}

# Wait for Activate.ps1 to exist
$activatePath = "$ProjectPath\venv\Scripts\Activate.ps1"
while (-not (Test-Path $activatePath)) {
    Write-Host "⏳ Waiting for Activate.ps1 to be created..."
    Start-Sleep -Seconds 15
}

# Activate virtual environment
& $activatePath

# Upgrade pip and install dependencies
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

[System.Environment]::SetEnvironmentVariable("STREAMLIT_EMAIL", "test@philips.com", "Machine")
 
 Write-Host "Env Variable Setup, Starting Application..."
Start-Sleep -Seconds 2

 Write-Host "Your app must be live on Port:$Port/ in few seconds..."

# Start streamlit  and redirect stdout and stderr



Start-Process python -ArgumentList "-m", "streamlit", "run", "app/streamlit_app.py", "--server.headless", "true", "--server.port", $Port.ToString() -RedirectStandardOutput $logFile -RedirectStandardError $errFile -NoNewWindow -Wait




