import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
__import__('pysqlite3') 
import sys 
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
import chromadb.api

chromadb.api.client.SharedSystemClient.clear_system_cache()

from dotenv import load_dotenv
load_dotenv()
#setting up the environment
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

## Set up streamlit app
st.title("RAG-PDFChat: AI-Powered Q&A with Contextual Memory")
st.write("Uplaod Pdf's and chat with their content")

available_models = [
    "Gemma2-9b-It",
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b",
    "mistral-saba-24b"
]
## Input the Groq API key
api_key=st.sidebar.text_input("Enter your Groq API: ", type="password")
model=st.sidebar.selectbox("Select an AI Model", available_models)

## check if groq api key is provided
if api_key:
    llm=ChatGroq(groq_api_key = api_key, model_name=model)
    ## Chat interface
    session_id = st.text_input("Session ID", value="default_session")
    ## Statefully manange chat history

    if 'store' not in st.session_state:
        st.session_state.store={}
    
    uploaded_files = st.file_uploader("Choose A PDf file",type="pdf",accept_multiple_files=True)

    ## Process uplaoded files

    if uploaded_files:
        documents=[]
        for uploaded_file in uploaded_files:
            temppdf = f"./temp.pdf"
            with open(temppdf,'wb') as file:
                file.write(uploaded_file.getvalue())
                file_name=uploaded_file.name
            
            loader = PyPDFLoader(temppdf)
            docs=loader.load()
            documents.extend(docs)

        # Split and create embedding for the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()

        # New Prompt
        contextialize_q_system_prompt = (
            "Given a chat history and the latest user question"
            "Which might reference context in the chat history,"
            "formulate a standalone question which cna be understood"
            "without the chat history. Do Not answer the question,"
            "just reformulate it if needed and otherwise return it as is."
        )

        contextialize_q_system_prompt= ChatPromptTemplate.from_messages(
            [
                ('system', contextialize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextialize_q_system_prompt)

        ## Answer question Prompt
        system_prompt = (
                "You are an assistant for question answering tasks."
                "Use the following pieces of retrieved context to answer."
                "the question. If you don't knwo the answer, say that you"
                "don't know. Use three sentences maximum and keep the answer concise."
                "\n\n"
                "{context}"
            )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm,qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)

        def get_session_history(session:str)->BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            
            return st.session_state.store[session_id]

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        user_input = st.text_input("Your Question: ")
        if user_input:
            session_history = get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {"input":user_input},
                config={
                    "configurable" : {"session_id":session_id}
                },  # constructs a key "abc123" in store
            )
            import time
            def stream_data():
                for word in response['answer'].split(" "):
                    yield word + " "
                    time.sleep(0.02)
            # st.write(st.session_state.store)
            st.write(f"Assistant as {model} : \n")
            st.write_stream(stream_data)
            # st.write("Chat History: ", session_history.messages)

else:
    st.warning("Please enter the Groq api Key")
            



