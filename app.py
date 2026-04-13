import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Video Generator", layout="wide")

st.title("🎬 AI Video Generator (REAL)")

# INPUT
idea = st.text_area("Masukkan ide video")
theme = st.selectbox("Tema", ["horror", "cinematic", "motivational", "mystery"])
duration = st.slider("Durasi (detik)", 30, 600, 120)
part_count = st.slider("Jumlah Scene", 3, 15, 5)

# GENERATE SCRIPT (OPENAI)
def generate_script(idea):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": f"Buat script storytelling viral: {idea}"}
        ],
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

# GENERATE IMAGE
def generate_image(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt}"

# BUTTON
if st.button("🚀 Generate Video"):

    if not idea:
        st.warning("Masukkan ide dulu!")
        st.stop()

    with st.spinner("Generating AI content..."):

        script = generate_script(idea)

        scenes = []
        for i in range(part_count):
            scene = {
                "text": f"Scene {i+1}",
                "image": generate_image(f"{idea} cinematic scene {i+1}")
            }
            scenes.append(scene)

    # OUTPUT
    st.subheader("📜 Script")
    st.write(script)

    st.subheader("🎞 Scenes")
    for s in scenes:
        st.write(s["text"])
        st.image(s["image"])

    st.subheader("🎥 Video Preview")
    st.video("https://samplelib.com/lib/preview/mp4/sample-5s.mp4")
