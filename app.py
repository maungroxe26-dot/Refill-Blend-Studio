import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Refill Blend Studio", page_icon="🧪", layout="wide")

# Inisialisasi State (Inventaris & Pustaka)
if 'inventaris_bahan' not in st.session_state:
    st.session_state.inventaris_bahan = [
        {"Nama Bahan": "Sweet Vanilla", "Merk": "Parfex", "Tipe": "Bibit", "Harga per ml (Rp)": 1800},
        {"Nama Bahan": "Absolute Alkohol", "Merk": "-", "Tipe": "Pelarut", "Harga per ml (Rp)": 100}
    ]
if 'pustaka_racikan' not in st.session_state:
    st.session_state.pustaka_racikan = pd.DataFrame(columns=["Nama Parfum", "Total Volume", "Rasio Bibit", "Komposisi"])

# Header
st.title("🧪 Refill Blend Studio")
tab1, tab2, tab3 = st.tabs(["🧮 Kalkulator Formula", "📦 Inventaris Bahan", "📚 Pustaka Racikan"])

# ==================== TAB 1: KALKULATOR & SIMPAN ====================
with tab1:
    st.header("Racikan Formula Baru")
    
    # Input Identitas
    nama_parfum = st.text_input("Nama Parfum Racikan", value="Racikan Baru")
    target_volume = st.number_input("Target Total Volume (ml)", min_value=5, max_value=500, value=30, step=5)
    
    opsi_konsentrasi = {"EDP (50% Bibit)": 0.50, "Extrait (60% Bibit)": 0.60}
    pilihan_tipe = st.selectbox("Pilih Tipe Konsentrasi", list(opsi_konsentrasi.keys()))
    rasio_bibit = opsi_konsentrasi[pilihan_tipe]

    # Hitung Otomatis
    ml_bibit_total = int(target_volume * rasio_bibit)
    ml_pelarut_total = target_volume - ml_bibit_total

    # Input Dinamis (Sederhana untuk demo)
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Bibit: {ml_bibit_total} ml")
        bahan_bibit = st.selectbox("Pilih Bibit Utama", [b["Nama Bahan"] for b in st.session_state.inventaris_bahan if b["Tipe"]=="Bibit"])
    with col2:
        st.info(f"Pelarut: {ml_pelarut_total} ml")
        bahan_pelarut = st.selectbox("Pilih Pelarut", [p["Nama Bahan"] for p in st.session_state.inventaris_bahan if p["Tipe"]=="Pelarut"])

    # Tombol Simpan
    if st.button("💾 Simpan ke Pustaka Racikan"):
        data_baru = {
            "Nama Parfum": nama_parfum,
            "Total Volume": f"{target_volume} ml",
            "Rasio Bibit": pilihan_tipe,
            "Komposisi": f"{bahan_bibit} & {bahan_pelarut}"
        }
        st.session_state.pustaka_racikan = pd.concat([st.session_state.pustaka_racikan, pd.DataFrame([data_baru])], ignore_index=True)
        st.success(f"Racikan '{nama_parfum}' berhasil disimpan!")

# ==================== TAB 2: INVENTARIS ====================
with tab2:
    st.header("Manajemen Inventaris")
    edited_bahan = st.data_editor(
        pd.DataFrame(st.session_state.inventaris_bahan),
        num_rows="dynamic", use_container_width=True
    )
    st.session_state.inventaris_bahan = edited_bahan.to_dict('records')

# ==================== TAB 3: PUSTAKA RACIKAN ====================
with tab3:
    st.header("📚 Pustaka Racikan Anda")
    if not st.session_state.pustaka_racikan.empty:
        st.dataframe(st.session_state.pustaka_racikan, use_container_width=True)
        if st.button("🧹 Hapus Semua Pustaka"):
            st.session_state.pustaka_racikan = pd.DataFrame(columns=["Nama Parfum", "Total Volume", "Rasio Bibit", "Komposisi"])
            st.rerun()
    else:
        st.write("Belum ada racikan yang disimpan.")
