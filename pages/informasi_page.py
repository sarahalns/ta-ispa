import streamlit as st
import database

def show_informasi_page(pindah_halaman): 
    top_left, top_right = st.columns([3,1])

    with top_left:
        st.markdown("""
            <div class='info-hero'>
                <h1 class='info-main-title'>
                    Transparansi <span class='highlight'>Prediksi</span><br>
                    & Metodologi Pakar
                </h1>
            </div>
            """, unsafe_allow_html=True)

    with top_right:
        if st.button("← Kembali ke Prediksi", use_container_width=True):
            pindah_halaman("input")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1], gap="large")
    with col1:
        st.markdown("""
        <div class='modern-card'>
        <div class='card-title'>🖥️ Tentang Sistem</div>

        <p class='card-text'>
        Sistem ini mentransformasikan keahlian klinis dokter Telinga Hidung Tenggoroan (THT) ke dalam basis aturan digital terstruktur, lalu memproses ketidakpastian indikator tersebut menggunakan metode Certainty Factor untuk menghasilkan derajat kepastian berupa persentase probabilitas penyakit.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='warning-card'>
        <div class='card-title'>⚠️ Batasan Sistem</div>
        <ul class='warning-list'>
        <li>Bukan pengganti diagnosis dokter</li>
        <li>Hanya asesmen awal ISPA bagian atas</li>
        <li>Akurasi dipengaruhi input pengguna</li>
        <li>Tidak menggantikan pemeriksaan klinis</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    bottom1, bottom2 = st.columns(2, gap="large")
    with bottom1:
        output_html = """
        <div class='modern-card scroll-card'><div class='card-title'>📊 Output Prediksi</div>
            <div class='prediction-info'>
                Hasil output sistem merupakan salah satu dari penyakit di bawah ini,
                yang terdiri dari satu hasil prediksi utama (probabilitas tertinggi)
                dan hasil pembanding lainnya sebagai kemungkinan tambahan.
            </div>
        """

        for kode, info in database.data_penyakit.items():
            major_indicators = []

            # ambil semua indikator major (CF = 0.8)
            for indikator_kode, nilai_cf in database.cf_pakar[kode].items():

                if nilai_cf == database.M:

                    # ambil nama indikator dari gejala / faktor / durasi
                    if indikator_kode in database.data_gejala:
                        major_indicators.append(
                            database.data_gejala[indikator_kode]["nama"]
                        )

                    elif indikator_kode in database.data_faktor_resiko:
                        major_indicators.append(
                            database.data_faktor_resiko[indikator_kode]["nama"]
                        )

            indikator_html = ""

            for indikator in major_indicators:
                indikator_html += f"""<div class='major-chip'>{indikator}</div>"""

            output_html += f"""<div class='prediction-card'>
                <div class='prediction-top'>
                    <div class='prediction-left'>
                        <div>
                            <div class='disease-name'>{info['nama']}</div>
                            <div class='disease-desc'>{info['desc']}</div>
                            <div class='major-title'>Indikator Major</div>
                            <div class='major-wrapper'>{indikator_html}</div>
                        </div>
                    </div>
                    <div class='probability-box'>%</div>
                </div>
            </div>
            """
        output_html += "</div>"
        st.markdown(output_html, unsafe_allow_html=True)

    with bottom2:
        indikator_html="""<div class='modern-card scroll-card'>
        <div class='card-title'>🩺 Indikator Klinis</div>
        <div class='prediction-info'>Kategori variabel yang dipertimbangkan sistem prediksi dalam proses menentukan penyakit ISPA bagian atas.</div>
        <div class='indicator-section-title'>Durasi Keluhan</div>
        <div class='duration-box'>Durasi kemunculan gejala digunakan sebagai indikator baseline untuk membedakan kondisi akut, sub-akut, dan kronis.</div>
        <div class='indicator-section-title'>Gejala Utama</div>
        <div class='indicator-grid'>
        """

        for kode, info in database.data_gejala.items():
            indikator_html+=f""" <div class='indicator-item'><div class='indicator-code'>{kode}</div>{info['nama']}</div>"""

        indikator_html+="""</div><div class='indicator-section-title'>Faktor Lingkungan & Riwayat</div><div class='risk-grid'>"""

        for kode, info in database.data_faktor_resiko.items():

            indikator_html+=f"""<div class='risk-item'>{info['nama']}</div>"""

        indikator_html+="</div></div>"

        st.markdown(indikator_html, unsafe_allow_html=True)
    
    st.markdown("""<div class='cf-section'>
            <div class='cf-left'>
                <div class='cf-badge'>LOGIC & CODE</div>
                <div class='cf-title'>Certainty Factor (CF) Algorithm</div>
                <div class='cf-subtitle'>Alur Perhitungan Sistem Prediksi Menggunakan Certainty Factor</div>
                <div class='cf-step'>
                    <span>1.</span>
                    <div>Ambil nilai bobot pakar (CF_Pakar) dari matriks indikator klinis (skala variabel pakar) </div>
                </div>
                <div class='cf-step'>
                    <span>2.</span>
                    <div>Terima nilai keyakinan pengguna (CF_User)dari form input (skala keyakinan user)</div>
                </div>
                <div class='cf-step'>
                    <span>3.</span>
                    <div>Hitung CF Gejala tunggal untuk setiap indikator klinis</div>
                </div>
                <div class='cf-step'>
                    <span>4.</span>
                    <div>Kombinasikan seluruh nilai CF_Gejala menggunakan persamaan Certainty Factor berbasis akumulasi evidence dengan normalisasi absolut untuk menjaga stabilitas nilai kombinasi</div>
                </div>
                <div class='cf-step'>
                    <span>5.</span>
                    <div>Urutkan hasil akhir persentase probabilitas dari 6 penyakit ISPA.
                    </div>
                </div>
                <div class='cf-total-box'>
                    <div class='cf-total-icon'>🩺</div>
                    <div>
                        <div class='cf-total-title'>33 TOTAL INDIKATOR KLINIS</div>
                        <div class='cf-total-sub'>(25 Gejala + 4 Kategori Durasi + 4 Faktor Risiko)</div>
                    </div>
                </div>
            </div>
            <div class='cf-right'>
                <div class='cf-panel'>
                    <div class='cf-panel-title'>// SKALA VARIABEL PAKAR</div>
                    <div class='cf-grid'>
                        <div class='cf-item major'>
                            <span>Major (M)</span>
                            <b>0.8</b>
                        </div>
                        <div class='cf-item medium'>
                            <span>Medium (MD)</span>
                            <b>0.6</b>
                        </div>
                        <div class='cf-item minor'>
                            <span>Minor (MN)</span>
                            <b>0.4</b>
                        </div>
                        <div class='cf-item none'>
                            <span>Tidak Ada (N)</span>
                            <b>0.0</b>
                        </div>
                    </div>
                    <div class='cf-panel-title second'>// SKALA KEYAKINAN PENGGUNA
                    </div>
                    <div class='cf-grid-user'>
                        <div class='cf-user tidak'>
                            <span>Tidak ada</span>
                            <b>-0.5</b>
                        </div>
                        <div class='cf-user mungkin'>
                            <span>Mungkin</span>
                            <b>0.0</b>
                        </div>
                        <div class='cf-user yakin'>
                            <span>Yakin</span>
                            <b>0.5</b>
                        </div>
                    </div>
                    <div class='cf-panel-title second'>
                        // RUMUS INTI
                    </div>
                    <div class='cf-formula-box'>
                        <div class='cf-formula-sub'>
                            // Rumus CF Gejala Tunggal
                        </div>
                        <div class='cf-formula-main'>
                            CF_ev = CF_pakar × CF_user
                        </div>
                        <div class='cf-formula-sub'>
                            // Kombinasi Gejala Baru
                        </div>
                        <div class='cf-formula-main second'>
                            CF_total = CF_total + CF_ev × (1 − |CF_total|)
                        </div>
                    </div>
                    <div class='cf-note'>Metode ini memungkinkan akumulasi bukti secara dinamis.</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)