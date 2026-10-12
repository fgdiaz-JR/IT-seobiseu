# IT seobiseu

Aplicación web para organizar servicios de tecnología. Permite imaginar una
mesa de ayuda donde una empresa registra clientes, sedes, solicitudes,
órdenes de trabajo e inventario.

Este README explica el proyecto paso a paso y con palabras sencillas. La idea
es que una persona que nunca ha programado pueda entender qué ocurre.

## 1. ¿Qué problema resuelve?

Cuando una empresa recibe muchos problemas de tecnología, es fácil olvidar
quién pidió ayuda, qué técnico está trabajando, qué equipo tiene el cliente o
qué materiales quedan en bodega.

IT seobiseu organiza esa información en un solo lugar:

- **Clientes:** empresas que reciben el servicio.
- **Sedes:** lugares donde trabaja cada cliente.
- **Tickets:** solicitudes o problemas reportados.
- **Órdenes de trabajo:** tareas que un técnico debe realizar.
- **Inventario:** equipos, repuestos y materiales disponibles.
- **SLA:** reglas que indican cuánto se puede tardar la respuesta y la solución.
- **Usuarios y roles:** personas que usan el sistema y lo que cada una puede hacer.

## 2. La aplicación explicada como una cadena

La aplicación tiene tres partes principales:

```text
Persona usuaria
      ↓
Frontend: pantallas que se ven en el navegador
      ↓
Backend: servidor que recibe, valida y procesa las solicitudes
      ↓
Oracle: base de datos donde se guarda la información
```

### Frontend: lo que se ve

El frontend está en [frontend/](frontend/). Son archivos HTML, CSS y
JavaScript. Esta parte muestra el menú, las tablas, los formularios, los
botones y los mensajes.

Por ejemplo, cuando una persona abre la pantalla de clientes, el navegador
lee [frontend/clientes.html](frontend/clientes.html). El diseño general está
en [frontend/styles/custom.css](frontend/styles/custom.css) y el comportamiento
interactivo está en [frontend/js/app.js](frontend/js/app.js).

El frontend también tiene un cliente para hablar con la API:
[frontend/js/api.js](frontend/js/api.js).

### Backend: el trabajador que procesa

El backend está en [backend/](backend/) y usa FastAPI, una herramienta de
Python para crear APIs.

Una API es como un mesero: el frontend pide algo, por ejemplo "muéstrame los
clientes", y el backend recibe el pedido, consulta la base de datos y devuelve
la respuesta.

El punto de entrada actual es [backend/main.py](backend/main.py). También
existe un endpoint de prueba:

```text
GET /api/v1/health
```

Si responde `status: ok`, el servidor está funcionando. La documentación
interactiva se crea automáticamente en:

```text
http://localhost:8000/docs
```

### Oracle: la memoria de la aplicación

Oracle guarda los datos aunque se cierre el navegador o se reinicie el
servidor. Los scripts para construir esta memoria están en [database/](database/).

- [01_tables.sql](database/01_tables.sql) crea las tablas.
- [02_constraints.sql](database/02_constraints.sql) conecta las tablas y evita datos inválidos.
- [03_data.sql](database/03_data.sql) agrega roles, SLA y datos iniciales.
- [04_queries.sql](database/04_queries.sql) contiene consultas útiles para reportes.

## 3. ¿Cómo se conectan las piezas?

Supongamos que alguien crea un ticket:

1. La persona llena el formulario en el navegador.
2. JavaScript revisa que los campos básicos estén completos.
3. El frontend envía los datos a FastAPI por una petición HTTP.
4. FastAPI revisa la petición y los permisos del usuario.
5. FastAPI guarda el ticket en Oracle.
6. Oracle confirma que el ticket fue guardado.
7. FastAPI devuelve una respuesta.
8. El frontend muestra el ticket o un mensaje de error.

El navegador **no se conecta directamente a Oracle**. Eso protege las
credenciales. Solo el backend conoce la contraseña de la base de datos.

## 4. Carpetas importantes

```text
IT seobiseu/
├── frontend/       Pantallas para el navegador
├── backend/        API FastAPI y conexión con Oracle
├── database/       Scripts SQL para crear y consultar la base de datos
├── README.md       Esta guía
├── .gitignore      Archivos secretos o temporales que Git no debe subir
└── Enunciado...    Documento con los requisitos académicos
```

La carpeta `ui-ux-pro-max-skill/`, si está presente, contiene la referencia de
diseño utilizada durante la mejora visual. No es necesaria para ejecutar la
aplicación.

## 5. Usar Oracle Cloud desde el navegador

Para una aplicación en línea se recomienda usar Oracle Autonomous Database
Always Free:

1. Crear una base de datos Autonomous Database en Oracle Cloud.
2. Entrar a la base y abrir **Database Actions**.
3. Abrir **SQL** o **SQL Worksheet**.
4. Crear un usuario separado para la aplicación, en lugar de usar `ADMIN`.
5. Ejecutar los scripts SQL como ese usuario, en el orden indicado.

