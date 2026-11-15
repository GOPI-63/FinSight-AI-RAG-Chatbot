import uuid

import streamlit as st

from rag_backend import KNOWLEDGE_BASE_NAME, get_answer


st.set_page_config(
    page_title="FinSight AI - Company Policy Assistant",
    page_icon="📘",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
        --page: #F8FAFC;
        --chat: #FFFFFF;
        --sidebar: #F1F5F9;
        --text: #172033;
        --muted: #475569;
        --user-chat: #E8F1FF;
        --blue: #2563EB;
        --input-border: #CBD5E1;
        --line: #E2E8F0;
    }
    .stApp {
        background: var(--page);
        color: var(--text);
    }
    [data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child {
        background: var(--sidebar);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text);
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }
    [data-testid="stSidebar"] .st-key-new-chat button {
        background: var(--blue);
        border: 1px solid var(--blue);
        color: #FFFFFF;
    }
    [data-testid="stSidebar"] .st-key-new-chat button:hover {
        background: #1D4ED8;
        border-color: #1D4ED8;
        color: #FFFFFF;
    }
    [data-testid="stSidebar"] button {
        background: #FFFFFF;
        border: 1px solid var(--line);
        color: var(--text);
    }
    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.8rem;
        background: var(--chat);
        color: var(--text);
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h4,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] blockquote {
        color: var(--text);
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: var(--user-chat);
    }
    [data-testid="stChatMessage"] table {
        color: var(--text);
        border-color: var(--line);
    }
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] td {
        color: var(--text);
        border-color: var(--line);
        background: var(--chat);
    }
    [data-testid="stChatMessage"] pre {
        background: #F1F5F9;
        border: 1px solid var(--line);
        border-radius: 8px;
    }
    [data-testid="stChatMessage"] pre code,
    [data-testid="stChatMessage"] code {
        color: #172033;
    }
    [data-testid="stChatInput"] {
        background: var(--chat);
        border: 1px solid var(--input-border);
        border-radius: 14px;
        z-index: 2;
    }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus {
        background: var(--chat);
        color: var(--text);
        -webkit-text-fill-color: var(--text);
        caret-color: var(--text);
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--muted);
        -webkit-text-fill-color: var(--muted);
        opacity: 1;
    }
    [data-testid="stChatInput"] button {
        background: var(--blue);
        color: #FFFFFF;
        border: 1px solid var(--blue);
    }
    [data-testid="stChatInput"] button svg {
        fill: #FFFFFF;
        color: #FFFFFF;
    }
    [data-testid="stChatInput"] button:hover {
        background: #1D4ED8;
        color: #FFFFFF;
    }
    .stApp [data-testid="stMarkdownContainer"] {
        color: var(--text);
    }
    .stApp [data-testid="stCaptionContainer"],
    .stApp small {
        color: var(--muted);
    }
    .stApp input,
    .stApp textarea {
        background: var(--chat);
        color: var(--text);
        border-color: var(--input-border);
    }
    .stApp input::placeholder,
    .stApp textarea::placeholder {
        color: var(--muted);
        opacity: 1;
    }
    .stApp button {
        color: var(--text);
    }
    .stApp [data-testid="stAlert"] {
        color: var(--text);
    }
    .block-container {
        padding-bottom: 7rem;
    }
    .app-header {
        padding: 0.4rem 0 1.1rem;
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.5rem;
    }
    .app-header h1 {
        color: var(--text);
        font-size: 1.9rem;
        margin: 0;
    }
    .app-header p {
        color: var(--muted);
        margin: 0.35rem 0 0;
        font-size: 1.02rem;
    }
    .welcome-card {
        background: linear-gradient(135deg, #F8FAFC, #EFF6FF);
        border: 1px solid #dbeafe;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .welcome-card h2 {
        color: var(--text);
        margin: 0 0 0.4rem;
    }
    .welcome-card p {
        color: var(--muted);
        margin: 0;
    }
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-bottom: 6rem;
        }
        .app-header h1 {
            font-size: 1.45rem;
        }
        [data-testid="stChatMessage"] {
            padding: 0.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def create_chat() -> dict:
    return {"id": uuid.uuid4().hex, "title": "New chat", "messages": []}


if "chats" not in st.session_state:
    st.session_state.chats = [create_chat()]
    st.session_state.active_chat_id = st.session_state.chats[0]["id"]
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def active_chat() -> dict:
    for chat in st.session_state.chats:
        if chat["id"] == st.session_state.active_chat_id:
            return chat
    chat = create_chat()
    st.session_state.chats.append(chat)
    st.session_state.active_chat_id = chat["id"]
    return chat


with st.sidebar:
    st.markdown("# 📘 FinSight AI")
    st.caption("Company Policy Assistant")
    if st.button(
        "＋  New chat",
        key="new-chat",
        use_container_width=True,
        type="primary",
    ):
        chat = create_chat()
        st.session_state.chats.append(chat)
        st.session_state.active_chat_id = chat["id"]
        st.rerun()

    st.markdown("### Chat history")
    previous_chats = [
        chat
        for chat in reversed(st.session_state.chats)
        if chat["messages"] and chat["id"] != st.session_state.active_chat_id
    ]
    if not previous_chats:
        st.caption("Your conversations will appear here.")
    for chat in previous_chats:
        if st.button(
            chat["title"],
            key=f"history-{chat['id']}",
            use_container_width=True,
        ):
            st.session_state.active_chat_id = chat["id"]
            st.rerun()

    st.divider()
    st.markdown("### About")
    st.caption(
        "Ask questions about company policies. Answers are grounded in the "
        "documents in the connected knowledge base."
    )
    st.markdown("**Knowledge base**")
    st.caption(KNOWLEDGE_BASE_NAME)


chat = active_chat()
st.markdown(
    """
    <div class="app-header">
      <h1>FinSight AI - Company Policy Assistant</h1>
      <p>Your intelligent company policy assistant.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not chat["messages"]:
    st.markdown(
        """
        <div class="welcome-card">
          <h2>How can I help you today?</h2>
          <p>Ask a question about the company policy handbook to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    examples = [
        "Explain the company policies.",
        "What are the employee responsibilities?",
        "Explain the leave policy.",
        "What are the company compliance guidelines?",
    ]
    example_columns = st.columns(2)
    for index, example in enumerate(examples):
        if example_columns[index % 2].button(
            example, key=f"example-{index}", use_container_width=True
        ):
            st.session_state.pending_question = example
            st.rerun()

for message in chat["messages"]:
    with st.chat_message(message["role"]):
        if message.get("error"):
            st.error(message["content"])
        else:
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        location = source["file"]
                        if source["page"] is not None:
                            location += f" · Page {source['page']}"
                        st.markdown(f"**{location}**")
                        if source["excerpt"]:
                            st.caption(source["excerpt"])

question = st.session_state.pending_question
st.session_state.pending_question = None
if question is None:
    question = st.chat_input("Ask a question about company policies...")

if question and question.strip():
    question = question.strip()
    chat["messages"].append({"role": "user", "content": question})
    if chat["title"] == "New chat":
        chat["title"] = question[:42] + ("..." if len(question) > 42 else "")

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the policy knowledge base..."):
            try:
                result = get_answer(question)
                answer = result["answer"]
                sources = result["sources"]
                st.markdown(answer)
                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            location = source["file"]
                            if source["page"] is not None:
                                location += f" · Page {source['page']}"
                            st.markdown(f"**{location}**")
                            if source["excerpt"]:
                                st.caption(source["excerpt"])
                chat["messages"].append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
            except Exception as exc:
                error = f"Unable to generate an answer: {exc}"
                st.error(error)
                chat["messages"].append(
                    {"role": "assistant", "content": error, "error": True}
                )
