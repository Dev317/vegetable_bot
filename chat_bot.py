import streamlit as st
from recommendation import get_response
import time


st.set_page_config(
    page_title='Rau sạch Vinh Hà',
    page_icon='https://vinhhaphuxuyen.vn/wp-content/uploads/2019/01/logovinha.png'
)

def img_to_html(src):
    img_html = "<img src='{src}' class='img-fluid'>".format(src=src)
    return img_html

def stream_output(response, m_placeholder):
    full_response = ""
    for chunk in response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        m_placeholder.markdown(full_response + "▌")
    m_placeholder.markdown(full_response)

st.title("🥬 Rau Vinh Hà Chat Bot")

INITIAL_MESSAGE = [
    {
        "role": "assistant",
        "content": "Chào mừng bạn đến với cửa hàng rau sạch Vinh Hà. Bạn cần tìm những sản phẩm gì?",
    },
]

if "messages" not in st.session_state:
    st.session_state.messages = INITIAL_MESSAGE

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Bạn cần tìm gì?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        intro_message_placeholder = st.empty()
        intro_response = "Dưới đây là những sản phẩm mà bạn có thể quan tâm:\n"
        stream_output(intro_response, intro_message_placeholder)
        st.session_state.messages.append({"role": "assistant", "content": intro_response})

        product_list, image_list = get_response(prompt)

        for idx in range(len(product_list)):
            stream_output(product_list[idx], st.empty())
            st.session_state.messages.append({"role": "assistant", "content": product_list[idx]})
            img = img_to_html(image_list[idx])
            st.markdown(img, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": img})
