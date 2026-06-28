import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Refill Blend Studio",
    page_icon="🧪",
    layout="wide"
)

# Database Karakter Kategori Aroma Universal (Standard Olfactive Families)
DATABASE_AROMA_AI = {
    "floral": {
        "top": ["Rose", "Peony", "Freesia"],
        "mid": ["Jasmine", "Lily of the Valley", "Magnolia"],
        "base": ["White Musk", "Sandalwood", "Soft Amber"],
        "vibe": "Anggun, Feminin, Klasik, dan Menyegarkan khas Bunga"
    },
    "woody": {
        "top": ["Cedar Leaf", "Cypress", "Cardamom"],
        "mid": ["Cedarwood", "Sandalwood", "Patchouli"],
        "base": ["Vetiver", "Oakmoss", "Gaiac Wood"],
        "vibe": "Hangat, Maskulin, Earthy, Tenang, dan Sangat Elegan"
    },
    "fruity": {
        "top": ["Red Berries", "Green Apple", "Peach"],
        "mid": ["Strawberry", "Blackcurrant", "Plum"],
        "base": ["Vanilla", "Light Musk"],
        "vibe": "Manis Buah, Ceria, Playful, Energetik, dan Segar"
    },
    "aquatic": {
        "top": ["Sea Notes", "Mint", "Calone"],
        "mid": ["Sea Salt", "Lavender", "Rosemary"],
        "base": ["Ambergris", "White Musk", "Sage"],
        "vibe": "Segar Nuansa Laut, Bersih, Sporty, Kasual, dan Ringan"
    },
    "citrus": {
        "top": ["Bergamot", "Lemon", "Mandarin Orange"],
        "mid": ["Grapefruit", "Orange Blossom", "Neroli"],
        "base": ["Clearwood", "Light Musk"],
        "vibe": "Sangat Segar, Tajam, Penuh Energi, Bersih, dan Terang"
    },
    "gourmand": {
        "top": ["Caramel", "Whipped Cream"],
        "mid": ["Vanilla Orchid", "Heliotrope", "Coconut"],
        "base": ["Vanilla Bean", "Brown Sugar", "Amber"],
        "vibe": "Manis Makanan, Hangat, Sangat Manis, Lembut, dan Cozy"
    },
    "oriental": {
        "top": ["Saffron", "Cinnamon", "Pink Pepper"],
        "mid": ["Amberwood", "Labdanum", "Clove"],
        "base": ["Amber", "Oud", "Incense", "Tonka Bean"],
        "vibe": "Mewah, Eksotis, Rempah Hangat, Deep, dan Tahan Lama"
    }
}

# Database Karakteristik Teknis Merk Pabrikan Parfum Refill
DATABASE_MERK_AI = {
    "luzi": "Karakter Eksklusif Luzi: Memiliki konsentrasi minyak yang pekat, sillage (jejak aroma) yang kuat, serta sangat baik dalam mengunci kedalaman Base Notes agar bertahan lebih lama.",
    "iberchem": "Karakter Eksklusif Iberchem: Sangat unggul dalam memancarkan Top Notes yang segar dan cerah, memiliki karakter cairan yang ringan, dan sangat stabil di iklim tropis.",
    "parfex": "Karakter Eksklusif Parfex: Menghasilkan transisi aroma (evaporasi) yang sangat halus dari Top ke Mid Notes, dengan akurasi aroma yang dikenal sangat rapi dan presisi.",
    "argeville": "Karakter Eksklusif Argeville: Cenderung memberikan nuansa akhir yang manis (sweet), padat (bold), dan memiliki karakter rempah atau kayu yang menonjol mantap.",
    "macco": "Karakter Eksklusif Macco: Memiliki daya ikat yang baik terhadap pelarut jenis alkohol, membuat aroma racikan stabil dan meminimalkan bau menyengat di awal semprotan.",
    "labor": "Karakter Eksklusif Labor: Dikenal dengan karakter aroma yang linear dan konsisten sejak awal disemprotkan hingga kering (drydown)."
}

