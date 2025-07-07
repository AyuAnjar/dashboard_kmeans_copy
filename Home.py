import streamlit as st

# Atur layout lebar penuh
st.set_page_config(layout="wide")

# Gaya tambahan
st.markdown("""
    <style>
    .big-font {
        font-size: 24px !important;
        font-weight: 600;
    }
    .highlight {
        background-color: #FDF5E6;
        padding: 10px;
        border-left: 6px solid #FFA500;
        border-radius: 4px;
    }
    .title-highlight {
        font-size: 32px !important;
        color: #2E8B57;
    }
    </style>
""", unsafe_allow_html=True)

# Judul besar
st.title("📊 Selamat Datang di Dashboard Clustering Data Penjualan")
# st.markdown("<h1 class='title-highlight'>📊 Selamat Datang di Dashboard Clustering Data Penjualan</h1>", unsafe_allow_html=True)

# Subjudul informatif
st.markdown("<div class='big-font'>👋 Halo! Dashboard ini dibuat untuk menganalisis pola penjualan minuman kopi kemasan siap minum menggunakan <i>K-Means Clustering</i>.</div>", unsafe_allow_html=True)
st.markdown("---")

# Dua kolom pembuka
# col1, col2 = st.columns([2, 1])
# with col1:
st.subheader("🎯 Tujuan Dashboard")
st.markdown("""
    <div class="highlight">
    <ul>
        <li>📌 Mengelompokkan produk berdasarkan tingkat penjualannya.</li>
        <li>📆 Menganalisis pengaruh hari peringatan nasional terhadap penjualan.</li>
        <li>📈 Menyediakan visualisasi dan insight interaktif dari hasil clustering.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.subheader("🎯 Tata Cara Penggunaan Dashboard")
st.markdown("""
    <div class="highlight">
    <ul>
        <li>1. Unggah Data Penjualan
            <br>Masuk ke halaman <strong>Upload Data</strong>, lalu unggah file data penjualan dalam format <strong>.csv.</strong> Pastikan file memuat informasi seperti <strong>id detail transaksi penjualan, no transaksi penjualan, kode barang, nama barang, dan qty</strong>.</li>
        <li>2. Lakukan Preprocessing
            <br>Buka halaman <strong>Preprocessing</strong> untuk membersihkan dan memproses data. Sistem akan mengolah data sesuai dengan kebutuhan clustering.</li>
        <li>3. Lakukan Clustering
            <br>Masuk ke halaman <strong>KMeans Clustering</strong> untuk menjalankan proses clustering. Hasil clustering akan divisualisasikan dalam bentuk scatter plot.</li>
        <li>4. Lihat Hasil dan Insight
            <br>Di halaman <strong>Hasil</strong>, Anda dapat melihat:
            <br>- Tabel ringkasan penjualan bulanan per produk.
            <br>- Grafik penjualan tiap produk.
            <br>- Daftar hari libur nasional dan dampaknya terhadap penjualan.
            <br>- Interpretasi dan insight penjualan.</li>
        <li>5. Dapatkan Saran
            <br>Buka halaman <strong>Saran</strong> untuk melihat rekomendasi penataan produk dan pengelolaan stok berdasarkan hasil clustering dan momen hari libur.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
