from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class Convocatoria(BaseModel):
    id: str = Field(..., alias="_id")
    titulo: str
    descripcion: str
    pais: str
    facultad: str
    nivel: str
    fecha_inicio: date
    fecha_cierre: date
    owner: Optional[str]

    class Config:
        alias_generator = lambda field: "_id" if field == "id" else field
        allow_population_by_field_name = True