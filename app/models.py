from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_core import core_schema
from typing import List, Optional, Any, Dict
from bson import ObjectId

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

# Modelo principal de la Convocatoria - Actualizado para coincidir con los datos reales
class Convocatoria(BaseModel):
    # El Field ahora debe usar 'validation_alias' en lugar de 'alias' para la conversión de BSON
    id: PyObjectId = Field(default_factory=PyObjectId, validation_alias="_id")
    
    # Campos directos sin alias (MongoDB guarda con nombres en inglés)
    subscriptionYear: str = "2024"
    country: str
    institution: str
    agreementType: str = "Intercambio"
    validity: str = "Vigente"
    state: str = "Activa"
    subscriptionLevel: str = "Universidad Nacional"
    languages: List[str] = []
    dreLink: Optional[str] = None
    agreementLink: Optional[str] = None
    properties: Optional[str] = Field(None, alias="Props")
    internationalLink: Optional[str] = None
    
    # Validador que mapea campos en español a inglés (compatibilidad con datos viejos)
    @model_validator(mode='before')
    @classmethod
    def map_spanish_fields(cls, data: Any) -> Any:
        """Mapea campos en español a inglés para compatibilidad con datos legacy."""
        if not isinstance(data, dict):
            return data
        
        # Mapeo de campos
        field_mapping = {
            'pais_destino': 'country',
            'universidad_destino': 'institution',
            'tipo_intercambio': 'agreementType',
            'estado': 'state',
            'programa': 'subscriptionLevel',
            'nivel_idioma': 'languages',
            'contacto': 'dreLink',
            'descripcion': 'properties',
        }
        
        # Aplicar mapeos solo si el campo en inglés no existe
        for spanish_field, english_field in field_mapping.items():
            if spanish_field in data and english_field not in data:
                data[english_field] = data[spanish_field]
        
        # Manejar fecha_creacion -> subscriptionYear
        if 'fecha_creacion' in data and 'subscriptionYear' not in data:
            fecha = data['fecha_creacion']
            if hasattr(fecha, 'year'):
                data['subscriptionYear'] = str(fecha.year)
        
        # Manejar fecha_fin -> validity
        if 'fecha_fin' in data and 'validity' not in data:
            fecha = data['fecha_fin']
            if hasattr(fecha, 'strftime'):
                data['validity'] = fecha.strftime("%B %Y")
            elif isinstance(fecha, str):
                data['validity'] = fecha
        
        return data
        if hasattr(values, 'data') and 'descripcion' in values.data:
            return values.data['descripcion']
        return None
    
    # Normaliza el campo 'languages' 
    @field_validator("languages", mode="before")
    def _normalize_languages(cls, v):
        """Convierte el campo languages en una lista normalizada."""
        if v is None or v == []:
            return []
        if isinstance(v, str):
            # Si es un string, convertirlo a lista
            return [v.capitalize()]
        if isinstance(v, list):
            # Si es una lista, normalizar cada elemento
            return [str(lang).capitalize() for lang in v if lang]
        return []

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
    
    class Config:
        populate_by_name = True