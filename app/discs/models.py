from pydantic import BaseModel, Field
from typing import List, Optional


class Track(BaseModel):
    """Modelo de datos para una canción del disco"""
    name: str = Field(..., description="Nombre de la canción")
    position: str = Field(..., description="Posición en el disco (ej: A1, B2)")
    duration: str = Field(..., description="Duración de la canción (ej: 3:45)")


class Disc(BaseModel):
    """Modelo de datos para un disco"""
    sku: str = Field(..., description="SKU único del disco")
    name: str = Field(..., description="Nombre del disco")
    description: str = Field(..., description="Descripción del disco")
    author: str = Field(..., description="Autor o artista del disco")
    publisher: str = Field(default="", description="Compañía discográfica")
    yearCreated: int = Field(..., description="Año de lanzamiento")
    country: str = Field(default="", description="País de origen")
    images: List[str] = Field(default_factory=list, description="Lista de URLs de imágenes")
    categories: List[str] = Field(default_factory=list, description="Categorías o géneros")
    trackList: List[Track] = Field(default_factory=list, description="Lista de canciones")
    type: str = Field(..., description="Tipo de disco (CDS, VINYLS, CASSETTES)")
    favorite: bool = Field(default=False, description="Indica si es favorito")
    enabled: bool = Field(default=True, description="Indica si está habilitado")

    class Config:
        """Configuración de Pydantic"""
        json_schema_extra = {
            "example": {
                "sku": "093624933595",
                "name": "The Black Parade",
                "description": "The Black Parade. Publicado en 2022",
                "author": "My Chemical Romance",
                "publisher": "",
                "yearCreated": 2022,
                "country": "",
                "images": ["1.jpg"],
                "categories": ["Rock"],
                "trackList": [
                    {
                        "name": "Welcome to the Black Parade",
                        "position": "A1",
                        "duration": "5:11"
                    }
                ],
                "type": "VINYLS",
                "favorite": True,
                "enabled": True
            }
        }
