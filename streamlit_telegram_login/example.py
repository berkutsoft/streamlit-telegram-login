import streamlit as st
import os

from streamlit_telegram_login import TelegramLoginWidgetComponent
from streamlit_telegram_login.helpers import YamlConfig

parent_dir = os.path.dirname(os.path.abspath(__file__))

config = YamlConfig(f"{parent_dir}/local_config.yaml")
telegram_login = TelegramLoginWidgetComponent(**config.config)
st.write("## Example")
if not st.session_state["username"]:
    value = telegram_login.button
    if value:
        st.write(value)
else:
    st.write(telegram_login.get_session)

    clicked = st.button("Clear cookies")
    if clicked:
        telegram_login.clear_session()
        st.write("Cookies have been successfully cleared")
