# Importing necessary libraries and modules
import streamlit as st  # Streamlit for building the web application
from chat_api_handler import ChatAPIHandler  # Custom module to handle chat API requests
from streamlit_mic_recorder import mic_recorder  # Custom module to record audio via microphone
from utils import get_timestamp, load_config, get_avatar  # Utility functions for timestamps, configuration loading, and avatars
from audio_handler import transcribe_audio  # Audio transcription function to convert speech to text
from pdf_handler import add_documents_to_db  # Function to handle and store PDF content in the database
from html_templates import css  # Custom CSS for styling the application
from database_operations import save_text_message, save_image_message, save_audio_message, load_messages, get_all_chat_history_ids, delete_chat_history, load_last_k_text_messages_ollama  # Functions for database operations like saving/loading messages
from utils import list_openai_models, list_ollama_models, command  # Functions to list OpenAI/Ollama models and process commands
import sqlite3  # SQLite for database management

# Function to toggle the PDF chat mode on (enables processing of PDFs)
def toggle_pdf_chat():
    st.session_state.pdf_chat = True  # Set PDF chat mode to true
    clear_cache()  # Clear cache to avoid conflicts with previous session data

# Function to turn off the PDF chat mode
def detoggle_pdf_chat():
    st.session_state.pdf_chat = False  # Set PDF chat mode to false

# Function to get a session key, either using a new session or an existing one
def get_session_key():
    # If the session key is "new_session", generate a new unique session key using timestamp
    if st.session_state.session_key == "new_session":
        st.session_state.new_session_key = get_timestamp()  # Generate a new session key
        return st.session_state.new_session_key  # Return the new session key
    return st.session_state.session_key  # Return the existing session key if it's not a new session

# Function to delete the chat session history for the current session key
def delete_chat_session_history():
    delete_chat_history(st.session_state.session_key)  # Delete session history from the database
    st.session_state.session_index_tracker = "new_session"  # Reset the session tracker to "new_session"

# Function to clear all cached resources to ensure fresh data
def clear_cache():
    st.cache_resource.clear()  # Clear cached resources (e.g., models, files)

# Function to list available model options based on the selected API (Ollama or OpenAI)
def list_model_options():
    if st.session_state.endpoint_to_use == "ollama":
        ollama_options = list_ollama_models()  # Fetch available models from Ollama
        if ollama_options == []:  # If no Ollama models are available
            st.warning("No ollama models available, please choose one from https://ollama.com/library and pull with /pull <model_name>")
        return ollama_options  # Return the list of available Ollama models
    elif st.session_state.endpoint_to_use == "openai":
        return list_openai_models()  # Fetch and return available OpenAI models

# Function to update the available models when the endpoint is changed
def update_model_options():
    st.session_state.model_options = list_model_options()  # Update the model options based on the selected API