Ejemplo para crear el usuario desde una sesión administrativa:

```sql
CREATE USER IT_SEOBISEU IDENTIFIED BY "Cambia_Esta_Clave_2026";

GRANT CREATE SESSION TO IT_SEOBISEU;
GRANT CREATE TABLE TO IT_SEOBISEU;
GRANT CREATE VIEW TO IT_SEOBISEU;
GRANT CREATE PROCEDURE TO IT_SEOBISEU;
GRANT CREATE TRIGGER TO IT_SEOBISEU;

ALTER USER IT_SEOBISEU QUOTA UNLIMITED ON DATA;
```

La contraseña del ejemplo es solo una muestra. Debe reemplazarse por una
contraseña nueva y privada.

Después de crear el usuario, ejecuta:

1. `database/01_tables.sql`
2. `database/02_constraints.sql`
3. `database/03_data.sql`

No ejecutes `04_queries.sql` como creación de tablas; ese archivo solo tiene
consultas de lectura.

## 6. Ejecutar el backend en el computador

Necesitas Python instalado.

### Crear un entorno separado

Un entorno virtual es una cajita donde se instalan las herramientas de este
proyecto sin dañar otros proyectos:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Crear la configuración privada

Copia `backend/.env.example` con el nombre `backend/.env` y completa tus datos:

```env
APP_ENV=development
FRONTEND_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
ORACLE_USER=IT_SEOBISEU
ORACLE_PASSWORD=tu_clave_privada
ORACLE_DSN=tu_servicio_de_oracle_cloud
JWT_SECRET_KEY=una_clave_larga_y_privada_de_al_menos_32_caracteres
```

El archivo `.env` es privado. No lo publiques ni lo envíes por chat.

### Encender el servidor

Desde la carpeta [backend/](backend/):

```powershell
uvicorn main:app --reload
```

Luego abre:

- API: `http://localhost:8000`
- Documentación: `http://localhost:8000/docs`
- Salud del servidor: `http://localhost:8000/api/v1/health`

## 7. Ver el frontend

El frontend necesita servirse como una página web. Desde la carpeta raíz se
puede usar el servidor sencillo de Python:

```powershell
python -m http.server 5500 --directory frontend
```

Después abre `http://localhost:5500`.

No conviene abrir solamente el archivo HTML con doble clic cuando se esté
probando la conexión con la API, porque un servidor web local se comporta más
parecido al despliegue real.

## 8. Cómo se publica en internet

Para poner todo en línea se publican dos cosas:

1. **Frontend:** puede publicarse en Netlify, Vercel, Cloudflare Pages o GitHub Pages.
2. **Backend:** puede publicarse en Render, Railway, Fly.io, Azure, Google Cloud Run u Oracle Cloud.

La base Oracle permanece en Oracle Cloud. En el servidor del backend se
configuran como secretos:

- `ORACLE_USER`
- `ORACLE_PASSWORD`
- `ORACLE_DSN`
- `JWT_SECRET_KEY`

El frontend debe apuntar a la URL pública del backend, no a
`localhost:8000`. Nunca se deben poner la contraseña, el Wallet de Oracle o la
clave JWT dentro de `frontend/`.

## 9. Seguridad explicada fácilmente

Una contraseña es como la llave de una casa. Por eso:

- `backend/.env` no se sube a GitHub.
- El Wallet de Oracle no se sube a GitHub.
- No se utiliza `ADMIN` desde la aplicación.
- Se usa un usuario de base de datos separado.
- `JWT_SECRET_KEY` debe ser larga y privada.
- El frontend nunca recibe las credenciales de Oracle.

El archivo [.gitignore](.gitignore) ayuda a que Git ignore archivos privados
y temporales.

## 10. Estado actual y siguiente trabajo

Actualmente el proyecto contiene:

- Interfaz visual responsive con modo claro y oscuro.
- Menú móvil y tabla de clientes adaptable a celulares.
- Estructura inicial de FastAPI.
- Endpoint de salud.
- Esquema Oracle con diez tablas relacionadas.
- Datos iniciales de roles, SLA y clientes.
- Cliente JavaScript preparado para usar tokens Bearer.

Todavía se debe completar para tener una aplicación productiva:

- Login real con JWT.
- Permisos reales por rol.
- CRUD completo de clientes, tickets, órdenes e inventario.
- Dashboard conectado a datos de Oracle.
- Reportes y exportación.
- Pruebas automatizadas.
- Despliegue público del frontend y backend.

## 11. Enlaces útiles

- [Oracle Autonomous Database Always Free](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-always-free.html)
- [Conectar Oracle con Wallet](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/connect-sql-dev182.html)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Bootstrap](https://getbootstrap.com/)

## Licencia y autoría

Proyecto académico de gestión de servicios TI.
