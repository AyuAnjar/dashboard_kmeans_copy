import streamlit as st
import pandas as pd
from utils.simulasi import (
    preprocess_data_simulasi, elbow_method_simulasi, 
    run_kmeans_simulasi, show_elbow_chart_simulasi, 
    show_cluster_chart_simulasi, show_summary_table_simulasi, 
    show_line_charts_simulasi
)

# Inisialisasi session state
if 'df_simulasi' not in st.session_state:
    st.session_state.df_simulasi = None

# Atur layout lebar penuh
st.set_page_config(layout="wide")

# Gaya tambahan
st.markdown("""
    <style>
    .highlight {
        background-color: #FDF5E6;
        padding: 10px;
        border-left: 6px solid #FFA500;
        border-radius: 4px;
    }
    .info-box {
        background-color: #F0F8FF;
        padding: 15px;
        border-left: 6px solid #1E90FF;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .upload-note {
        font-size: 16px;
        color: #555;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# st.markdown("<div class='big-font'>👋 Halo! Halaman Simulasi dibuat untuk menguji dan menganalisis performa penjualan dari produk baru yang hanya terjual dalam periode tertentu dengan jumlah terbatas. </i>.</div>", unsafe_allow_html=True)
st.title("🎯 Tujuan Halaman Simulasi")
st.markdown("""
    <div class="highlight">
    <ul>
        <li>📆 Menguji dan menganalisis performa penjualan dari produk baru yang hanya terjual dalam periode tertentu dengan jumlah terbatas.</li>
        <li>📈Pengguna dapat menilai apakah sebuah produk layak untuk dijual kembali atau dipertimbangkan masuk ke dalam jajaran produk tetap di toko.</li>
        <li>📌 Dasar pengambilan keputusan ketika menerima tawaran produk baru dari supplier atau pihak ketiga.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
st.write("---")

# Judul Halaman
st.title("📂 Upload Data Penjualan Percobaan")

# Deskripsi Awal
st.markdown("""
<div class="info-box">
    <p class="upload-note">
    Silakan unggah file <strong>CSV</strong> berisi data penjualan minuman kopi kemasan siap minum. 
    Pastikan file memiliki kolom penting seperti: <code>id_detail_transaksi_penjualan</code>, <code>no_transaksi_penjualan</code>, <code>kode_barang</code>, <code>nama_barang</code> dan <code>qty</code>.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("📤 Unggah file CSV kamu di sini", type="csv")
if uploaded:
    df = pd.read_csv(uploaded, dtype={'no_transaksi_penjualan': str, 'kode_barang': str})
    expected = {'no_transaksi_penjualan', 'id_detail_transaksi_penjualan', 'kode_barang', 'nama_barang', 'qty'}
    if expected.issubset(df.columns):
        st.session_state.df_simulasi = df
        st.session_state.uploaded_file = uploaded
        st.success("✅ Data berhasil diunggah!")
        st.markdown("#### 🔍 Pratinjau Data:")
        st.dataframe(df.head())
    else:
        st.error("❌ Kolom wajib belum lengkap! Pastikan terdapat kolom: no_transaksi_penjualan, qty, dan nama_barang.")
elif st.session_state.df_simulasi is not None:
        st.info("📁 Menampilkan data dari file yang sudah diunggah sebelumnya.")
        st.dataframe(st.session_state.df_simulasi.head())
st.write("---")

# Judul
st.title("🧹 Preprocessing Data Penjualan")
# Penjelasan
# st.markdown("""
# <div class='section-box'>
#     <p class='note'>
#     Tahapan ini akan membersihkan dan mempersiapkan data penjualan sebelum dilakukan proses clustering.  
#     Proses mencakup:
#     </p>
#     <ul>
#         <li> Penghapusan kolom tidak relevan</li>
#         <li> Normalisasi data</li>
#         <li> Deteksi dan pembersihan data tidak valid</li>
#         <li> Pembuatan kombinasi produk per bulan</li>
#     </ul>
# </div>
# """, unsafe_allow_html=True)

# Proses preprocessing
if st.session_state.get("df_simulasi") is not None:
    with st.spinner("🔄 Sedang memproses data..."):
        processed = preprocess_data_simulasi(st.session_state.df_simulasi)
        st.session_state.processed_df_simulasi = processed

    st.success("✅ Preprocessing selesai! Data siap untuk clustering.")
    st.markdown("### 🔍 Pratinjau Data Hasil Preprocessing")
    st.dataframe(processed, use_container_width=True)

    # with st.expander("📘 Keterangan Tambahan"):
    #     st.markdown("""
    #     - Data sudah dikelompokkan berdasarkan bulan dan produk.
    #     - Nilai transaksi kosong telah diisi dengan 0.
    #     - Format nama produk sudah dikapitalisasi.
    #     """)
else:
    st.warning("⚠️ Silakan unggah data terlebih dahulu.")
st.write("---")

# Judul halaman
st.title("🔍 K-Means Clustering Produk")
# Penjelasan awal
# st.markdown("""
# <div class="highlight-box">
#     <p class="step">
#     Proses clustering akan mengelompokkan produk berdasarkan pola <b>jumlah transaksi</b> dan <b>total penjualan</b>.  
#     Langkah-langkahnya meliputi:
#     </p>
#     <ul>
#         <li>📉 Penetapan jumlah cluster 3 sesuai dengan tujuan analisis yang didukung Metode Elbow</li>   
#         <li>📊 Menjalankan algoritma K-Means pada data</li>
#         <li>🎨 Menampilkan visualisasi hasil clustering</li>
#     </ul>
# </div>
# """, unsafe_allow_html=True)

# Cek data
if 'processed_df_simulasi' in st.session_state and st.session_state.processed_df_simulasi is not None:
    df = st.session_state.processed_df_simulasi

    # Jalankan elbow method jika belum ada
    if 'pivot_simulasi' not in st.session_state or 'distortions' not in st.session_state:
        with st.spinner("🔄 Menghitung inertia untuk berbagai jumlah cluster..."):
            pivot, distortions = elbow_method_simulasi(df)
            st.session_state.pivot_simulasi = pivot
            st.session_state.distortions_simulasi = distortions
    else:
        pivot = st.session_state.pivot_simulasi
        distortions = st.session_state.distortions_simulasi

    # Tampilkan grafik Elbow
    st.subheader("📉 Elbow Method")
    show_elbow_chart_simulasi(distortions)
    st.caption("Pada perhitungan ini menggunakan cluster 3 karena data akan terbagi menjadi cluster rendah, sedang dan tinggi.")

    # # Pilih jumlah cluster
    # default_k = st.session_state.get("selected_k", 3)
    # k = st.selectbox("🔢 Pilih Jumlah Cluster", options=[3], index=0)  # Hanya cluster 3 yang digunakan

    # Jalankan Clustering
    if st.button("🚀 Jalankan Clustering"):
        with st.spinner("🧠 Melakukan clustering..."):
            clustered = run_kmeans_simulasi(df, n_clusters=3)
            st.session_state.clustered_df_simulasi = clustered
            # st.session_state.selected_k = k

        st.success("✅ Clustering selesai!")

    # Tampilkan hasil clustering jika sudah ada
    if 'clustered_df_simulasi' in st.session_state:
        clustered = st.session_state.clustered_df_simulasi

        st.subheader("📍 Visualisasi Hasil Clustering")
        show_cluster_chart_simulasi(clustered)

        st.subheader("📊 Ringkasan Jumlah Produk per Cluster")
        cluster_counts = clustered.groupby('cluster')['kategori'].value_counts().reset_index(name='Jumlah Data')
        cluster_counts.columns = ['Cluster', 'Kategori Cluster', 'Jumlah Data']
        st.dataframe(cluster_counts, use_container_width=True)

        with st.expander("📦 Rincian Data per Cluster"):
            for i in sorted(clustered['cluster'].unique()):
                st.markdown(f"### 🔹 Cluster {i} - {clustered[clustered['cluster'] == i]['kategori'].iloc[0]}")
                st.dataframe(clustered[clustered['cluster'] == i], use_container_width=True)

else:
    st.warning("⚠️ Silakan lakukan preprocessing data terlebih dahulu.")
st.write("---")

st.title("📊 Ringkasan Hasil Clustering & Grafik Penjualan")
# st.markdown("""
# <div class="highlight-box">
#     <p class="note">
#     Halaman ini menampilkan <strong>analisis penjualan bulanan</strong> berdasarkan hasil clustering, 
#     serta mengevaluasi <strong>pengaruh hari libur nasional</strong> terhadap produk.
#     </p>
# </div>
# """, unsafe_allow_html=True)

# Pastikan data sudah di-cluster
if 'clustered_df_simulasi' in st.session_state:
    df = st.session_state.clustered_df_simulasi

    # if 'bulan' not in df.columns:
    #     df['bulan'] = pd.to_datetime(df['tanggal']).dt.to_period('M').astype(str)

    # hari_libur = get_hari_libur_bulanan(df)

    # # Daftar hari libur
    # with st.expander("📅 Daftar Hari Libur Nasional"):
    #     if hari_libur:
    #         for bulan, libur in hari_libur.items():
    #             st.write(f"📌 {bulan}: {libur}")
    #     else:
    #         st.write("❌ Tidak ada hari libur yang terdeteksi.")

    # st.info("ℹ️ Data hari libur hanya mencakup tahun 2022 hingga 2027.")
    # st.write("---")

    # Tabel ringkasan penjualan
    st.subheader("📋 Ringkasan Penjualan Bulanan")
    summary_df = show_summary_table_simulasi(df)
    st.write("---")

    st.subheader("📈 Grafik Penjualan Tiap Produk")
    with st.expander("📈 Grafik Penjualan Tiap Produk"):
        show_line_charts_simulasi(df)

else:
    st.warning("⚠️ Silakan lakukan preprocessing dan clustering data terlebih dahulu.")