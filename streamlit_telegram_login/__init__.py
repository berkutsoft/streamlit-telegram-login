import os
from datetime import datetime, timedelta
from typing import Optional, Union
import streamlit.components.v1 as components
import extra_streamlit_components as stx
import jwt
import streamlit as st
from jwt import DecodeError

_RELEASE = False
# comment out the following line to use the local dev server
# use streamlit run __init__.py to run the local dev server
_RELEASE = True

parent_dir = os.path.dirname(os.path.abspath(__file__))

if not _RELEASE:
    _telegram_login_button = components.declare_component(
        "streamlit_telegram_login",
        url="http://localhost:3000",
    )
else:
    frontend_dir = os.path.join(parent_dir, "frontend")
    _telegram_login_button = components.declare_component("streamlit_telegram_login", path=frontend_dir)


class TelegramLoginWidgetComponent:
    """
    Widget component for login via Telegram.

    Attributes:
      bot_username: str - bot name in Telegram
      button_style: str - button style (large, normal)
      userpic: bool - whether to show user's avatar
      corner_radius: Optional[int] - radius of button corners rounding
      request_access: bool - whether to request access to the account
      expiry_days: float - expiration date of the cookie in days
      cookie_key: str - cookie storage key
      cookie_manager: cookieManager: cookieManager - manager for working with cookies
      session_keys: tuple - user session keys
      cookie_name: str - cookie name
      key: str - key for JWT token encoding
      token: str - current JWT token
      session_data: dict - user session data
    """
    def __init__(
        self,
        bot_username: str,
        *,
        button_style: str = "large",
        userpic: bool = True,
        corner_radius: Optional[int] = None,
        request_access: bool = True,
        expiry_days: float = 30.0,
        cookie_key: str = "init"
    ):
        """
        Initializes the Telegram Login Widget Component.

        Args:
            bot_username: str - Username of the Telegram bot
            button_style: str - Style of the login button (large, medium, small)
            userpic: bool - Whether to show user profile picture
            corner_radius: Optional[int] - Corner radius of the button or None for default
            request_access: bool - Whether to request account access
            expiry_days: float - Cookie expiry days
            cookie_key: str - Key to use for cookie storage
        """
        self.bot_username = bot_username
        self.button_style = button_style
        self.userpic = userpic
        self.corner_radius = corner_radius
        self.request_access = request_access
        self.cookie_expiry_days = expiry_days
        self.cookie_key = cookie_key
        self.cookie_manager = stx.CookieManager(key=cookie_key)
        self.session_keys = ("id", "first_name", "username", "photo_url", "auth_date", "hash", "exp_date")
        self.cookie_name = "Berkut11"
        self.key = "ABCBCA1"
        self.token = self.cookie_manager.get(self.cookie_name)
        self.session_data = self._token_decode(self.token)
        self._init_session_state()

    def _init_session_state(self):
        """Initializes the state of the session."""
        if token := st.session_state.get(self.cookie_key) and st.session_state[self.cookie_key].get(self.cookie_name):
            if session_data := self._token_decode(token):
                st.session_state.update(session_data)
        else:
            for key in self.session_keys:
                if key not in st.session_state:
                    st.session_state[key] = self.session_data.get(key)

    @property
    def button(self):
        """"
        Returns the login button widget. 
        Also, if the data came after authorization, we save them in the session
        """""
        _button = _telegram_login_button(
            bot_username=self.bot_username,
            button_style=self.button_style,
            userpic=self.userpic,
            corner_radius=self.corner_radius,
            request_access=self.request_access,
        )
        if _button:
            self.set_session(**_button)
        return _button

    def _token_encode(self, data: dict) -> str:
        """Encodes data into JWT token."""
        return jwt.encode(data, self.key, algorithm='HS256')

    def _token_decode(self, token: Union[str, bytes]) -> dict:
        """Decodes JWT token into data."""
        try:
            return jwt.decode(token, self.key, algorithms=['HS256'])
        except DecodeError:
            return {}

    def _set_exp_date(self) -> float:
        """Sets the expiration date of the session"""
        return (datetime.now() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def set_session(self, **kwargs):
        """Set Session Data"""
        session_data = {key: val for key, val in kwargs.items() if key in self.session_keys}
        session_data["exp_date"] = self._set_exp_date()
        st.session_state.update(session_data)
        self.cookie_manager.set(
            self.cookie_name,
            self._token_encode(session_data),
            key=self.__class__.__name__,
            expires_at=datetime.now() + timedelta(seconds=self.cookie_expiry_days)
        )

    @property
    def get_session(self) -> dict:
        """Returns session data"""
        return {key: st.session_state[key] for key in self.session_keys}

    def clear_session(self):
        """Clears session data"""
        for key in self.session_keys:
            if key in st.session_state:
                del st.session_state[key]
        if self.cookie_manager.get(self.cookie_name):
            self.cookie_manager.delete(self.cookie_name)
