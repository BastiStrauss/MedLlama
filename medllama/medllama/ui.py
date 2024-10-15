import streamlit as st
import time
from PIL import Image
from transformers import pipeline
import torch

def main():
    st.set_page_config(page_title="Medical Bot - A fine-tuned Llama 3 to answer medical questions")

    # Load and display the logo
    with Image.open("/app/assets/uni_ms_logo2.png") as logo:
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

    @st.cache_resource
    def load_model():
        return pipeline(
            'text-generation',
            model='bastistrauss/MedicalLlama-3.1-8b',
            tokenizer='bastistrauss/MedicalLlama-3.1-8b',
            torch_dtype=torch.bfloat16,
            device_map='auto',  # Use 'cuda' if you have a GPU
            trust_remote_code=True
        )

    # Load the model
    with st.spinner('Loading model... This may take several minutes.'):
        generator = load_model()

    # Function to generate a response using the model
    def response_generator(user_input):
        output = generator(
            user_input,
            max_length=512,
            do_sample=True,
            temperature=0.7,
            num_return_sequences=1,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        response = output[0]['generated_text']
        return response

    # Function to animate text
    def animate_text(output):
        text_container = st.empty()
        display_text = ""
        for i in range(len(output) + 1):
            display_text = output[:i]
            text_container.write(display_text)
            time.sleep(0.05)
        time.sleep(1)

    # Initialize session state messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "user":
            with st.chat_message("user", avatar=":material/person:"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant", avatar='/app/assets/uni_ms_logo.png'):
                st.markdown(content)

    # Handle user input
    if prompt := st.chat_input("Ask your medical questions here"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(prompt)

        with st.spinner("Generating response..."):
            response = response_generator(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar='/app/assets/uni_ms_logo.png'):
            animate_text(response)

    # Display the initial message if the message history is empty
    if len(st.session_state.messages) == 0:
        time.sleep(2)
        initial_message = "How can I help you with your medical questions?"
        st.session_state.messages.append({"role": "assistant", "content": initial_message})
        with st.chat_message("assistant", avatar='/app/assets/uni_ms_logo.png'):
            animate_text(initial_message)

if __name__ == "__main__":
    main()
