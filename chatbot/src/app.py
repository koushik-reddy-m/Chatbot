import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Add a title for the chatbot
st.title("🤖 AI Chatbot")
st.subheader("Welcome to the AI Chatbot! Feel free to ask any questions.")

# Function to get response from the AI
def get_response(user_query, chat_history):
    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

# Display conversation history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(f"**🤖 Bot:** {message.content}")
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(f"**🧑 You:** {message.content}")

# User input
user_query = st.chat_input("Type your message here...")
if user_query:
    # Append user query to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with chat_container:
        with st.chat_message("Human"):
            st.markdown(f"**🧑 You:** {user_query}")

        with st.chat_message("AI"):
            response_placeholder = st.empty()  # Placeholder for streaming response
            full_response = ""
            for response in get_response(user_query, st.session_state.chat_history):
                full_response += response
                response_placeholder.markdown(f"**🤖 Bot:** {full_response}")

            # Append AI response to chat history
            st.session_state.chat_history.append(AIMessage(content=full_response))
