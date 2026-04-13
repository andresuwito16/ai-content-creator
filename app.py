import streamlit as st
from openai import OpenAI
import requests
import asyncio
import edge_tts

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Video Studio Pro", layout="wide")

# UI Styling
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stTextArea textarea { font-size: 1.2rem !important; }
    .css-1n76uvr { border-radius: 20px; border: 1px solid #333; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 AI Video Studio: High-Quality Edition")
st.write("Membuat aset video dengan kualitas estetik tinggi untuk TikTok/Reels.")

topic = st.text_input("Apa topik besar video Anda?", placeholder="Contoh: Gelapnya sisi lain dunia kerja")

if st.button("PROSES KONTEN PREMIUM 🚀"):
    if topic:
        try:
            # 1. GENERATE NASKAH DENGAN STRUKTUR VIRAL
            with st.spinner("🧠 Meracik naskah dengan Hook, Story, dan CTA..."):
                prompt_naskah = f"""
                Buat naskah video pendek tentang {topic}. 
                Bagi jadi 3 bagian:
                1. HOOK: Kalimat mengejutkan untuk 3 detik pertama.
                2. CONTENT: Inti pesan yang emosional/edukatif.
                3. CTA: Ajakan follow yang halus.
                Total maksimal 50 kata. Bahasa Indonesia gaul/estetik.
                """
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt_naskah}])
                naskah = res.choices[0].message.content

            # 2. GENERATE GAMBAR SINEMATIK (DALL-E 3)
            with st.spinner("📸 Memotret visual sinematik 4K..."):
                # Kita minta DALL-E buat gambar yang sangat detail
                img_res = client.images.generate(
                    model="dall-e-3",
                    prompt=f"Cinematic wide shot, highly detailed, realistic, atmospheric lighting, professional photography for: {topic}. No text in image.",
                    size="1024x1024",
                    quality="hd"
                )
                img_url = img_res.data[0].url

            # 3. GENERATE SUARA (Ardi Neural - Natural)
            with st.spinner("🎙️ Rekaman suara narator..."):
                voice_file = "pro_voice.mp3"
                communicate = edge_tts.Communicate(naskah, "id-ID-ArdiNeural", rate="+5%")
                asyncio.run(communicate.save(voice_file))

            # --- DISPLAY HASIL ---
            st.divider()
            
            col1, col2 = st.columns([1, 1.2])
            
            with col1:
                st.image(img_url, caption="Visual Asset (HD)", use_column_width=True)
                with open(voice_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                st.download_button("📥 Download Suara", open(voice_file, "rb"), "audio.mp3")

            with col2:
                st.subheader("📝 Script Storyboard")
                st.markdown(f"> {naskah}")
                
                st.info("💡 **Cara Edit Biar Setara Pro:**\n"
                        "1. Masukkan gambar ke CapCut.\n"
                        "2. Tambahkan audio di atas.\n"
                        "3. Gunakan 'Keyframe' pada gambar agar bergerak perlahan (Slow Zoom).\n"
                        "4. Tambahkan 'Auto Captions' dengan font 'The Bold Font'.\n"
                        "5. Tambahkan background music 'Sad Cinematic' atau 'Phonk' dengan volume 10%.")

        except Exception as e:
            st.error(f"Error: {e}")
