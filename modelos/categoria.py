"""Modelo Categoria."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    """Representa una categoría o género literario (ej. Novela, Ciencia).

    Attributes:
        id: Identificador único en base de datos. None si aún no se
            ha guardado.
        nombre: Nombre de la categoría.
    """

    nombre: str
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío")
        self.nombre = self.nombre.strip()