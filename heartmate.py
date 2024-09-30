from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Define the initial prompt to set the chatbot's behavior
# initial_prompt = (
#     "You are a highly knowledgeable and experienced cardiologist."
#     "Your primary role is to answer all queries related to the heart in a crisp and concise manner."
#     "Provide accurate and precise information about heart health, heart diseases, treatments, symptoms, prevention, and any other heart-related topics." 
#     "Avoid answering any general queries that are not related to cardiology."
#     "Your responses should be clear, direct, and focused on delivering the necessary information efficiently."
#     "Always maintain a professional and helpful tone."
#     "NOTE: Do not answer to any general questions apart from the mentioned task."
# )

initial_prompt = (
"You are a knowledgeable and concise cardiologist."
"Your primary role is to answer all heart-related queries asked by the user in a clear and accurate manner."
"You should not answer any general queries that are not related to the heart."
"To ensure you provide the best possible response, ask follow-up questions to understand more about the user's query."
"Keep your answers crisp and to the point, focusing on providing valuable information and guidance about heart health."
"Remember, you are here to help users with their heart-related concerns and provide them with precise and helpful answers."
)

# Initialize our Streamlit app
st.set_page_config(page_title="Heartmate.ai", page_icon="💬")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [{"role": "assistant", "content": initial_prompt}]

# Streamlit page title
st.title("Heartmate.ai👨‍⚕️")

st.markdown("<h5 style='text-align: left; color: white;'>I'm HeartMate❤️, your expert cardiologist here to answer all your heart-related queries. Ask me anything about heart health!</h5>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state['chat_history'][1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_input = st.chat_input("Ask Heartmate!")

if user_input:
    # Add user's message to chat history and display it
    st.chat_message("user").markdown(user_input)
    st.session_state['chat_history'].append({"role": "user", "content": user_input})

    # Prepare the conversation history
    conversation_history = [entry['content'] for entry in st.session_state['chat_history']]
    combined_input = "\n".join(conversation_history)

    # Get the response from Gemini API
    response = chat.send_message(combined_input, stream=True)
    
    response_text = ""
    for chunk in response:
        response_text += chunk.text

    # Add the bot response to the chat history
    st.session_state['chat_history'].append({"role": "assistant", "content": response_text})

    # Display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(response_text)