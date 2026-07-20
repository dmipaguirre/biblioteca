"""Repositorio de datos para la entidad Usuario (tabla `usuarios`)."""

from typing import List, Optional

from datos.base import RepositorioBase
from datos.conexion import obtener_cursor
from modelos.enums import RolUsuario
from modelos.usuario import Usuario


class UsuariosRepo(RepositorioBase[Usuario]):
    """Acceso a datos (SQL puro) para la tabla `usuarios`."""

    _COLUMNAS = "id, nombre, correo, contrasena_hash, rol, fecha_registro"

    def obtener_por_id(self, id_: int) -> Optional[Usuario]:
        with obtener_cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUMNAS} FROM usuarios WHERE id = %s", (id_,)
            )
            fila = cursor.fetchone()
        return self._fila_a_usuario(fila) if fila else None

    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        """Busca un usuario por correo. Usado por el flujo de login."""
        with obtener_cursor() as cursor:
            cursor.execute(
                f"SELECT {self._COLUMNAS} FROM usuarios WHERE correo = %s",
                (correo.strip().lower(),),
            )
            fila = cursor.fetchone()
        return self._fila_a_usuario(fila) if fila else None

    def crear(self, entidad: Usuario) -> Usuario:
        with obtener_cursor() as cursor:
            cursor.execute(
                """INSERT INTO usuarios (nombre, correo, contrasena_hash, rol, fecha_registro)
                   VALUES (%s, %s, %s, %s, %s)""",
                (
                    entidad.nombre,
                    entidad.correo,
                    entidad.contrasena_hash,
                    entidad.rol.value,
                    entidad.fecha_registro,
                ),
            )
            entidad.id = cursor.lastrowid
        return entidad

    def actualizar(self, entidad: Usuario) -> None:
        if entidad.id is None:
            raise ValueError("No se puede actualizar un usuario sin id")
        with obtener_cursor() as cursor:
            cursor.execute(
                """UPDATE usuarios
                   SET nombre = %s, correo = %s, contrasena_hash = %s, rol = %s
                   WHERE id = %s""",
                (
                    entidad.nombre,
                    entidad.correo,
                    entidad.contrasena_hash,
                    entidad.rol.value,
                    entidad.id,
                ),
            )

    def eliminar(self, id_: int) -> None:
        with obtener_cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_,))

    def listar_todos(self) -> List[Usuario]:
        with obtener_cursor() as cursor:
            cursor.execute(f"SELECT {self._COLUMNAS} FROM usuarios ORDER BY nombre")
            filas = cursor.fetchall()
        return [self._fila_a_usuario(fila) for fila in filas]

    @staticmethod
    def _fila_a_usuario(fila: dict) -> Usuario:
        """Convierte una fila del cursor (dict) en un objeto Usuario."""
        return Usuario(
            id=fila["id"],
            nombre=fila["nombre"],
            correo=fila["correo"],
            contrasena_hash=fila["contrasena_hash"],
            rol=RolUsuario(fila["rol"]),
            fecha_registro=fila["fecha_registro"],
        )