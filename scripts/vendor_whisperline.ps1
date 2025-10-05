Param(
    [string]$SourcePath = 'C:\Users\Andre\OneDrive - Andre Collier\Shared\shared\whisperline_extracted-master\whisperline_extracted-master'
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$dst = Join-Path $repoRoot 'third_party\whisperline_extracted'

Write-Host "Vendoring whisperline_extracted from $SourcePath to $dst"

if (-Not (Test-Path $SourcePath)) {
    Write-Error "Source path not found: $SourcePath"
    exit 2
}

if (Test-Path $dst) {
    Write-Host "Removing existing destination $dst"
    Remove-Item -Recurse -Force $dst
}

Copy-Item -Path $SourcePath -Destination $dst -Recurse -Force
Write-Host "Vendored successfully."
