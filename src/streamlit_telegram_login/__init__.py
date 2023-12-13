import os
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
        request_access: bool = True
    ):
        self.bot_username = bot_username
        self.button_style = button_style
        self.userpic = userpic
        self.corner_radius = corner_radius
        self.request_access = request_access
        self.session_keys = ("id", "first_name", "username", "photo_url", "auth_date", "hash")


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

    def set_session(self, **kwargs):
        for key in kwargs:
            if key in self.session_keys:
                st.session_state[key] = kwargs[key]

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
    import yaml
    with open(f'{parent_dir}/config.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    widget_settings = config.get('witget_settings')
    # widget_settings = dict.fromkeys(widget_settings)
    telegram_login = TelegramLoginWidgetComponent(**widget_settings)
    st.write("## Example")
    # telegram_login.clear_session()
    value = telegram_login.get_session or telegram_login.button
    if value:
        st.write(value)
        telegram_login.set_session(**value)

