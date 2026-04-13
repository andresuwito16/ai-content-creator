import streamlit as st
from openai import OpenAI
import requests
import os
import edge_tts
import asyncio
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

# --- KONFIGURASI API ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Video Pro Creator", layout="wide")
st.title("🎬 AI Video Pro Creator")
st.markdown("Generate video viral dalam hitungan detik!")

# --- SIDEBAR FITUR ---
with st.sidebar:
    st.header("⚙️ Pengaturan Video")
    voice_speed = st.slider("Kecepatan Suara", 0.8, 1.5, 1.0)
    bg_music = st.checkbox("Tambah Musik Latar (Soft)", value=True)
    video_size = st.selectbox("Ukuran Video", ["9:16 (TikTok/Reels)", "16:9 (YouTube)"])

# --- FUNGSI GENERATOR ---
async def generate_voice(text, output_file):
    communicate = edge_tts.Communicate(text, "id-ID-ArdiNeural", rate=f"{'+' if voice_speed>=1 else '-'}{int(abs(voice_speed-1)*100)}%")
    await communicate.save(output_file)

def create_video(image_path, audio_path, script_text, output_path):
    # Load audio untuk durasi
    audio = AudioFileClip(audio_path)
    
    # Buat clip gambar sesuai durasi audio
    img_clip = ImageClip(image_path).set_duration(audio.duration)
    
    # Efek Zoom In sederhana (agar tidak kaku)
    img_clip = img_clip.resize(lambda t: 1 + 0.02*t) 

    # Tambah Caption Otomatis (Teks di tengah)
    txt_clip = TextClip(script_text, fontsize=40, color='white', font='Arial-Bold', 
                        method='caption', size=(img_clip.w*0.8, None)).set_duration(audio.duration)
    txt_clip = txt_clip.set_position(('center', 'center'))

    # Gabungkan
    video = CompositeVideoClip([img_clip, txt_clip])
    video = video.set_audio(audio)
    video.write_videofile(output_path, fps=24, codec="libx264")

# --- MAIN APP ---
topic = st.text_input("Apa ide konten Anda hari ini?", placeholder="Contoh: 3 Tips hidup bahagia tanpa hutang")

if st.button("PROSES VIDEO SEKARANG 🚀"):
    if topic:
        try:
            # 1. GENERATE NASKAH
            with st.spinner("🤖 AI sedang menulis naskah viral..."):
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Buatkan naskah konten edukasi singkat tentang {topic}. Maksimal 30 kata, bahasa Indonesia yang sangat persuasif."}]
                )
                naskah = res.choices[0].message.content
                st.success("Naskah Berhasil Dibuat!")
                st.write(f"💬 *{naskah}*")

            # 2. GENERATE GAMBAR (DALL-E 3)
            with st.spinner("🎨 Membuat visual sinematik..."):
                img_res = client.images.generate(
                    model="dall-e-3",
                    prompt=f"Cinematic realistic high quality, {topic}, colorful, masterpiece",
                    size="1024x1024"
                )
                img_url = img_res.data[0].url
                img_data = requests.get(img_url).content
                with open("temp_image.png", "wb") as f:
                    f.write(img_data)

            # 3. GENERATE VOICE OVER (Gratis & Natural)
            with st.spinner("🎙️ Mengisi suara narator..."):
                asyncio.run(generate_voice(naskah, "temp_audio.mp3"))

            # 4. RENDERING VIDEO
            with st.spinner("🎬 Menggabungkan semua elemen jadi video..."):
                create_video("temp_image.png", "temp_audio.mp3", naskah, "final_video.mp4")
            
            # TAMPILKAN HASIL
            st.divider()
            st.balloons()
            st.subheader("✅ Video Anda Siap!")
            col1, col2 = st.columns(2)
            with col1:
                st.video("final_video.mp4")
            with col2:
                st.image("temp_image.png", caption="Thumbnail Generasi AI")
                with open("final_video.mp4", "rb") as file:
                    st.download_button("📥 DOWNLOAD VIDEO SEKARANG", file, "video_konten_ai.mp4", "video/mp4")

        except Exception as e:
            st.error(f"Aduh, ada kendala teknik: {e}")
    else:
        st.warning("Silakan isi ide kontennya dulu ya!")
