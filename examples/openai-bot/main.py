#################################### Import Packages ####################################

import os
import json
import faiss
import openai
import pinecone
from typing import List
from pypdf import PdfMerger
from pydantic import BaseModel
from textbase import bot, Message

from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.vectorstores import Pinecone
from langchain.prompts import PromptTemplate
from langchain.docstore import InMemoryDocstore
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

#################################### SpaceINDIA_bot class ####################################

class SpaceINDIA_bot(object):

  def __init__(self,
               openai_key=None,
               pinecone_key=None,
               pinecone_env="",
               pinecone_indexname=""):
    
    assert pinecone_env != ""
    assert pinecone_indexname != ""
    assert pinecone_key != None
    assert openai_key != None

    self.embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2')

    openai.api_key = openai_key
    self.index_name = pinecone_indexname
    self.PINECONE_API_KEY = pinecone_key
    self.PINECONE_API_ENV = pinecone_env

    self.llm = OpenAI(model_name="gpt-3.5-turbo")
    pinecone.init(api_key=self.PINECONE_API_KEY, 
                  environment=self.PINECONE_API_ENV)
    
    # Text splitter initialization
    self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,  
                                                        chunk_overlap=0,
                                                        separators=["\n\n", "\n", " ", ""])
    
  def create_langchain(self):  
    # Prompt Template
    template = """

    You are chatting with SpaceINDIA bot. It is aware with the
    accomplishments done by India and other nations about space 
    missions, events , UAP activities that held till September 2023.

    {context}

    You: {input}
    SpaceINDIA bot:

    """
    SYSTEM_PROMPT = PromptTemplate(input_variables=["input", "context"], 
                                    template=template,)
    
    # Chain initialization
    chain = load_qa_chain(self.llm,chain_type="stuff",
                          prompt=SYSTEM_PROMPT)

    return chain

  def create_vectorstore(self):

    pdfs = ['/content/papers/James Webb Space Telescope (JWST) — A complete guide _ Space.pdf',
            '/content/papers/Chandrayaan3_PLS_MNRASL-23-08-2023-16-57-50.pdf', 
            '/content/papers/LVM3M4_Chandrayaan3_brochure.pdf',
            '/content/papers/Aditya_L1_Booklet.pdf',
            '/content/papers/2307.03173.pdf',
            '/content/papers/2308.10712.pdf']

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write("result.pdf")
    merger.close()
    loader = PyPDFLoader("/content/result.pdf")
    data = loader.load()
    docs=self.text_splitter.split_documents(data)
    docsearch=Pinecone.from_texts([t.page_content for t in docs], self.embeddings, index_name=self.index_name)

    return docsearch

  def retrieve_vectorstore(self):

    vectorstore = Pinecone.from_existing_index(index_name=self.index_name,
                                               embedding=self.embeddings)
    
    return vectorstore

  def generate(self,query,vectorstore,chain):

    context = vectorstore.similarity_search(query,k=3)

    bot_repsonse = chain.run(input_documents=context, input=query)

    return bot_repsonse

#################################### Create Setup ####################################

index_name = "langchainpinecone"
os.environ["OPENAI_API_KEY"]="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"

chatbot = SpaceINDIA_bot(openai_key=os.environ["OPENAI_API_KEY"],
               pinecone_key=os.environ.get('PINECONE_API_KEY', 'b9e4dcda-4cb4-4589-b91b-eeaad51fd689'),
               pinecone_env=os.environ.get('PINECONE_API_ENV', 'gcp-starter'),
               pinecone_indexname=index_name)

vectorstore = chatbot.retrieve_vectorstore()
chain = chatbot.create_langchain()

#################################### Inferene testing ####################################

@bot()
def on_message(message_history: List[Message], state: dict = None):

    question = message_history[-1]['content'][0]['value']

    bot_response = chatbot.generate(question,vectorstore,chain)

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }
