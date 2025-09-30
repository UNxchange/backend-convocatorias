#!/bin/bash

# 🚀 Script de Instalación Completa
# Backend de Convocatorias UnxChange
# Instala MongoDB, configura el entorno y base de datos

set -e  # Salir si hay errores

echo "🚀 Instalación Completa - Backend Convocatorias"
echo "================================================"

# Detectar sistema operativo
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    DISTRO=$(lsb_release -si 2>/dev/null || echo "unknown")
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    OS="windows"
fi

echo "🔍 Sistema detectado: $OS"

# Función para instalar MongoDB según el OS
install_mongodb() {
    echo "📦 Instalando MongoDB..."
    
    case $OS in
        "linux")
            if command -v apt-get &> /dev/null; then
                # Ubuntu/Debian
                wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
                echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
                sudo apt-get update
                sudo apt-get install -y mongodb-org
                sudo systemctl enable mongod
                sudo systemctl start mongod
            elif command -v yum &> /dev/null; then
                # CentOS/RHEL/Fedora
                sudo tee /etc/yum.repos.d/mongodb-org-6.0.repo << 'EOF'
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/6.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
EOF
                sudo yum install -y mongodb-org
                sudo systemctl enable mongod
                sudo systemctl start mongod
            fi
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew tap mongodb/brew
                brew install mongodb-community
                brew services start mongodb/brew/mongodb-community
            else
                echo "❌ Homebrew no encontrado. Instala Homebrew primero:"
                echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                exit 1
            fi
            ;;
        "windows")
            echo "⚠️  Para Windows, ejecuta setup_complete.bat en su lugar"
            echo "💡 O instala MongoDB manualmente desde: https://www.mongodb.com/download-center/community"
            exit 1
            ;;
        *)
            echo "❌ Sistema operativo no soportado: $OS"
            exit 1
            ;;
    esac
}

# Verificar si MongoDB ya está instalado
check_mongodb() {
    if command -v mongod &> /dev/null; then
        echo "✅ MongoDB ya está instalado"
        
        # Verificar si está corriendo
        if pgrep mongod > /dev/null; then
            echo "✅ MongoDB está corriendo"
        else
            echo "⚠️  MongoDB no está corriendo, iniciando..."
            case $OS in
                "linux")
                    sudo systemctl start mongod
                    ;;
                "macos")
                    brew services start mongodb/brew/mongodb-community
                    ;;
            esac
        fi
        return 0
    else
        echo "📦 MongoDB no encontrado, instalando..."
        install_mongodb
        return $?
    fi
}

# Configurar Python y entorno virtual
setup_python_env() {
    echo "🐍 Configurando entorno Python..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 no encontrado"
        echo "💡 Instala Python 3.8+ desde: https://www.python.org/downloads/"
        exit 1
    fi
    
    # Crear entorno virtual
    if [ ! -d "convocatorias" ]; then
        python3 -m venv convocatorias
        echo "✅ Entorno virtual creado"
    else
        echo "✅ Entorno virtual ya existe"
    fi
    
    # Activar entorno virtual
    source convocatorias/bin/activate
    
    # Instalar dependencias
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas"
}

# Configurar archivos de configuración
setup_config() {
    echo "⚙️  Configurando archivos..."
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo "✅ Archivo .env creado desde .env.example"
        echo "💡 Revisa y ajusta la configuración en .env si es necesario"
    else
        echo "✅ Archivo .env ya existe"
    fi
}

# Función principal
main() {
    echo "Iniciando instalación completa..."
    
    # Verificar que estamos en el directorio correcto
    if [ ! -f "requirements.txt" ]; then
        echo "❌ requirements.txt no encontrado"
        echo "💡 Asegúrate de estar en el directorio del proyecto backend-convocatorias"
        exit 1
    fi
    
    # Paso 1: Instalar/verificar MongoDB
    check_mongodb
    
    # Paso 2: Configurar entorno Python
    setup_python_env
    
    # Paso 3: Configurar archivos
    setup_config
    
    # Paso 4: Configurar base de datos
    echo "🗄️  Configurando base de datos..."
    python setup_database.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!"
        echo "========================================"
        echo ""
        echo "✅ MongoDB instalado y corriendo"
        echo "✅ Entorno Python configurado"
        echo "✅ Base de datos poblada con 613 convocatorias"
        echo "✅ Backend listo para usar"
        echo ""
        echo "🚀 Para iniciar el backend:"
        echo "   source convocatorias/bin/activate"
        echo "   python start_server.py"
        echo ""
        echo "🌐 URLs disponibles:"
        echo "   API: http://localhost:8008"
        echo "   Docs: http://localhost:8008/docs"
        echo ""
    else
        echo ""
        echo "❌ Error durante la configuración de la base de datos"
        echo "💡 Revisa los mensajes de error arriba"
        exit 1
    fi
}

# Ejecutar instalación
main "$@"