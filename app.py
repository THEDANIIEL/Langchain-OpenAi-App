import os 
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

os.environ['OPEN-AI-API'] = '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'

st.title("Daniel GPT")
prompt =st.text_input('Plug in your prompt here:')

#prompts templates
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'write me a youtube vide title about{topic}'
) 

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'],
    template = 'write me a youtube vide script based on this title TITLE: {title} while levraging this wikipedia research: {wikipedia_research}'
) 

#memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat-history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat-history')

#llms
llm = OpenAI(temperture=9.0)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)
wiki = WikipediaAPIWrapper()


if prompt:
    title = title_chain.run(prompt)
    wiki_reaesrch = wiki.run(prompt)
    script = script_chain.run(title=title, wikipedia_research=wiki_reaesrch)
    st.write(title)
    st.write(script)


    with st.expander('title history'):
        st.info(title_memory.buffer)

    with st.expander('script history'):
        st.info(script_memory.buffer)

    with st.expander('wikipedia research'):
        st.info(wiki_reaesrch)