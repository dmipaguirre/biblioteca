"""Modelo Usuario."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from modelos.enums import RolUsuario


@dataclass
class Usuario:
    """Representa a un usuario del sistema: administrador o lector.

    Importante: `contrasena_hash` debe contener siempre el hash de la
    contraseña (nunca la contraseña en texto plano). El hashing se
    realiza en la capa de lógica, no en este modelo.

    Attributes:
        id: Identificador único en base de datos. None si aún no se
            ha guardado.
        nombre: Nombre completo del usuario.
        correo: Correo electrónico, usado para iniciar sesión.
        contrasena_hash: Hash de la contraseña del usuario.
        rol: Rol del usuario (admin o lector).
        fecha_registro: Fecha en que el usuario se registró.
    """

    nombre: str
    correo: str
    contrasena_hash: str
    id: Optional[int] = None
    rol: RolUsuario = field(default=RolUsuario.LECTOR)
    fecha_registro: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío")
        if not self.correo or "@" not in self.correo:
            raise ValueError("El correo del usuario no es válido")
        self.nombre = self.nombre.strip()
        self.correo = self.correo.strip().lower()

    def es_admin(self) -> bool:
        """Indica si el usuario tiene rol de administrador."""
        return self.rol == RolUsuario.ADMIN

    def es_lector(self) -> bool:
        """Indica si el usuario tiene rol de lector."""
        return self.rol == RolUsuario.LECTOR