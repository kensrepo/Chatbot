import streamlit as st
import logging as log
import os
import toml
from pathlib import Path
from dotenv import load_dotenv
#Class level env variables
def buildChatBotConfig():
    filepath = Path(__file__).parent.parent.parent / ".streamlit" / "config.toml"
    config = toml.load(filepath)
    required_config_vars = {
        "TOKEN_URL":config['ACCESS_TOKEN_URL']['URL'],
        "ACCESS_TOKEN_HEADERS":config['ACCESS_TOKEN_HEADERS'],
        "LLM_API_URL":config['LLM_API']['URL'], 
        "LLM_API_REQ_BODY":config['LLM_API_REQ_BODY'], 
        "LLM_API_HEADERS":config['LLM_API_HEADERS'], 
        "LOG_LEVEL":config['LOGGING']['LOG_LEVEL'],
        "LOG_DIR":config['LOGGING']['LOG_DIR'],
        "TOKEN_URL_TIMEOUT":config['TOKEN_URL_TIMEOUT']['value'],
        "LLM_API_TIMEOUT":config['LLM_API_TIMEOUT']['value']
        }
    
    
    # Cache token and expiry in session state
    if "token_info" not in st.session_state:
        st.session_state.token_info = {
            "access_token": None,
            "expires_at": 0  # epoch timestamp when token expires
        }   
    return required_config_vars
        





