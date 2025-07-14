from fastapi import APIRouter, HTTPException, Query, Body, status, Depends
from typing import List, Optional
from bson import ObjectId
import sys
import os

# Agregar el directorio raíz al path para importar notification_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ..models import Convocatoria, ConvocatoriaCreate, ConvocatoriaUpdate
from ..database import get_convocatoria_collection
# ¡NUEVO! Importamos nuestras dependencias de seguridad
from ..security import get_current_user, require_admin_or_pro_role, require_admin_role, TokenData
# Importamos el cliente de notificaciones
from notification_client import notification_client

router = APIRouter(
    prefix="/convocatorias",
    tags=["Convocatorias"]
)

collection = get_convocatoria_collection()

# --- PROTECCIÓN DE ENDPOINTS ---

# POST protegido solo para administradores
@router.post("/", response_model=Convocatoria, status_code=status.HTTP_201_CREATED)
async def create_convocatoria(
    convocatoria: ConvocatoriaCreate = Body(...),
    current_user: TokenData = Depends(require_admin_or_pro_role) # <-- Dependencia de administrador
):
    convocatoria_dict = convocatoria.dict(by_alias=True)
    result = await collection.insert_one(convocatoria_dict)
    new_convocatoria = await collection.find_one({"_id": result.inserted_id})
    return new_convocatoria

# GET protegido para cualquier usuario autenticado
@router.get("/", response_model=List[Convocatoria])
async def get_convocatorias(
    # ... (todos los parámetros de query como antes)
    q: Optional[str] = Query(None, min_length=3, description="Búsqueda por texto..."),
    country: Optional[str] = Query(None, description="Filtrar por país..."),
    language: Optional[str] = Query(None, description="Filtrar por idioma..."),
    state: Optional[str] = Query(None, description="Filtrar por estado..."),
    agreement_type: Optional[str] = Query(None, description="Filtrar por tipo de convenio"),
    subscription_level: Optional[str] = Query(None, description="Filtrar por nivel de suscripción"),
    limit: int = Query(20, gt=0, le=200),
    skip: int = Query(0, ge=0),
    # Añadimos la dependencia de autenticación básica
    current_user: TokenData = Depends(get_current_user) # <-- Dependencia de usuario autenticado
):
    query = {}
    # ... (la lógica de construcción de la query no cambia)
    if q: query["$text"] = {"$search": q}
    if country: query["country"] = {"$regex": f"^{country}$", "$options": "i"}
    if language: query["languages"] = {"$regex": language, "$options": "i"}
    if state: query["state"] = {"$regex": f"^{state}$", "$options": "i"}
    if agreement_type: query["agreementType"] = {"$regex": f"^{agreement_type}$", "$options": "i"}
    if subscription_level: query["subscriptionLevel"] = {"$regex": subscription_level, "$options": "i"}
    
    cursor = collection.find(query).skip(skip).limit(limit)
    results = await cursor.to_list(length=limit)
    return results

# GET por ID protegido para cualquier usuario autenticado
@router.get("/{id}", response_model=Convocatoria)
async def get_convocatoria_by_id(
    id: str,
    current_user: TokenData = Depends(get_current_user) # <-- Dependencia de usuario autenticado
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")
    convocatoria = await collection.find_one({"_id": ObjectId(id)})
    if convocatoria:
        return convocatoria
    raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")

# PATCH protegido solo para administradores
@router.patch("/{id}", response_model=Convocatoria)
async def update_convocatoria(
    id: str,
    convocatoria_update: ConvocatoriaUpdate = Body(...),
    current_user: TokenData = Depends(require_admin_role) # <-- Dependencia de administrador
):
    # ... (la lógica interna no cambia)
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")
    update_data = {k: v for k, v in convocatoria_update.dict(by_alias=True).items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")
    updated_convocatoria = await collection.find_one({"_id": ObjectId(id)})
    return updated_convocatoria

# DELETE protegido solo para administradores
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_convocatoria(
    id: str,
    current_user: TokenData = Depends(require_admin_role) # <-- Dependencia de administrador
):
    # ... (la lógica interna no cambia)
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")
    return

@router.post("/{id}/interest", status_code=status.HTTP_200_OK)
async def express_interest(
    id: str,
    current_user: TokenData = Depends(get_current_user)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")

    if not current_user.sub:
        raise HTTPException(status_code=401, detail="Usuario no autenticado correctamente")
    
    # Obtener la convocatoria antes de actualizar
    convocatoria = await collection.find_one({"_id": ObjectId(id)})
    if not convocatoria:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")
    
    # Verificar si el usuario ya está interesado
    if current_user.sub in convocatoria.get("interestedUsers", []):
        return {"message": "El usuario ya había expresado interés en esta convocatoria"}
    
    # Registrar el interés
    result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$addToSet": {"interestedUsers": current_user.sub}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")
    
    # Enviar correo de confirmación de interés
    try:
        # Extraer el nombre del usuario del email (parte antes del @)
        username = current_user.sub.split('@')[0]
        
        await notification_client.send_interest_confirmation_email(
            user_email=current_user.sub,
            username=username,
            convocatoria_data=convocatoria
        )
        print(f"✅ Correo de confirmación de interés enviado a {current_user.sub}")
    except Exception as e:
        print(f"❌ Error al enviar correo de confirmación: {e}")
        # No fallar la operación si hay problemas con las notificaciones
    
    return {"message": "Interés registrado exitosamente"}

# Endpoint para que un usuario retire su interés
@router.delete("/{id}/interest", status_code=status.HTTP_200_OK)
async def remove_interest(
    id: str,
    current_user: TokenData = Depends(get_current_user)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de convocatoria inválido")
    
    if not current_user.sub:
        raise HTTPException(status_code=401, detail="Usuario no autenticado correctamente")
    
    # Obtener la convocatoria antes de actualizar
    convocatoria = await collection.find_one({"_id": ObjectId(id)})
    if not convocatoria:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")
    
    # Verificar si el usuario tenía interés registrado
    if current_user.sub not in convocatoria.get("interestedUsers", []):
        return {"message": "El usuario no tenía interés registrado en esta convocatoria"}
    
    # Remover el interés
    result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$pull": {"interestedUsers": current_user.sub}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Convocatoria con id {id} no encontrada")
    
    # Enviar correo de confirmación de remoción de interés
    try:
        # Extraer el nombre del usuario del email (parte antes del @)
        username = current_user.sub.split('@')[0]
        
        await notification_client.send_interest_removal_email(
            user_email=current_user.sub,
            username=username,
            convocatoria_data=convocatoria
        )
        print(f"✅ Correo de confirmación de remoción de interés enviado a {current_user.sub}")
    except Exception as e:
        print(f"❌ Error al enviar correo de confirmación: {e}")
        # No fallar la operación si hay problemas con las notificaciones
    
    return {"message": "Interés removido exitosamente"}