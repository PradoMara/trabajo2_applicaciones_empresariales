from components.client_table import render_clients_table


def render_list_view(filters: dict[str, str]) -> None:
	render_clients_table(filters)
