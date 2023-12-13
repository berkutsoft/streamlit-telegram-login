# streamlit-telegram-login

Streamlit component that implements a telegram bot widget

## Installation instructions 

```sh
pip install streamlit-telegram-login
```

## Usage instructions

```python
import streamlit as st

from streamlit_telegram_login import streamlit_telegram_login

value = streamlit_telegram_login()

st.write(value)
