import google.generativeai as genai
import streamlit as st
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv


# Load the API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


st.set_page_config(
    page_title="Heathmate.ai",
    page_icon="💬",
    layout="centered"
)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

bot_starting_messages = {
    "AI Cardiologist (Heart)": "Hello, I'm your Heart Specialist Bot. I'm here to provide you with expert advice and answer any questions you have about your heart health.",
    "AI Orthopedic Specialist (Bones)": "Hello, I'm your Bones Specialist Bot. I'm here to assist you with information and guidance on maintaining healthy bones and addressing any bone-related concerns.",
    "AI Pulmonologist (Lungs)": "Hello, I'm your Lungs Specialist Bot. I'm ready to help you with any questions or advice regarding your lung health and respiratory system."
}
    

st.title("🤖 AI Heathmate")
        
    # Create a selection box for patient scenarios
selected_scenario = st.selectbox("Select a Healthmate:", list(bot_starting_messages.keys()))

    # Display the selected scenario
st.write("**Selected Healthmate:**", bot_starting_messages[selected_scenario])

 # display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


    


def read_pdf(pdf_path):
    text = ""
    pdf_read = PdfReader(pdf_path)
    for page in pdf_read.pages:
        text += page.extract_text()
    return text

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
instruction = """
You are a knowledgeable cardiologist specializing in heart diseases and diagnosis. 
Start each conversation by greeting the user politely. 
If the patient asks a query, follow up with relevant questions to gather more details. 
Provide concise, conversational responses, avoiding unnecessary details. 
Address all heart-related questions thoroughly. 
For non-cardiology questions, give a brief response and gently remind the user of your expertise in heart-related issues, inviting them to ask any heart-related questions they may have.
"""

# input field for user's message
user_query = st.chat_input("Message Bot")

if user_query:
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
        
    response = chat.send_message(user_query)
    # st.write(f"Bot: {response.text}")
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})

    with st.chat_message("assistant"):
        st.markdown(response.text)
