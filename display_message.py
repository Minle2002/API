import streamlit as st

from data import DataController

# Function to display messages
def display_messages():
    print('displaying message for ', DataController.get_program_state())
    for msg in DataController.get_messages():
        if msg['sender'].lower() == "you":
            st.markdown(
                f'<div style="background-color: green; padding: 10px 20px; border-radius: 10px; color: white; text-align: right; width: 75%; float: right; clear: both; border-bottom-right-radius: 0; margin: 10px 0 0px auto;">{msg["message"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div style="background-color: blue; padding: 10px 20px; border-radius: 10px; color: white; text-align: left; width: 75%; float: left; clear: both; border-bottom-left-radius: 0; margin: 10px auto 0px 0;">{msg["sender"]}: {msg["message"]}</div>',
                unsafe_allow_html=True
            )
