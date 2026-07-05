%%writefile streamlit_chat_app.py
import streamlit as st
import os
from google import genai

st.set_page_config(
    page_title="Data Analyst AI Assistant",
    page_icon="📊",
    layout="wide"
)

SYSTEM_PROMPT = """Kamu adalah Senior Data Analyst AI Assistant yang berpengalaman lebih dari 10 tahun.

Keahlianmu meliputi:
- SQL (PostgreSQL, MySQL, BigQuery) — query, optimasi, joins, subquery, window function
- Python untuk analisis data (pandas, numpy, matplotlib, seaborn, plotly)
- Microsoft Excel & Google Sheets (rumus, pivot table, VLOOKUP, dashboard)
- Visualisasi data (Tableau, Power BI, Looker Studio)
- Statistik dasar dan lanjutan (mean, median, regresi, korelasi, uji hipotesis)
- Data cleaning, EDA (Exploratory Data Analysis), dan storytelling dengan data

Cara kamu menjawab:
- Selalu gunakan Bahasa Indonesia yang jelas dan mudah dipahami
- Berikan contoh kode atau rumus yang konkret jika relevan
- Jelaskan konsep secara bertahap untuk pemula
- Jika ada beberapa cara, jelaskan kelebihan dan kekurangan masing-masing
- Selalu berikan konteks bisnis agar jawaban terasa relevan dan praktis
- Gunakan emoji secara wajar untuk membuat jawaban lebih mudah dibaca

Jika pertanyaan di luar bidang data analyst, kamu bisa menjawab secara umum,
tapi ingatkan pengguna bahwa spesialisasimu adalah di dunia data."""

google_api_key = os.environ.get("GOOGLE_API_KEY")

if not google_api_key:
    st.error("❌ GOOGLE_API_KEY tidak ditemukan.")
    st.stop()

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/data-configuration.png", width=80)
    st.title("📊 Data Analyst\nAI Assistant")
    st.caption("Powered by Google Gemini")
    st.divider()
    st.markdown("**🧠 Topik yang bisa ditanyakan:**")
    st.markdown("""
- 🗄️ SQL & Database
- 🐍 Python (pandas, numpy)
- 📊 Excel & Google Sheets
- 📈 Visualisasi Data
- 📐 Statistik & Probabilitas
- 🔍 EDA & Data Cleaning
- 📋 Tableau & Power BI
""")
    st.divider()
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)
    st.divider()
    st.caption("💡 Tanyakan apa saja seputar dunia Data Analyst!")

st.title("📊 Data Analyst AI Assistant")
st.caption("Asisten AI khusus Data Analyst — SQL, Python, Excel, Statistik, dan Visualisasi Data")
st.divider()

if "genai_client" not in st.session_state:
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
    except Exception as e:
        st.error(f"❌ Gagal terhubung ke Gemini: {e}")
        st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.genai_client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_PROMPT}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
Halo! 👋 Saya **Data Analyst AI Assistant** siap membantu kamu!

| Topik | Contoh Pertanyaan |
|-------|-------------------|
| 🗄️ **SQL** | "Bagaimana cara membuat query JOIN di PostgreSQL?" |
| 🐍 **Python** | "Cara groupby dan agregasi di pandas?" |
| 📊 **Excel** | "Rumus VLOOKUP untuk mencari data?" |
| 📈 **Visualisasi** | "Kapan pakai bar chart vs line chart?" |
| 📐 **Statistik** | "Apa itu p-value dan bagaimana membacanya?" |

Silakan tanyakan apa saja! 😊
""")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Tanyakan seputar SQL, Python, Excel, Statistik, atau Visualisasi Data...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sedang menganalisis..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                answer = response.text if hasattr(response, "text") else str(response)
            except Exception as e:
                answer = f"❌ Terjadi error: {e}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    # ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 13px;'>"
    "© 2025 <b>Muhammad Faturrahman</b> · Data Analyst AI Assistant · "
    "Powered by Google Gemini"
    "</div>",
    unsafe_allow_html=True
)
