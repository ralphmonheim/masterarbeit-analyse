Param([string]$file)
$python = $env:PYTHON -or "python"
& $python (Join-Path $PSScriptRoot 'check_commit_msg.py') $file
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
