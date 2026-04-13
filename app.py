import streamlit as st
from openai import OpenAI
import asyncio
import edge_tts
import os

# 1. SETUP API & CONFIG
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Studio: Video Pro", layout="wide")

# CSS Styling untuk tampilan premium
st.markdown("""
    <style>
    .stApp { background: #0f1116; color: white; }
    .stButton>button { background: linear-gradient(45deg, #ff4b4b, #ff8181); color: white; border: none; font-weight: bold; border-radius: 10px; }
    .script-box { background: #1e2128; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 AI Video Studio: Ultra Edition")
st.write("Ubah ide sederhana menjadi aset video berkelas dalam hitungan detik.")

# 2. SIDEBAR UNTUK SETTING PRO
with st.sidebar:
    st.header("🎨 Pengaturan Video")
    tone = st.selectbox("Pilih Nada Video", ["Inspiratif & Semangat", "Sedih & Emosional", "Misterius & Dark", "Edukasi Santai"])
    target = st.selectbox("Target Audiens", ["Umum", "Gen Z (Viral)", "Profesional/Bisnis"])
    model_ai = st.selectbox("Kualitas Gambar", ["Standard", "HD Sinematik"])

# 3. AREA INPUT
topic = st.text_area("Apa ide besar konten Anda?", placeholder="Contoh: Rahasia orang sukses yang tidak pernah dibagikan di sekolah...", height=100)

if st.button("GENERATE KONTEN PREMIUM 🚀"):
    if topic:
        try:
            # --- TAHAP 1: GENERATE NASKAH BERSIH (THE CORE) ---
            with st.spinner("🧠 AI sedang menyusun narasi viral..."):
                prompt_naskah = f"""
                Tulis naskah narasi video pendek tentang {topic}.
                Target Audiens: {target}.
                Nada Bicara: {tone}.
                
                PERATURAN KETAT:
                1. Tuliskan LANGSUNG kalimat yang harus dibaca narator.
                2. JANGAN pakai label 'Hook', 'CTA', 'Scene', atau tanda kurung.
                3. JANGAN pakai angka list.
                4. Bahasa Indonesia yang natural dan tidak kaku.
                5. Berikan alur yang emosional dan bikin orang penasaran.
                Maksimal 60 kata.
                """
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": prompt_naskah}]
                )
                naskah = res.choices[0].message.content

            # --- TAHAP 2: GENERATE VISUAL (DALL-E 3) ---
            with st.spinner("📸 Memotret visual estetik..."):
                visual_prompt = f"Professional cinematography, {topic}, {tone} atmosphere, highly detailed, 4k, realistic lighting, no text."
                img_res = client.images.generate(
                    model="dall-e-3",
                    prompt=visual_prompt,
                    size="1024x1024",
                    quality="hd" if model_ai == "HD Sinematik" else "standard"
                )
                img_url = img_res.data[0].url

            # --- TAHAP 3: GENERATE SUARA (NADA SESUAI PILIHAN) ---
            with st.spinner("🎙️ Mengisi suara narator..."):
                voice_file = "final_voice.mp3"
                # Mengatur kecepatan berdasarkan nada
                speed = "+10%" if tone == "Inspiratif & Semangat" else "-5%"
                communicate = edge_tts.Communicate(naskah, "id-ID-ArdiNeural", rate=speed)
                asyncio.run(communicate.save(voice_file))

            # --- TAHAP 4: DISPLAY HASIL ---
            st.divider()
            col1, col2 = st.columns([1, 1.2])

            with col1:
                st.image(img_url, caption="Visual Asset Generasi AI", use_column_width=True)
                with open(voice_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                st.download_button("📥 Download Suara", open(voice_file, "rb"), "narasi_ai.mp3")

            with col2:
                st.markdown("### 📝 Naskah Narasi")
                st.markdown(f'<div class="script-box">{naskah}</div>', unsafe_allow_html=True)
                
                st.success("✅ Aset Video Selesai Dibuat!")
                st.info("💡 **Tips Editor:** Masukkan gambar ke aplikasi editing (seperti CapCut), pasang audio ini, dan nyalakan fitur 'Auto Captions' untuk hasil yang sempurna.")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Silakan tulis ide topiknya dulu ya!")
