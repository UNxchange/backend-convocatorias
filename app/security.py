import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # <-- Cambios aquí
from jose import JWTError, jwt
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# --- CONFIGURACIÓN (sin cambios) ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# --- ESQUEMA DE SEGURIDAD ---
# Usamos HTTPBearer en lugar de OAuth2PasswordBearer.
# Esto le dice a Swagger que solo pida un token Bearer.
security_scheme = HTTPBearer()

# --- MODELOS DE DATOS (sin cambios) ---
class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

# --- FUNCIONES DE SEGURIDAD ---

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> TokenData:
    """
    Decodifica el token JWT y devuelve los datos del usuario (sub y rol).
    Esta dependencia ahora usa HTTPBearer.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        token_data = TokenData(sub=email, role=role)
    except JWTError:
        raise credentials_exception
    
    return token_data

# La dependencia para el rol de admin no necesita cambios, ya que depende de get_current_user.
async def require_admin_role(current_user: TokenData = Depends(get_current_user)):
    """
    Verifica que el usuario autenticado tenga el rol de "administrador".
    """
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para realizar esta acción. Se requiere rol de administrador.",
        )
    return current_user