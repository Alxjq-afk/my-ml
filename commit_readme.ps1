param(
    [string]$Message = "docs: update README (CI badge and features)",
    [switch]$InitIfNeeded
)

# Comprueba si git está instalado
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git no está disponible en el PATH. Instala Git for Windows (https://git-scm.com/download/win) y vuelve a ejecutar este script."
    exit 1
}

# ¿Estamos dentro de un repo git?
$inside = & git rev-parse --is-inside-work-tree 2>$null
if ($LASTEXITCODE -ne 0 -or $inside -ne 'true') {
    if ($InitIfNeeded) {
        git init
        git branch -M main
        Write-Host "Repositorio inicializado (branch 'main')."
    } else {
        Write-Host "No parece un repositorio git. Si quieres inicializar uno y hacer el commit, ejecuta este script con -InitIfNeeded."
        exit 1
    }
}

# Añadir y commitear README.md
git add README.md
if ($LASTEXITCODE -ne 0) {
    Write-Error "Error al añadir README.md. Asegúrate de que el fichero existe y de tener permisos."
    exit 1
}

git commit -m "$Message"
if ($LASTEXITCODE -ne 0) {
    Write-Error "git commit falló. Puede que no hubiera cambios que commitear o haya un conflicto."
    exit 1
}

Write-Host "README.md commiteado con mensaje: $Message"

Write-Host "Si quieres añadir un remote y hacer push, puedes ejecutar (ajusta la URL a tu repo):"
Write-Host "  git remote add origin https://github.com/anune/my-ml.git"
Write-Host "  git push -u origin main"
