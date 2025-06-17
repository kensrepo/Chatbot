# Prompt user for the service name
$serviceName = Read-Host "Enter the name of the service"
$Port = Read-Host "Enter a free port number"
$currentScriptPath = $MyInvocation.MyCommand.Path
$appDirectory = (Get-Item $currentScriptPath).Directory.Parent.FullName
$stopScriptPath = Join-Path $appDirectory "build\stopexistingservice.ps1"
$startScriptPath = Join-Path $appDirectory "build\startchatbotservice.ps1"
$PwshPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$NssmPath = Join-Path $appDirectory "build\nssm.exe"

# Check if the service already exists
$existingService = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if ($existingService) {
    Write-Host "Service '$serviceName' already exists. Skipping creation."

    # Just run the start script
} else {
    Write-Host "Service '$serviceName' does not exist. Proceeding to create it."

    # Validate NSSM presence
    if (-not (Test-Path $NssmPath)) {
        Write-Error "nssm.exe not found at $NssmPath"
        Read-Host "Press Enter to exit"
        exit 1
    }

    # Construct PowerShell arguments
    $ScriptCommand = "-ExecutionPolicy Bypass -File `"$startScriptPath`" -Port $Port"

    # Install the service
    & $NssmPath install $ServiceName $PwshPath $ScriptCommand

    # Set directories
    & $NssmPath set $ServiceName AppDirectory $appDirectory

    # Set log file locations
    $logDir = Join-Path $appDirectory "logs"
    $stdoutLog = Join-Path $logDir "service-stdout.log"
    $stderrLog = Join-Path $logDir "service-stderr.log"

    & $NssmPath set $ServiceName AppStdout $stdoutLog
    & $NssmPath set $ServiceName AppStderr $stderrLog
    & $NssmPath set $ServiceName AppStdoutCreationDisposition 4
    & $NssmPath set $ServiceName AppStderrCreationDisposition 4

}
    # Start the service
& $PwshPath -ExecutionPolicy Bypass -File $startScriptPath -Port $Port -serviceName $serviceName

# Wait for user input before closing
Read-Host "Press Enter to exit"
