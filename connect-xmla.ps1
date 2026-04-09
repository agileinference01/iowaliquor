#!/usr/bin/env pwsh
# Direct XMLA Connection to Power BI Desktop localhost:63159

param(
    [string]$Server = "localhost:63159",
    [string]$Port = "63159"
)

# XMLA Discover request to list databases
function Get-PowerBIDatabases {
    param(
        [string]$Server = "localhost:63159"
    )
    
    $url = "http://$Server/"
    
    # XMLA Discover SOAP request
    $xmlaRequest = @"
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
  <SOAP-ENV:Body>
    <Discover xmlns="urn:schemas-microsoft-com:xml-analysis">
      <RequestType>DISCOVER_DATASOURCES</RequestType>
      <Restrictions/>
      <Properties/>
    </Discover>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"@

    try {
        $response = Invoke-WebRequest -Uri $url `
            -Method Post `
            -Body $xmlaRequest `
            -ContentType "application/soap+xml" `
            -ErrorAction Stop
        
        Write-Host "✓ Connected to Power BI at $Server" -ForegroundColor Green
        Write-Host ""
        Write-Host "Response:" -ForegroundColor Cyan
        Write-Host $response.Content
    }
    catch {
        Write-Host "✗ Connection failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Main
Write-Host "=== Connecting to Power BI XMLA Endpoint ===" -ForegroundColor Cyan
Write-Host "Server: $Server" -ForegroundColor White
Write-Host "Port: $Port" -ForegroundColor White
Write-Host ""

Get-PowerBIDatabases -Server $Server
