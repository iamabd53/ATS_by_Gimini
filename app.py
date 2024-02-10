import streamlit as st
import google.generativeai as genai 
import os
import PyPDF2 as pdf 

from dotenv import load_dotenv

load_dotenv()


# Gemini
def get_gemini_response(input):
    genai.configure(api_key='Your API Key')
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ''
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text= text+str(page.extract_text)
    return text


input_prompts = """
Hey act like a skilled or a very experience ATS(Application Treacking System) with deep understanding of tech field, software engineering,
data science , data analyst. your task is to evaluate the resume based on the given job discription, You must consider the job market is very
competitive and you should provide best assistance for improving the resume. Assign the precentage matching based on JD and
the missing keywords with high accuracy,
note: read each and every word from the resume very clearly, don't forget a single word, and also give recommedation as well as where to learn missing skills
resume:{text}
description:{}

I want the responce in this manner =
{{"Resume match %" : %, "MissingKeywords:[]","Profile Summary":""}}
"""

st.title('ATS powered by gimini')
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")

uploaded_file = st.file_uploader('Upload your resume', type='pdf',
                                 help= 'please upload your resume')

submit = st.button('submit')

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompts)
        st.subheader(response)
