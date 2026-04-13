import streamlit as st
from openai import OpenAI
import asyncio
import edge_tts
import json

# 1. SETUP API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Storyboard Studio", layout="wide")

# Styling
st.markdown("""
    <style>
    .scene-card { background: #1e2128; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #00ffcc; }
    .stButton>button { width: 100%; background: #00ffcc; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 AI Storyboard Creator")
st.write("Hasil per adegan untuk mempermudah editing manual di CapCut/Premiere.")

# 2. INPUT & SETTING
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    ratio = st.radio("Rasio Gambar:", ["9:16 (TikTok/Reels)", "16:9 (YouTube/Landscape)"])
    num_scenes = st.slider("Jumlah Adegan:", 3, 5, 3)
    tone = st.selectbox("Tone Suara:", ["Inspiratif", "Misterius", "Enerjik"])

topic = st.text_area("Apa ide konten Anda?", placeholder="Contoh: 3 Fakta unik tentang laut terdalam", height=100)

# Mapping Rasio untuk DALL-E
size_map = {
    "9:16 (TikTok/Reels)": "1024x1792",
    "16:9 (YouTube/Landscape)": "1792x1024"
}

if st.button("GENERATE STORYBOARD 🚀"):
    if topic:
        try:
            # --- TAHAP 1: GENERATE STORYBOARD (NASKAH) ---
            with st.spinner("🧠 Merancang adegan..."):
                prompt_script = f"""
                Buatlah storyboard video pendek tentang {topic} sebanyak {num_scenes} adegan.
                Format harus JSON murni tanpa teks lain:
                {{
                  "scenes": [
                    {{
                      "narration": "teks yang dibaca narator",
                      "visual_desc": "deskripsi visual untuk gambar"
                    }}
                  ]
                }}
                PERATURAN: Narasi hanya berisi kalimat yang dibaca (Tanpa label Hook/CTA).
                """
                
                # Menggunakan GPT untuk struktur JSON
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=[{"role": "user", "content": prompt_script}],
                    response_format={ "type": "json_object" }
                )
                storyboard = json.loads(response.choices[0].message.content)

            # --- TAHAP 2: PROSES PER ADEGAN ---
            st.divider()
            for i, scene in enumerate(storyboard['scenes']):
                st.markdown(f"### 🎬 Adegan {i+1}")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Generate Gambar
                    with st.spinner(f"🎨 Membuat Gambar {i+1}..."):
                        img_res = client.images.generate(
                            model="dall-e-3",
                            prompt=f"Cinematic, {scene['visual_desc']}, highly detailed, no text",
                            size=size_map[ratio],
                            quality="standard"
                        )
                        st.image(img_res.data[0].url, use_column_width=True)
                
                with col2:
                    # Tampilkan Narasi
                    st.markdown(f'<div class="scene-card">{scene["narration"]}</div>', unsafe_allow_html=True)
                    
                    # Generate Audio per Adegan
                    voice_name = "voice_scene_" + str(i) + ".mp3"
                    communicate = edge_tts.Communicate(scene["narration"], "id-ID-ArdiNeural")
                    asyncio.run(communicate.save(voice_name))
                    
                    with open(voice_name, "rb") as f:
                        st.audio(f.read(), format="audio/mp3")
                    
                    st.download_button(f"📥 Download Audio {i+1}", open(voice_name, "rb"), voice_name)

            st.balloons()
            st.success("✅ Storyboard Selesai! Silakan download aset per adegan untuk disatukan di CapCut.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Isi topiknya dulu!")
