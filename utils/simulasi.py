import streamlit as st
import plotly.express as px
import pandas as pd
# from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

def preprocess_data_simulasi(df):
    # 1. Hapus kolom tidak dibutuhkan
    kolom_dihapus = [
        'diskon', 'sub_harga', 'keterangan', 'foto_barang', 'id_satuan', 'nama_satuan',
        'id_golongan', 'nama_golongan', 'id_sub_golongan', 'nama_sub_golongan',
        'harga_jual_grosir', 'harga_jual_eceran', 'harga_jual_tanggal'
    ]
    df = df.drop(columns=[col for col in kolom_dihapus if col in df.columns])

    # 2. Normalisasi teks
    df['nama_barang'] = df['nama_barang'].astype(str).str.strip().str.lower()
    df['kode_barang'] = df['kode_barang'].astype(str)
    df['kode_barang'] = df['kode_barang'].str.replace(",", "", regex=False).str.strip().str.upper()

    # 3. Pastikan qty numerik dan bersihkan data tidak valid
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    df = df.dropna(subset=['qty'])

    # 4. Hapus duplikat berdasarkan id_detail_transaksi
    df['id_detail_transaksi_penjualan'] = df['id_detail_transaksi_penjualan'].astype(str)
    df = df.drop_duplicates(subset='id_detail_transaksi_penjualan')

    # 5. Ekstrak bulan dari no_transaksi
    df['no_transaksi_penjualan'] = df['no_transaksi_penjualan'].astype(str).str.replace(",", "")
    df['tanggal_str'] = df['no_transaksi_penjualan'].str.extract(r'(\d{6})')[0]
    df['bulan'] = pd.to_datetime(df['tanggal_str'], format='%y%m%d', errors='coerce')
    df = df.dropna(subset=['bulan'])
    df['bulan'] = df['bulan'].dt.to_period('M').astype(str)

    # 6. Hitung jumlah transaksi & total penjualan
    df_grouped = df.groupby(['kode_barang', 'nama_barang', 'bulan']).agg(
        jumlah_transaksi=('id_detail_transaksi_penjualan', 'count'),
        total_penjualan=('qty', 'sum')
    ).reset_index()

    # 7. Buat kombinasi lengkap berdasarkan range dinamis dari data
    bulan_tersedia = pd.to_datetime(df['bulan'], errors='coerce')
    bulan_tersedia = bulan_tersedia.dropna().dt.to_period('M')

    start_bulan = bulan_tersedia.min()
    end_bulan = bulan_tersedia.max()

    bulan_range = pd.period_range(start=start_bulan, end=end_bulan, freq='M').astype(str)

    barang_unik = df[['kode_barang', 'nama_barang']].drop_duplicates()

    kombinasi = pd.MultiIndex.from_product(
        [barang_unik['kode_barang'], bulan_range],
        names=['kode_barang', 'bulan']
    ).to_frame(index=False)

    kombinasi = kombinasi.merge(barang_unik, on='kode_barang', how='left')

    # 8. Gabungkan semua kombinasi
    hasil_final = pd.merge(
        kombinasi,
        df_grouped,
        on=['kode_barang', 'nama_barang', 'bulan'],
        how='left'
    )
    hasil_final['jumlah_transaksi'] = hasil_final['jumlah_transaksi'].fillna(0).astype(int)
    hasil_final['total_penjualan'] = hasil_final['total_penjualan'].fillna(0).astype(int)

    # 9. Format nama_barang ke kapitalisasi awal
    hasil_final['nama_barang'] = hasil_final['nama_barang'].str.title()

    # 10. Ubah index agar mulai dari 1
    hasil_final = hasil_final.reset_index(drop=True)
    hasil_final.index = hasil_final.index + 1
    
    return hasil_final

def elbow_method_simulasi(df):
    # Pivot data agar format cocok untuk clustering
    pivot = df.pivot_table(
        index=['kode_barang', 'nama_barang'],
        columns='bulan',
        values='total_penjualan',
        fill_value=0
    )

    # Scaling dilakukan sekali sebelum loop
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(pivot)

    # Hitung inertia untuk berbagai jumlah cluster
    distortions = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(scaled_data)
        distortions.append(kmeans.inertia_)

    return pivot, distortions

def show_elbow_chart_simulasi(distortions):
    fig = px.line(
        x=list(range(1, len(distortions)+1)),
        y=distortions,
        labels={'x': 'Jumlah Cluster', 'y': 'Inertia'}
    )
    st.plotly_chart(fig)

def show_cluster_chart_simulasi(df):
    # Warna ditentukan secara manual agar konsisten
    color_map = {
        'Penjualan Rendah': 'red',
        'Penjualan Sedang': 'orange',
        'Penjualan Tinggi': 'green'
    }

    fig = px.scatter(
        df,
        x='nama_barang',
        y='total_penjualan',
        color='kategori',
        color_discrete_map=color_map,
        hover_data=['kode_barang', 'nama_barang'],
        opacity=0.6,
    )
    st.plotly_chart(fig)

def run_kmeans_simulasi(df, n_clusters=3):
    # Ambil hanya kolom numerik untuk clustering
    clustering_data = df[['jumlah_transaksi', 'total_penjualan']]

    # Scaling
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)

    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    df['cluster'] = kmeans.fit_predict(scaled_data)

    # Tambahkan kategori berdasarkan mean total_penjualan per cluster
    cluster_avg = df.groupby('cluster')['total_penjualan'].mean().sort_values()
    kategori_labels = ['Penjualan Rendah', 'Penjualan Sedang', 'Penjualan Tinggi']
    kategori_mapping = {cluster_id: kategori_labels[i] for i, cluster_id in enumerate(cluster_avg.index)}
    df['kategori'] = df['cluster'].map(kategori_mapping)

    return df

def show_summary_table_simulasi(df):
    df_terjual = df[df['total_penjualan'] > 0]

    summary = df_terjual.groupby(['bulan', 'kategori', 'nama_barang']).agg(
        jumlah_per_produk=('total_penjualan', 'sum')
    ).reset_index()

    summary['produk_info'] = summary['nama_barang'] + ' (' + summary['jumlah_per_produk'].astype(int).astype(str) + ')'

    summary_agg = summary.groupby(['bulan', 'kategori']).agg(
        jumlah_merek=('nama_barang', 'nunique'),
        qty_penjualan=('jumlah_per_produk', 'sum'),
        produk_info=('produk_info', lambda x: ', '.join(sorted(x)))
    ).reset_index()

    # summary_agg['hari_libur'] = summary_agg['bulan'].map(hari_libur_bulanan).fillna('-')

    summary_agg = summary_agg.reset_index(drop=True)
    summary_agg.index = summary_agg.index + 1

    st.dataframe(summary_agg[['bulan', 'kategori', 'jumlah_merek', 'qty_penjualan', 'produk_info']],
                 use_container_width=True)
    return summary_agg

def show_line_charts_simulasi(df):

    df['bulan_format'] = pd.to_datetime(df['bulan']).dt.strftime('%m-%y')
    produk_list = df['nama_barang'].unique()

    for i in range(0, len(produk_list), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(produk_list):
                produk = produk_list[i + j]
                chart_data = df[df['nama_barang'] == produk].sort_values('bulan')
                fig = px.line(
                    chart_data,
                    x='bulan_format',
                    y='total_penjualan',
                    title=produk,
                    markers=True
                )
                with cols[j]:
                    st.plotly_chart(fig, use_container_width=True)