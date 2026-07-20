"""Repositorio de datos para la entidad Categoria (tabla `categorias`)."""

from typing import List, Optional

from datos.base import RepositorioBase
from datos.conexion import obtener_cursor
from modelos.categoria import Categoria


class CategoriasRepo(RepositorioBase[Categoria]):
    """Acceso a datos (SQL puro) para la tabla `categorias`."""

    def obtener_por_id(self, id_: int) -> Optional[Categoria]:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM categorias WHERE id = %s", (id_,))
            fila = cursor.fetchone()
        return self._fila_a_categoria(fila) if fila else None

    def crear(self, entidad: Categoria) -> Categoria:
        with obtener_cursor() as cursor:
            cursor.execute(
                "INSERT INTO categorias (nombre) VALUES (%s)", (entidad.nombre,)
            )
            entidad.id = cursor.lastrowid
        return entidad

    def actualizar(self, entidad: Categoria) -> None:
        if entidad.id is None:
            raise ValueError("No se puede actualizar una categoría sin id")
        with obtener_cursor() as cursor:
            cursor.execute(
                "UPDATE categorias SET nombre = %s WHERE id = %s",
                (entidad.nombre, entidad.id),
            )

    def eliminar(self, id_: int) -> None:
        with obtener_cursor() as cursor:
            cursor.execute("DELETE FROM categorias WHERE id = %s", (id_,))

    def listar_todos(self) -> List[Categoria]:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
            filas = cursor.fetchall()
        return [self._fila_a_categoria(fila) for fila in filas]

    @staticmethod
    def _fila_a_categoria(fila: dict) -> Categoria:
        """Convierte una fila del cursor (dict) en un objeto Categoria."""
        return Categoria(id=fila["id"], nombre=fila["nombre"])