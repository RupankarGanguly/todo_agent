import streamlit as st
from agent import createAgent

st.set_page_config(page_title="AI Todo Manager", page_icon="✅", layout="centered")

if "agent" not in st.session_state:
    st.session_state.agent = createAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("✅ AI Task Manager")
st.caption("Powered by LangChain + Groq")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Manage your tasks...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = st.session_state.agent.invoke(
                {"messages": [{"role": "user", "content": query}]},
                {"configurable": {"thread_id": "1"}},
            )
            answer = res["messages"][-1].content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
