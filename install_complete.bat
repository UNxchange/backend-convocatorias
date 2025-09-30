@echo off
REM 🚀 Script de Instalación Completa para Windows
REM Backend de Convocatorias UnxChange

echo.
echo ========================================
echo   Instalacion Completa - Windows
echo   Backend Convocatorias UnxChange  
echo ========================================
echo.

REM Verificar si estamos en el directorio correcto
if not exist "requirements.txt" (
    echo ERROR: requirements.txt no encontrado
    echo Asegurate de estar en el directorio del proyecto backend-convocatorias
    pause
    exit /b 1
)

REM Paso 1: Verificar/Instalar MongoDB
echo Paso 1: Verificando MongoDB...
where mongod >nul 2>&1
if %errorlevel% neq 0 (
    echo MongoDB no encontrado. Instalando...
    
    REM Verificar si winget está disponible
    where winget >nul 2>&1
    if %errorlevel% equ 0 (
        echo Instalando MongoDB con winget...
        winget install MongoDB.Server
        if %errorlevel% neq 0 (
            echo ERROR: No se pudo instalar MongoDB con winget
            echo.
            echo Instala MongoDB manualmente desde:
            echo https://www.mongodb.com/download-center/community
            echo.
            echo Despues ejecuta este script nuevamente
            pause
            exit /b 1
        )
    ) else (
        echo winget no disponible.
        echo.
        echo Por favor instala MongoDB manualmente desde:
        echo https://www.mongodb.com/download-center/community
        echo.
        echo Despues ejecuta este script nuevamente
        pause
        exit /b 1
    )
) else (
    echo MongoDB encontrado
)

REM Verificar si MongoDB está corriendo
echo Verificando servicio MongoDB...
sc query MongoDB | findstr "RUNNING" >nul
if %errorlevel% neq 0 (
    echo Iniciando servicio MongoDB...
    net start MongoDB >nul 2>&1
    if %errorlevel% neq 0 (
        echo Intentando iniciar MongoDB manualmente...
        start /B mongod --dbpath "C:\data\db" >nul 2>&1
        timeout /t 3 >nul
    )
)

REM Paso 2: Configurar entorno Python
echo.
echo Paso 2: Configurando entorno Python...

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    echo Instala Python 3.8+ desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "convocatorias" (
    echo Creando entorno virtual...
    python -m venv convocatorias
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
) else (
    echo Entorno virtual ya existe
)

REM Activar entorno virtual
echo Activando entorno virtual...
call .\convocatorias\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Instalar dependencias
echo Instalando dependencias Python...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

REM Paso 3: Configurar archivos
echo.
echo Paso 3: Configurando archivos...
if not exist ".env" (
    copy ".env.example" ".env"
    echo Archivo .env creado desde .env.example
    echo Revisa y ajusta la configuracion en .env si es necesario
) else (
    echo Archivo .env ya existe
)

REM Paso 4: Configurar base de datos
echo.
echo Paso 4: Configurando base de datos...
python setup_database.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   INSTALACION COMPLETADA EXITOSAMENTE
    echo ========================================
    echo.
    echo ✓ MongoDB instalado y corriendo
    echo ✓ Entorno Python configurado  
    echo ✓ Base de datos poblada con 613 convocatorias
    echo ✓ Backend listo para usar
    echo.
    echo Para iniciar el backend:
    echo   start_server.bat
    echo.
    echo O manualmente:
    echo   .\convocatorias\Scripts\activate.bat
    echo   python start_server.py
    echo.
    echo URLs disponibles:
    echo   API: http://localhost:8008
    echo   Docs: http://localhost:8008/docs
    echo.
) else (
    echo.
    echo ERROR: Fallo la configuracion de la base de datos
    echo Revisa los mensajes de error arriba
)

pause