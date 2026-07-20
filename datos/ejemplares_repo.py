"""Repositorio de datos para la entidad Ejemplar (tabla `ejemplares`)."""

from typing import List, Optional

from datos.base import RepositorioBase
from datos.conexion import obtener_cursor
from modelos.ejemplar import Ejemplar
from modelos.enums import EstadoEjemplar


class EjemplaresRepo(RepositorioBase[Ejemplar]):
    """Acceso a datos (SQL puro) para la tabla `ejemplares`."""

    _COLUMNAS = "id, libro_id, codigo, estado"

    def obtener_por_id(self, id_: int) -> Optional[Ejemplar]:
        with obtener_cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUMNAS} FROM ejemplares WHERE id = %s", (id_,)
            )
            fila = cursor.fetchone()
        return self._fila_a_ejemplar(fila) if fila else None

    def crear(self, entidad: Ejemplar) -> Ejemplar:
        with obtener_cursor() as cursor:
            cursor.execute(
                "INSERT INTO ejemplares (libro_id, codigo, estado) VALUES (%s, %s, %s)",
                (entidad.libro_id, entidad.codigo, entidad.estado.value),
            )
            entidad.id = cursor.lastrowid
        return entidad

    def actualizar(self, entidad: Ejemplar) -> None:
        if entidad.id is None:
            raise ValueError("No se puede actualizar un ejemplar sin id")
        with obtener_cursor() as cursor:
            cursor.execute(
                "UPDATE ejemplares SET libro_id = %s, codigo = %s, estado = %s WHERE id = %s",
                (entidad.libro_id, entidad.codigo, entidad.estado.value, entidad.id),
            )

    def eliminar(self, id_: int) -> None:
        with obtener_cursor() as cursor:
            cursor.execute("DELETE FROM ejemplares WHERE id = %s", (id_,))

    def listar_todos(self) -> List[Ejemplar]:
        with obtener_cursor() as cursor:
            cursor.execute(f"SELECT {self._COLUMNAS} FROM ejemplares ORDER BY codigo")
            filas = cursor.fetchall()
        return [self._fila_a_ejemplar(fila) for fila in filas]

    def listar_por_libro(self, libro_id: int) -> List[Ejemplar]:
        """Devuelve todos los ejemplares (de cualquier estado) de un libro."""
        with obtener_cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUMNAS} FROM ejemplares WHERE libro_id = %s ORDER BY codigo",
                (libro_id,),
            )
            filas = cursor.fetchall()
        return [self._fila_a_ejemplar(fila) for fila in filas]

    def contar_disponibles(self, libro_id: int) -> int:
        """Cuenta cuántos ejemplares de un libro están disponibles ahora mismo.

        La capa de lógica usa este dato para decidir si un préstamo
        puede aprobarse automáticamente.
        """
        with obtener_cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS total FROM ejemplares WHERE libro_id = %s AND estado = %s",
                (libro_id, EstadoEjemplar.DISPONIBLE.value),
            )
            fila = cursor.fetchone()
        return fila["total"] if fila else 0

    def obtener_disponible_para_libro(self, libro_id: int) -> Optional[Ejemplar]:
        """Devuelve un ejemplar disponible cualquiera de ese libro, o None."""
        with obtener_cursor() as cursor:
            cursor.execute(
                f"""SELECT {self._COLUMNAS} FROM ejemplares
                    WHERE libro_id = %s AND estado = %s
                    LIMIT 1""",
                (libro_id, EstadoEjemplar.DISPONIBLE.value),
            )
            fila = cursor.fetchone()
        return self._fila_a_ejemplar(fila) if fila else None

    @staticmethod
    def _fila_a_ejemplar(fila: dict) -> Ejemplar:
        """Convierte una fila del cursor (dict) en un objeto Ejemplar."""
        return Ejemplar(
            id=fila["id"],
            libro_id=fila["libro_id"],
            codigo=fila["codigo"],
            estado=EstadoEjemplar(fila["estado"]),
        )