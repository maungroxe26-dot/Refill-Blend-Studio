import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Refill Blend Studio",
    page_icon="🧪",
    layout="wide"
)

# Inisialisasi Database Sementara (Session State) jika belum ada
if 'inventaris_bahan' not in st.session_state:
    st.session_state.inventaris_bahan = [
        {"Nama Bahan": "Searah Baccarat (Luzi)", "Tipe": "Bibit", "Harga per ml (Rp)": 1500},
        {"Nama Bahan": "Vanilla Lace (Parfex)", "Tipe": "Bibit", "Harga per ml (Rp)": 2000},
        {"Nama Bahan": "Citrus Fresh (Iberchem)", "Tipe": "Bibit", "Harga per ml (Rp)": 1200},
        {"Nama Bahan": "Absolute Alkohol", "Tipe": "Pelarut", "Harga per ml (Rp)": 100},
        {"Nama Bahan": "Fixative Premium", "Tipe": "Pelarut", "Harga per ml (Rp)": 600},
    ]

if 'inventaris_kemasan' not in st.session_state:
    st.session_state.inventaris_kemasan = [
        {"Nama Kemasan": "Botol Spray 30ml + Stiker", "Harga Satuan (Rp)": 7000},
        {"Nama Kemasan": "Botol Spray 50ml + Stiker + Box", "Harga Satuan (Rp)": 10000},
    ]

# Header Aplikasi
st.title("🧪 Refill Blend Studio")
st.caption("Aplikasi Kalkulator Formula & HPP khusus Parfum Refill / Fragrance Oil Blending")
st.markdown("---")

# Menu Navigasi Tab
tab1, tab2 = st.tabs(["🧮 Kalkulator Formula & HPP", "📦 Kelola Inventaris Bahan"])

# ==================== TAB 1: KALKULATOR FORMULA ====================
with tab1:
    st.header("Racikan Formula Baru")
    
    # Input Data Dasar Varian
    col_var1, col_var2 = st.columns(2)
    with col_var1:
        nama_varian = st.text_input("Nama Varian Parfum", value="Varian Nova")
    with col_var2:
        df_kemasan = pd.DataFrame(st.session_state.inventaris_kemasan)
        pilihan_kemasan = st.selectbox("Pilih Botol & Kemasan", df_kemasan["Nama Kemasan"].tolist())
        harga_kemasan = df_kemasan[df_kemasan["Nama Kemasan"] == pilihan_kemasan]["Harga Satuan (Rp)"].values[0]

    st.subheader("Komposisi Cairan")
    st.info("Pilih bahan dari inventaris dan tentukan volume (ml) yang digunakan.")

    # List pilihan bahan dari inventaris
    df_bahan = pd.DataFrame(st.session_state.inventaris_bahan)
    list_nama_bahan = df_bahan["Nama Bahan"].tolist()

    # Dynamic inputs menggunakan kontainer
    jumlah_bahan = st.number_input("Jumlah jenis bahan yang dicampur", min_value=1, max_value=10, value=3)
    
    racikan_user = []
    
    # Tampilkan baris input dinamis
    for i in range(int(jumlah_bahan)):
        col_b1, col_b2 = st.columns([3, 1])
        with col_b1:
            idx_default = min(i, len(list_nama_bahan)-1)
            bahan_terpilih = st.selectbox(f"Bahan {i+1}", list_nama_bahan, key=f"bahan_{i}", index=idx_default)
        with col_b2:
            vol_terpilih = st.number_input(f"Volume (ml)", min_value=0.0, max_value=500.0, value=10.0, step=0.5, key=f"vol_{i}")
        
        # Ambil harga per ml dari inventaris
        harga_per_ml = df_bahan[df_bahan["Nama Bahan"] == bahan_terpilih]["Harga per ml (Rp)"].values[0]
        tipe_bahan = df_bahan[df_bahan["Nama Bahan"] == bahan_terpilih]["Tipe"].values[0]
        
        racikan_user.append({
            "Nama Bahan": bahan_terpilih,
            "Tipe": tipe_bahan,
            "Volume (ml)": vol_terpilih,
            "Harga/ml": harga_per_ml,
            "Subtotal (Rp)": vol_terpilih * harga_per_ml
        })

    # Perhitungan Total
    df_racikan = pd.DataFrame(racikan_user)
    total_volume_cairan = df_racikan["Volume (ml)"].sum()
    total_biaya_cairan = df_racikan["Subtotal (Rp)"].sum()
    total_hpp_produk = total_biaya_cairan + harga_kemasan

    # Menghitung persentase rasio bibit vs pelarut
    vol_bibit = df_racikan[df_racikan["Tipe"] == "Bibit"]["Volume (ml)"].sum()
    vol_pelarut = df_racikan[df_racikan["Tipe"] == "Pelarut"]["Volume (ml)"].sum()
    
    rasio_bibit_pct = (vol_bibit / total_volume_cairan * 100) if total_volume_cairan > 0 else 0
    rasio_pelarut_pct = (vol_pelarut / total_volume_cairan * 100) if total_volume_cairan > 0 else 0

    st.markdown("---")
    st.subheader(f"📊 Hasil Analisis Ringkasan: {nama_varian}")
    
    # Ringkasan Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Volume Cairan", f"{total_volume_cairan:.1f} ml")
    m2.metric("Rasio Komposisi (Bibit : Pelarut)", f"{rasio_bibit_pct:.0f}% : {rasio_pelarut_pct:.0f}%")
    st.metric("💰 TOTAL HPP PER BOTOL", f"Rp {total_hpp_produk:,.0f}")

    # Tabel Rincian Biaya
    st.write("**Rincian Komposisi Biaya:**")
    st.dataframe(df_racikan[["Nama Bahan", "Tipe", "Volume (ml)", "Subtotal (Rp)"]], use_container_width=True)
    
    st.write(f"- Biaya Wadah/Kemasan ({pilihan_kemasan}): **Rp {harga_kemasan:,}**")
    st.write(f"- Total Biaya Essens Cairan: **Rp {total_biaya_cairan:,}**")

