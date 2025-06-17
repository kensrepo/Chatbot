import streamlit as st
import requests
import time
import logging as log
from config.chatbotconfig import buildChatBotConfig

req_env_variables = buildChatBotConfig()

TOKEN_URL = req_env_variables.get('TOKEN_URL')
LLM_API_URL = req_env_variables.get('LLM_API_URL')
ACCESS_TOKEN_PAYLOAD = req_env_variables.get('ACCESS_TOKEN_HEADERS')
LLM_API_REQ_BODY = req_env_variables.get('LLM_API_REQ_BODY')
LLM_API_HEADERS = req_env_variables.get('LLM_API_HEADERS')
LLM_API_TIMEOUT = req_env_variables.get('LLM_API_TIMEOUT')
TOKEN_URL_TIMEOUT = req_env_variables.get('TOKEN_URL_TIMEOUT')


def get_access_token():
    if 'token_info' not in st.session_state:
        st.session_state.token_info = {
        "access_token": None,
        "expires_at": 0  
    }
    token_info = st.session_state.token_info
    now = time.time()
    if token_info["access_token"] and token_info["expires_at"] > now + 30:
        # Return cached token if still valid (with 30s buffer)
        return token_info["access_token"]
    
    log.info("payload for requesting access token: "+str(ACCESS_TOKEN_PAYLOAD))
    try:
        response = requests.post(TOKEN_URL, data=ACCESS_TOKEN_PAYLOAD, timeout=TOKEN_URL_TIMEOUT)
    except requests.exceptions.Timeout as e:
        with st.chat_message("assistant"):
            st.write(str(e)+' Please Contact Adminstrator')
        st.session_state.chat_history.append({"role": "assistant", "content": e})
    except Exception as e:
        log.error(e)
        with st.chat_message("assistant"):
            st.write(e)
        st.session_state.chat_history.append({"role": "assistant", "content": e})
        return None
    log.info("Response from: "+TOKEN_URL+" "+str(response.status_code))

    token_json = response.json()
    access_token = token_json["access_token"]
    expires_in = token_json.get("expires_in", 3600)  # seconds

    # Cache token and expiry time
    st.session_state.token_info["access_token"] = access_token
    st.session_state.token_info["expires_at"] = now + expires_in

    return access_token


#This method send POST request to API_URL with required access token and other params
def call_chat_api(user_input, access_token):
    log.info("call_chat_api() invoked")
    first_key = list(LLM_API_HEADERS.keys())[0]
    LLM_API_HEADERS[first_key] = f"Bearer {access_token}"
    LLM_API_REQ_BODY['input'] = user_input
    try:
        resp = requests.post(LLM_API_URL, headers=LLM_API_HEADERS, json=LLM_API_REQ_BODY, timeout=LLM_API_TIMEOUT)
        log.info("Response from "+LLM_API_URL+" "+str(resp))
        resp.raise_for_status()
        return resp.json()
    
    except requests.exceptions.Timeout as e:
        with st.chat_message("assistant"):
            st.write(str(e)+' Please Contact Adminstrator')
        st.session_state.chat_history.append({"role": "assistant", "content": e})

    except Exception as e:
        log.error(e)
        with st.chat_message("assistant"):
            st.write(e)
        st.session_state.chat_history.append({"role": "assistant", "content": e})
        return None