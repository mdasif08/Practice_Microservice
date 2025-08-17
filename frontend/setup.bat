@echo off
echo 🚀 Setting up Commit Trail Frontend...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

echo ✅ Node.js version: 
node --version

echo 📦 Installing dependencies...
npm install

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully!
    echo.
    echo 🎉 Setup complete! You can now start the development server:
    echo    npm run dev
    echo.
    echo 📖 For more information, see README.md
) else (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

pause