def analisis_aroma_racikan(list_info_bibit):
    """Fungsi Engine AI Universal untuk mendeteksi karakter wangi dan pengaruh merk pabrikan"""
    top_notes = set()
    mid_notes = set()
    base_notes = set()
    vibes = set()
    catatan_merk = set()
    
    terdeteksi = False
    
    for bibit in list_info_bibit:
        # Pengecekan aman jika user mengosongkan sel merk/nama di data editor
        nama_lower = str(bibit.get("nama", "")).lower()
        merk_lower = str(bibit.get("merk", "")).lower()
        
        # 1. Analisis Karakter Wangi
        for kunci, data in DATABASE_AROMA_AI.items():
            if kunci in nama_lower:
                top_notes.update(data["top"])
                mid_notes.update(data["mid"])
                base_notes.update(data["base"])
                vibes.add(data["vibe"])
                terdeteksi = True
                
        # 2. Analisis Pengaruh Merk Pabrikan
        for merk_kunci, deskripsi in DATABASE_MERK_AI.items():
            if merk_kunci in merk_lower:
                catatan_merk.add(deskripsi)
                
    if not terdeteksi:
        return None
        
    return {
        "top": list(top_notes),
        "mid": list(mid_notes),
        "base": list(base_notes),
        "vibe": " & ".join(vibes),
        "catatan_merk": list(catatan_merk)
    }

# Inisialisasi Database Umum bawaan aplikasi (Sudah dilengkapi Kolom Merk)
if 'inventaris_bahan' not in st.session_state:
    st.session_state.inventaris_bahan = [
        {"Nama Bahan": "Sweet Vanilla (Gourmand)", "Merk": "Parfex", "Tipe": "Bibit", "Harga per ml (Rp)": 1800},
        {"Nama Bahan": "Bergamot Fresh (Citrus)", "Merk": "Iberchem", "Tipe": "Bibit", "Harga per ml (Rp)": 1500},
        {"Nama Bahan": "Rose Jasmine (Floral)", "Merk": "Luzi", "Tipe": "Bibit", "Harga per ml (Rp)": 2000},
        {"Nama Bahan": "Sandalwood Luxe (Woody)", "Merk": "Argeville", "Tipe": "Bibit", "Harga per ml (Rp)": 2200},
        {"Nama Bahan": "Absolute Alkohol", "Merk": "-", "Tipe": "Pelarut", "Harga per ml (Rp)": 100},
        {"Nama Bahan": "Fixative Pengawet", "Merk": "-", "Tipe": "Pelarut", "Harga per ml (Rp)": 600},
    ]

if 'inventaris_kemasan' not in st.session_state:
    st.session_state.inventaris_kemasan = [
        {"Nama Kemasan": "Botol Spray Standar 30ml", "Harga Satuan (Rp)": 5000},
        {"Nama Kemasan": "Botol Spray Premium 50ml", "Harga Satuan (Rp)": 8000},
    ]

# Header Aplikasi
st.title("🧪 Refill Blend Studio")
st.caption("Kalkulator Formula, HPP, dan Simulasi Karakter Aroma Universal Berdasarkan Kualitas Pabrikan Bibit")
st.markdown("---")

# Menu Navigasi Tab
tab1, tab2 = st.tabs(["🧮 Kalkulator & Analisis AI", "📦 Kelola Inventaris Bahan"])

