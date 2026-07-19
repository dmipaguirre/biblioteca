"""Modelo Libro."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Libro:
    """Representa el título de un libro (no una copia física).

    Un libro puede tener varios `Ejemplar` asociados (ver modelos/ejemplar.py).

    Attributes:
        id: Identificador único en base de datos. None si aún no se
            ha guardado.
        titulo: Título del libro.
        autor_id: FK hacia Autor.id.
        categoria_id: FK hacia Categoria.id.
        isbn: Código ISBN del libro.
        descripcion: Sinopsis o descripción breve (opcional).
    """

    titulo: str
    autor_id: int
    categoria_id: int
    isbn: str
    descripcion: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.titulo or not self.titulo.strip():
            raise ValueError("El título del libro no puede estar vacío")
        if not self.isbn or not self.isbn.strip():
            raise ValueError("El ISBN no puede estar vacío")
        self.titulo = self.titulo.strip()
        self.isbn = self.isbn.strip()