# ==================== TAB 2: KELOLA INVENTARIS ====================
with tab2:
    st.header("Manajemen Inventaris Bahan & Harga")
    
    col_inv1, col_inv2 = st.columns(2)
    
    with col_inv1:
        st.subheader("1. Daftar Bibit & Pelarut")
        st.dataframe(pd.DataFrame(st.session_state.inventaris_bahan), use_container_width=True)
        
        # Form Tambah Bahan
        with st.expander("➕ Tambah Bahan Baru"):
            with st.form("form_bahan"):
                new_nama = st.text_input("Nama Bahan (Contoh: Macallan / DPG)")
                new_tipe = st.selectbox("Tipe Bahan", ["Bibit", "Pelarut"])
                new_harga = st.number_input("Harga per ml (Rp)", min_value=1, value=1000)
                submit_bahan = st.form_submit_button("Simpan Bahan")
                if submit_bahan and new_nama:
                    st.session_state.inventaris_bahan.append({
                        "Nama Bahan": new_nama, "Tipe": new_tipe, "Harga per ml (Rp)": new_harga
                    })
                    st.success(f"{new_nama} berhasil ditambahkan!")
                    st.rerun()

    with col_inv2:
        st.subheader("2. Daftar Botol & Kemasan")
        st.dataframe(pd.DataFrame(st.session_state.inventaris_kemasan), use_container_width=True)
        
        # Form Tambah Kemasan
        with st.expander("➕ Tambah Kemasan Baru"):
            with st.form("form_kemasan"):
                new_kemasan_nama = st.text_input("Nama Kemasan (Contoh: Botol Roll-on 10ml)")
                new_kemasan_harga = st.number_input("Harga Satuan (Rp)", min_value=1, value=5000)
                submit_kemasan = st.form_submit_button("Simpan Kemasan")
                if submit_kemasan and new_kemasan_nama:
                    st.session_state.inventaris_kemasan.append({
                        "Nama Kemasan": new_kemasan_nama, "Harga Satuan (Rp)": new_kemasan_harga
                    })
                    st.success(f"{new_kemasan_nama} berhasil ditambahkan!")
                    st.rerun()
