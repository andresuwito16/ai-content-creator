import streamlit as st
from openai import OpenAI
import requests

# Ambil Key dari Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

st.title("AI Video Content Creator 🎬")

topic = st.text_input("Masukkan Ide Konten:", placeholder="Contoh: Tips menanam cabe")

if st.button("MULAI GENERATE KONTEN ✨"):
    if topic:
        try:
            # 1. Generate Naskah
            st.info("Membuat naskah... ✍️")
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Buatkan naskah video pendek viral tentang {topic}. Maksimal 50 kata, bahasa Indonesia santai."}]
            )
            naskah = completion.choices[0].message.content
            st.subheader("Naskah AI:")
            st.write(naskah)

            # 2. Generate Suara
            st.info("Mengisi suara... 🎙️")
            voice_url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
            data = {"text": naskah, "model_id": "eleven_multilingual_v2"}
            
            audio_req = requests.post(voice_url, json=data, headers=headers)
            if audio_req.status_code == 200:
                st.audio(audio_req.content, format='audio/mp3')
            else:
                st.error("Gagal di ElevenLabs. Cek API Key atau Kuota gratis Anda.")

            # 3. Generate Gambar
            st.info("Membuat gambar... 🎨")
            img_gen = client.images.generate(
                model="dall-e-2",
                prompt=f"Realistic photo of {topic}",
                n=1,
                size="1024x1024"
            )
            st.image(img_gen.data[0].url)

        except Exception as e:
            st.error(f"Pesan Error: {e}")
    else:
        st.warning("Isi dulu topiknya!")
