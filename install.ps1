Write-Host "🚀 Установка зависимостей для WhatsApp Dialog Emulator..." -ForegroundColor Green

# Проверяем, установлен ли Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Python не найден. Установите Python 3.10+ с python.org" -ForegroundColor Red
    exit 1
}

# Обновляем pip
python -m pip install --upgrade pip

# Устанавливаем зависимости
Write-Host "📦 Установка Python-пакетов..." -ForegroundColor Yellow
python -m pip install playwright pyfiglet

# Устанавливаем Chromium
Write-Host "🌐 Установка Chromium для Playwright..." -ForegroundColor Yellow
python -m playwright install chromium

Write-Host "✅ Готово! Теперь запускай: python main.py" -ForegroundColor Green