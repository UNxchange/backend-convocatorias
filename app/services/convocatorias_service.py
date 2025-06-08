from app.models import Convocatoria
from app.db import mongodb

class ConvocatoriaService:
    @staticmethod
    async def crear(convocatoria_data: dict):
        existing = await mongodb.db.convocatorias.find_one({"_id": convocatoria_data["_id"]})
        if existing:
            return False
        await mongodb.db.convocatorias.insert_one(convocatoria_data)
        return True

    @staticmethod
    async def listar():
        convocatorias_cursor = mongodb.db.convocatorias.find()
        convocatorias = []
        async for doc in convocatorias_cursor:
            convocatorias.append(Convocatoria(**doc))
        return convocatorias

    @staticmethod
    async def obtener(convocatoria_id: str):
        doc = await mongodb.db.convocatorias.find_one({"_id": convocatoria_id})
        if doc:
            return Convocatoria(**doc)
        return None

    @staticmethod
    async def actualizar(convocatoria_id: str, convocatoria_actualizada: Convocatoria):
        await mongodb.db.convocatorias.replace_one({"_id": convocatoria_id}, convocatoria_actualizada.dict(by_alias=True))
        return True

    @staticmethod
    async def eliminar(convocatoria_id: str):
        await mongodb.db.convocatorias.delete_one({"_id": convocatoria_id})
        return True
