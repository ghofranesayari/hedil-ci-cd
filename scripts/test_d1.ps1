param(
    [switch]$Coverage,
    [int]$MinCoverage = 20
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (!(Test-Path $python)) {
    Write-Error '.venv introuvable. Lancez d''abord: scripts\install_env.bat'
}

$ciTempRoot = Join-Path ([System.IO.Path]::GetTempPath()) 'aebm-ci'
$pytestBaseTemp = Join-Path $ciTempRoot 'pytest-tmp'
$pytestCacheDir = Join-Path $ciTempRoot 'pytest-cache'

New-Item -ItemType Directory -Force -Path $ciTempRoot | Out-Null
New-Item -ItemType Directory -Force -Path $pytestBaseTemp | Out-Null
New-Item -ItemType Directory -Force -Path $pytestCacheDir | Out-Null

$env:COVERAGE_FILE = Join-Path $ciTempRoot '.coverage'

$pytestArgs = @(
    '-m', 'pytest',
    '-c', 'pytest.ini',
    'tests_d1',
    '--basetemp', $pytestBaseTemp,
    '-o', "cache_dir=$pytestCacheDir"
)

if ($Coverage) {
    Write-Host "[INFO] Tests D1 avec couverture (seuil $MinCoverage%)."
    $pytestArgs += @(
        '--cov=src',
        '--cov=ui',
        '--cov-report=term-missing',
        '--cov-report=xml:coverage.xml',
        "--cov-fail-under=$MinCoverage",
        '-q'
    )
} else {
    Write-Host '[INFO] Tests D1 sans couverture.'
    $pytestArgs += '-q'
}

& $python @pytestArgs
exit $LASTEXITCODE
