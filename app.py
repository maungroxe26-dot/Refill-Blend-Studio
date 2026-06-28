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

    st.markdown("---")
    st.subheader("💡 Panduan & Pengaturan Konsentrasi Otomatis")
    st.write("Pilih tipe konsentrasi dan tentukan total target volume parfum yang ingin dibuat.")

    # Pilihan Konsentrasi Otomatis beserta standar rasio bibitnya untuk parfum refill
    opsi_konsentrasi = {
        "EDP (Eau de Parfum) - Awet & Standar Toko Refill [Rasio Bibit 50%]": 0.50,
        "Extrait de Parfum - Sangat Pekat & Tahan Lama [Rasio Bibit 70%]": 0.70,
        "Custom (Atur Manual Komposisi di Bawah)": None
    }
    
    pilihan_tipe = st.selectbox("Pilih Tipe Konsentrasi", list(opsi_konsentrasi.keys()))
    rasio_bibit_otomatis = opsi_konsentrasi[pilihan_tipe]

    col_vol1, col_vol2 = st.columns(2)
    with col_vol1:
        target_volume = st.number_input("Target Total Volume Parfum (ml)", min_value=5.0, max_value=500.0, value=30.0, step=5.0)

    # Filter bahan berdasarkan tipe untuk mempermudah kalkulator otomatis
    df_bahan = pd.DataFrame(st.session_state.inventaris_bahan)
    list_bibit = df_bahan[df_bahan["Tipe"] == "Bibit"]["Nama Bahan"].tolist()
    list_pelarut = df_bahan[df_bahan["Tipe"] == "Pelarut"]["Nama Bahan"].tolist()

    st.markdown("---")
    st.subheader("🧪 Komposisi Campuran Cairan")

    racikan_user = []

    # LOGIKA 1: JIKA MEMILIH EDP ATAU EXTRAIT (OTOMATIS)
    if rasio_bibit_otomatis is not None:
        st.success(f"Mode Otomatis Aktif! Sistem mengunci rasio untuk tipe: {pilihan_tipe}")
        
        # Hitung jatah ml masing-masing kelompok
        ml_bibit_total = target_volume * rasio_bibit_otomatis
        ml_pelarut_total = target_volume * (1.0 - rasio_bibit_otomatis)

        col_auto1, col_auto2 = st.columns(2)
        with col_auto1:
            st.write(f"**Alokasi Bibit Parfum (Total: {ml_bibit_total:.1f} ml):**")
            # Pengguna bisa melakukan layering bibit (misal dicampur 2 jenis bibit)
            jumlah_layer_bibit = st.number_input("Berapa jenis bibit parfum yang dicampur? (Layering)", min_value=1, max_value=5, value=1, key="count_bibit")
            
            # Bagi rata volume bibit awal sebagai rekomendasi awal
            vol_per_bibit = ml_bibit_total / jumlah_layer_bibit
            
            for i in range(int(jumlah_layer_bibit)):
                col_sub1, col_sub2 = st.columns([2, 1])
                with col_sub1:
                    bibit_pilihan = st.selectbox(f"Pilih Bibit {i+1}", list_bibit, key=f"auto_bibit_{i}")
                with col_sub2:
                    vol_bibit = st.number_input(f"Volume (ml)", min_value=0.0, max_value=target_volume, value=vol_per_bibit, step=0.5, key=f"auto_vol_bibit_{i}")
                
                harga_per_ml = df_bahan[df_bahan["Nama Bahan"] == bibit_pilihan]["Harga per ml (Rp)"].values[0]
                racikan_user.append({
                    "Nama Bahan": bibit_pilihan, "Tipe": "Bibit", "Volume (ml)": vol_bibit,
                    "Harga/ml": harga_per_ml, "Subtotal (Rp)": vol_bibit * harga_per_ml
                })

        with col_auto2:
            st.write(f"**Alokasi Pelarut / Absolute (Total: {ml_pelarut_total:.1f} ml):**")
            jumlah_layer_pelarut = st.number_input("Berapa jenis pelarut yang digunakan? (Misal: Absolute + Fixative)", min_value=1, max_value=3, value=1, key="count_pelarut")
            
            vol_per_pelarut = ml_pelarut_total / jumlah_layer_pelarut
            
            for j in range(int(jumlah_layer_pelarut)):
                col_sub3, col_sub4 = st.columns([2, 1])
                with col_sub3:
                    pelarut_pilihan = st.selectbox(f"Pilih Pelarut {j+1}", list_pelarut, key=f"auto_pelarut_{j}")
                with col_sub4:
                    vol_pelarut = st.number_input(f"Volume (ml)", min_value=0.0, max_value=target_volume, value=vol_per_pelarut, step=0.5, key=f"auto_vol_pelarut_{j}")
                
                harga_per_ml = df_bahan[df_bahan["Nama Bahan"] == pelarut_pilihan]["Harga per ml (Rp)"].values[0]
                racikan_user.append({
                    "Nama Bahan": pelarut_pilihan, "Tipe": "Pelarut", "Volume (ml)": vol_pelarut,
                    "Harga/ml": harga_per_ml, "Subtotal (Rp)": vol_pelarut * harga_per_ml
                })

    # LOGIKA 2: JIKA MEMILIH CUSTOM (MANUAL SEPERTI VERSI SEBELUMNYA)
    else:
        st.info("Mode Manual Aktif. Silakan masukkan bahan dan volume secara bebas.")
        list_nama_all = df_bahan["Nama Bahan"].tolist()
        jumlah_bahan = st.number_input("Jumlah jenis bahan yang dicampur", min_value=1, max_value=10, value=3)
        
        for i in range(int(jumlah_bahan)):
            col_b1, col_b2 = st.columns([3, 1])
            with col_b1:
                idx_default = min(i, len(list_nama_all)-1)
                bahan_terpilih = st.selectbox(f"Bahan {i+1}", list_nama_all, key=f"manual_bahan_{i}", index=idx_default)
            with col_b2:
                vol_terpilih = st.number_input(f"Volume (ml)", min_value=0.0, max_value=500.0, value=10.0, step=0.5, key=f"manual_vol_{i}")
            
            harga_per_ml = df_bahan[df_bahan["Nama Bahan"] == bahan_terpilih]["Harga per ml (Rp)"].values[0]
            tipe_bahan = df_bahan[df_bahan["Nama Bahan"] == bahan_terpilih]["Tipe"].values[0]
            
            racikan_user.append({
                "Nama Bahan": bahan_terpilih, "Tipe": tipe_bahan, "Volume (ml)": vol_terpilih,
                "Harga/ml": harga_per_ml, "Subtotal (Rp)": vol_terpilih * harga_per_ml
            })

    # ==================== PROSES PERHITUNGAN AKHIR ====================
    df_racikan = pd.DataFrame(racikan_user)
    total_volume_cairan = df_racikan["Volume (ml)"].sum()
    total_biaya_cairan = df_racikan["Subtotal (Rp)"].sum()
    total_hpp_produk = total_biaya_cairan + harga_kemasan

    vol_bibit_real = df_racikan[df_racikan["Tipe"] == "Bibit"]["Volume (ml)"].sum()
    vol_pelarut_real = df_racikan[df_racikan["Tipe"] == "Pelarut"]["Volume (ml)"].sum()
    
    rasio_bibit_pct = (vol_bibit_real / total_volume_cairan * 100) if total_volume_cairan > 0 else 0
    rasio_pelarut_pct = (vol_pelarut_real / total_volume_cairan * 100) if total_volume_cairan > 0 else 0

    # Peringatan Validasi jika di mode otomatis tapi total ml diubah manual oleh user hingga tidak pas
    if rasio_bibit_otomatis is not None and abs(total_volume_cairan - target_volume) > 0.01:
        st.warning(f"⚠️ Perhatian: Total volume campuran saat ini ({total_volume_cairan:.1f} ml) tidak sama dengan target volume botol yang Anda tentukan ({target_volume} ml). Harap sesuaikan angka ml di atas agar pas.")

    st.markdown("---")
    st.subheader(f"📊 Hasil Analisis Ringkasan: {nama_varian}")
    
    # Ringkasan Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Volume Cairan", f"{total_volume_cairan:.1f} ml")
    m2.metric("Rasio Nyata (Bibit : Pelarut)", f"{rasio_bibit_pct:.0f}% : {rasio_pelarut_pct:.0f}%")
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
