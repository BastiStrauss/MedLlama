import streamlit as st
import time
import random
import webbrowser
from PIL import Image

def main():
    # Delay to allow the Streamlit server to start
    time.sleep(5)
    
    # Open the web browser to the Streamlit app URL
    webbrowser.open("http://localhost:8501")

    st.set_page_config(page_title="Medical Bot - A fine-tuned Llama 3 to answer medical questions")

    # Load and display the logo
    with Image.open("/app/assets/uni_ms.png") as logo:
        st.image(logo)

    # Main title
    custom_title_main = "<h2 style='color: #006e89;'>Medical Bot</h2>"
    st.markdown(custom_title_main, unsafe_allow_html=True)

    # Sidebar content
    with st.sidebar:
        custom_title_chathistory = "<h1 style='color: #006e89;'>Chat History</h1>"
        st.markdown(custom_title_chathistory, unsafe_allow_html=True)

        if st.button('Chat History 1'):
            st.session_state.selected_history = 'History 1'
        if st.button('Chat History 2'):
            st.session_state.selected_history = 'History 2'
        if st.button('Chat History 3'):
            st.session_state.selected_history = 'History 3'

        custom_title_about = "<h3 style='color: #006e89;'>About</h3>"
        st.markdown(custom_title_about, unsafe_allow_html=True)

        st.markdown('''
        This app is a fine-tuned Llama 3 powered chatbot built to better answer medical inquiries. 
        Always check answers for their correctness.
        ''')

        def display_github():
            st.markdown('<a href="https://github.com/BastiStrauss/BastiStrauss" target="_blank"><img src="https://img.shields.io/badge/github-BastiStrauss-blue?style=flat&logo=github"></a>', unsafe_allow_html=True)

        display_github()

        st.markdown("""
        <div class='fixed-link'>
            <a href='https://www.uni-muenster.de/en/' target='_blank' style='color: #006e89;'>living.knowledge</a>
        </div>
        """, unsafe_allow_html=True)

    # Function to generate a random response
    def response_generator(user_input):
        responses = [
            "Hello there! How can I assist you today?",
            "Hi, how can I help you with your medical questions?",
            "I'm here to help, please tell me your medical concern.",
            "Could you please provide more details about your symptoms or condition?"
        ]
        time.sleep(1)
        return random.choice(responses)

    # Function to animate text
    def animate_text(output):
        text_container = st.empty()
        display_text = ""
        for i in range(len(output) + 1):
            display_text = output[:i]
            text_container.write(display_text)
            time.sleep(0.05)
        time.sleep(1)

    # Initializing session state messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "user":
            with st.chat_message("user", avatar="🥸"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)

    # Handle user input
    if prompt := st.chat_input("Ask your medical questions here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🥸"):
            st.markdown(prompt)

        response = response_generator(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🤖"):
            animate_text(response)

    # Display the initial message after one second if the message history is empty
    if len(st.session_state.messages) == 0:
        time.sleep(2)
        initial_message = "How can I help you with your medical questions?"
        st.session_state.messages.append({"role": "assistant", "content": initial_message})
        with st.chat_message("assistant", avatar="🤖"):
            animate_text(initial_message)

if __name__ == "__main__":
    main()