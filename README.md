# Backend Convocatorias - UNxChange

Servicio backend para la gestión de convocatorias de movilidad académica, desarrollado con **FastAPI** y **MongoDB**.

## Características

- **API RESTful** para gestión completa de convocatorias (CRUD)
- **Autenticación JWT** con roles (administrador, profesional, usuario)
- **Sistema de interés** - Los usuarios pueden expresar interés en convocatorias
- **Notificaciones por email** para confirmación de interés
- **Búsqueda avanzada** con filtros por país, idioma, estado, etc.
- **Integración con MongoDB** usando `motor` (driver asíncrono)
- **Validación de datos** con Pydantic v2
- **Documentación automática** con Swagger/OpenAPI

## Requisitos

- Python 3.8+
- MongoDB (Atlas o local)
- Servicio de notificaciones (para emails)

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/UNxchange/backend-convocatorias.git
   cd backend-convocatorias
   ```

2. Crea un entorno virtual e instala dependencias:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno en un archivo `.env`:
   ```env
   MONGO_URI="mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
   DATABASE_NAME="unxchange"
   SECRET_KEY="tu_clave_secreta_jwt"
   ALGORITHM="HS256"
   NOTIFICATIONS_SERVICE_URL="http://localhost:8002"
   ```

4. (Opcional) Cargar datos de prueba:
   ```sh
   # Si tienes un archivo DataConvenios.json, primero preprocésalo:
   python preprocess_json.py
   
   # Luego carga los datos en MongoDB:
   python load_data.py
   ```

## Ejecución

Para desarrollo:
```sh
uvicorn app.main:app --reload
```

Para producción:
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en [http://localhost:8000](http://localhost:8000).

## Documentación de la API

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints principales

### Convocatorias

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `GET` | `/convocatorias` | Lista convocatorias con filtros | Usuario autenticado |
| `POST` | `/convocatorias` | Crea nueva convocatoria | Admin/Profesional |
| `GET` | `/convocatorias/{id}` | Obtiene convocatoria por ID | Usuario autenticado |
| `PATCH` | `/convocatorias/{id}` | Actualiza convocatoria | Solo Admin |
| `DELETE` | `/convocatorias/{id}` | Elimina convocatoria | Solo Admin |
| `POST` | `/convocatorias/{id}/interest` | Expresar interés | Usuario autenticado |
| `DELETE` | `/convocatorias/{id}/interest` | Remover interés | Usuario autenticado |

### Usuarios

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| `GET` | `/usuarios` | Lista usuarios | Por implementar |
| `GET` | `/usuarios/{id}` | Obtiene usuario por ID | Por implementar |

### Parámetros de búsqueda disponibles

- `q`: Búsqueda por texto libre (mínimo 3 caracteres)
- `country`: Filtrar por país
- `language`: Filtrar por idioma
- `state`: Filtrar por estado (Vigente/No Vigente)
- `agreement_type`: Filtrar por tipo de convenio
- `subscription_level`: Filtrar por nivel de suscripción
- `limit`: Número máximo de resultados (default: 20, max: 200)
- `skip`: Número de resultados a omitir (paginación)

## Autenticación y Autorización

El sistema utiliza **JWT Bearer tokens** con tres roles:

- **Usuario**: Puede ver convocatorias y expresar interés
- **Profesional**: Como usuario + puede crear convocatorias
- **Administrador**: Acceso completo (crear, editar, eliminar)

### Formato del token
```
Authorization: Bearer <jwt_token>
```

El token debe contener los claims:
- `sub`: Email del usuario
- `role`: Rol del usuario (usuario/profesional/administrador)

## Estructura del proyecto

```
backend-convocatorias/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── database.py          # Configuración de MongoDB
│   ├── models.py            # Modelos Pydantic
│   ├── security.py          # Autenticación JWT
│   └── routes/
│       ├── convocatorias.py # Endpoints de convocatorias
│       └── usuarios.py      # Endpoints de usuarios
├── notification_client.py   # Cliente para servicio de notificaciones
├── load_data.py            # Script para cargar datos
├── preprocess_json.py      # Script para limpiar datos JSON
├── requirements.txt        # Dependencias
└── README.md
```

## Modelos de datos

### Convocatoria
```json
{
  "id": "ObjectId",
  "subscriptionYear": "string",
  "country": "string",
  "institution": "string",
  "agreementType": "string",
  "validity": "string",
  "state": "string",
  "subscriptionLevel": "string",
  "languages": ["string"],
  "dreLink": "string (opcional)",
  "agreementLink": "string (opcional)",
  "properties": "string (opcional)",
  "internationalLink": "string (opcional)",
  "interestedUsers": ["string"]
}
```

## Pruebas

Para hacer pruebas de los endpoints:

1. **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
2. **Herramientas externas**: Postman, Insomnia, curl, etc.
3. **Pytest** (por implementar):
   ```sh
   pytest
   ```

## Integración con otros servicios

- **Servicio de notificaciones**: Para envío de emails de confirmación
- **Servicio de autenticación**: Para validación de tokens JWT

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).