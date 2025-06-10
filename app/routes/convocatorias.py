from fastapi import APIRouter, HTTPException, Query, Body, status
from typing import List, Optional
from bson import ObjectId

from ..models import Convocatoria, ConvocatoriaCreate, ConvocatoriaUpdate
from ..database import get_convocatoria_collection

router = APIRouter(
    prefix="/convocatorias",
    tags=["Convocatorias"]
)

collection = get_convocatoria_collection()

# Endpoint para crear (sin cambios)
@router.post("/", response_model=Convocatoria, status_code=status.HTTP_201_CREATED)
async def create_convocatoria(convocatoria: ConvocatoriaCreate = Body(...)):
    convocatoria_dict = convocatoria.dict(by_alias=True)
    result = await collection.insert_one(convocatoria_dict)
    new_convocatoria = await collection.find_one({"_id": result.inserted_id})
    return new_convocatoria

# Endpoint GET con filtros mejorados
@router.get("/", response_model=List[Convocatoria])
async def get_convocatorias(
    q: Optional[str] = Query(None, min_length=3, description="Búsqueda por texto en institución, país o propiedades."),
    country: Optional[str] = Query(None, description="Filtrar por país (exacto, case-insensitive)"),
    language: Optional[str] = Query(None, description="Filtrar por idioma (debe estar en la lista de idiomas)"),
    state: Optional[str] = Query(None, description="Filtrar por estado (Vigente/No Vigente)"),
    agreement_type: Optional[str] = Query(None, description="Filtrar por tipo de convenio"),
    subscription_level: Optional[str] = Query(None, description="Filtrar por nivel de suscripción (ej. Facultad de Ciencias Humanas)"),
    limit: int = Query(20, gt=0, le=200, description="Número de resultados a devolver"),
    skip: int = Query(0, ge=0, description="Número de resultados a omitir para paginación")
):
    query = {}

    if q:
        query["$text"] = {"$search": q}

    if country:
        query["country"] = {"$regex": f"^{country}$", "$options": "i"}

    if language:
        # Busca si el idioma está presente en el array 'languages'
        query["languages"] = {"$regex": language, "$options": "i"}

    if state:
        query["state"] = {"$regex": f"^{state}$", "$options": "i"}
        
    if agreement_type:
        query["agreementType"] = {"$regex": f"^{agreement_type}$", "$options": "i"}
    
    if subscription_level:
         query["subscriptionLevel"] = {"$regex": subscription_level, "$options": "i"}

    cursor = collection.find(query).skip(skip).limit(limit)
    results = await cursor.to_list(length=limit)
    return results

# Endpoint para obtener una convocatoria por ID (sin cambios)
@router.get("/{id}", response_model=Convocatoria)
async def get_convocatoria_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")
        
    convocatoria = await collection.find_one({"_id": ObjectId(id)})
    if convocatoria:
        return convocatoria
    raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")

# ¡NUEVO! Endpoint para actualizar una convocatoria (PATCH)
@router.patch("/{id}", response_model=Convocatoria)
async def update_convocatoria(id: str, convocatoria_update: ConvocatoriaUpdate = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")

    # Excluye los campos que no se enviaron en el request para no sobreescribir con None
    update_data = {k: v for k, v in convocatoria_update.dict(by_alias=True).items() if v is not None}

    if len(update_data) < 1:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")

    updated_convocatoria = await collection.find_one({"_id": ObjectId(id)})
    return updated_convocatoria

# ¡NUEVO! Endpoint para eliminar una convocatoria
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_convocatoria(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")
        
    result = await collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")

    return