# ==================== TAB 1: KALKULATOR FORMULA ====================
with tab1:
    st.header("Racikan Formula Baru")
    
    col_var1, col_var2 = st.columns(2)
    with col_var1:
        nama_varian = st.text_input("Nama Varian / Kode Racikan", value="Racikan No. 01")
    with col_var2:
        df_kemasan = pd.DataFrame(st.session_state.inventaris_kemasan)
        # Menghindari error jika tabel kemasan kosong
        if not df_kemasan.empty and "Nama Kemasan" in df_kemasan.columns:
            pilihan_kemasan = st.selectbox("Pilih Botol & Kemasan", df_kemasan["Nama Kemasan"].tolist())
            harga_kemasan = df_kemasan[df_kemasan["Nama Kemasan"] == pilihan_kemasan]["Harga Satuan (Rp)"].values[0]
        else:
            pilihan_kemasan = "Kemasan Belum Diisi"
            harga_kemasan = 0

    st.markdown("---")
    st.subheader("💡 Panduan & Pengaturan Konsentrasi Otomatis")
    
    opsi_konsentrasi = {
        "EDP (Eau de Parfum) - Standar Toko Refill [Rasio Bibit 50%]" : 0.50,
        "Extrait de Parfum - Sangat Pekat & Tahan Lama [Rasio Bibit 60%]": 0.60,
        "Custom (Atur Manual Komposisi Bebas)": None
    }
    
    pilihan_tipe = st.selectbox("Pilih Tipe Konsentrasi", list(opsi_konsentrasi.keys()))
    rasio_bibit_otomatis = opsi_konsentrasi[pilihan_tipe]

    col_vol1, col_vol2 = st.columns(2)
    with col_vol1:
        target_volume = st.number_input("Target Total Volume Parfum (ml)", min_value=5.0, max_value=500.0, value=30.0, step=5.0)

    df_bahan = pd.DataFrame(st.session_state.inventaris_bahan)
    
    # Menghindari error jika tabel bahan kosong
    if not df_bahan.empty and "Tipe" in df_bahan.columns and "Nama Bahan" in df_bahan.columns:
        list_bibit = df_bahan[df_bahan["Tipe"] == "Bibit"]["Nama Bahan"].tolist()
        list_pelarut = df_bahan[df_bahan["Tipe"] == "Pelarut"]["Nama Bahan"].tolist()
    else:
        list_bibit = []
        list_pelarut = []

    st.markdown("---")
    st.subheader("🧪 Komposisi Campuran Cairan")

    racikan_user = []
    info_bibit_terpakai = []

    if not list_bibit or not list_pelarut:
        st.error("⚠️ Data Bibit atau Pelarut di Tab Inventaris kosong/tidak lengkap. Silakan isi terlebih dahulu.")
    else:
        # LOGIKA MODE OTOMATIS
        if rasio_bibit_otomatis is not None:
            st.success(f"Mode Otomatis Aktif! Rasio dikunci untuk: {pilihan_tipe}")
            ml_bibit_total = target_volume * rasio_bibit_otomatis
            ml_pelarut_total = target_volume * (1.0 - rasio_bibit_otomatis)

            col_auto1, col_auto2 = st.columns(2)
            with col_auto1:
                st.write(f"**Alokasi Bibit Parfum (Total: {ml_bibit_total:.1f} ml):**")
                jumlah_layer_bibit = st.number_input("Berapa jenis bibit parfum yang dicampur?", min_value=1, max_value=5, value=1, key="count_bibit")
                vol_per_bibit = ml_bibit_total / jumlah_layer_bibit
                
                for i in range(int(jumlah_layer_bibit)):
                    col_sub1, col_sub2 = st.columns([2, 1])
                    with col_sub1:
                        bibit_pilihan = st.selectbox(f"Pilih Bibit {i+1}", list_bibit, key=f"auto_bibit_{i}")
                        merk_pilihan = df_bahan[df_bahan["Nama Bahan"] == bibit_pilihan]["Merk"].values[0]
                        info_bibit_terpakai.append({"nama": bibit_pilihan, "merk": merk_pilihan})
                    with col_sub2:
                        vol_bibit = st.number_input(f"Volume (ml)", min_value=0.0, max_value=target_volume, value=vol_per_bibit, step=0.5, key=f"auto_vol_bibit_{i}")
                    
                    harga_per_ml = df_bahan[df_bahan["Nama Bahan"] == bibit_pilihan]["Harga per ml (Rp)"].values[0]
                    racikan_user.append({
                        "Nama Bahan": f"{bibit_pilihan} ({merk_pilihan})", "Tipe": "Bibit", "Volume (ml)": vol_bibit,
                        "Harga/ml": harga_per_ml, "Subtotal (Rp)": vol_bibit * harga_per_ml
                    })

            with col_auto2:
                st.write(f"**Alokasi Pelarut (Total: {ml_pelarut_total:.1f} ml):**")
                jumlah_layer_pelarut = st.number_input("Berapa jenis cairan pelarut?", min_value=1, max_value=3, value=1, key="count_pelarut")
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

        # LOGIKA MODE CUSTOM/MANUAL
        else:
            st.info("Mode Manual Aktif. Silakan masukkan bahan dan volume secara bebas.")
            list_nama_all = df_bahan["Nama Bahan"].tolist()
            jumlah_bahan = st.number_input("Jumlah jenis bahan yang dicampur", min_value=1, max_value=10, value=3)
            
            for i in range(int(jumlah_bahan)):
                col_b1, col_b2 = st.columns([3, 1])
                with col_b1:
                    idx_default = min(i, len(list_nama_all)-1)
                    bahan_terpilih = st.selectbox(f"Bahan {i+1}", list_nama_all, key=f"manual_bahan_{i}", index=idx_default)
                    
                    tipe_bahan = df_bahan[df_bahan["Nama Bahan"] == bahan_terpilih]["Tipe"].values[0]
                    merk_pilihan = df_bahan[df_bahan["Nama Bahan"] == bahan_terpilih]["Merk"].values[0]
                    
                    if tipe_bahan == "Bibit":
                        info_bibit_terpakai.append({"nama": bahan_terpilih, "merk": merk_pilihan})
                with col_b2:
                    vol_terpilih = st.number_input(f"Volume (ml)", min_value=0.0, max_value=500.0, value=10.0, step=0.5, key=f"manual_vol_{i}")
                
                harga_per_ml = df_bahan[df_bahan["Nama Bahan"] == bahan_terpilih]["Harga per ml (Rp)"].values[0]
                
                racikan_user.append({
                    "Nama Bahan": f"{bahan_terpilih} ({merk_pilihan})" if tipe_bahan == "Bibit" else bahan_terpilih, 
                    "Tipe": tipe_bahan, "Volume (ml)": vol_terpilih,
                    "Harga/ml": harga_per_ml, "Subtotal (Rp)": vol_terpilih * harga_per_ml
                })

        # PROSES KALKULASI AKHIR
        df_racikan = pd.DataFrame(racikan_user)
        total_volume_cairan = df_racikan["Volume (ml)"].sum()
        total_biaya_cairan = df_racikan["Subtotal (Rp)"].sum()
        total_hpp_produk = total_biaya_cairan + harga_kemasan

        vol_bibit_real = df_racikan[df_racikan["Tipe"] == "Bibit"]["Volume (ml)"].sum()
        vol_pelarut_real = df_racikan[df_racikan["Tipe"] == "Pelarut"]["Volume (ml)"].sum()
        rasio_bibit_pct = (vol_bibit_real / total_volume_cairan * 100) if total_volume_cairan > 0 else 0
        rasio_pelarut_pct = (vol_pelarut_real / total_volume_cairan * 100) if total_volume_cairan > 0 else 0

        # ==================== SEKSI ANALISIS AROMA AI ====================
        st.markdown("---")
        st.header("🧠 AI Olfactory Profile Analysis")
        
        hasil_analisis = analisis_aroma_racikan(info_bibit_terpakai)
        
        if hasil_analisis and vol_bibit_real > 0:
            st.subheader(f"✨ Karakter Utama Campuran: *{hasil_analisis['vibe']}*")
            
            if hasil_analisis["catatan_merk"]:
                st.markdown("##### 🏢 Pengaruh Teknis Pabrikan Terhadap Aroma:")
                for catatan in hasil_analisis["catatan_merk"]:
                    st.info(catatan)

            col_ai1, col_ai2, col_ai3 = st.columns(3)
            with col_ai1:
                st.markdown("🟢 **Top Notes (Kesan Pertama - 15 Menit Pertama)**")
                for note in hasil_analisis["top"]:
                    st.markdown(f"- {note}")
            with col_ai2:
                st.markdown("🟡 **Mid/Heart Notes (Inti Wangi - 15 Menit s/d 4 Jam)**")
                for note in hasil_analisis["mid"]:
                    st.markdown(f"- {note}")
            with col_ai3:
                st.markdown("🔴 **Base Notes (Daya Tahan Akhir - Di atas 4 Jam)**")
                for note in hasil_analisis["base"]:
                    st.markdown(f"- {note}")
        else:
            st.info("💡 **Tips AI:** Agar profil aroma muncul otomatis, pastikan nama bibit mengandung kategori aroma (*Floral, Woody, Fruity, Aquatic, Citrus, Gourmand, atau Oriental*).")

        if rasio_bibit_otomatis is not None and abs(total_volume_cairan - target_volume) > 0.01:
            st.warning(f"⚠️ Perhatian: Total volume campuran saat ini ({total_volume_cairan:.1f} ml) tidak sama dengan target volume botol yang Anda tentukan ({target_volume} ml). Harap sesuaikan angka ml di atas agar pas.")

        # Ringkasan Keuangan HPP
        st.markdown("---")
        st.subheader(f"📊 Ringkasan Finansial & Rasio: {nama_varian}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Volume Cairan", f"{total_volume_cairan:.1f} ml")
        m2.metric("Rasio (Bibit : Pelarut)", f"{rasio_bibit_pct:.0f}% : {rasio_pelarut_pct:.0f}%")
        st.metric("💰 TOTAL HPP PER BOTOL", f"Rp {total_hpp_produk:,.0f}")

        st.write("**Rincian Komposisi Biaya:**")
        st.dataframe(df_racikan[["Nama Bahan", "Tipe", "Volume (ml)", "Subtotal (Rp)"]], use_container_width=True)
        st.write(f"- Biaya Wadah/Kemasan ({pilihan_kemasan}): **Rp {harga_kemasan:,}**")
        st.write(f"- Total Biaya Cairan Esens: **Rp {total_biaya_cairan:,}**")

