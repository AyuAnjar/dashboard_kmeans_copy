import streamlit as st
from utils.preprocessing import preprocess_data

# Atur layout penuh
st.set_page_config(layout="wide")

# CSS tambahan untuk styling
st.markdown("""
    <style>
    .section-box {
        background-color: #F5FFFA;
        padding: 20px;
        border-left: 6px solid #3CB371;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .note {
        font-size: 16px;
        color: #444;
    }
    </style>
""", unsafe_allow_html=True)

# Judul
st.title("🧹 Preprocessing Data Penjualan")

# Penjelasan
st.markdown("""
<div class='section-box'>
    <p class='note'>
    Tahapan ini akan membersihkan dan mempersiapkan data penjualan sebelum dilakukan proses clustering.  
    Proses mencakup:
    </p>
    <ul>
        <li> Penghapusan kolom tidak relevan</li>
        <li> Normalisasi data</li>
        <li> Deteksi dan pembersihan data tidak valid</li>
        <li> Pembuatan kombinasi produk per bulan</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Proses preprocessing
if st.session_state.get("df") is not None:
    with st.spinner("🔄 Sedang memproses data..."):
        processed = preprocess_data(st.session_state.df)
        st.session_state.processed_df = processed

    st.success("✅ Preprocessing selesai! Data siap untuk clustering.")
    st.markdown("### 🔍 Pratinjau Data Hasil Preprocessing")
    st.dataframe(processed, use_container_width=True)

    with st.expander("📘 Keterangan Tambahan"):
        st.markdown("""
        - Data sudah dikelompokkan berdasarkan bulan dan produk.
        - Nilai transaksi kosong telah diisi dengan 0.
        - Format nama produk sudah dikapitalisasi.
        """)
else:
    st.warning("⚠️ Silakan unggah data terlebih dahulu melalui halaman **Upload Data**.")
