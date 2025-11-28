# Script PowerShell para crear acceso directo a JARVIS en el escritorio
# Ejecutar como: powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ProjectPath = "C:\Users\anune\PYTHON"
$LauncherPath = "$ProjectPath\jarvis_launcher.bat"
$ShortcutPath = "$DesktopPath\JARVIS.lnk"

# Verificar que el launcher existe
if (-not (Test-Path $LauncherPath)) {
    Write-Host "Error: No se encontro $LauncherPath"
    Write-Host "Asegura que el proyecto esta en $ProjectPath"
    exit 1
}

# Crear objeto WScript.Shell
$WshShell = New-Object -ComObject WScript.Shell

# Crear acceso directo
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $LauncherPath
$Shortcut.WorkingDirectory = $ProjectPath
$Shortcut.Description = "JARVIS Advanced v2.0 - Voice Assistant"
$Shortcut.IconLocation = "C:\Windows\System32\cmd.exe,0"  # Icono de CMD
$Shortcut.Save()

Write-Host ""
Write-Host "========================================================"
Write-Host "          ACCESO DIRECTO CREADO EXITOSAMENTE"
Write-Host "========================================================"
Write-Host ""
Write-Host "Ubicacion: $ShortcutPath"
Write-Host "Destino: $LauncherPath"
Write-Host "Carpeta proyecto: $ProjectPath"
Write-Host ""
Write-Host "Ahora puedes hacer doble-click en 'JARVIS' en tu escritorio!"
Write-Host ""
