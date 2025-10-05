Vendor instructions for whisperline_extracted

This directory is intended to hold a vendored copy of the upstream
`whisperline_extracted` repository so the project can import it even when
the upstream repo is not pip-installable.

To vendor the local clone into this folder, run (PowerShell):

  $src = 'C:\Users\Andre\OneDrive - Andre Collier\Shared\shared\whisperline_extracted-master\whisperline_extracted-master'
  $dst = Join-Path $PSScriptRoot '..' 'whisperline_extracted'
  Remove-Item -Recurse -Force $dst -ErrorAction SilentlyContinue
  Copy-Item -Recurse -Force $src $dst

Or use the helper script at ../../scripts/vendor_whisperline.ps1

After vendoring, the adapter will find the package under third_party and
import it automatically.
