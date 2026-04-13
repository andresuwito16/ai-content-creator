import streamlit as st
from openai import OpenAI
import requests
import asyncio
import edge_tts

# 1. Koneksi API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Konfigurasi Halaman
st.set_page_config(page_title="AI Video Creator Pro", layout="wide")

st.title("🎬 AI Content Generator Pro")
st.caption("Ubah ide jadi naskah narasi dan visual estetik tanpa label pengganggu.")

# 3. Input User
topic = st.text_input("Apa ide konten Anda?", placeholder="Contoh: Manfaat bangun jam 5 pagi")

if st.button("MULAI GENERATE KONTEN ✨"):
    if topic:
        try:
            # --- BAGIAN 1: GENERATE NASKAH BERSIH ---
            with st.spinner("🧠 Meracik naskah narasi..."):
                prompt_naskah = f"""
                Buat naskah video pendek viral tentang {topic}. 
                PERATURAN KETAT:
                - Tuliskan LANGSUNG kalimat yang harus dibaca narator.
                - JANGAN sertakan label seperti 'Hook', 'Content', 'CTA', atau angka.
                - JANGAN berikan penjelasan atau tanda kurung.
                - Gunakan bahasa Indonesia yang santai dan estetik.
                Maksimal 50 kata.
                """
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": prompt_naskah}]
                )
                naskah = res.choices[0].message.content

            # --- BAGIAN 2: GENERATE GAMBAR HD ---
            with st.spinner("🎨 Membuat visual sinematik..."):
                img_res = client.images.generate(
                    model="dall-e-3",
                    prompt=f"Cinematic realistic high quality, {topic}, colorful, masterpiece, no text",
                    size="1024x1024"
                )
                img_url = img_res.data[0].url

            # --- BAGIAN 3: GENERATE SUARA ---
            with st.spinner("🎙️ Mengisi suara narator..."):
                voice_file = "voice.mp3"
                communicate = edge_tts.Communicate(naskah, "id-ID-ArdiNeural")
                asyncio.run(communicate.save(voice_file))

            # --- TAMPILAN HASIL ---
            st.divider()
            col1, col2 = st.columns([1, 1])

            with col1:
                st.image(img_url, use_column_width=True, caption="Visual Asset")
                with open(voice_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
            
            with col2:
                st.markdown("### 📝 Naskah Narasi (Siap Pakai)")
                st.success(naskah)
                st.info("💡 **Tips:** Gabungkan gambar dan suara ini di CapCut, lalu gunakan fitur 'Auto Captions' agar teks muncul otomatis di layar.")

        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {e}")
    else:
        st.warning("Silakan masukkan topik terlebih dahulu!")
