import os
from datetime import datetime, timedelta
from typing import Optional
import streamlit.components.v1 as components


_RELEASE = __name__ != "__main__"
# comment out the following line to use the local dev server
# use streamlit run __init__.py to run the local dev server

parent_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(parent_dir, "frontend")
_telegram_login_button = components.declare_component("streamlit_telegram_login", path=frontend_dir)


class TelegramLoginWidgetComponent:
    def __init__(
        self,
        bot_username: str,
        *,
        button_style: str = "large",
        userpic: bool = True,
        corner_radius: Optional[int] = None,
        request_access: bool = True,
        cookie_expiry_days: float = 30.0
    ):
        self.bot_username = bot_username
        self.button_style = button_style
        self.userpic = userpic
        self.corner_radius = corner_radius
        self.request_access = request_access
        self.cookie_expiry_days = cookie_expiry_days
        self.exp_date = self._set_exp_date()
        self.session_keys = ("id", "first_name", "username", "photo_url", "auth_date", "hash", "exp_date")
        if st.session_state.get("exp_date") and st.session_state["exp_date"] > datetime.utcnow().timestamp():
            self.clear_session()

    @property
    def button(self):
        _button = _telegram_login_button(
            bot_username=self.bot_username,
            button_style=self.button_style,
            userpic=self.userpic,
            corner_radius=self.corner_radius,
            request_access=self.request_access,
        )
        return _button

    def _set_exp_date(self) -> int:
        return int((datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp())

    def set_session(self, **kwargs):
        for key in kwargs:
            if key in self.session_keys:
                st.session_state[key] = kwargs[key]
        st.session_state["exp_date"] = self.exp_date

    @property
    def get_session(self) -> Optional[dict]:
        result = dict.fromkeys(self.session_keys)
        for key in self.session_keys:
            if key not in st.session_state:
                return None
            result[key] = st.session_state[key]
        return result
    
    def clear_session(self):
        for key in self.session_keys:
            if key in st.session_state:
                del st.session_state[key]


if not _RELEASE:
    import streamlit as st
    from streamlit_telegram_login.helpers import YamlConfig

    config = YamlConfig(f"{parent_dir}/local_config.yaml")
    # widget_settings = dict.fromkeys(widget_settings)
    telegram_login = TelegramLoginWidgetComponent(**config.config)
    st.write("## Example")
    # telegram_login.clear_session()
    value = telegram_login.get_session or telegram_login.button
    if value:
        st.write(value)
        telegram_login.set_session(**value)

