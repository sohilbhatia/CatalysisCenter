# CatalysisCenter
Question answering catalysis queries backed by a ripgrep processor and NLP model

This program functions on search.py 
Ripgrepy is used as the search processor for a database of files. Rake is used to extract keywords from a user question. PyPDF is used to convert PDFs in the database to text files. Hugging Face transformers and the deepset/bert-base-cased-squad2 question answering model is used to retrieve an answer from the file. 

## Streamlit
Streamlit is used to run the UI interface of the app. You can simply install the streamlit python package in a virtual environment.
<pre>import streamlit as st </pre>
To import the streamlit package

## File Paths
Before running the code, make sure the file path strings are aligned to your file path. This way datasets are saved on your local machine, and existing datasets are being accessed from a specified folder.

Take for example:
<pre>result = re.search('/YOUR FILE PATH HERE/(.*).pdf', standard)</pre>

## Ripgrep
Ripgrep is a fast search tool to search your datasets. It uses the keywords extracted from the question (Rake) and finds matches in every document. Documents which don't have matches are discarded from the search. Once these documents are identified, it applies the question-answering model on each piece of text.

Note:
<pre>searcher = rg.pre("/Users/sohilbhatia/Downloads/convertly.command").pre_glob("*.pdf").multiline().smart_case().json().H().n().run().as_json</pre>
These functions of <code>rg</code> or <code>ripgrepy.Ripgrepy</code> come from the following Ripgrepy documentation: https://ripgrepy.readthedocs.io/en/latest/
The functions used in this program convert each file to a pdf format (if not already), search multiline, and returns each search in a json format.

## HuggingFace Transformers and QA Models
Hugging Face provides a variety of question-answering models on its platform. The one used in this project is here:
<pre>
model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
</pre>
You can learn more about the current offerings of models here: https://huggingface.co/models

## Running the Project
Simply run:
<code> streamlit run app.py </code>





Copyright for PNNL use only (c)
