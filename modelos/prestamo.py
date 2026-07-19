"""Modelo Prestamo."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from modelos.enums import EstadoPrestamo


@dataclass
class Prestamo:
    """Representa el préstamo de un `Ejemplar` a un `Usuario`.

    Nota de diseño: este modelo solo almacena datos, no aplica reglas
    de negocio (por ejemplo, no calcula la fecha límite ni valida el
    máximo de préstamos permitidos). Esas reglas viven en la capa
    `logica/`, que es quien construye y valida instancias de Prestamo.

    Attributes:
        id: Identificador único en base de datos. None si aún no se
            ha guardado.
        usuario_id: FK hacia Usuario.id.
        ejemplar_id: FK hacia Ejemplar.id.
        fecha_prestamo: Fecha en que se realizó el préstamo.
        fecha_limite: Fecha límite de devolución.
        fecha_devolucion: Fecha real de devolución. None mientras el
            préstamo sigue activo.
        estado: Estado actual del préstamo.
    """

    usuario_id: int
    ejemplar_id: int
    fecha_prestamo: date
    fecha_limite: date
    id: Optional[int] = None
    fecha_devolucion: Optional[date] = None
    estado: EstadoPrestamo = field(default=EstadoPrestamo.ACTIVO)

    def esta_atrasado(self, hoy: Optional[date] = None) -> bool:
        """Indica si el préstamo sigue activo y ya pasó su fecha límite.

        Args:
            hoy: Fecha de referencia para la comparación. Si no se
                indica, se usa la fecha actual del sistema.
        """
        hoy = hoy or date.today()
        return self.estado == EstadoPrestamo.ACTIVO and hoy > self.fecha_limite

    def dias_restantes(self, hoy: Optional[date] = None) -> int:
        """Días que faltan para la fecha límite (negativo si ya venció)."""
        hoy = hoy or date.today()
        return (self.fecha_limite - hoy).days