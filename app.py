import streamlit as st
from openai import OpenAI
import asyncio
import edge_tts
import json

# 1. SETUP API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Pro Content Studio", layout="wide")

# CSS untuk memperbaiki tampilan gambar agar sesuai Rasio
st.markdown("""
    <style>
    .scene-container { background: #111; padding: 30px; border-radius: 20px; margin-bottom: 50px; border: 1px solid #333; }
    .narration-text { font-size: 1.1rem; line-height: 1.8; color: #e0e0e0; background: #222; padding: 20px; border-radius: 10px; }
    img { border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); object-fit: cover; }
    .stButton>button { background: #ff4b4b; color: white; height: 3em; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎥 Pro AI Storyboard Studio")
st.write("Generasi konten mendalam dengan narasi panjang dan visual presisi.")

# 2. KONFIGURASI
with st.sidebar:
    st.header("🎬 Video Settings")
    ratio = st.selectbox("Pilih Rasio Video:", ["9:16 (TikTok/Reels/Shorts)", "16:9 (YouTube/Landscape)"])
    num_scenes = st.slider("Jumlah Adegan:", 2, 4, 3)
    voice_speed = st.slider("Kecepatan Suara:", 0.8, 1.2, 1.0)

topic = st.text_area("Topik/Ide Mendalam:", placeholder="Contoh: Mengapa kesehatan mental lebih penting dari sekadar kesuksesan finansial?", height=120)

# Mapping Resolusi DALL-E 3
size_map = {
    "9:16 (TikTok/Reels/Shorts)": "1024x1792",
    "16:9 (YouTube/Landscape)": "1792x1024"
}

if st.button("MULAI PRODUKSI KONTEN 🚀"):
    if topic:
        try:
            # --- TAHAP 1: GENERATE NASKAH PANJANG ---
            with st.spinner("✍️ Menyusun narasi mendalam (2 paragraf per adegan)..."):
                prompt_script = f"""
                Buatlah storyboard video untuk topik: {topic}.
                Buatlah {num_scenes} adegan.
                Setiap adegan WAJIB memiliki narasi minimal 2 paragraf panjang (sekitar 80-100 kata per adegan).
                
                Format JSON:
                {{
                  "scenes": [
                    {{
                      "narration": "Paragraf 1... Paragraf 2...",
                      "visual_prompt": "Deskripsi visual detail"
                    }}
                  ]
                }}
                PERATURAN: Narasi harus bersih tanpa label teknis. Bahasa Indonesia formal-estetik.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o", # Menggunakan GPT-4o untuk hasil naskah lebih cerdas
                    messages=[{"role": "user", "content": prompt_script}],
                    response_format={ "type": "json_object" }
                )
                storyboard = json.loads(response.choices[0].message.content)

            # --- TAHAP 2: DISPLAY & GENERATE ---
            for i, scene in enumerate(storyboard['scenes']):
                st.markdown(f"## 🎞️ ADEGAN {i+1}")
                
                # Layout Kolom Berdasarkan Rasio
                if "9:16" in ratio:
                    col_img, col_txt = st.columns([1, 1.5]) # Gambar vertikal butuh ruang lebih sempit
                else:
                    col_img, col_txt = st.columns([1.5, 1]) # Gambar horizontal butuh ruang lebih lebar

                with col_img:
                    with st.spinner(f"🎨 Generating Visual {i+1}..."):
                        img_res = client.images.generate(
                            model="dall-e-3",
                            prompt=f"Cinematic realistic, {scene['visual_prompt']}, masterpiece, 8k, lighting dramatic, no text",
                            size=size_map[ratio],
                            quality="hd"
                        )
                        st.image(img_res.data[0].url)

                with col_txt:
                    st.markdown(f'<div class="narration-text">{scene["narration"]}</div>', unsafe_allow_html=True)
                    
                    # Generate Suara
                    voice_file = f"audio_scene_{i}.mp3"
                    v_rate = f"{'+' if voice_speed >= 1 else '-'}{int(abs(voice_speed-1)*100)}%"
                    communicate = edge_tts.Communicate(scene["narration"], "id-ID-ArdiNeural", rate=v_rate)
                    asyncio.run(communicate.save(voice_file))
                    
                    st.audio(voice_file)
                    st.download_button(f"📥 Simpan Audio {i+1}", open(voice_file, "rb"), voice_file)
                
                st.divider()

            st.balloons()
            st.success("✅ Semua aset telah siap! Silakan gabungkan di aplikasi editor favorit Anda.")

        except Exception as e:
            st.error(f"Terjadi Kendala: {e}")
    else:
        st.warning("Mohon isi topiknya terlebih dahulu.")
