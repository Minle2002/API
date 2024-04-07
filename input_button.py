import symptoms as sym
import streamlit as st
from datetime import datetime


def display_2_options(names, callbacks, key_suffix=None):
    col1, col2 = st.columns(2)
    # Generate a unique suffix if none is provided
    if key_suffix is None:
        key_suffix = datetime.now().strftime("%Y%m%d%H%M%S%f")
        
    with col1:
        st.button(names[0], on_click=callbacks[0], key=f"{names[0]}_btn_{key_suffix}")
    with col2:
        st.button(names[1], on_click=callbacks[1], key=f"{names[1]}_btn_{key_suffix}")



def display_input_field(label, on_submit, key_suffix=""):
    cols = st.columns([4, 1])  # Divide the row into a 4:1 ratio
    with cols[0]:
        message = st.text_input(label, key=f"{label}_text_{key_suffix}", help="Message")

    with cols[1]:
        st.button("Send", on_click=lambda: on_submit(message), key=f"{label}_send_{key_suffix}")


def symptom_popup(label,symptoms,on_submit):
    selected_value = ""
    with st.form(key= label):
        selected_value = st.selectbox("Select a symptom", symptoms)
        submit = st.form_submit_button(label='Submit')
    if submit:
        on_submit(selected_value)

def add_remove_symptom_popup(symptoms,selected_symptoms,on_add, on_remove):
    add = ""
    sub = ""
    col1, col2 = st.columns(2)
    print(len(symptoms),len(selected_symptoms))
    with col1:
        with st.form(key= "Add Symptom"):
            add = st.selectbox("Select a symptom to add", sym.model_symptoms)
            add_btn = st.form_submit_button(label='Submit')
            
    with col2:
        with st.form(key= "Remove Symptom"):
            sub = st.selectbox("Select a symptom to remove", selected_symptoms)
            sub_btn = st.form_submit_button(label='Submit')

    if add_btn:
        on_add(add)
    if sub_btn:
        on_remove(sub)
        
def add_remove_detect_symptom_popup(symptoms,selected_symptoms,on_add, on_remove,on_detect):
    print("we get call for add_remove_detect")
    add_remove_symptom_popup(symptoms,selected_symptoms,on_add, on_remove)
    detect = st.button("Detect Disease")
    if detect:
        on_detect()