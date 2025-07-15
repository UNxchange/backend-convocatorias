from pydantic import BaseModel, Field, field_validator
from pydantic_core import core_schema
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

# Helper para ObjectId - VERSIÓN CORREGIDA PARA PYDANTIC V2
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type, _handler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(
                                cls.validate
                            ),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
# clase de estudiante interesado
class UserInterest(BaseModel):
    username: str
    interestedAt: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None

# Modelo principal de la Convocatoria
class Convocatoria(BaseModel):
    # El Field ahora debe usar 'validation_alias' en lugar de 'alias' para la conversión de BSON
    id: PyObjectId = Field(default_factory=PyObjectId, validation_alias="_id")
    subscriptionYear: str
    country: str
    institution: str
    agreementType: str
    validity: str
    state: str
    subscriptionLevel: str
    languages: List[str] = []
    dreLink: Optional[str] = None
    agreementLink: Optional[str] = None
    # 'alias' está bien aquí para el output, pero es bueno ser consistente
    properties: Optional[str] = Field(None, validation_alias="Props")
    internationalLink: Optional[str] = None
    # agregar lista de estudiantes interesados
    interestedUsers: List[str] = Field(default_factory=list, description="Lista de usernames de usuarios interesados")

    # Normaliza el campo 'languages'
    @field_validator("languages", mode="before")
    def _capitalize_languages(cls, v):
        """Asegura que cada idioma empiece en mayúscula y sin duplicados."""
        if v is None:
            return []
        if isinstance(v, str):
            # Permite que el cliente envíe un único string de idiomas
            v = [v]
        if not isinstance(v, list):
            raise TypeError("languages debe ser una lista de strings")

        clean: List[str] = []
        for lang in v:
            if not isinstance(lang, str):
                raise TypeError("Cada idioma debe ser string")
            capitalized = lang.strip().capitalize()
            if capitalized and capitalized not in clean:
                clean.append(capitalized)
        return clean

    class Config:
        # allow_population_by_field_name es ahora el comportamiento por defecto y puede ser removido
        arbitrary_types_allowed = True
        # json_encoders está obsoleto, Pydantic V2 maneja esto mejor automáticamente
        json_schema_extra = {"example": {"id": "60d5ec9af682fbd17a5e8e89", "subscriptionYear": "2019",
        "country": "Alemania",
        "institution": "Bergische Universität Wuppertal",
        "agreementType": "Intercambio",
        "validity": "March - 2024",
        "state": "No Vigente",
        "dreLink": "http://www.dre.unal.edu.co/uploads/tx_unalori/CI_2019__Bergische_Universitaet_Wuppertal__Alemania_.pdf",
        "subscriptionLevel": "Universidad Nacional de Colombia",
        "agreementLink": "http://www.dre.unal.edu.co/es/convocatorias.html?cvc%5BshowUid%5D=1915&cHash=97dd8e0cf2f164a8144820073ab40f0c&pointer=8&listtype=1",
        "languages": "Alemán inglés",
        "Props": "Enfoque internacional\nRelación con la comunidad local\nPatrimonio industrial\nInterdisciplinariedad\nInvestigación innovadora\nEnfoque práctico\nArte y diseño\nArquitectura y espacios urbanos\nCultura visual y estudios de medios",
        "internationalLink": "https://www.internationales.uni-wuppertal.de/en/incoming/international-students/exchange-students-from-buw-partner-universities.html"}} # Actualiza el ejemplo

        
    

# Modelo para crear una nueva convocatoria
class ConvocatoriaCreate(BaseModel):
    subscriptionYear: str
    country: str
    institution: str
    agreementType: str
    validity: str
    state: str = "Vigente"
    subscriptionLevel: str
    languages: List[str] = []
    dreLink: Optional[str] = None
    agreementLink: Optional[str] = None
    properties: Optional[str] = Field(None, alias="Props")
    internationalLink: Optional[str] = None
    interestedUsers: List[str] = Field(default_factory=list)
    # La configuración de alias ya no necesita 'allow_population_by_field_name'
    class Config:
        populate_by_name = True


# Modelo para actualizar una convocatoria
class ConvocatoriaUpdate(BaseModel):
    subscriptionYear: Optional[str] = None
    country: Optional[str] = None
    institution: Optional[str] = None
    agreementType: Optional[str] = None
    validity: Optional[str] = None
    state: Optional[str] = None
    subscriptionLevel: Optional[str] = None
    languages: Optional[List[str]] = None
    dreLink: Optional[str] = None
    agreementLink: Optional[str] = None
    properties: Optional[str] = Field(None, alias="Props")
    internationalLink: Optional[str] = None
    interestedUsers: Optional[List[str]] = None
    
    class Config:
        populate_by_name = True

# Modelo para estadísticas de convocatorias
class ConvocatoriaStats(BaseModel):
    total_acuerdos_suscritos: int = Field(description="Total de acuerdos suscritos")
    acuerdos_activos: int = Field(description="Acuerdos con estado 'Vigente'")
    total_aplicaciones: int = Field(description="Total de usuarios que han expresado interés")
    estadisticas_por_idioma: dict = Field(description="Conteo de convocatorias por idioma")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_acuerdos_suscritos": 150,
                "acuerdos_activos": 75,
                "total_aplicaciones": 320,
                "estadisticas_por_idioma": {
                    "Inglés": 85,
                    "Español": 60,
                    "Alemán": 25,
                    "Francés": 15
                }
            }
        }