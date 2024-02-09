from scrape import findAllUrls, get_body_content

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import pickle
import os
from langchain.chat_models import ChatOpenAI

load_dotenv()
url = 'https://www.laptop.lk/'

arr = findAllUrls(url)


def save_page_data(page_url, content):
    text_split = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    chunks = text_split.split_text()
    embeddings = OpenAIEmbeddings()
    vs = FAISS.from_texts(chunks,embedding=embeddings)
    try:
        with open(f"{page_url}.pkl", "wb") as f:
            pickle.dump(vs, f)
            print(f"Saved {page_url} to disk.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_recommendations(vs):
    user_query = input("Enter your query: ")
    docs = vs.similarity_search(query=user_query)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    with get_openai_callback() as callback:
        response = chain.run(input_documents=docs, question=user_query)
    

