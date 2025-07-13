import streamlit as st
import pandas as pd

# Inisialisasi session state
if 'df' not in st.session_state:
    st.session_state.df = None

# Atur layout lebar penuh
st.set_page_config(layout="wide")

# Gaya tambahan
# st.markdown("""
#     <style>
#     .info-box {
#         background-color: #F0F8FF;
#         padding: 15px;
#         border-left: 6px solid #1E90FF;
#         border-radius: 5px;
#         margin-bottom: 15px;
#     }
#     .upload-note {
#         font-size: 16px;
#         color: #555;
#         line-height: 1.6;
#     }
#     </style>
# """, unsafe_allow_html=True)
st.markdown("""
    <style>
    .info-box {
        background-color: #F0F8FF;
        padding: 15px;
        border-left: 6px solid #1E90FF;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .upload-note {
        font-size: 16px;
        color: #333;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Judul Halaman
st.title("📂 Upload Data Penjualan")

# Deskripsi Awal
# st.markdown("""
# <div class="info-box">
#     <p class="upload-note">
#     Silakan unggah file <strong>CSV</strong> berisi data penjualan minuman kopi kemasan siap minum. 
#     Pastikan file memiliki kolom penting seperti: <code>id_detail_transaksi_penjualan</code>, <code>no_transaksi_penjualan</code>, <code>kode_barang</code>, <code>nama_barang</code> dan <code>qty</code>.
#     </p>
# </div>
# """, unsafe_allow_html=True)

st.info(
    """
📤 **Silakan unggah file CSV** berisi data penjualan minuman kopi kemasan siap minum.  
Pastikan file memiliki kolom penting seperti: `id_detail_transaksi_penjualan`, `no_transaksi_penjualan`, `kode_barang`, `nama_barang`, dan `qty`.
"""
)



st.markdown("### 📝 Contoh Format Kolom:")
st.code("id_detail_transaksi_penjualan, no_transaksi_penjualan, kode_barang, nama_barang, qty, ...", language="csv")
st.markdown("Pastikan file tidak kosong dan dipisahkan oleh koma (`,`).")
st.write("---")

uploaded = st.file_uploader("📤 Unggah file CSV kamu di sini", type="csv")
if uploaded:
    df = pd.read_csv(uploaded, dtype={'no_transaksi_penjualan': str, 'kode_barang': str})
    expected = {'no_transaksi_penjualan', 'id_detail_transaksi_penjualan', 'kode_barang', 'nama_barang', 'qty'}
    if expected.issubset(df.columns):
        st.session_state.df = df
        st.session_state.uploaded_file = uploaded
        st.success("✅ Data berhasil diunggah!")
        st.markdown("#### 🔍 Pratinjau Data:")
        st.dataframe(df.head())
    else:
        st.error("❌ Kolom wajib belum lengkap! Pastikan terdapat kolom: no_transaksi_penjualan, qty, dan nama_barang.")
elif st.session_state.df is not None:
        st.info("📁 Menampilkan data dari file yang sudah diunggah sebelumnya.")
        st.dataframe(st.session_state.df.head())

# Footer info
st.caption("📌 Setelah data berhasil diunggah, silakan lanjut ke halaman *Preprocessing Data*.")
