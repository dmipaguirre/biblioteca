"""Modelo Autor."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Autor:
    """Representa a un autor de uno o varios libros.

    Attributes:
        id: Identificador único en base de datos. None si aún no se
            ha guardado (por ejemplo, al crear un autor nuevo).
            
        nombre: Nombre completo del autor.
    """

    nombre: str
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del autor no puede estar vacío")
        self.nombre = self.nombre.strip()