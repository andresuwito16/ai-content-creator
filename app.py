# 1. GENERATE NASKAH (TANPA LABEL)
            with st.spinner("🧠 Meracik naskah bersih..."):
                prompt_naskah = f"""
                Buat naskah video pendek viral tentang {topic}. 
                PERATURAN KETAT:
                - Tuliskan LANGSUNG kalimat yang harus dibaca narator.
                - JANGAN sertakan label seperti 'Hook', 'Content', 'CTA', atau angka 1, 2, 3.
                - JANGAN berikan penjelasan atau tanda kurung.
                - Gunakan bahasa Indonesia yang santai dan estetik.
                - Alur: Kalimat pembuka yang bikin kaget, inti pesan, lalu ajakan follow di akhir.
                Maksimal 50 kata.
                """
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": prompt_naskah}]
                )
                naskah = res.choices[0].message.content
