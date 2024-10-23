import streamlit as st
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
import torch
from threading import Thread
import accelerate

def main():
    st.set_page_config(page_title="Medical Bot - A fine-tuned Llama 3.1 to answer medical questions")

    # Load and display the logo
    st.image("/app/assets/uni_ms_logo2.png")

    # Main title
    custom_title_main = "<h2 style='color: #006e89;'>Medical Bot</h2>"
    st.markdown(custom_title_main, unsafe_allow_html=True)

    # Sidebar content
    with st.sidebar:
        #custom_title_chathistory = "<h1 style='color: #006e89;'>Chat History</h1>"
        #st.markdown(custom_title_chathistory, unsafe_allow_html=True)

        custom_title_about = "<h3 style='color: #006e89;'>About</h3>"
        st.markdown(custom_title_about, unsafe_allow_html=True)

        st.markdown('''
        This app is a fine-tuned Llama 3.1 powered chatbot built to better answer medical inquiries. 
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
        
    # Cache the model for faster inference
    @st.cache_resource
    def load_model():
        tokenizer = AutoTokenizer.from_pretrained(
            'bastistrauss/MedicalLlama-3.1-8b-52',
            trust_remote_code=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            'bastistrauss/MedicalLlama-3.1-8b-52',
            torch_dtype=torch.bfloat16,
            device_map='auto',
            trust_remote_code=True
        )
        return model, tokenizer

    # Load the model
    with st.spinner('Loading model... This may take several minutes.'):
        model, tokenizer = load_model()

    def response_generator(prompt):
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        generation_kwargs = dict(
            input_ids=input_ids,
            max_length=500,
            do_sample=True,
            temperature=0.7,
            num_return_sequences=1,
            streamer=streamer
        )
        thread = Thread(target=model.generate, kwargs=generation_kwargs)
        thread.start()
        generated_text = ""
        for new_text in streamer:
            yield new_text

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

        with st.chat_message("assistant", avatar='/app/assets/uni_ms_logo.png'):
            message_placeholder = st.empty()
            generated_text = ""
            for new_text in response_generator(prompt):
                generated_text += new_text
                message_placeholder.markdown(generated_text)
                time.sleep(0.05)  # Sleep time to simulate typewriter
        st.session_state.messages.append({"role": "assistant", "content": generated_text})

    # Display the initial message if the message history is empty
    if len(st.session_state.messages) == 0:
        time.sleep(2)
        initial_message = "How can I help you with your medical questions?"
        st.session_state.messages.append({"role": "assistant", "content": initial_message})
        with st.chat_message("assistant", avatar='/app/assets/uni_ms_logo.png'):
            st.markdown(initial_message)

if __name__ == "__main__":
    main()
