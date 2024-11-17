# Langchain: Summarize YouTube Videos or Website URLs
This Streamlit application uses Langchain to provide summaries for YouTube videos or website URLs. It utilizes state-of-the-art language models to generate concise and informative summaries, highlighting important points in bold.

Features
Summarize YouTube Videos: Enter a YouTube URL to get a summary of the video's content.

Summarize Website URLs: Enter any valid URL to get a summarized version of the webpage.

User-Friendly Interface: A simple and intuitive Streamlit interface to enter URLs and view summaries.

Secure API Key Input: Enter your GROQ API key securely using a password input field.

Installation
Follow these steps to set up and run the application:

Clone the Repository:

bash
git clone https://github.com/yourusername/langchain-summarize.git
cd langchain-summarize
Install Dependencies: Make sure you have Python installed. Then, install the required packages:

bash
pip install -r requirements.txt
Usage
Run the Streamlit App:

bash
streamlit run app.py
Enter the GROQ API Key:

In the sidebar, enter your GROQ API key.

Summarize a URL:

Enter the URL you wish to summarize (either YouTube or a website URL).

Click on the "Summarize the content from YT or Website URL" button.

View the summarized content in the main area of the application.

Code Explanation
Importing Libraries
python
import validators
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
These imports bring in the necessary libraries for validators, Streamlit, Langchain, and document loaders.

Streamlit Configuration
python
st.set_page_config(page_title='Langchain: Summarize a YT videos or URL')
st.title("Langchain: Summarize a YT videos or URL")
st.subheader("Summarize URL")
Setting up the Streamlit page with a title and subtitle.

Sidebar for API Key
python
with st.sidebar:
    groq_api_key = st.text_input("GROQ API KEY", value="", type="password")
Adding a text input in the sidebar to securely enter the GROQ API key.

URL Input
python
generic_url = st.text_input("URL", label_visibility="collapsed")
A text input field for entering the URL to be summarized.

Language Model and Prompt Template
python
llm = ChatGroq(model='llama-3.1-70b-versatile', groq_api_key=groq_api_key)

prompt_template = """
consider yourself as text summarizer who will provide the summary of the content provided to you in 400 words,
in points with important words and points highlighted in bold:
context:{text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=['text'])
Setting up the language model and creating a prompt template for summarization.

Summarize Button Logic
python
if st.button("Summarize the content from YT or Website URL"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please enter the information")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It may be a YT or Website URL")
    else:
        try:
            with st.spinner("WAITING....."):
                # Loading data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})

                docs = loader.load()

                # Chain
                chain = load_summarize_chain(llm=llm, chain_type='stuff', prompt=prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")
This section handles the logic when the "Summarize" button is clicked:

Checks if the API key and URL are provided.

Validates the URL.

Loads the data using appropriate loaders based on the URL type.

Runs the summarization chain and displays the output.
