import streamlit as st
from database import cf_pakar

def get_major_indikator(kode_penyakit):
    return [
        item["nama"]

        for item in st.session_state.semua_indikator
        if (
            item["match"]
            and item["kode"] in cf_pakar[kode_penyakit]
            and cf_pakar[kode_penyakit][item["kode"]] == 0.8
        )
    ]

def show_hasil_page(pindah_halaman):
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_kiri, col_kanan = st.columns([7, 3.2], gap="large")
    with col_kiri:
        if st.session_state.hasil:

            top = st.session_state.hasil[0]
            matched_gejala = get_major_indikator(top["kode"])
                            
            # KARTU HASIL UTAMA
            st.markdown(f"""
            <div class="hasil-main-card">
                <div style="flex: 1;">
                    <p style="font-size: 11px; font-weight: 800; color: #64748B; letter-spacing: 1px; margin-bottom: 5px;">HASIL PREDIKSI UTAMA</p>
                    <h1 style="color: #1E293B; margin-top: 0px; margin-bottom: 10px; font-size: 38px; font-weight: 800;">{top['nama']}</h1>
                    <p style="color: #475569; font-size: 14px; line-height: 1.6; margin-bottom: 0px;">
                        Pasien menunjukkan gejala klinis yang secara signifikan berkorelasi dengan pola penyakit <b>{top['nama']}</b> berdasarkan perhitungan algoritma Certainty Factor.
                    </p>
                    <div class="indikator-section"><div class="indikator-title">INDIKATOR UTAMA TERDETEKSI:</div>
                    <div class="indikator-list">{"".join([
                                f"""<div class='indikator-chip'><span>{g}</span></div>"""
                                for g in matched_gejala
                            ])
                        }
                    </div>
                </div>
                </div>
                <div class="hasil-score-box">
                    <h2 style="color: #0369A1; font-size: 36px; font-weight: 800; margin: 0px;">{top['skor']:.2f}%</h2>
                    <p style="color: #0284C7; font-size: 11px; font-weight: 800; margin: 0px; letter-spacing: 0.5px;">CONFIDENCE</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # KARTU ANALISIS DETAIL (HASIL BANDING)
            st.markdown("<h3 style='color: #1E293B; margin-top: 35px; margin-bottom: 15px; font-size: 18px; font-weight: 700;'>Hasil Pembanding<span style='float:right; color:#94A3B8;'>📊</span></h3>", unsafe_allow_html=True)
            
            # Looping untuk membuat Custom Progress Bar
            for h in st.session_state.hasil[1:]:
                matched_gejala_detail = get_major_indikator(h["kode"])

                st.markdown(f"""
                <div class="hasil-detail-card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="font-weight: 700; color: #1E293B; font-size: 14px;">{h['nama']}</span>
                        <span style="font-weight: 800; color: #0F766E; font-size: 13px;">{h['skor']:.2f}%</span>
                    </div>
                    <div class="custom-progress-bg">
                        <div class="custom-progress-fill" style="width: {int(h['skor'])}%;"></div>
                    </div>
                    <div class="mini-indikator-title">INDIKATOR UTAMA TERDETEKSI:</div>
                    <div class="mini-indikator-list">
                        {
                            "".join([
                                f"""<div class='mini-indikator-item'>● {g}</div>"""
                                for g in matched_gejala_detail
                            ])
                        }
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.markdown(f"""<div class="hasil-main-card gagal-card">
                <div style="flex:1;">
                    <p style="font-size:11px;font-weight:800;color:#64748B;letter-spacing:1px;margin-bottom:5px;">STATUS ANALISIS</p>
                    <h1 style="color:#1E293B;margin-top:0;margin-bottom:14px;font-size:42px;font-weight:800;line-height:1.1;">Hasil Tidak Dapat Disimpulkan</h1>
                    <p style="color:#475569;font-size:15px;line-height:1.8;margin-bottom:0;">
                        Sistem belum menemukan pola indikator klinis yang cukup kuat
                        untuk memenuhi ambang minimum untuk menghasilkan prediksi penyakit ISPA.
                        Confidence seluruh penyakit berada di bawah threshold
                        yang ditetapkan sistem pakar.
                    </p>
                </div>
                <div class="hasil-score-box score-gagal">
                    <h2 style="color:#64748B;font-size:30px;font-weight:800;margin:0;">CF &lt; 0</h2>
                    <p style="color:#94A3B8;font-size:11px;font-weight:800;margin:0;letter-spacing:1px;">LOW CONFIDENCE</p>
                </div>
            </div>
            """, unsafe_allow_html=True)


            if "hasil_durasi" in st.session_state and st.session_state.hasil_durasi:
                durasi_cards = ""
                for p in st.session_state.hasil_durasi:
                    matched_gejala_durasi = get_major_indikator(p["kode"])

                    relevan_text = (
                        "Gejala yang masih relevan:<br><b>" +
                        ", ".join(matched_gejala_durasi[:4]) +
                        "</b>"
                    ) if matched_gejala_durasi else (
                        "Belum ditemukan indikator klinis yang cukup relevan."
                    )

                    durasi_cards += f"""<div class="durasi-analysis-item">
                        <div class="durasi-top">
                            <div class="durasi-penyakit">{p['nama']}</div>
                            <div class="durasi-status">BELOW LIMIT</div>
                        </div>
                        <div class="durasi-small-desc">{relevan_text}</div>
                        <div class="durasi-bottom">
                            <div class="durasi-label">CONFIDENCE</div>
                            <div class="durasi-score"> {p['skor']:.2f} %</div>
                        </div>
                    </div> """

                st.markdown(f"""
                <div class="durasi-analysis-card">
                    <div class="durasi-analysis-title">
                        Analisis Hasil
                    </div>
                    <div class="durasi-analysis-desc">
                        Berikut adalah kemungkinan penyakit yang masih memiliki
                        keterkaitan dengan durasi gejala:
                        <b>{st.session_state.durasi_label}</b>.
                        Namun secara keseluruhan belum memenuhi
                        threshold minimum aturan penyakit pada sistem.
                    </div>
                    <div class="durasi-analysis-grid">{durasi_cards}</div>
                </div>""", unsafe_allow_html=True)

        # tombol bawah
        st.write("")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("↻ Prediksi Ulang",use_container_width=True,type="primary"):
                pindah_halaman("input")

        with col_btn2:
            if st.button("Pelajari Tentang Sistem",use_container_width=True,type="primary"):
                pindah_halaman("informasi")
                
    with col_kanan:
        ringkasan_html = f"""<div class="hasil-sidebar-card scroll-hasil">
            <h4 style="margin-top:0;color:#1E293B;font-size:16px;margin-bottom:10px;font-weight:800;">📋 Ringkasan Indikator Klinis Terpilih</h4>
            <p class='sidebar-label'>Informasi Dasar</p>
            <div class='sidebar-row'><span>Usia</span><span><b>{st.session_state.usia_input} tahun</b></span></div>
            <div class='sidebar-row'><span>Tanggal Mulai Gejala</span><span><b>{st.session_state.tgl_input}</b></span></div>
            <div class='sidebar-row'><span>Durasi Gejala</span><span><b>{st.session_state.durasi_label}</b></span>
            </div>
            <p class='sidebar-label'>Gejala Fisik</p>
        """
        gejala_sorted = sorted([item for item in st.session_state.semua_indikator if item["kode"].startswith("G")], key=lambda x: x["match"], reverse=True)

        for item in gejala_sorted:
            if item["match"]:
                ringkasan_html += f"""<div class='gejala-match'>
                    <div><div class='gejala-name'>● {item['nama']}</div></div>
                    <div class='gejala-score'>
                        {
                            "Yakin" if item['nilai'] == 0.5 else
                            "Mungkin" if item['nilai'] == 0.0 else
                            "Tidak Ada"
                        }
                        </div>
                </div>"""

            else:
                ringkasan_html += f"""<div class='gejala-unmatch'>● {item['nama']}<span style='float:right'>
                {
                    "Yakin" if item['nilai'] == 0.5 else
                    "Mungkin" if item['nilai'] == 0.0 else
                    "Tidak Ada"
                }
                </span></div>"""
        
        ringkasan_html += """<p class='sidebar-label'>Faktor Risiko</p>"""

        faktor_final = st.session_state.faktor_aktif.copy()

        if st.session_state.usia_input <= 5 or st.session_state.usia_input >= 60:
                faktor_final.insert(0, "Usia Rentan")

        for item in faktor_final:
            ringkasan_html += f"""<div class='risk-pill'>{item}</div>"""
        ringkasan_html += "</div>"

        st.markdown(ringkasan_html, unsafe_allow_html=True)