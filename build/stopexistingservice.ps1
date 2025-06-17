param (
    [string]$ServiceName
)
# Check if the service exists
$service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue

if ($service) {
Write-Host "Service '$ServiceName' exists with status: $($service.Status)"

# Stop the service if it's running or pending
if ($service.Status -in @('Running', 'StartPending', 'StopPending')) {
    try {
        Write-Host "Stopping service..."
        Stop-Service -Name $ServiceName -Force -ErrorAction Stop
        Write-Host "Service stopped successfully."
    } catch {
        Write-Warning "Failed to stop the service: $_"
    }
}

} else {
    Write-Host "Service '$ServiceName' does not exist. Creating the service"
}

