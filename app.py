import streamlit as st
from langchain.llms import OpenAI
from ai_core.parsing import read_file
from ai_core.chunking import chunk_file
from ai_core.embeddings import embed_files

st.set_page_config(page_title="CompareGPT", page_icon="📖", layout="wide")
st.header("📖 CompareGPT")

api_key_input = st.sidebar.text_input('OpenAI API Key', type='password')

st.session_state["OPEN_API_KEY"] = api_key_input
openai_api_key = st.session_state.get("OPENAI_API_KEY")
llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

if not openai_api_key:
    st.warning('Please enter your OpenAI API key!', icon='⚠')

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))

uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf"],
    help="Scanned documents are not supported yet!",
)
 
try:
    file = read_file(uploaded_file)
except Exception as e:
    st.error(e)
    st.stop()

chunked_file = chunk_file(read_file, chunk_size=1000)

with st.spinner('Loading document... Drink coffee, it is gonna take a while'):
    vector_retriever = embed_files([chunked_file])

with st.form(key="chatbot_form"):
    input_text = st.text_area("Query the document")
    submit = st.form_submit_button("Submit")

if submit:
    generate_response(input_text)