# Main function to control the flow of the application
def main():
    st.title("Multimodal Local Chat App")  # Set the title of the application
    st.write(css, unsafe_allow_html=True)  # Apply custom CSS for styling the app

    # Initialize session state if not already done
    if "db_conn" not in st.session_state:
        st.session_state.session_key = "new_session"  # Set initial session key to "new_session"
        st.session_state.new_session_key = None  # Initialize a variable for new session key
        st.session_state.session_index_tracker = "new_session"  # Track the session index
        st.session_state.db_conn = sqlite3.connect(config["chat_sessions_database_path"], check_same_thread=False)  # Connect to the chat sessions database
        st.session_state.audio_uploader_key = 0  # Initialize the audio uploader key for handling uploads
        st.session_state.pdf_uploader_key = 1  # Initialize the PDF uploader key
        st.session_state.endpoint_to_use = "ollama"  # Default API endpoint is Ollama
        st.session_state.model_options = list_model_options()  # Get the list of models based on the selected API
        st.session_state.model_tracker = None  # Initialize model tracker

    # If a new session is started, update the session index tracker
    if st.session_state.session_key == "new_session" and st.session_state.new_session_key != None:
        st.session_state.session_index_tracker = st.session_state.new_session_key  # Update session index tracker with the new session key
        st.session_state.new_session_key = None  # Reset the new session key

    # Sidebar for selecting chat sessions and model options
    st.sidebar.title("Chat Sessions")
    chat_sessions = ["new_session"] + get_all_chat_history_ids()  # Get all chat history IDs and add the option for a new session
    index = chat_sessions.index(st.session_state.session_index_tracker)  # Find the index of the current session
    st.sidebar.selectbox("Select a chat session", chat_sessions, key="session_key", index=index)  # Dropdown to select session

    # Create two columns in the sidebar for selecting API and model
    api_col, model_col = st.sidebar.columns(2)
    api_col.selectbox(label="Select an API", options=["ollama", "openai"], key="endpoint_to_use", on_change=update_model_options)  # API selection dropdown
    model_col.selectbox(label="Select a Model", options=st.session_state.model_options, key="model_to_use")  # Model selection dropdown

    # File uploaders for PDF, image, and audio files
    uploaded_pdf = st.sidebar.file_uploader("Upload a pdf file", accept_multiple_files=True, key=st.session_state.pdf_uploader_key, type=["pdf"], on_change=toggle_pdf_chat)  # PDF uploader
    uploaded_image = st.sidebar.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"], on_change=detoggle_pdf_chat)  # Image uploader
    uploaded_audio = st.sidebar.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"], key=st.session_state.audio_uploader_key)  # Audio uploader

    # If PDF is uploaded, process it and add it to the database
    if uploaded_pdf:
        with st.spinner("Processing pdf..."):
            add_documents_to_db(uploaded_pdf)  # Add PDF to the database for processing
            st.session_state.pdf_uploader_key += 2  # Increment the PDF uploader key to trigger on_change event again

    # Handle voice recording from the microphone
    if voice_recording:
        transcribed_audio = transcribe_audio(voice_recording["bytes"])  # Transcribe the recorded audio to text
        llm_answer = ChatAPIHandler.chat(user_input=transcribed_audio, chat_history=load_last_k_text_messages_ollama(get_session_key(), config["chat_config"]["chat_memory_length"]))  # Get a response from the chatbot
        save_audio_message(get_session_key(), "user", voice_recording["bytes"])  # Save the recorded audio message to the database
        save_text_message(get_session_key(), "assistant", llm_answer)  # Save the assistant's response to the database
        st.session_state.audio_uploader_key += 2  # Increment the audio uploader key
        user_input = None  # Reset user input

    # If the user uploads an image, process the image and generate a response
    if uploaded_image:
        with st.spinner("Processing image..."):
            llm_answer = ChatAPIHandler.chat(user_input=user_input, chat_history=[], image=uploaded_image.getvalue())  # Get a response from the model based on the uploaded image
            save_text_message(get_session_key(), "user", user_input)  # Save user input
            save_image_message(get_session_key(), "user", uploaded_image.getvalue())  # Save the uploaded image
            save_text_message(get_session_key(), "assistant", llm_answer)  # Save the assistant's response
            user_input = None  # Reset user input

    # If the user uploads audio, transcribe and generate a response
    if uploaded_audio:
        transcribed_audio = transcribe_audio(uploaded_audio.getvalue())  # Transcribe the audio to text
        llm_answer = ChatAPIHandler.chat(user_input=user_input + "\n" + transcribed_audio, chat_history=[])  # Get a response from the model based on the transcribed audio
        save_text_message(get_session_key(), "user", user_input)  # Save user input
        save_audio_message(get_session_key(), "user", uploaded_audio.getvalue())  # Save the uploaded audio
        save_text_message(get_session_key(), "assistant", llm_answer)  # Save the assistant's response
        st.session_state.audio_uploader_key += 2  # Increment the audio uploader key
        user_input = None  # Reset user input

    # If the user types input in the chat box
    if user_input:
        llm_answer = ChatAPIHandler.chat(user_input=user_input, chat_history=load_last_k_text_messages_ollama(get_session_key(), config["chat_config"]["chat_memory_length"]))  # Get a response from the chatbot
        save_text_message(get_session_key(), "user", user_input)  # Save user input
        save_text_message(get_session_key(), "assistant", llm_answer)  # Save the assistant's response
        user_input = None  # Reset user input

    # Display the chat history
    if (st.session_state.session_key != "new_session") != (st.session_state.new_session_key != None):
        with chat_container:
            chat_history_messages = load_messages(get_session_key())  # Load the chat history for the current session

        # Display each message in the chat history
        for message in chat_history_messages:
            with st.chat_message(name=message["sender_type"], avatar=get_avatar(message["sender_type"])):
                if message["message_type"] == "text":
                    st.write(message["content"])  # Display text message
                if message["message_type"] == "image":
                    st.image(message["content"])  # Display image message
                if message["message_type"] == "audio":
                    st.audio(message["content"], format="audio/wav")  # Display audio message

    # If a new session is started, rerun the application to reflect changes
    if (st.session_state.session_key == "new_session") and (st.session_state.new_session_key != None):
        st.rerun()  # Restart the application to handle the new
















####################################################################################################################################


# Import necessary libraries
from transformers import pipeline  # For automatic speech recognition (ASR) using Hugging Face models
import librosa  # For audio processing (loading and manipulation)
import io  # For working with in-memory byte data
from utils import load_config, timeit  # Utility functions (load config and timing)
import os  # For interacting with the operating system (e.g., file removal)
import subprocess  # For running system commands like FFmpeg

# Load the configuration file
config = load_config()

def convert_webm_to_wav_ffmpeg(audio_bytes):
    # Save the WebM bytes (audio) to a temporary WebM file
    with open("temp_audio.webm", "wb") as f:
        f.write(audio_bytes)

    # Use FFmpeg (a command-line tool) to convert the WebM file to WAV format
    result = subprocess.run(
        ["ffmpeg", "-fflags", "+igndts", "-i", "temp_audio.webm", "-c:a", "pcm_s16le", "temp_audio.wav"], 
        capture_output=True
    )

    # Check if FFmpeg conversion was successful (return code 0 means success)
    if result.returncode != 0:
        # Print any errors if the conversion failed
        print(result.stderr.decode())
        raise RuntimeError("FFmpeg failed to convert WebM to WAV")

    # Read the WAV file back into memory (as bytes)
    with open("temp_audio.wav", "rb") as f:
        wav_data = f.read()

    # Convert the WAV data into a BytesIO object for in-memory handling
    wav_io = io.BytesIO(wav_data)

    # Clean up: remove the temporary WebM and WAV files
    os.remove("temp_audio.webm")
    os.remove("temp_audio.wav")

    # Return the WAV audio a
