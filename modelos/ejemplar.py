"""Modelo Ejemplar."""

from dataclasses import dataclass, field
from typing import Optional

from modelos.enums import EstadoEjemplar


@dataclass
class Ejemplar:
    """Representa una copia física concreta de un `Libro`.

    Los préstamos se realizan sobre un ejemplar específico, no sobre
    el libro en general, ya que es la copia física la que se entrega.

    Attributes:
        id: Identificador único en base de datos. None si aún no se
            ha guardado.
        libro_id: FK hacia Libro.id.
        codigo: Código/identificador único del ejemplar (ej. etiqueta física).
        estado: Estado actual del ejemplar (disponible o prestado).
    """

    libro_id: int
    codigo: str
    id: Optional[int] = None
    estado: EstadoEjemplar = field(default=EstadoEjemplar.DISPONIBLE)

    def __post_init__(self) -> None:
        if not self.codigo or not self.codigo.strip():
            raise ValueError("El código del ejemplar no puede estar vacío")
        self.codigo = self.codigo.strip()

    def esta_disponible(self) -> bool:
        """Indica si el ejemplar puede prestarse en este momento."""
        return self.estado == EstadoEjemplar.DISPONIBLE