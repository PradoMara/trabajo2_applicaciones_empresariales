# Trabajo 2 - Aplicaciones Empresariales

## Descripcion general
Aplicacion web construida con Streamlit para gestionar clientes mediante operaciones CRUD.

Actualmente el proyecto funciona con backend real en SQLite (sin datos simulados), manteniendo validaciones en formularios y flujo completo desde la interfaz hasta la persistencia de datos.

## Alcance actual
- Registro de clientes con ID autogenerado.
- Actualizacion de informacion de clientes existentes.
- Consulta de clientes por ID, nombre o correo.
- Eliminacion logica (cambio de estado a Inactivo).
- Listado de clientes activos.
- Tarjetas de metricas (totales y estados) calculadas desde la base de datos.

## Reglas de validacion implementadas
- Nombre del cliente:
	- Requiere al menos una letra.
	- Por defecto no permite numeros.
	- Permite numeros cuando se marca la opcion de empresa o razon social.
- Correo electronico:
	- Debe contener `@`.
	- Debe terminar en `.com` o `.cl`.
- Telefono:
	- Permite solo numeros, o formato con `+` al inicio.
	- Debe tener mas de 8 digitos.

## Arquitectura del proyecto
La aplicacion esta organizada por capas simples para separar responsabilidades:
- `app/`: configuracion visual general, header, layout y barra lateral.
- `views/`: vistas por caso de uso (registrar, actualizar, obtener, eliminar, listar).
- `components/`: componentes reutilizables de UI y formularios.
- `data/`: acceso a datos y logica de persistencia en SQLite.
- `styles/`: tema visual y estilos de la interfaz.

## Estructura de carpetas y archivos
```text
trabajo2_applicaciones_empresariales/
├─ README.md
└─ src/
	 ├─ main.py
	 ├─ requirements.txt
	 ├─ app/
	 │  ├─ header.py
	 │  ├─ layout.py
	 │  └─ sidebar.py
	 ├─ components/
	 │  ├─ client_card.py
	 │  ├─ client_form.py
	 │  ├─ client_table.py
	 │  └─ metrics.py
	 ├─ data/
	 │  └─ db.py
	 ├─ styles/
	 │  └─ theme.py
	 └─ views/
			├─ delete_view.py
			├─ get_view.py
			├─ list_view.py
			├─ register_view.py
			└─ update_view.py
```

## Flujo funcional resumido
1. `main.py` inicia la aplicacion, aplica tema y prepara base de datos.
2. Las vistas (`views/`) exponen cada operacion de negocio.
3. Los formularios en `components/client_form.py` validan entradas y ejecutan acciones CRUD.
4. La capa `data/db.py` centraliza consultas, busquedas, metricas y cambios de estado.

## Estado del proyecto
Version funcional con enfoque en gestion de clientes, separacion por modulos y persistencia local.