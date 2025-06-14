# Backend Convocatorias

Servicio backend para la gestión de convocatorias, desarrollado con **FastAPI** y **MongoDB**.

## Características

- API RESTful para crear, listar, actualizar y eliminar convocatorias.
- Autenticación JWT.
- Integración con MongoDB usando `motor`.
- Validación de datos con Pydantic.

## Requisitos

- Python 3.8+
- MongoDB (Atlas o local)

## Instalación

1. Clona el repositorio:

   ```sh
   git clone <URL_DEL_REPOSITORIO>
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
   SECRET_KEY="clave_secreta"
   ALGORITHM="HS256"
   ```

## Ejecución

```sh
uvicorn main:app --reload
```

La API estará disponible en [http://localhost:8000](http://localhost:8000).

## Endpoints principales

- `GET /convocatorias` — Lista todas las convocatorias.
- `POST /convocatorias` — Crea una nueva convocatoria.
- `GET /convocatorias/{id}` — Obtiene una convocatoria por ID.
- `PUT /convocatorias/{id}` — Actualiza una convocatoria.
- `DELETE /convocatorias/{id}` — Elimina una convocatoria.

## Autenticación

Algunos endpoints requieren autenticación JWT. Debes incluir el token en el header:

```
Authorization: Bearer <token>
```
