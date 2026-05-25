import streamlit as st

from datetime import date
from database import data_gejala, data_durasi, data_faktor_resiko, data_penyakit, cf_pakar, aturan_konsistensi_gejala,  aturan_dependensi_gejala

skala_user = {
    "Tidak Ada": -0.5,
    "Mungkin": 0.0,
    "Yakin": 0.5
}

def highlight_keywords(text, keywords):
    for word in keywords:
        text = text.replace(
            word,
            f"<span class='highlight-gejala'>{word}</span>"
        )
    return text

def show_input_page(pindah_halaman):
    st.markdown("""
        <div style='margin-bottom: 25px;'>
            <p style='color: #0F766E; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 5px;'>
                Asesmen Awal Kesehatan
            </p>
            <h1 class='info-main-title'>
                Sistem Prediksi Penyakit ISPA Bagian Atas
            </h1>
            <p class='sub-title'>
                Teknologi berbasis Certainty Factor untuk memprediksi tingkat probabilitas rangkaian penyakit Infeksi Saluran Pernapasan Akut (ISPA) bagian atas melalui skrining indikator klinis mandiri.
            </p>
        </div>
    """, unsafe_allow_html=True)
        
    col_main, col_side = st.columns([2, 1], gap="large")

    pesan_konflik = []

    with col_main:
        with st.container(height=950):
            # Section Parameter Awal (Usia dan Tanggal)
            st.markdown("""
                <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                    <div style='background-color: #E0E7FF; padding: 12px; border-radius: 12px; text-align: center; font-size: 20px; margin-top: 5px;'>
                        📅
                    </div>
                    <div style='margin-left: 20px;'>
                        <h3 style='margin-bottom: 0px; padding-bottom: 0px; line-height: 1;'>Parameter Klinis Awal</h3>
                        <p style='font-size: 14px; margin-top: 5px; padding-top: 0px;'>Lengkapi data usia dan durasi keluhan Anda sebagai parameter dasar dalam kalkulasi prediksi risiko penyakit.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
                   
            with st.container():        
                st.markdown(f"<p style='color: #1E293B; font-weight: 600; font-size: 16px; margin-bottom: 5px;'>Berapa usia Anda saat ini?</p>", unsafe_allow_html=True)

                usia_input = st.number_input(
                    label="Usia",
                    min_value=0,
                    max_value=120,
                    step=1,
                    label_visibility="collapsed"
                )

                st.markdown("<div style='margin-bottom:18px;'></div>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #1E293B; font-weight: 600; font-size: 16px; margin-bottom: 5px;'>Secara umum, kapan Anda pertama kali merasakan gejala awal?</p>", unsafe_allow_html=True)

                tgl_mulai = st.date_input(
                    label="Tanggal Mulai Gejala",
                    value=None,
                    label_visibility="collapsed"
                )

            usia_rentan = 0.0
            if usia_input < 5 or usia_input > 60:
                usia_rentan = 1.0

            durasi_final = None
            if tgl_mulai is not None:
                if tgl_mulai > date.today():
                    st.error("Tanggal mulai gejala tidak boleh melebihi tanggal hari ini.")
                else:
                    selisih_hari = (date.today() - tgl_mulai).days
                    durasi_final = None
                    for d_kode, info in data_durasi.items():
                        if info["min"] <= selisih_hari <= info["max"]:
                            durasi_final = d_kode
                            break
            else:
                selisih_hari = None
                        
            st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

            # Section Gejala
            st.markdown("""
                <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                    <div style='background-color: #E0E7FF; padding: 12px; border-radius: 12px; text-align: center; font-size: 20px; margin-top: 5px;'>
                        🏥
                    </div>
                    <div style='margin-left: 20px;'>
                        <h3 style='margin-bottom: 0px; padding-bottom: 0px; line-height: 1;'>Observasi Gejala Fisik</h3>
                        <p style='font-size: 14px; margin-top: 5px; padding-top: 0px;'>Tentukan tingkat keyakinan Anda terhadap setiap gejala fisik yang dirasakan untuk memulai kalkulasi bobot prediksi penyakit.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
                
            with st.container():
                user_responses = {}
                for g_kode, info in data_gejala.items():
                    col_nama, col_badge = st.columns([4, 1.5])
                    
                    with col_nama:
                        pertanyaan = highlight_keywords(info["tanya"],info.get("highlight", []))
                        st.markdown(f"<p class='pertanyaan-gejala'>{pertanyaan}</p>",unsafe_allow_html=True)
                        
                    with col_badge:
                        st.markdown("""
                            <div style='background-color: #DBEAFE; color: #1D4ED8; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-align: center; float: right; margin-top: 2px;'>
                                NILAI KEYAKINAN
                            </div>
                        """, unsafe_allow_html=True)
                    
                    resp = st.radio(
                        label=f"Pilihan {g_kode}",
                        options=list(skala_user.keys()),
                        horizontal=True,
                        label_visibility="collapsed",
                        key=f"radio_{g_kode}"
                    )
                    
                    user_responses[g_kode] = skala_user[resp]
                    st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
                
            # Section Faktor Resiko
            st.markdown("""
                <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                    <div style='background-color: #E0E7FF; padding: 12px; border-radius: 12px; text-align: center; font-size: 20px; margin-top: 5px;'>
                        ⚠️
                    </div>
                    <div style='margin-left: 20px;'>
                        <h3 style='margin-bottom: 0px; padding-bottom: 0px; line-height: 1;'>Indikator Risiko Eksternal</h3>
                        <p style='font-size: 14px; margin-top: 5px; padding-top: 0px;'>Pilih skala keyakinan mengenai riwayat paparan dan kondisi lingkungan Anda sebagai variabel pendukung dalam kalkulasi prediksi</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            with st.container():
                user_responses_resiko = {}
                # Looping untuk memunculkan pertanyaan faktor risiko
                for f_kode, info in data_faktor_resiko.items():
                    if f_kode == "F04":
                        continue

                    col_faktor, col_badge2 = st.columns([4, 1.5])
                    with col_faktor:
                        st.markdown(f"<p style='color: #1E293B; font-weight: 600; font-size: 16px; margin-bottom: 0px;'>{info['tanya']}</p>", unsafe_allow_html=True)
                
                    with col_badge2:
                        st.markdown("""
                            <div style='background-color: #DBEAFE; color: #1D4ED8; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-align: center; float: right; margin-top: 2px;'>
                                NILAI KEYAKINAN
                            </div>
                        """, unsafe_allow_html=True)

                    resp = st.radio(
                        label=f"Pilihan {f_kode}",
                        options=list(skala_user.keys()),
                        horizontal=True, 
                        label_visibility="collapsed", 
                        key=f"radio_resiko_{f_kode}"
                    )
                    
                    user_responses_resiko[f_kode] = skala_user[resp]

            ada_konflik = False

            for nama_kelompok, aturan in aturan_konsistensi_gejala.items():

                gejala_aktif = []

                for kode in aturan["kode"]:
                    if user_responses.get(kode, 0) > 0:
                        gejala_aktif.append(kode)

                # Jika lebih dari 1 gejala aktif dalam 1 kelompok
                if len(gejala_aktif) > 1:

                    nama_gejala = [
                        data_gejala[k]["nama"]
                        for k in gejala_aktif
                    ]

                    pesan_konflik.append({
                        "kelompok": nama_kelompok,
                        "gejala": nama_gejala,
                        "pesan": aturan["pesan"]
                    })
                    ada_konflik = True
            
            for nama_dep, aturan in aturan_dependensi_gejala.items():
                trigger = aturan["trigger"]
                # kalau trigger dipilih
                if user_responses.get(trigger, 0) > 0:
                    valid = False

                    # cek apakah salah satu required dipilih
                    for req in aturan["required"]:
                        if user_responses.get(req, 0) > 0:
                            valid = True

                    # kalau tidak valid
                    if not valid:
                        pesan_konflik.append({
                            "kelompok": nama_dep,
                            "gejala": [data_gejala[trigger]["nama"]],
                            "pesan": aturan["pesan"]
                        })   
                        ada_konflik = True
        
        if pesan_konflik:
            for konflik in pesan_konflik:
                st.markdown(f"""<div class="conflict-card">
                    <div class="conflict-header">
                        <div class="conflict-icon">⚠️</div>
                        <div>
                            <div class="conflict-title">Konflik Gejala {konflik['kelompok']}</div>
                            <div class="conflict-subtitle">Gejala yang dipilih:<b>{", ".join(konflik['gejala'])}</b> </div>
                        </div>
                    </div>
                    <div class="conflict-desc">{konflik['pesan']}</div>
                </div>
                """, unsafe_allow_html=True)

        submit = st.button("Kirim", use_container_width=True, type="primary", disabled=ada_konflik)
        if submit:
            if durasi_final is None:
                st.markdown("""<div class="custom-warning">⚠️ Silakan pilih tanggal mulai gejala terlebih dahulu.</div>""", unsafe_allow_html=True)
                st.stop()

            hasil_prediksi = []
            hasil_durasi = []
            for p_kode, nama_p in data_penyakit.items():

                cf_total = 0.0

                current_inputs = {durasi_final: 1.0}
                if usia_rentan > 0:
                    current_inputs["F04"] = usia_rentan
                current_inputs.update(user_responses)
                current_inputs.update(user_responses_resiko)

                # FILTER DURASI OTOMATIS
                rule_durasi = [
                    kode
                    for kode in cf_pakar[p_kode]
                    if kode.startswith("D")
                ]

                if rule_durasi:
                    if durasi_final not in rule_durasi:
                        continue

                # HITUNG CF
                if p_kode in cf_pakar:
                    for ev_kode, bobot_p in cf_pakar[p_kode].items():
                        val_user = current_inputs.get(ev_kode, -0.5)
                        cf_ev = val_user * bobot_p

                        if cf_ev != 0:
                            if cf_total == 0:
                                cf_total = cf_ev

                            else:
                                cf_total = (
                                    cf_total +
                                    cf_ev * (1 - abs(cf_total))
                                )

                data_hasil = {
                    "kode": p_kode,
                    "nama": nama_p["nama"],
                    "desc": nama_p["desc"],
                    "skor": cf_total * 100
                }

                # hasil utama
                if cf_total >= 0.0:
                    hasil_prediksi.append(data_hasil)

                # hasil inkonklusif
                else:
                    hasil_durasi.append(data_hasil)
    
            # 1. Simpan Tanggal & Usia
            st.session_state.tgl_input = (tgl_mulai.strftime("%d %b %Y") if tgl_mulai else "Tidak diisi")
            st.session_state.durasi_label = data_durasi[durasi_final]["label"]
            st.session_state.usia_input = usia_input

            # 2. Simpan Gejala yang dipilih (Buatkan HTML Pill-nya sekalian)
            gejala_terpilih_html = ""
            for g_kode, val in user_responses.items():
                if val > 0: # Hanya ambil jika user yakin
                    teks_gejala = data_gejala[g_kode]['nama'] 
                    gejala_terpilih_html += f'<div class="gejala-pill">• {teks_gejala}</div>\n'
            
            # Jaga-jaga kalau user iseng tidak pilih gejala sama sekali
            if not gejala_terpilih_html:
                gejala_terpilih_html = '<div class="gejala-pill" style="color: #EF4444;">Tidak ada gejala signifikan</div>'
                
            st.session_state.gejala_html = gejala_terpilih_html

            # SEMUA INDIKATOR
            st.session_state.semua_indikator = []

            # GEJALA
            for g_kode, val in user_responses.items():

                st.session_state.semua_indikator.append({
                    "kode": g_kode,
                    "nama": data_gejala[g_kode]["nama"],
                    "nilai": round(val, 2),
                    "match": val >= 0
                })

            # FAKTOR RISIKO
            st.session_state.faktor_aktif = []
            for f_kode, val in user_responses_resiko.items():
                if val > 0:
                    nama_faktor = data_faktor_resiko[f_kode]["nama"]
                    st.session_state.faktor_aktif.append(
                        nama_faktor
                    )

                    st.session_state.semua_indikator.append({
                        "kode": f_kode,
                        "nama": nama_faktor,
                        "nilai": round(val, 2),
                        "match": True
                    })
            
            # usia rentan otomatis
            if usia_rentan > 0:
                st.session_state.semua_indikator.append({
                    "kode": "F04",
                    "nama": data_faktor_resiko["F04"]["nama"],
                    "nilai": usia_rentan,
                    "match": True
                })

            # DURASI
            st.session_state.semua_indikator.append({
                "kode": durasi_final,
                "nama": data_durasi[durasi_final]["label"],
                "nilai": 1.0,
                "match": True
            })

            # HASIL
            st.session_state.hasil = sorted(
                hasil_prediksi,
                key=lambda x: x['skor'],
                reverse=True
            )

            st.session_state.hasil_durasi = sorted(
                hasil_durasi,
                key=lambda x: x['skor'],
                reverse=True
            )

            pindah_halaman('hasil')

    with col_side:
        if st.button("ℹ️ Tentang Website (Klik Di Sini)", use_container_width=True):
            pindah_halaman("informasi")

        st.markdown("""
            <div class='action-card'>

            <div style="display:flex;align-items:center;gap:10px;margin-bottom: 7px;">
            <div style="width:48px;height:48px;border-radius:50%;background:rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;font-size:24px;color:white;">ℹ️</div>

            <div style="font-size:20px;font-weight:700;color:white;">
            Cara Penggunaan
            </div>
            </div>

            <div style="display:flex;gap:18px;margin-bottom:15px;">
            <div style="color:#93C5FD;font-size:24px;font-weight:700;min-width:24px;">1.</div>

            <div>
            <div style="font-size:18px;font-weight:650;color:white;margin-bottom:4px;">
            Isi Parameter Klinis
            </div>

            <div style="font-size:14px;color:#DBEAFE;line-height:1.6;">
            Masukkan usia Anda saat ini dan pilih tanggal pertama kali keluhan mulai dirasakan tubuh.
            </div>
            </div>
            </div>

            <div style="display:flex;gap:18px;margin-bottom:15px;">
            <div style="color:#93C5FD;font-size:24px;font-weight:700;min-width:24px;">2.</div>

            <div>
            <div style="font-size:18px;font-weight:650;color:white;margin-bottom:4px;">
            Evaluasi Gejala Fisik
            </div>

            <div style="font-size:14px;color:#DBEAFE;line-height:1.6;">
            Pilih skala keyakinan yang paling sesuai untuk setiap daftar keluhan fisik yang Anda alami.
            </div>
            </div>
            </div>

            <div style="display:flex;gap:18px;margin-bottom:15px;">
            <div style="color:#93C5FD;font-size:24px;font-weight:700;min-width:24px;">3.</div>

            <div>
            <div style="font-size:18px;font-weight:650;color:white;margin-bottom:4px;">
            Tentukan Risiko Eksternal
            </div>

            <div style="font-size:14px;color:#DBEAFE;line-height:1.6;">
            Pilih tingkat kepastian untuk faktor kondisi lingkungan sekitar serta riwayat kontak Anda.
            </div>
            </div>
            </div>
                    
            <div style="display:flex;gap:18px;margin-bottom:15px;">
            <div style="color:#93C5FD;font-size:24px;font-weight:700;min-width:24px;">4.</div>

            <div>
            <div style="font-size:18px;font-weight:650;color:white;margin-bottom:4px;">
            Klik "Kirim"
            </div>

            <div style="font-size:14px;color:#DBEAFE;line-height:1.6;">
            Sistem menghitung probablitias penyakit dan mengarahkan ke halaman hasil.
            </div>
            </div>
            </div>

            </div>
            """, unsafe_allow_html=True)
       
        st.markdown("""
            <div class='cf-guide-card'>
                <div class='cf-guide-title'>🎯 Panduan Nilai Keyakinan</div>
                <div class='cf-item'>
                    <div class='cf-badge tidak'>Tidak Ada</div>
                    <div class='cf-desc'>
                        Anda sama sekali tidak merasakan gejala atau kondisi pemicu tersebut.
                    </div>
                </div>
                <div class='cf-item'>
                    <div class='cf-badge mungkin'>Mungkin</div>
                    <div class='cf-desc'>
                        Gejala atau kondisi pemicu terasa samar, sesekali muncul, atau Anda kurang pasti merasakannya.
                    </div>
                </div>
                <div class='cf-item'>
                    <div class='cf-badge yakin'>Yakin</div>
                    <div class='cf-desc'>
                        Gejala atau kondisi pemicu benar-benar nyata, jelas, dan sedang Anda alami saat ini.
                    </div>
                </div>

            </div>
            """, unsafe_allow_html=True)