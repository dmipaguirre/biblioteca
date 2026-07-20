"""Conexión a la base de datos MySQL.

Las credenciales se leen desde variables de entorno (archivo `.env` en
la raíz del proyecto), nunca escritas directamente en el código, para
poder mantenerlas fuera del control de versiones.

Variables esperadas en `.env`:
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=biblioteca_app
    DB_PASSWORD=una_contrasena_segura
    DB_NAME=biblioteca
"""

import os
from contextlib import contextmanager
from typing import Iterator

import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()


class ConfiguracionBDError(Exception):
    """Error al leer la configuración de conexión a la base de datos."""


def _config_desde_entorno() -> dict:
    """Lee y valida las variables de entorno necesarias para conectar."""
    faltantes = [
        var for var in ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME")
        if var not in os.environ
    ]
    if faltantes:
        raise ConfiguracionBDError(
            "Faltan variables de entorno en el archivo .env: "
            + ", ".join(faltantes)
        )
    return {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ.get("DB_PORT", 3306)),
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "database": os.environ["DB_NAME"],
    }


@contextmanager
def obtener_conexion() -> Iterator["pymysql.connections.Connection"]:
    """Entrega una conexión a MySQL y garantiza que se cierre al terminar.

    Uso:
        with obtener_conexion() as conexion:
            ...
    """
    config = _config_desde_entorno()
    conexion = pymysql.connect(
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        **config,
    )
    try:
        yield conexion
    finally:
        conexion.close()


@contextmanager
def obtener_cursor() -> Iterator["pymysql.cursors.DictCursor"]:
    """Entrega un cursor listo para ejecutar queries.

    Hace commit automáticamente si todo sale bien, o rollback si ocurre
    una excepción dentro del bloque `with`. Este es el punto de entrada
    que deben usar los repositorios concretos.

    Uso:
        with obtener_cursor() as cursor:
            cursor.execute("SELECT * FROM autores WHERE id = %s", (1,))
            fila = cursor.fetchone()
    """
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        try:
            yield cursor
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()