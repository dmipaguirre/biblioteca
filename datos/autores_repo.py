"""Repositorio de datos para la entidad Autor (tabla `autores`)."""

from typing import List, Optional

from datos.base import RepositorioBase
from datos.conexion import obtener_cursor
from modelos.autor import Autor


class AutoresRepo(RepositorioBase[Autor]):
    """Acceso a datos (SQL puro) para la tabla `autores`."""

    def obtener_por_id(self, id_: int) -> Optional[Autor]:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM autores WHERE id = %s", (id_,))
            fila = cursor.fetchone()
        return self._fila_a_autor(fila) if fila else None

    def crear(self, entidad: Autor) -> Autor:
        with obtener_cursor() as cursor:
            cursor.execute(
                "INSERT INTO autores (nombre) VALUES (%s)", (entidad.nombre,)
            )
            entidad.id = cursor.lastrowid
        return entidad

    def actualizar(self, entidad: Autor) -> None:
        if entidad.id is None:
            raise ValueError("No se puede actualizar un autor sin id")
        with obtener_cursor() as cursor:
            cursor.execute(
                "UPDATE autores SET nombre = %s WHERE id = %s",
                (entidad.nombre, entidad.id),
            )

    def eliminar(self, id_: int) -> None:
        with obtener_cursor() as cursor:
            cursor.execute("DELETE FROM autores WHERE id = %s", (id_,))

    def listar_todos(self) -> List[Autor]:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM autores ORDER BY nombre")
            filas = cursor.fetchall()
        return [self._fila_a_autor(fila) for fila in filas]

    @staticmethod
    def _fila_a_autor(fila: dict) -> Autor:
        """Convierte una fila del cursor (dict) en un objeto Autor."""
        return Autor(id=fila["id"], nombre=fila["nombre"])