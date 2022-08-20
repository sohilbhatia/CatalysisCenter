# CatalysisCenter
Question answering catalysis queries backed by a ripgrep processor and NLP model

This program functions on search.py 
Ripgrepy is used as the search processor for a database of files. Rake is used to extract keywords from a user question. PyPDF is used to convert PDFs in the database to text files. Hugging Face transformers and the deepset/bert-base-cased-squad2 question answering model is used to retrieve an answer from the file. 

Implementation involves downloading the specified packages in search.py

blend.py explores the ripgrep search processor in detail

extractly.py is a keyword extracter for user input and query 
