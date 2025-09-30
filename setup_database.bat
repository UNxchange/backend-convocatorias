@echo off
echo.
echo ========================================
echo   Setup Rapido de Base de Datos
echo   Backend Convocatorias UnxChange  
echo ========================================
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call .\convocatorias\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: No se pudo activar el entorno virtual
    echo Asegurate de que existe: .\convocatorias\Scripts\activate.bat
    pause
    exit /b 1
)

REM Instalar dependencias si no están
echo Instalando dependencias...
pip install -r requirements.txt

REM Ejecutar setup de base de datos
echo.
echo Configurando base de datos...
python setup_database.py

REM Verificar si fue exitoso
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   CONFIGURACION COMPLETADA EXITOSAMENTE
    echo ========================================
    echo.
    echo Para iniciar el backend ejecuta:
    echo   start_server.bat
    echo.
    echo O manualmente:
    echo   python start_server.py
    echo.
) else (
    echo.
    echo ERROR: La configuracion fallo
    echo Revisa los mensajes de error arriba
)

pause