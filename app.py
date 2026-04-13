import streamlit as st
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="AI Content Master", page_icon="🎬", layout="centered")

# Custom CSS agar tampilan lebih mewah
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        color: #1E1E1E;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="main-header">🚀 AI Content Factory</p>', unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Ubah ide mentah menjadi video siap posting dalam hitungan detik.</p>", unsafe_allow_html=True)
st.divider()

# --- INPUT USER ---
col1, col2 = st.columns([2, 1])

with col1:
    user_idea = st.text_area("Apa ide konten Anda?", placeholder="Contoh: 3 Tips rahasia sukses jualan online...", height=120)

with col2:
    theme = st.selectbox("Pilih Tema/Vibe", ["Edukasi Pro", "Horor Mencekam", "Komedi Santai", "Motivasi Kuat"])
    platform = st.radio("Format Video", ["TikTok/Shorts (9:16)", "YouTube (16:9)"])

# --- TOMBOL PROSES ---
if st.button("MULAI GENERATE KONTEN ✨"):
    if not user_idea:
        st.error("Silakan isi ide konten terlebih dahulu!")
    else:
        # Progress Bar ala website profesional
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Simulasi Tahap 1: Naskah
        status_text.text("🤖 AI sedang merangkai narasi...")
        time.sleep(2) # Simulasi proses AI
        progress_bar.progress(30)

        # Simulasi Tahap 2: Suara
        status_text.text("🎙️ Mengonversi teks menjadi suara natural...")
        time.sleep(2)
        progress_bar.progress(60)

        # Simulasi Tahap 3: Gambar & Video
        status_text.text("🎨 Membuat visual dan menggabungkan video...")
        time.sleep(2)
        progress_bar.progress(100)
        
        status_text.success("🎉 Konten Anda Selesai!")

        # --- TAMPILAN HASIL ---
        st.divider()
        st.subheader("Hasil Produksi AI")
        
        tab1, tab2, tab3 = st.tabs(["📺 Preview Video", "📜 Naskah", "🎙️ Audio"])
        
        with tab1:
            st.info("Video hasil gabungan gambar, subtitle, dan voice-over akan muncul di sini.")
            # st.video("hasil_video.mp4") # Un-comment jika file sudah siap

        with tab2:
            st.write(f"**Narasi ({theme}):**")
            st.write("Ini adalah draf narasi yang dihasilkan berdasarkan ide Anda...")
            st.button("Salin Naskah")

        with tab3:
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Contoh audio
            st.download_button("Download Audio", "data", file_name="vo_konten.mp3")