# ==================== TAB 2: KELOLA INVENTARIS (INTERAKTIF) ====================
with tab2:
    st.header("Manajemen Inventaris Bahan & Harga")
    st.info("💡 **Petunjuk Penggunaan:**\n- **Edit Data:** Ketuk (klik) langsung pada teks atau angka di dalam tabel untuk mengubahnya.\n- **Tambah Data:** Gulir ke baris kosong paling bawah tabel (ada tanda **+**), lalu ketik data baru di situ.\n- **Hapus Data:** Klik kotak kecil di ujung kiri baris yang ingin dihapus, lalu tekan ikon **Tong Sampah** di pojok kanan atas tabel.")
    
    col_inv1, col_inv2 = st.columns(2)
    
    with col_inv1:
        st.subheader("1. Daftar Bibit & Pelarut")
        # Menampilkan Data Editor Interaktif
        df_tampil_bahan = pd.DataFrame(st.session_state.inventaris_bahan)
        
        # Konfigurasi kolom agar lebih rapi saat diedit
        config_kolom_bahan = {
            "Tipe": st.column_config.SelectboxColumn(
                "Tipe", options=["Bibit", "Pelarut"], required=True
            ),
            "Merk": st.column_config.SelectboxColumn(
                "Merk", options=["Luzi", "Iberchem", "Parfex", "Argeville", "Macco", "Labor", "Expression", "-", "Lainnya"], required=True
            ),
            "Harga per ml (Rp)": st.column_config.NumberColumn(
                "Harga per ml (Rp)", min_value=0, step=100, required=True
            )
        }
        
        edited_bahan = st.data_editor(
            df_tampil_bahan,
            num_rows="dynamic", # Memungkinkan penambahan dan penghapusan baris
            use_container_width=True,
            column_config=config_kolom_bahan,
            key="editor_bahan"
        )
        # Simpan perubahan secara otomatis
        st.session_state.inventaris_bahan = edited_bahan.to_dict('records')

    with col_inv2:
        st.subheader("2. Daftar Botol & Kemasan")
        df_tampil_kemasan = pd.DataFrame(st.session_state.inventaris_kemasan)
        
        config_kolom_kemasan = {
            "Harga Satuan (Rp)": st.column_config.NumberColumn(
                "Harga Satuan (Rp)", min_value=0, step=500, required=True
            )
        }
        
        edited_kemasan = st.data_editor(
            df_tampil_kemasan,
            num_rows="dynamic", # Memungkinkan penambahan dan penghapusan baris
            use_container_width=True,
            column_config=config_kolom_kemasan,
            key="editor_kemasan"
        )
        # Simpan perubahan secara otomatis
        st.session_state.inventaris_kemasan = edited_kemasan.to_dict('records')
