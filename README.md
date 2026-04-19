# Gestión de Clientes - Aplicaciones Empresariales

## Descripción General
Aplicación web profesional construida con **Streamlit** para la gestión integral de clientes mediante operaciones CRUD avanzadas y análisis de datos en tiempo real.

El proyecto utiliza un motor de persistencia real basado en **SQLite**, garantizando la integridad de los datos, trazabilidad mediante auditoría y una experiencia de usuario (UX) moderna y fluida.

## Características Principales (Alcance Final)
- **Dashboard Estadístico:** Visualización interactiva con gráficos de dona y barras (Plotly) que muestran la distribución de la cartera por estado y tipo de cliente al iniciar la aplicación.
- **Gestión Completa de Clientes:**
    - **Registro:** Con ID autoincremental y validaciones estrictas.
    - **Actualización:** Modificación de datos existentes con registro automático de motivos de cambio.
    - **Obtención:** Búsqueda rápida por ID, nombre o correo electrónico.
    - **Desactivación:** Eliminación lógica de clientes (paso a estado Inactivo) conservando el registro histórico.
    - **Eliminación Física:** Nueva funcionalidad para borrado definitivo de registros de la base de datos con confirmación de seguridad.
    - **Reactivación:** Permite devolver al estado "Activo" a clientes previamente desactivados.
- **Sistema de Auditoría:** Historial detallado de cambios por cliente, permitiendo consultar qué se cambió, quién (simulado) y por qué.
- **Validaciones en Tiempo Real:** Verificación instantánea de disponibilidad de correo, nombre y teléfono mientras el usuario escribe, evitando errores al final del proceso.

## Reglas de Validación y Seguridad
- **Validación de Identidad:**
- **Nombre:** Mínimo 3 caracteres. Permite números solo si se marca como "Empresa/Razón Social". Bloqueo de nombres duplicados en tiempo real.
- **Contacto:**
- **Correo Electrónico:** Validación de formato estándar. Verificación de duplicados instantánea para evitar registros redundantes.
- **Teléfono:** Solo números o prefijo `+`. Mínimo 8 dígitos. Verificación de duplicados ignorando espacios.
- **Seguridad de Datos:** Confirmación obligatoria mediante casilla de verificación para la eliminación permanente de registros.

## Arquitectura del Proyecto
La aplicación sigue un enfoque modular y escalable:
- `app/`: Configuración visual general, configuración de página, header y layout.
- `views/`: Vistas de usuario organizadas por pestañas (Estadísticas, Registro, Actualización, Búsqueda, Desactivación, Auditoría, etc.).
- `components/`: Componentes reutilizables de UI, tarjetas de clientes (`client_card.py`) y formularios complejos (`client_form.py`).
- `data/`: Capa de persistencia en SQLite (`db.py`) que maneja la lógica de negocio, auditoría y consultas estadísticas.
- `styles/`: Gestión de la apariencia visual y temas personalizados.

## Estructura de Directorios
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
		├─ stats_view.py       
		├─ register_view.py
		├─ update_view.py
		├─ get_view.py
		├─ deactivate_view.py  
		├─ reactivate_view.py
		├─ delete_view.py      
		├─ audit_view.py       
		└─ list_view.py
```

## Requisitos e Instalación
El proyecto requiere Python 3.x y las dependencias listadas en `requirements.txt`.

1.  Crear entorno virtual: `python -m venv venv`
2.  Activar entorno: `source venv/bin/activate` (Linux/Mac) o `.\venv\Scripts\activate` (Windows)
3.  Instalar dependencias: `pip install -r src/requirements.txt`
4.  Ejecutar aplicación: `streamlit run src/main.py`

## Estado del Proyecto
**Finalizado.** El sistema cumple con todos los requerimientos de una aplicación empresarial: persistencia robusta, validaciones preventivas, análisis visual de datos y auditoría de procesos.
