import streamlit as st
import logging as log
import time
from api.service import call_chat_api
from api.service import get_access_token  
from config.loggingconfig import logging_setup
from pathlib import Path

# Apply custom logging config
log.getLogger("streamlit").setLevel(log.ERROR)
log.config.dictConfig(logging_setup)
log = log.getLogger(__name__)
image_path = Path(__file__).parent / "images" / "WCLOGO.jpg"
title_image_path = Path(__file__).parent / "images" / "TITLE_LOGO.png"
st.set_page_config(
    page_title="AI Help - Windchill",
    page_icon=image_path,
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://www.cognizant.com"
    }
)

def buildChatBot():
    try:
        st.title("AI Help - Windchill")       
        log.info("buildChatBot() invoked")
        with st.chat_message(name="assistant", avatar=image_path):
            st.write("I am a Chatbot powered by C&CM System Team, how can I help you?")

        # Initialize chat history to recall past messsages
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        #Display all the chat history from session_state
        for msg in st.session_state.chat_history:
            avatarPath = image_path if msg['role'] != 'user' else None
            with st.chat_message(msg["role"], avatar=avatarPath):
                st.markdown(msg["content"])

        #Consume user input
        user_input = st.chat_input("Prompt here!")   
        if user_input is not None:
            log.info("User input: "+user_input)

            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.chat_history.append({"role":"user", "content":user_input})      
            with st.spinner("Thinking.."): 
                access_token = get_access_token()

            if access_token is None:
                return
            # Add user message to chat history
            # Call Philips chatbot API
            with st.spinner("Thinking.."):   
                response = call_chat_api(user_input, access_token)

            if response is None:
                return
            
            responseContent = response["content"]
            responseUrls = response["refUrls"]

            #Build chatbot response here
            with st.chat_message("assistant", avatar=image_path):
                placeholder = st.empty()
                placeholder.markdown("|")
                time.sleep(0.9)
                final_response=""
                for response_token in responseContent:
                    final_response+=response_token
                    placeholder.markdown(final_response+"|")
                    time.sleep(0.001)
                placeholder.write(final_response+"  \n\nSources:")

                #Iterate over reference Urls, and display them in the expanders
                log.info("Source Urls: "+str(responseUrls))
                for index, url in enumerate(responseUrls):
                    with st.expander(str(index+1)+":"):
                        st.write(url)

                #Save the bot's reply in the chat history
                st.session_state.chat_history.append({"role": "assistant", "content": final_response})
                
    except Exception as e:
        log.error(e)
        with st.chat_message("assistant"):
            st.write(e)
        st.session_state.chat_history.append({"role": "assistant", "content": e})
        return None
    
#Chatbot execution starts here
buildChatBot()

