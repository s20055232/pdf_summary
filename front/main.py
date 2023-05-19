import streamlit as st
import requests

label = []
base_url = "http://localhost:8000/"
st.title("PDF Knowledge Base")

uploaded_file = st.file_uploader("Browse Files...", help="上傳你的pdf文件提供解析")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    print(uploaded_file)
    res = requests.post(
        url=base_url + "upload/",
        files={"file": (uploaded_file.name, bytes_data)},
    )
    print(res.status_code)
    if res.status_code == 200:
        label.append(uploaded_file.name)


option = st.selectbox("選擇你要解析的pdf", label)
text_input = st.text_input(
        "輸入問題 👇"
    )

if option and text_input:
    res = requests.post(url=base_url + f"parsing/", json={"file_name": option, "query": text_input})
