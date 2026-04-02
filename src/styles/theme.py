import streamlit as st


def apply_theme() -> None:
	st.markdown(
		"""
		<style>
		.block-title {
			font-size: 1.1rem;
			font-weight: 700;
			margin-bottom: 0.4rem;
		}
		.card {
			padding: 1rem;
			border-radius: 0.8rem;
			border: 1px solid rgba(255,255,255,0.12);
			background: rgba(255,255,255,0.03);
		}
		</style>
		""",
		unsafe_allow_html=True,
	)
