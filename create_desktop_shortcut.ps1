# Script PowerShell para crear acceso directo a JARVIS en el escritorio
# Ejecutar como: powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ProjectPath = "C:\Users\anune\PYTHON"
$LauncherPath = "$ProjectPath\jarvis_launcher.bat"
$ShortcutPath = "$DesktopPath\JARVIS.lnk"

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
Write-Host ""
Write-Host "Ahora puedes hacer doble-click en 'JARVIS' en tu escritorio!"
Write-Host ""
