#!/usr/bin/env pwsh
# Power BI Desktop Local Connection Script
# Connects to Power BI Desktop's local XMLA endpoint at localhost:63159

param(
    [string]$Server = "localhost:63159",
    [string]$Database = "",
    [switch]$ListDatabases,
    [switch]$DeployModel
)

# Check if Power BI Desktop is running
function Test-PowerBIDesktop {
    $process = Get-Process -Name "msmdsrv" -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "Power BI Desktop is running." -ForegroundColor Green
        return $true
    } else {
        Write-Host "Power BI Desktop is not running. Please start Power BI Desktop and open a .pbix file." -ForegroundColor Yellow
        return $false
    }
}

# Get list of databases from local Power BI instance
function Get-LocalPowerBIDatabases {
    param([string]$Server = "localhost:63159")
    
    try {
        $databases = Invoke-ASCmd -Server $Server -Query '{"version":"1.0","admin":{"listDatabases":{}}}'
        Write-Host "Connected to Power BI Desktop successfully!" -ForegroundColor Green
        $databases | ConvertFrom-Json | ForEach-Object {
            $_.result.databases | ForEach-Object {
                Write-Host "  Database: $($_.name) (ID: $($_.id))" -ForegroundColor Cyan
            }
        }
    }
    catch {
        Write-Host "Failed to connect: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Deploy the semantic model to Power BI Desktop
function Deploy-ToPowerBIDesktop {
    param(
        [string]$Server = "localhost:63159",
        [string]$DatabaseName = "main"
    )
    
    Write-Host "Deploying semantic model to Power BI Desktop..." -ForegroundColor Yellow
    
    # Using Tabular Editor for deployment (if available)
    $tabularEditorPath = "${env:ProgramFiles}\Tabular Editor\3\TabularEditor.exe"
    if (Test-Path $tabularEditorPath) {
        $modelPath = Join-Path $PSScriptRoot "main.SemanticModel"
        Write-Host "Found Tabular Editor at: $tabularEditorPath" -ForegroundColor Green
        Write-Host "Model path: $modelPath" -ForegroundColor Green
        
        # Deploy using Tabular Editor CLI
        & $tabularEditorPath $modelPath -A "$Server" -D "$DatabaseName" -C
        Write-Host "Deployment completed!" -ForegroundColor Green
    }
    else {
        Write-Host "Tabular Editor not found. Alternative deployment methods:" -ForegroundColor Yellow
        Write-Host "1. Open the .pbip file in Power BI Desktop directly" -ForegroundColor White
        Write-Host "2. Use DAX Studio to connect and run queries" -ForegroundColor White
        Write-Host "3. Install Tabular Editor 3 for advanced deployment" -ForegroundColor White
    }
}

# Main execution
Write-Host "=== Power BI Desktop Local Connection Tool ===" -ForegroundColor Cyan
Write-Host "Server: $Server" -ForegroundColor White

if ($ListDatabases) {
    if (Test-PowerBIDesktop) {
        Get-LocalPowerBIDatabases -Server $Server
    }
}
elseif ($DeployModel) {
    if (Test-PowerBIDesktop) {
        Deploy-ToPowerBIDesktop -Server $Server -DatabaseName $Database
    }
}
else {
    Write-Host ""
    Write-Host "Usage options:" -ForegroundColor Yellow
    Write-Host "  .\connect-pbi-local.ps1 -ListDatabases    # List all databases in Power BI Desktop" -ForegroundColor White
    Write-Host "  .\connect-pbi-local.ps1 -DeployModel -Database 'main'  # Deploy model to Power BI Desktop" -ForegroundColor White
    Write-Host ""
    Write-Host "Alternative connection methods:" -ForegroundColor Yellow
    Write-Host "  1. DAX Studio: Connect to localhost:63159" -ForegroundColor White
    Write-Host "  2. SSMS (SQL Server Management Studio): Connect to localhost:63159" -ForegroundColor White
    Write-Host "  3. Tabular Editor: Open .tmdl files and connect to localhost:63159" -ForegroundColor White
    Write-Host "  4. Power BI Desktop: Open main.pbip file directly" -ForegroundColor White
}