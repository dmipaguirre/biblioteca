"""Repositorio de datos para la entidad Prestamo (tabla `prestamos`)."""

from typing import List, Optional

from datos.base import RepositorioBase
from datos.conexion import obtener_cursor
from modelos.enums import EstadoPrestamo
from modelos.prestamo import Prestamo


class PrestamosRepo(RepositorioBase[Prestamo]):
    """Acceso a datos (SQL puro) para la tabla `prestamos`."""

    _COLUMNAS = (
        "id, usuario_id, ejemplar_id, fecha_prestamo, fecha_limite, "
        "fecha_devolucion, estado"
    )

    def obtener_por_id(self, id_: int) -> Optional[Prestamo]:
        with obtener_cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUMNAS} FROM prestamos WHERE id = %s", (id_,)
            )
            fila = cursor.fetchone()
        return self._fila_a_prestamo(fila) if fila else None

    def crear(self, entidad: Prestamo) -> Prestamo:
        with obtener_cursor() as cursor:
            cursor.execute(
                """INSERT INTO prestamos
                       (usuario_id, ejemplar_id, fecha_prestamo, fecha_limite,
                        fecha_devolucion, estado)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    entidad.usuario_id,
                    entidad.ejemplar_id,
                    entidad.fecha_prestamo,
                    entidad.fecha_limite,
                    entidad.fecha_devolucion,
                    entidad.estado.value,
                ),
            )
            entidad.id = cursor.lastrowid
        return entidad

    def actualizar(self, entidad: Prestamo) -> None:
        if entidad.id is None:
            raise ValueError("No se puede actualizar un préstamo sin id")
        with obtener_cursor() as cursor:
            cursor.execute(
                """UPDATE prestamos
                   SET usuario_id = %s, ejemplar_id = %s, fecha_prestamo = %s,
                       fecha_limite = %s, fecha_devolucion = %s, estado = %s
                   WHERE id = %s""",
                (
                    entidad.usuario_id,
                    entidad.ejemplar_id,
                    entidad.fecha_prestamo,
                    entidad.fecha_limite,
                    entidad.fecha_devolucion,
                    entidad.estado.value,
                    entidad.id,
                ),
            )

    def eliminar(self, id_: int) -> None:
        with obtener_cursor() as cursor:
            cursor.execute("DELETE FROM prestamos WHERE id = %s", (id_,))

    def listar_todos(self) -> List[Prestamo]:
        with obtener_cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUMNAS} FROM prestamos ORDER BY fecha_prestamo DESC"
            )
            filas = cursor.fetchall()
        return [self._fila_a_prestamo(fila) for fila in filas]

    def listar_por_usuario(self, usuario_id: int) -> List[Prestamo]:
        """Historial completo de préstamos de un usuario (activos e históricos)."""
        with obtener_cursor() as cursor:
            cursor.execute(
                f"""SELECT {self._COLUMNAS} FROM prestamos
                    WHERE usuario_id = %s
                    ORDER BY fecha_prestamo DESC""",
                (usuario_id,),
            )
            filas = cursor.fetchall()
        return [self._fila_a_prestamo(fila) for fila in filas]

    def contar_activos_por_usuario(self, usuario_id: int) -> int:
        """Cuenta los préstamos activos de un usuario.

        La capa de lógica usa este dato para aplicar la regla de
        máximo 4 préstamos simultáneos.
        """
        with obtener_cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS total FROM prestamos WHERE usuario_id = %s AND estado = %s",
                (usuario_id, EstadoPrestamo.ACTIVO.value),
            )
            fila = cursor.fetchone()
        return fila["total"] if fila else 0

    def listar_activos_o_atrasados(self) -> List[Prestamo]:
        """Para la vista de control del administrador: préstamos no devueltos."""
        with obtener_cursor() as cursor:
            cursor.execute(
                f"""SELECT {self._COLUMNAS} FROM prestamos
                    WHERE estado IN (%s, %s)
                    ORDER BY fecha_limite""",
                (EstadoPrestamo.ACTIVO.value, EstadoPrestamo.ATRASADO.value),
            )
            filas = cursor.fetchall()
        return [self._fila_a_prestamo(fila) for fila in filas]

    @staticmethod
    def _fila_a_prestamo(fila: dict) -> Prestamo:
        """Convierte una fila del cursor (dict) en un objeto Prestamo."""
        return Prestamo(
            id=fila["id"],
            usuario_id=fila["usuario_id"],
            ejemplar_id=fila["ejemplar_id"],
            fecha_prestamo=fila["fecha_prestamo"],
            fecha_limite=fila["fecha_limite"],
            fecha_devolucion=fila["fecha_devolucion"],
            estado=EstadoPrestamo(fila["estado"]),
        )