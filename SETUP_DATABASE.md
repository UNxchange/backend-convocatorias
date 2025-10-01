# 🚀 Guía de Configuración de Base de Datos - Backend Convocatorias

Esta guía te permitirá replicar completamente la base de datos en cualquier equipo desde cero.

## 📋 Prerrequisitos

1. **MongoDB instalado** (versión 4.4 o superior)
2. **Python 3.8+**
3. **Git** para clonar el repositorio

## 🔧 Instalación Paso a Paso

### 1. Instalar MongoDB

#### En Windows:
```powershell
# Opción 1: Con winget (recomendado)
winget install MongoDB.Server

# Opción 2: Descarga manual desde https://www.mongodb.com/download-center/community
```

#### En macOS:
```bash
# Con Homebrew
brew tap mongodb/brew
brew install mongodb-community
```

#### En Ubuntu/Debian:
```bash
# Importar clave GPG
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Añadir repositorio
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Instalar
sudo apt-get update
sudo apt-get install -y mongodb-org
```

### 2. Iniciar MongoDB

#### Windows:
```powershell
# Iniciar servicio
net start MongoDB

# O manualmente (si no está como servicio)
mongod --dbpath "C:\data\db"
```

#### macOS/Linux:
```bash
# Iniciar servicio
sudo brew services start mongodb/brew/mongodb-community
# O en Linux:
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 3. Clonar y Configurar el Proyecto

```bash
# Clonar repositorio
git clone https://github.com/UNxchange/backend-convocatorias.git
cd backend-convocatorias

# Cambiar a rama estable
git checkout estable

# Crear entorno virtual
python -m venv convocatorias

# Activar entorno virtual
# Windows:
.\convocatorias\Scripts\Activate.ps1
# macOS/Linux:
source convocatorias/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu configuración
```

**Contenido de .env:**
```properties
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=unxchange_local
SECRET_KEY=your-super-secret-key-change-this-in-production-unxchange-2025
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Inicializar la Base de Datos

#### Opción A: Script Automático (Recomendado)
```bash
python setup_database.py
```

#### Opción B: Paso a paso
```bash
# 1. Verificar conexión
python test_connection.py

# 2. Cargar datos limpios
python load_data.py

# 3. Verificar carga
python test_endpoints.py
```

## 📊 Archivos de Datos Incluidos

- **`DataConvenios_limpio.json`** - 613 convocatorias listas para insertar
- **`DataConvenios.json`** - Datos originales sin procesar
- **`load_data.py`** - Script de carga de datos
- **`test_connection.py`** - Verificador de conexión

## 🔍 Verificación de Instalación

### Verificar MongoDB
```bash
# Conectar a MongoDB
mongosh

# Verificar base de datos
use unxchange_local
db.convocatorias.countDocuments()
# Debe retornar: 613
```

### Verificar Backend
```bash
# Iniciar servidor
python start_server.py

# Verificar en navegador:
# http://localhost:8008/docs
```

### Probar Endpoints
```bash
# Ejecutar suite de pruebas
python test_endpoints.py
```

## 🚨 Solución de Problemas Comunes

### Error: "No module named 'motor'"
```bash
pip install motor
```

### Error: "Connection refused to MongoDB"
```bash
# Verificar que MongoDB esté corriendo
# Windows:
net start MongoDB

# macOS/Linux:
sudo systemctl status mongod
```

### Error: "Database not found"
```bash
# Ejecutar inicialización
python load_data.py
```

### Puerto 8008 ocupado
Editar `start_server.py` y cambiar el puerto:
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8009)  # Cambiar puerto
```

## 📁 Estructura de Base de Datos Resultante

```
MongoDB (localhost:27017)
└── unxchange_local
    └── convocatorias (613 documentos)
        ├── Índices:
        │   ├── _id_ (único)
        │   └── search_index (texto: institution, country, properties)
        └── Campos:
            ├── _id: ObjectId
            ├── subscriptionYear: String
            ├── country: String
            ├── institution: String
            ├── agreementType: String
            ├── validity: String
            ├── state: String
            ├── subscriptionLevel: String
            ├── languages: Array[String]
            ├── dreLink: String (opcional)
            ├── agreementLink: String (opcional)
            ├── Props: String (opcional)
            └── internationalLink: String (opcional)
```

## 🎯 Resultado Esperado

Al finalizar tendrás:
- ✅ MongoDB corriendo en puerto 27017
- ✅ Base de datos `unxchange_local` creada
- ✅ Colección `convocatorias` con 613 documentos
- ✅ Índices de búsqueda configurados
- ✅ Backend corriendo en puerto 8008
- ✅ Todos los endpoints funcionando

---

## 📞 Soporte

Si encuentras problemas, revisa:
1. Los logs de MongoDB
2. El archivo `.env` está configurado correctamente
3. Todas las dependencias están instaladas
4. MongoDB está corriendo en el puerto correcto

**¡Listo para usar!** 🚀