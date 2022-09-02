from gettext import find
import streamlit as st
from cmath import exp
from glob import glob
from ripgrepy import Ripgrepy
import json
import re
from transformers import BertForQuestionAnswering, AutoTokenizer
from transformers import AutoModelForQuestionAnswering, pipeline
from transformers import pipeline
from PyPDF2 import PdfReader
from multi_rake import Rake
import os
import streamlit_modal as modal

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import io 
import base64

import random
import string

new_datasets = []
rake = Rake()

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def save_uploadedfile(uploadedfile, set_name):
    newpath = r'/Users/sohilbhatia/Downloads/' + set_name 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for i in uploadedfile:
        with open(os.path.join(newpath,i.name),"wb") as f:
            f.write(i.getbuffer())
    return st.success("Sucessfully created " + set_name + " dataset")

def findContext(word, file_name):
    rg = Ripgrepy(word, '/Users/sohilbhatia/Downloads/searchdb/' + file_name + '.pdf')

    searcher = rg.pre("/Users/sohilbhatia/Downloads/convertly.command").after_context(30).pre_glob("*.pdf").multiline().smart_case().json().H().n().run().as_json

    json_object = json.loads(searcher)
    dict_length = len(json_object)
    dataset = []
        


    for i in range(dict_length):
        excerpt = json_object[i]['data']['lines']['text']
        dataset.append(excerpt)

    return dataset

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def refreshDatasets(header):
    st.header(header + " Dataset")
    path = "/Users/sohilbhatia/Downloads/"+header
    dir_list = os.listdir(path)
    with st.expander("View " + header + " Dataset"):
        for c in dir_list:
            image_col, text_col = st.columns((1,3))
            with image_col:
                st.write(c)
            with text_col:
                pdfpath = "/Users/sohilbhatia/Downloads/" + header + "/" + c
                with open(pdfpath, "rb") as pdf_file:
                    PDFbyte = pdf_file.read()

                st.download_button(label="Download Database File", 
                    data=PDFbyte,
                    file_name=c,
                    mime='application/octet-stream', key=''.join(random.choices(string.ascii_uppercase + string.digits, k=7)))


with st.sidebar:
    image = Image.open('/Users/sohilbhatia/Downloads/pnnl-logo.png')
    st.image(image)

    choose = option_menu("Catalysis Search", ["Database Search", "Create Datasets", "View Datasets"],
                         icons=['search', 'cloud-arrow-up', 'file-bar-graph'],
                         menu_icon="cursor-fill", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#D77900"},
    }
    )

if choose=="Create Datasets":
    st.title("Create Datasets")
    st.caption("Create your own dataset and upload your specified documents. You can view the exisiting datasets in the View Datasets tab.")

    form = st.form(key='my-form')
    set_name = form.text_input("Dataset Name")
    uploader = form.file_uploader("Upload PDF Files",type=['pdf'], accept_multiple_files=True)
    submit = form.form_submit_button("Create Dataset")
                    
    if submit:
            save_uploadedfile(uploader, set_name)

    if (set_name != ''):
        st.session_state[set_name] = set_name

if choose == "View Datasets":
    st.title("View Datasets")
    st.caption("View our vast database of PNNL Catalysis publications. Search for your specific document or create a new dataset of documents. Once uploaded, you can begin searching this dataset in Catalysis Search.")
    for i in st.session_state:
            if (st.session_state.get(i)!=False) and (st.session_state.get(i)!=True):
                refreshDatasets(i)

    st.header("Starter Dataset")
    
    path = "/Users/sohilbhatia/Downloads/searchdb/"
    dir_list = os.listdir(path)

    with st.expander("View Starter Dataset"):
        for c in dir_list:
            image_col, text_col = st.columns((1,3))
            with image_col:
                st.write(c)
            with text_col:
                pdfpath = "/Users/sohilbhatia/Downloads/searchdb/" + c
                with open(pdfpath, "rb") as pdf_file:
                    PDFbyte = pdf_file.read()

                st.download_button(label="Download Database File", 
                    data=PDFbyte,
                    file_name=c,
                    mime='application/octet-stream')


