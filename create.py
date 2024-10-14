import streamlit as st

st.set_page_config(page_title="Recipe IG Importer", page_icon="📖", layout="wide")
st.header("📖 Recipe IG Importer")

api_key_input = st.sidebar.text_input('OpenAI API Key', type='password')
st.session_state["OPENAI_API_KEY"] = api_key_input

openai_api_key = st.session_state.get("OPENAI_API_KEY")

if not api_key_input:
    st.warning('Please enter your OpenAI API key!', icon='⚠')

uploaded_file = st.file_uploader(
    "Upload a pdf",
    type=["pdf"],
    help="Scanned documents are not supported yet!",
)

url_input = st.text_input("Enter the URL of the recipe")

if st.button("Submit"):
    st.write(url_input)

# if not uploaded_file:
#     st.warning("Please upload a pdf file", icon="⚠")
#     st.stop()
 
# try:
#     file = read_file(uploaded_file)
# except Exception as e:
#     st.error(e)
#     st.stop()

# chunked_file = chunk_file(file, chunk_size=1000)

# with st.spinner('Loading document... Drink coffee, it is gonna take a while'):
#     chain = create_chain([chunked_file])

# with st.form(key="chatbot_form"):
#     input_text = st.text_area("Query the document")
#     submit = st.form_submit_button("Submit")

# if submit:
#     answer_col, question_col = st.columns(2)

#     with st.spinner("Thinking..."):
#         response = query(query=input_text, chain=chain)

#     with answer_col:
#         st.markdown("### Answer")
#         st.markdown(response.answer)

#     with question_col:
#         st.markdown("### Sources")
#         st.markdown(input_text)
