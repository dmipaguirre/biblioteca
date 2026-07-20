# Sistema de gestión de biblioteca

Aplicación en Python para gestionar el catálogo, los usuarios y los préstamos de
una biblioteca. El proyecto está organizado por capas y utiliza MySQL como base
de datos, modelos basados en `dataclasses` y repositorios con SQL parametrizado.

> **Estado del proyecto:** en desarrollo. Los modelos y la capa de acceso a
> datos están implementados; la interfaz, la lógica de negocio y las pruebas
> todavía están pendientes. Por ahora, `main.py` únicamente muestra un mensaje
> de inicialización.

## Funcionalidades implementadas

- Modelos para autores, categorías, libros, ejemplares, usuarios y préstamos.
- Validaciones básicas de los datos en los modelos.
- Roles de usuario (`admin` y `lector`).
- Estados de ejemplares y préstamos mediante enumeraciones.
- Operaciones CRUD para todas las entidades mediante el patrón Repository.
- Búsqueda de libros por título, autor y categoría.
- Consulta de ejemplares disponibles.
- Consulta del historial y de los préstamos activos de un usuario.
- Transacciones automáticas con `commit` y `rollback`.
- Configuración de MySQL mediante variables de entorno.

## Requisitos

- Python 3.14 o posterior.
- MySQL.
- Los paquetes [`PyMySQL`](https://pypi.org/project/PyMySQL/) y
  [`python-dotenv`](https://pypi.org/project/python-dotenv/).

El archivo `pyproject.toml` todavía no declara las dependencias externas. Para
trabajar con la capa de datos, instálalas manualmente:

```bash
python -m pip install pymysql python-dotenv
```

## Configuración

1. Clona el repositorio y entra en la carpeta del proyecto.
2. Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias indicadas en la sección anterior.
4. Crea un archivo `.env` en la raíz con la conexión a MySQL:

   ```dotenv
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=biblioteca_app
   DB_PASSWORD=una_contrasena_segura
   DB_NAME=biblioteca
   ```

No publiques este archivo ni incluyas credenciales reales en el código.

## Base de datos

Los repositorios esperan una base de datos ya creada con las siguientes tablas
y columnas:

| Tabla | Columnas utilizadas |
| --- | --- |
| `autores` | `id`, `nombre` |
| `categorias` | `id`, `nombre` |
| `libros` | `id`, `titulo`, `autor_id`, `categoria_id`, `isbn`, `descripcion` |
| `ejemplares` | `id`, `libro_id`, `codigo`, `estado` |
| `usuarios` | `id`, `nombre`, `correo`, `contrasena_hash`, `rol`, `fecha_registro` |
| `prestamos` | `id`, `usuario_id`, `ejemplar_id`, `fecha_prestamo`, `fecha_limite`, `fecha_devolucion`, `estado` |

El repositorio aún no incluye migraciones ni un script SQL de creación. El
diagrama entidad-relación disponible en `MER.html` sirve como referencia para
las relaciones del dominio.

## Ejecución

Ejecuta el punto de entrada desde la raíz del proyecto:

```bash
python main.py
```

Salida actual:

```text
Inicializando biblioteca...
```

## Ejemplo de uso de un repositorio

Con la base de datos configurada, se puede acceder a las entidades desde la
capa `datos`:

```python
from datos.libros_repo import LibrosRepo

repositorio = LibrosRepo()

for libro in repositorio.buscar(titulo="Quijote"):
    print(libro.titulo, libro.isbn)
```

Los repositorios abren y cierran su propia conexión. Cada operación confirma la
transacción si finaliza correctamente y ejecuta `rollback` si se produce una
excepción.

## Estructura del proyecto

```text
biblioteca/
├── config/                 # Configuración adicional (pendiente)
├── datos/                  # Conexión y repositorios MySQL
│   └── base/               # Contrato común RepositorioBase
├── interfaz/               # Interfaz de usuario (pendiente)
├── logica/                 # Reglas y casos de uso (pendiente)
├── logs/                   # Archivos de registro de la aplicación
├── modelos/                # Entidades y enumeraciones del dominio
├── tests/                  # Pruebas automatizadas (pendientes)
├── main.py                 # Punto de entrada
├── MER.html                # Diagrama entidad-relación
├── PROJECT_STRUCTURE.md    # Resumen de la estructura de carpetas
└── pyproject.toml          # Metadatos y configuración del proyecto
```

## Diseño

La separación por capas busca mantener responsabilidades claras:

- `modelos`: representa los datos del dominio sin acceder a la base de datos.
- `datos`: contiene SQL y transforma filas de MySQL en objetos del dominio.
- `logica`: alojará las reglas de negocio, como límites de préstamos, fechas de
  devolución y almacenamiento seguro de contraseñas.
- `interfaz`: contendrá la interacción con administradores y lectores.

Las contraseñas deben llegar a `Usuario.contrasena_hash` ya cifradas; nunca se
deben guardar contraseñas en texto plano.

## Próximos pasos

- Implementar los servicios y reglas de negocio.
- Desarrollar la interfaz de usuario.
- Añadir migraciones o un script de creación de la base de datos.
- Declarar las dependencias en `pyproject.toml`.
- Incorporar pruebas unitarias y de integración.
