import streamlit as st
from openai import OpenAI
import requests
import asyncio
import edge_tts

# --- CONFIG ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

st.set_page_config(page_title="AI Video Maker Pro", layout="wide")

# CSS untuk tampilan ala aplikasi mahal
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #ff4b4b; color: white; }
    .content-box { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 AI Content Generator Pro")
st.caption("Ubah ide jadi konten video siap upload (TikTok, Reels, Shorts)")

# --- INPUT AREA ---
with st.container():
    col_a, col_b = st.columns([3, 1])
    with col_a:
        topic = st.text_input("Apa ide konten Anda?", placeholder="Contoh: 3 Alasan kenapa harus investasi emas")
    with col_b:
        style = st.selectbox("Gaya Gambar", ["Cinematic", "Anime", "3D Render", "Cyberpunk"])

if st.button("MULAI GENERATE KONTEN ✨"):
    if topic:
        try:
            # 1. GENERATE NASKAH (GPT-3.5)
            with st.spinner("✍️ Menulis naskah viral..."):
                prompt_naskah = f"Buatkan naskah video pendek viral tentang {topic}. Gunakan hook yang menarik di awal. Maksimal 60 kata. Bahasa Indonesia santai."
                res = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt_naskah}])
                naskah = res.choices[0].message.content

            # 2. GENERATE GAMBAR (DALL-E 3)
            with st.spinner("🎨 Membuat visual berkualitas tinggi..."):
                img_res = client.images.generate(
                    model="dall-e-3",
                    prompt=f"{style} style illustration of {topic}, high resolution, 9:16 aspect ratio feel",
                    size="1024x1024"
                )
                img_url = img_res.data[0].url

            # 3. GENERATE SUARA (Edge-TTS - Gratis & Cepat)
            with st.spinner("🎙️ Mengisi suara narator..."):
                voice_file = "voice.mp3"
                communicate = edge_tts.Communicate(naskah, "id-ID-ArdiNeural")
                asyncio.run(communicate.save(voice_file))

            # --- DISPLAY HASIL (Layout Editor) ---
            st.divider()
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 🖼️ Visual & Audio")
                st.image(img_url, use_column_width=True)
                with open(voice_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
            
            with col2:
                st.markdown("### 📝 Naskah Konten")
                st.info(naskah)
                st.success("✅ Konten siap digabungkan!")
                st.write("💡 **Tips:** Gunakan aplikasi CapCut, masukkan gambar ini dan tambahkan audionya. Gunakan fitur 'Auto Captions' di CapCut untuk hasil video paling pro!")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Masukkan ide dulu!")