if choose == "Database Search":

    st.title("Catalysis Database from PNNL")

    st.header("Catalysis Search")
    st.caption("Search a wide array of PNNL publications. We'll extract keywords from your question and find doucments that match. From here you'll get a few answers relating to your query.")

    options = []
    for i in st.session_state:
        if (st.session_state.get(i)!=False) and (st.session_state.get(i)!=True):
            options.append(i)
    
    user_dataset = st.selectbox("Select Your Dataset", options=options)
    searchy = st.text_input("Type a search query", placeholder="Your search")

    onclick = st.button("Search")


    if onclick:
        userquestion = searchy


        keywords = rake.apply(userquestion)

        key_dataset = []

        def findKey(word):
            keys = rake.apply(word)
            return keys

        for i in keywords:
            temp = re.findall(r'\d+', i[0])
            res = list(map(int, temp))
            if not res:
                if (i[1]>1.0):
                    key_dataset.append(i[0])
            else:
                for numero in res:
                    key_dataset.append(str(numero))

        def get_unique_vals(numbers):

                list_of_unique_numbers = []

                unique_numbers = set(numbers)

                for number in unique_numbers:
                    list_of_unique_numbers.append(number)

                return list_of_unique_numbers

        def findMatches(word, user_dataset):
            rg = Ripgrepy(word, '/Users/sohilbhatia/Downloads/'+user_dataset)

            searcher = rg.pre("/Users/sohilbhatia/Downloads/convertly.command").pre_glob("*.pdf").multiline().smart_case().json().H().n().run().as_json

            json_object = json.loads(searcher)


            dict_length = len(json_object)

            
            dataset = []
            context = []


            for i in range(dict_length):
                standard = json_object[i]['data']['path']['text']
                line_num = json_object[i]['data']['line_number']
                excerpt = json_object[i]['data']['lines']['text']
                extraction = excerpt.replace('\n', '')

                result = re.search('/Users/sohilbhatia/Downloads/' + user_dataset + '/(.*).pdf', standard)
                dataset.append(result.group(1))
                context.append({"Title": result.group(1),
                                "Excerpt": excerpt,
                                "Line Number": line_num})

            comp = get_unique_vals(dataset)

            return comp, context


        set1 = findMatches(key_dataset[0], user_dataset)
        set2 = findMatches(key_dataset[1], user_dataset)
        contexts = set1[1] + set2[1]
        term = list(set(set1[0]) | set(set2[0]))

        def engageModel(name, user_dataset):
            path = "/Users/sohilbhatia/Downloads/" + user_dataset + "/"
            path+=str(name)
            path+=".pdf"

            reader = PdfReader(path)
            context = ""
            for page in reader.pages:
                context += page.extract_text() + "\n"

            model_name = "deepset/roberta-base-squad2"
            nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)


            QA_input = {"question":userquestion,
            "context": context}
            res = nlp(QA_input)

            model = AutoModelForQuestionAnswering.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
  

            return {"Answer": res['answer'],
                    "Page": name}

        st.header("")
        st.header("Results")
        for i in term:
            comp = engageModel(i, user_dataset)
            expander = st.expander("See more from the result of " + str(comp["Answer"]))
            expander.write("Found in database file " + str(comp["Page"]))
            expander.subheader("Related Excerpts:")
            for i in contexts:
                if (i["Title"] == comp["Page"]):
                    expander.write('In Line Number ' + str(i["Line Number"]) + ':')
                    expander.caption('"..."' + i["Excerpt"] + '..."')
                    
            with expander:
                pdfpath = "/Users/sohilbhatia/Downloads/" + user_dataset + "/" + str(comp["Page"]) + ".pdf"

                with open(pdfpath, "rb") as pdf_file:
                    PDFbyte = pdf_file.read()

                st.download_button(label="Download Database File", 
                        data=PDFbyte,
                        file_name=str(comp["Page"]),
                        mime='application/octet-stream')
        






