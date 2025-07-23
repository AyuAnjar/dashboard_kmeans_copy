import streamlit as st
from utils.clustering import elbow_method, run_kmeans, show_elbow_chart, show_cluster_chart

# Atur layout lebar penuh
st.set_page_config(layout="wide")

# Gaya CSS tambahan
st.markdown("""
    <style>
    .highlight-box {
        background-color: #f0f9ff;
        padding: 16px;
        border-left: 6px solid #1e90ff;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .step {
        font-size: 16px;
        color: #333;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Judul halaman
st.title("🔍 K-Means Clustering Produk")

# Penjelasan awal
st.markdown("""
<div class="highlight-box">
    <p class="step">
    Proses clustering akan mengelompokkan produk berdasarkan pola <b>jumlah transaksi</b> dan <b>total penjualan</b>.  
    Langkah-langkahnya meliputi:
    </p>
    <ul>
        <li>📉 Penetapan jumlah cluster 3 sesuai dengan tujuan analisis yang didukung Metode Elbow</li>   
        <li>📊 Menjalankan algoritma K-Means pada data</li>
        <li>🎨 Menampilkan visualisasi hasil clustering</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Cek data
if 'processed_df' in st.session_state and st.session_state.processed_df is not None:
    df = st.session_state.processed_df

    # Jalankan elbow method jika belum ada
    if 'pivot' not in st.session_state or 'distortions' not in st.session_state:
        with st.spinner("🔄 Menghitung inertia untuk berbagai jumlah cluster..."):
            pivot, distortions = elbow_method(df)
            st.session_state.pivot = pivot
            st.session_state.distortions = distortions
    else:
        pivot = st.session_state.pivot
        distortions = st.session_state.distortions

    # Tampilkan grafik Elbow
    st.subheader("📉 Elbow Method")
    show_elbow_chart(distortions)
    st.caption("Pada perhitungan ini menggunakan cluster 3 karena data akan terbagi menjadi cluster rendah, sedang dan tinggi.")

    # # Pilih jumlah cluster
    # default_k = st.session_state.get("selected_k", 3)
    # k = st.selectbox("🔢 Pilih Jumlah Cluster", options=[3], index=0)  # Hanya cluster 3 yang digunakan

    # Jalankan Clustering
    if st.button("🚀 Jalankan Clustering"):
        with st.spinner("🧠 Melakukan clustering..."):
            clustered = run_kmeans(df, n_clusters=3)
            st.session_state.clustered_df = clustered
            # st.session_state.selected_k = k

        st.success("✅ Clustering selesai!")

    # Tampilkan hasil clustering jika sudah ada
    if 'clustered_df' in st.session_state:
        clustered = st.session_state.clustered_df

        st.subheader("📍 Visualisasi Hasil Clustering")
        show_cluster_chart(clustered)

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
    