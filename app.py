import streamlit as st
import pandas as pd

st.set_page_config(page_title="Refill Blend Studio", layout="wide")

# DATABASE AI (Sederhana)
DB_NOTES = {
    "Vanilla": {"top": "-", "mid": "Vanilla Orchid", "base": "Vanilla Bean", "vibe": "Manis/Cozy"},
    "Rose": {"top": "Bergamot", "mid": "Rose", "base": "White Musk", "vibe": "Feminin/Anggun"},
    "Sandalwood": {"top": "Cardamom", "mid": "Sandalwood", "base": "Amber", "vibe": "Maskulin/Earthy"}
}

# Inisialisasi State
if 'inventaris_bahan' not in st.session_state:
    st.session_state.inventaris_bahan = [
        {"Nama Bahan": "Vanilla", "Tipe": "Bibit", "Harga per ml (Rp)": 2000},
        {"Nama Bahan": "Rose", "Tipe": "Bibit", "Harga per ml (Rp)": 2500},
        {"Nama Bahan": "Sandalwood", "Tipe": "Bibit", "Harga per ml (Rp)": 3000},
        {"Nama Bahan": "Alkohol", "Tipe": "Pelarut", "Harga per ml (Rp)": 100}
    ]

tab1, tab2 = st.tabs(["🧮 Racik & Analisis AI", "📦 Inventaris"])

with tab1:
    st.header("Racik Parfum Multi-Bibit")
    nama_parfum = st.text_input("Nama Parfum")
    vol_total = st.number_input("Total Volume (ml)", value=30)
    
    # Pilih Bibit (Multi-select)
    pilihan_bibit = st.multiselect("Pilih Bibit (Bisa lebih dari 1)", [b["Nama Bahan"] for b in st.session_state.inventaris_bahan if b["Tipe"]=="Bibit"])
    
    if pilihan_bibit:
        # Input volume per bibit
        vol_per_bibit = vol_total * 0.6 / len(pilihan_bibit) # Default 60% bibit dibagi rata
        total_biaya_bibit = 0
        notes_list = []
        
        st.write("---")
        for b in pilihan_bibit:
            harga = [x["Harga per ml (Rp)"] for x in st.session_state.inventaris_bahan if x["Nama Bahan"]==b][0]
            total_biaya_bibit += (vol_per_bibit * harga)
            if b in DB_NOTES: notes_list.append(DB_NOTES[b])
            st.write(f"Bibit: {b} | Volume: {vol_per_bibit:.1f} ml")

        # Analisis AI Sederhana
        st.info("🧠 AI Olfactory Analysis: Notes akan muncul di sini berdasarkan database.")
        
        # Kalkulasi HPP
        harga_botol = 5000
        total_hpp = total_biaya_bibit + harga_botol
        st.subheader("📊 Estimasi Harga")
        col1, col2 = st.columns(2)
        col1.metric("Total HPP", f"Rp {total_hpp:,.0f}")
        col2.metric("Rekomendasi Harga Jual (Profit 100%)", f"Rp {total_hpp*2:,.0f}")

with tab2:
    st.header("Inventaris")
    st.session_state.inventaris_bahan = st.data_editor(pd.DataFrame(st.session_state.inventaris_bahan), num_rows="dynamic").to_dict('records')
