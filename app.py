import validators
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

#streamlit
st.set_page_config(page_title='Langchain: Summarize a YT videos or URL')
st.title("Langchain: Summarize a YT videos or URL")
st.subheader("Summarize URL")


with st.sidebar:
    groq_api_key=st.text_input("GROQ API KEY",value="",type="password")

generic_url=st.text_input("URL",label_visibility="collapsed")

llm=ChatGroq(model='llama-3.1-70b-versatile',groq_api_key=groq_api_key)

prompt_template="""
consider yourself as text summarizer who will provide the summary of the content provided to you in 400 words,
in points with important words and points highlighted in bold:
context:{text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=['text'])


if st.button("Summarize the content from YT or Website URL"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please enter the information")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It may be a YT or Website URL")


    else:
        try:
            with st.spinner("WAITING....."):
                #loading data
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})


                docs=loader.load()

                #chain
                chain=load_summarize_chain(llm=llm,chain_type='stuff',prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")