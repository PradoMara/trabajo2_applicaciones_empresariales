from app.sidebar import render_sidebar
from components.client_table import render_clients_table


def render_list_view() -> None:
	filters = render_sidebar()
	render_clients_table(filters)
