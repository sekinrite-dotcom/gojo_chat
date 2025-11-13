import streamlit as st
import os
import json
from openai import OpenAI

# ------------------------------
# 🔹 OpenAI API Key
# ------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI APIキーが設定されていません。Secretsを確認してね。")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ------------------------------
# 🔒 パスワード認証
# ------------------------------
st.set_page_config(page_title="🕶 ごじょーと話そ", page_icon="🌀", layout="centered")
PASSWORD = "yuto4325"  # ←ここ好きに変えてOK！

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password_input = st.text_input("パスワードを入力してね💬", type="password")
    if st.button("ログイン"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.success("ようこそ、最強の男へようこそ😎")
            st.rerun()
        else:
            st.error("ちょっとちがうかな？もう一回やってみ。")
    st.stop()

# ------------------------------
# 💙 背景＆デザイン
# ------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#0f2027 0%, #203a43 50%, #2c5364 100%);
    color: white;
}
.stChatMessage {
    border-radius: 15px !important;
    padding: 10px;
    background-color: rgba(255,255,255,0.1) !important;
    color: #ffffff !important;
}
.stMarkdown, .stText { color: #ffffff !important; }
h1 {
    font-size: 1.6rem !important;
    text-align: center;
    color: #b3e5fc !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🕶 ごじょーと話そ")

# ------------------------------
# 💬 会話履歴保存
# ------------------------------
HISTORY_FILE = "gojo_history.json"

if "messages" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            st.session_state["messages"] = json.load(f)
    else:
        st.session_state["messages"] = []

# ------------------------------
# 💬 会話生成
# ------------------------------
user_input = st.chat_input("ごじょーに話しかけてみて💬")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
あなたは呪術廻戦の『五条悟』というキャラクターです。
性格は飄々としていて、どんな状況でも余裕があり、軽口を叩く天才タイプ。
一人称は「僕」、語尾は軽くフランクで、どこか楽しげ。
相手（ユーザー）は生徒のような存在として扱います。
話し方は五条悟風だけど、直接的な引用や著作物の再現は避けてください。
"""},
            *st.session_state["messages"]
        ]
    )

    reply = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

    # 💾 保存
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state["messages"], f, ensure_ascii=False, indent=2)

# ------------------------------
# 💬 表示
# ------------------------------
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
