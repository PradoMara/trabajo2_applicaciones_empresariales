import streamlit as st
import pandas as pd
import plotly.express as px
from data.db import get_metrics, get_client_stats


def render_metrics() -> None:
	# Métricas Numéricas
	metrics = get_metrics()
	col1, col2, col3, col4 = st.columns(4)
	col1.metric("Total Clientes", str(metrics.get("Clientes", 0)))
	col2.metric("Activos", str(metrics.get("Activos", 0)), delta_color="normal")
	col3.metric("Pendientes", str(metrics.get("Pendientes", 0)))
	col4.metric("Inactivos", str(metrics.get("Inactivos", 0)), delta_color="inverse")

	st.divider()

	# Gráficos de Dashboard
	stats = get_client_stats()
	
	if metrics.get("Clientes", 0) > 0:
		g1, g2 = st.columns(2)
		
		with g1:
			st.subheader("Distribución por Estado")
			df_status = pd.DataFrame(stats["status"])
			if not df_status.empty:
				fig_status = px.pie(
					df_status, 
					names="label", 
					values="value", 
					hole=0.4,
					color="label",
					color_discrete_map={
						"Activo": "#2ecc71", 
						"Pendiente": "#f1c40f", 
						"Inactivo": "#e74c3c"
					}
				)
				fig_status.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
				st.plotly_chart(fig_status, use_container_width=True)
		
		with g2:
			st.subheader("Clientes por Tipo")
			df_types = pd.DataFrame(stats["types"])
			if not df_types.empty:
				fig_types = px.bar(
					df_types, 
					x="label", 
					y="value",
					color="label",
					color_discrete_map={
						"Nuevo": "#3498db",      # Azul claro
						"Recurrente": "#2980b9",  # Azul oscuro
						"VIP": "#f39c12"         # Naranja/Oro
					},
					labels={"label": "Tipo", "value": "Cantidad"},
					text_auto=True
				)
				fig_types.update_layout(
					margin=dict(t=0, b=0, l=0, r=0), 
					height=300,
					showlegend=False
				)
				st.plotly_chart(fig_types, use_container_width=True)
	else:
		st.info("Aún no hay datos suficientes para generar gráficos de análisis.")
