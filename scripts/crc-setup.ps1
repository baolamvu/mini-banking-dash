# OpenShift Local setup helper (Windows PowerShell)
# Run from project root after installing OpenShift Local 2.61

Write-Host "=== OpenShift Local Setup Helper ===" -ForegroundColor Cyan

# 1. Verify crc installed
try {
    crc version
} catch {
    Write-Host "ERROR: crc not found. Install OpenShift Local first." -ForegroundColor Red
    exit 1
}

# 2. Configure resources (adjust if needed)
Write-Host "`nConfiguring cluster resources..." -ForegroundColor Yellow
crc config set cpus 6
crc config set memory 14336
crc config set disk_size 50

# 3. Setup with pull secret
$pullSecret = "$env:USERPROFILE\pull-secret.txt"
if (-not (Test-Path $pullSecret)) {
    Write-Host "WARNING: Pull secret not found at $pullSecret" -ForegroundColor Yellow
    Write-Host "Download from: https://console.redhat.com/openshift/create/local"
    Write-Host "Then run: crc setup --pull-secret $pullSecret"
} else {
    Write-Host "Running crc setup..." -ForegroundColor Yellow
    crc setup --pull-secret $pullSecret
}

# 4. Start cluster
Write-Host "`nStarting cluster (may take 5-15 minutes)..." -ForegroundColor Yellow
Write-Host "If daemon error occurs, run 'crc daemon' in another terminal first." -ForegroundColor Gray
crc start

# 5. Show credentials
Write-Host "`n=== Cluster Ready ===" -ForegroundColor Green
crc console --credentials

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  oc login -u kubeadmin -p <password> https://api.crc.testing:6443 --insecure-skip-tls-verify"
Write-Host "  oc apply -f openshift/00-namespace.yaml"
Write-Host "  oc apply -f openshift/01-postgresql.yaml"
Write-Host "  # wait for postgres ready, then deploy app (see instruction.txt)"
