import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from PyPDF2 import PdfReader
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key not set up! Please set it in the environment.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Extract text from different file types
def extract_text_from_files(files):
    text_list = []
    
    for file in files:
        try:
            file_extension = file.name.split(".")[-1].lower()
            
            if file_extension == "pdf":
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text_list.append(extracted_text)
            
            elif file_extension == "txt":
                text_list.append(file.getvalue().decode("utf-8"))
            
            elif file_extension == "csv":
                df = pd.read_csv(file)
                text_list.append(df.to_string(index=False))
            
            elif file_extension in ["xls", "xlsx"]:
                df = pd.read_excel(file)
                text_list.append(df.to_string(index=False))
            
            else:
                st.warning(f"Unsupported file type: {file.name}")
        
        except Exception as e:
            st.error(f"Error reading file {file.name}: {str(e)}")

    return "\n".join(text_list) if text_list else None

# Split text into chunks
def split_text_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

# Generate vector store with embeddings
def create_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Create conversational chain
def get_conversational_chain():
    prompt_template = """
    Answer the question as accurately as possible based on the provided context. 
    If the answer is not available in the context, respond with "Answer not available in the context."

    Context: {context}
    Question: {question}
    Answer:
    """
    try:
        model = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-latest", client=genai, temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        return load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    except Exception as e:
        st.error(f"Error initializing language model: {str(e)}")
        return None

# Process user input
def process_user_query(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error("Error loading vector store. Ensure files are processed first.")
        return {"output_text": [f"Error: {str(e)}"]}

    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    if not chain:
        return {"output_text": ["Error: Unable to initialize conversational chain."]}

    try:
        return chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")
        return {"output_text": [f"Error: {str(e)}"]}

# Clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Upload files and ask me a question."}]

# Main application
def main():
    st.set_page_config(page_title="Gemini File Chatbot", page_icon="🤖")

    with st.sidebar:
        st.title("File Uploader")
        files = st.file_uploader("Upload Files", accept_multiple_files=True, type=["pdf", "txt", "csv", "xls", "xlsx"])
        if st.button("Submit & Process"):
            with st.spinner("Processing files..."):
                extracted_text = extract_text_from_files(files)
                if not extracted_text:
                    st.warning("No extractable text found. Please upload a different file.")
                    return
                try:
                    text_chunks = split_text_into_chunks(extracted_text)
                    create_vector_store(text_chunks)
                    st.success("Files processed successfully!")
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")

        st.button("🗑️ Clear Chat History", on_click=clear_chat_history)

    st.title("💬 Chat with Your Files using Gemini")
    if "messages" not in st.session_state:
        clear_chat_history()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = process_user_query(user_prompt)
                if response and "output_text" in response:
                    full_response = "".join(response["output_text"])
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
