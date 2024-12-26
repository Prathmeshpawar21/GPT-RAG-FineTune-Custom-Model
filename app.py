# __python_version = 3.12.0
import base64
import os
import streamlit as st
from dotenv import load_dotenv 
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFaceEndpoint
from htmlTemplates import css, bot_template, user_template

# Function to extract text from PDFs
def get_pdf_text(pdfs):
    text = ""
    try:
        for pdf in pdfs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        if not text:
            return None  # Return None if no text extracted
        return text
    except Exception as e:
        st.error("Error extracting text from uploaded files.")
        st.error("Please upload valid PDF files.")
        return None

# Function to split raw text into chunks
def get_text_chunks(raw_text):
    if not raw_text:
        return None  # Return None if no raw text is provided
    try:
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
        chunks = text_splitter.split_text(raw_text)
        if not chunks:
            return None
        return chunks
    except Exception as e:
        return None

# Function to create a vector store from text chunks
def get_vector_store(text_chunks):
    if not text_chunks:
        return None
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(text_chunks, embeddings)
        return vector_store
    except Exception as e:
        return None

# Function to create the conversational retrieval chain
def get_conversation_chain(vector_store):
    try:
        load_dotenv()
        API_TOKEN = os.getenv("API_KEY")
        if not API_TOKEN:
            st.error("Missing API key. Please check your environment variables.")
            return None
        
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            max_length=128,
            temperature=0.5,
            huggingfacehub_api_token=API_TOKEN
        )

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except Exception as e:
        st.error("Error creating the conversation chain.")
        return None

# Function to handle user input
def handle_userinput(user_question):
    try:
        if st.session_state.conversation is None:
            st.warning("Please upload and process documents first.")
            return
        response = st.session_state.conversation.invoke({'question': user_question})
        st.session_state.chat_history = response.get('chat_history', [])
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    except Exception:
        st.error("Error during conversation. Please try again.")

# Main function
def main():
    st.set_page_config(page_title="PDF QnA", page_icon="📜", layout="wide")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with Multiple PDF's :books:")
    user_question = st.text_input("Ask a question")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        pdfs = st.file_uploader(
            "Upload your PDF's here and click on 'process'",
            accept_multiple_files=True,
            type=["pdf"]
        )


        if st.button("Process"):
            with st.spinner("Processing..."):
                if not pdfs:
                    st.error("Please upload at least one PDF file.")
                    return

                raw_text = get_pdf_text(pdfs)
                if not raw_text:
                    st.error("No text could be extracted from the uploaded PDFs. Please check the files.")
                    return

                text_chunks = get_text_chunks(raw_text)
                if not text_chunks:
                    st.error("Failed to split text into chunks. Please try again.")
                    return

                vector_store = get_vector_store(text_chunks)
                if not vector_store:
                    st.error("Failed to create a vector store. Please try again.")
                    return

                conversation_chain = get_conversation_chain(vector_store)
                if conversation_chain is None:
                    st.error("Failed to initialize the conversation chain. Please try again.")
                    return

                st.session_state.conversation = conversation_chain
                st.success("Documents processed successfully!")

if __name__ == '__main__':
    main()

