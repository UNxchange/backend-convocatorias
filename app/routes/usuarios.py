from fastapi import APIRouter

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/")
async def listar_usuarios():
    """
    Endpoint placeholder para usuarios.
    """
    return {"message": "Endpoint de usuarios - Por implementar"}

@router.get("/{usuario_id}")
async def obtener_usuario(usuario_id: str):
    """
    Obtener información de un usuario específico.
    """
    return {"usuario_id": usuario_id, "message": "Usuario encontrado"}
