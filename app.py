import streamlit as st
import time
import base64
import importlib

from pages import input_page
from pages import hasil_page
from pages import informasi_page

importlib.reload(input_page)
importlib.reload(hasil_page)
importlib.reload(informasi_page)

# config
st.set_page_config(page_title="Sistem Prediksi ISPA Atas", page_icon="🩺", layout="wide")

with open("style.css") as f:
    css = f.read() 
    st.markdown(f"""<style>{css} /* {time.time()} */</style>""", unsafe_allow_html=True)

# navigation function
def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman
    st.rerun()

# init page
if 'page' not in st.session_state:
    st.session_state.page = 'input'

# if 'hasil' not in st.session_state:
#     st.session_state.hasil = [
#         {
#             "kode":"P01",
#             "nama":"Common Cold",
#             "skor":99.2
#         },
#         {
#             "kode":"P02",
#             "nama":"Rinitis Akut",
#             "skor":84.5
#         },
#         {
#             "kode":"P04",
#             "nama":"Sinusitis Akut",
#             "skor":72.3
#         }
#     ]

# if 'usia_input' not in st.session_state:
#     st.session_state.usia_input = 21

# if 'tgl_input' not in st.session_state:
#     st.session_state.tgl_input = "15 Mei 2026"

# if 'durasi_label' not in st.session_state:
#     st.session_state.durasi_label = "Gejala berlangsung <= 10 hari"

# if 'gejala_html' not in st.session_state:
#     st.session_state.gejala_html = """
#     <div class='gejala-pill'>Demam Ringan</div>
#     <div class='gejala-pill'>Hidung Tersumbat</div>
#     <div class='gejala-pill'>Bersin Berulang</div>
#     """
# if 'semua_indikator' not in st.session_state:
#     st.session_state.semua_indikator = [
#         {
#             "kode":"G01",
#             "nama":"Demam Tinggi",
#             "nilai":0.5,
#             "match":True
#         },
#         {
#             "kode":"G02",
#             "nama":"Demam Ringan",
#             "nilai":0.5,
#             "match":True
#         },
#         {
#             "kode":"G04",
#             "nama":"Hidung Tersumbat",
#             "nilai":0.5,
#             "match":True
#         },
#         {
#             "kode":"G14",
#             "nama":"Bersin Berulang",
#             "nilai":0.5,
#             "match":True
#         },
#         {
#             "kode":"G03",
#             "nama":"Sakit Kepala",
#             "nilai":0.5,
#             "match":True
#         },{
#             "kode":"G08",
#             "nama":"Hidung Bau",
#             "nilai":0.5,
#             "match":True
#         },{
#             "kode":"F02",
#             "nama":"Perubahan Cuaca",
#             "nilai":0.5,
#             "match":True
#         }

#     ]

# if 'faktor_aktif' not in st.session_state:
#     st.session_state.faktor_aktif = [
#         "Paparan Polusi",
#         "Kontak Penderita"
#     ]

# background opening
def set_background_opening(file_gambar):
    with open(file_gambar, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{encoded_string}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# opening page
query_params = st.query_params
if "opened" not in query_params:

    try:
        set_background_opening("background_opening.jpg")
    except FileNotFoundError:
        pass

    st.markdown("""
        <div style='text-align: center; margin-top: 15vh;'>
            <h1 style='color:#1E293B; font-size: 60px; margin-top: 0px; margin-bottom: 0px; padding-bottom: 0px;'>SISTEM PREDIKSI BERBASIS CERTAINTY FACTOR</h1>
            <h1 style='color:#2563EB; font-size: 60px; margin-top: 0px; padding-top: 0px;'>UNTUK ASESMEN AWAL PENYAKIT ISPA BAGIAN ATAS</h1>
            <p style='color:#64748B; font-size: 16px; margin-top: 20px;'>
                Mengarahkan ke sistem prediksi....
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_space1, col_loading, col_space2 = st.columns([1, 2, 1])
    
    with col_loading:
        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1)
            
    time.sleep(0.3)
    st.query_params["opened"] = "true"
    pindah_halaman('input')

elif st.session_state.page == 'input':
    input_page.show_input_page(pindah_halaman)

elif st.session_state.page == 'informasi':
    informasi_page.show_informasi_page(pindah_halaman)

elif st.session_state.page == 'hasil':
    hasil_page.show_hasil_page(pindah_halaman)
