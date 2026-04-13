import streamlit as st
import openai
import requests

# Konfigurasi API dari Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]

st.title("AI Video Content Creator 🎬")
st.markdown("Aplikasi pembuat naskah, suara, dan gambar otomatis.")

topic = st.text_input("Masukkan Ide Konten:", placeholder="Contoh: Tips diet sehat")

if st.button("MULAI GENERATE KONTEN ✨"):
    if topic:
        try:
            # 1. GENERATE NASKAH (OpenAI)
            st.info("Sedang memikirkan naskah... 🤔")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Buatkan naskah video pendek viral tentang {topic}. Maksimal 50 kata, bahasa santai."}]
            )
            naskah = response.choices[0].message.content
            st.subheader("Naskah AI:")
            st.write(naskah)

            # 2. GENERATE SUARA (ElevenLabs)
            st.info("Sedang mengubah naskah jadi suara... 🎙️")
            voice_url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" # Suara 'Rachel'
            headers = {"xi-api-key": ELEVENLABS_API_KEY}
            data = {"text": naskah, "model_id": "eleven_multilingual_v2"}
            
            audio_response = requests.post(voice_url, json=data, headers=headers)
            if audio_response.status_code == 200:
                st.audio(audio_response.content, format='audio/mp3')
            else:
                st.error("Gagal generate suara. Cek ElevenLabs Key Anda.")

            # 3. GENERATE GAMBAR (DALL-E)
            st.info("Sedang membuat gambar ilustrasi... 🎨")
            img_response = openai.Image.create(
                prompt=f"Cinematic realistic illustration for: {topic}",
                n=1,
                size="1024x1024"
            )
            st.image(img_response['data'][0]['url'], caption="Ilustrasi Visual")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Masukkan ide konten dulu ya!")
