from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Convocatoria
from app.services.convocatorias_service import ConvocatoriaService

router = APIRouter(
    prefix="/convocatorias",
    tags=["Convocatorias"],
    responses={404: {"description": "No encontrado"}}
)

@router.post("/", summary="Crear una nueva convocatoria", response_description="Convocatoria creada")
async def creaar_convocatoria(convocatoria: Convocatoria):
    """
    Crea una nueva convocatoria de movilidad académica.
    """
    convocatoria_dict = convocatoria.dict(by_alias=True)
    success = await ConvocatoriaService.crear(convocatoria_dict)
    if not success:
        raise HTTPException(status_code=400, detail="Convocatoria ya existe")
    return {"mensaje": "Convocatoria creada exitosamente"}

@router.get("/", response_model=List[Convocatoria], summary="Listar convocatorias", response_description="Lista de convocatorias")
async def listar_convocatorias():
    """
    Lista todas las convocatorias existentes.
    """
    return await ConvocatoriaService.listar()

@router.get("/{convocatoria_id}", response_model=Convocatoria, summary="Obtener convocatoria por ID", response_description="Convocatoria encontrada")
async def obtener_convocatoria(convocatoria_id: str):
    """
    Obtiene el detalle de una convocatoria específica por su ID.
    """
    convocatoria = await ConvocatoriaService.obtener(convocatoria_id)
    if not convocatoria:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return convocatoria

@router.put("/{convocatoria_id}", summary="Actualizar convocatoria", response_description="Convocatoria actualizada")
async def actualizar_convocatoria(convocatoria_id: str, convocatoria_actualizada: Convocatoria):
    """
    Actualiza los datos de una convocatoria existente.
    """
    convocatoria_existente = await ConvocatoriaService.obtener(convocatoria_id)
    if not convocatoria_existente:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    convocatoria_actualizada.owner = convocatoria_existente.owner
    convocatoria_dict = convocatoria_actualizada.dict(by_alias=True)
    convocatoria_bd = Convocatoria(**convocatoria_dict)
    await ConvocatoriaService.actualizar(convocatoria_id, convocatoria_bd)
    return {"mensaje": "Convocatoria actualizada exitosamente"}

@router.delete("/{convocatoria_id}", summary="Eliminar convocatoria", response_description="Convocatoria eliminada")
async def eliminar_convocatoria(convocatoria_id: str):
    """
    Elimina una convocatoria existente.
    """
    convocatoria_existente = await ConvocatoriaService.obtener(convocatoria_id)
    if not convocatoria_existente:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    await ConvocatoriaService.eliminar(convocatoria_id)
    return {"mensaje": "Convocatoria eliminada exitosamente"}
