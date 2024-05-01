import streamlit as st

from groq import Groq
import random

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

from settings import GROQ_API_KEY


def main():
  conversational_memory_length=10

  memory=ConversationBufferWindowMemory(k=conversational_memory_length)


  if 'chat_historn' not in st.session_state:
      st.session_state.chat_history = []
  else :
      for message in st.session_state.chat_history:
          memory.save_context({'input':message['human'],'output':message['AI']})


  groq_chat = ChatGroq(
      groq_api_key=GROQ_API_KEY,
  )

  conversation = ConversationChain(
      llm=groq_chat,
      memory=memory
  )

  st.title("Chatbot")
  st.write("Welcome to a chatbot")
  user_question = st.text_input("Ask a question")

  if user_question:
      response = conversation(user_question)
      message = {'human':user_question,'AI':response}
      st.session_state.chat_history.append(message)
      st.write("Chatbot:", response['response'])

if __name__ == "__main__":
    main()