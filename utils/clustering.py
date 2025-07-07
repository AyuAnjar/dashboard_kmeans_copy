# import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import streamlit as st

def elbow_method(df):
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

def show_elbow_chart(distortions):
    fig = px.line(
        x=list(range(1, len(distortions)+1)),
        y=distortions,
        labels={'x': 'Jumlah Cluster', 'y': 'Inertia'}
    )
    st.plotly_chart(fig)

def show_cluster_chart(df):
    # Warna ditentukan secara manual agar konsisten
    color_map = {
        'Penjualan Rendah': 'red',
        'Penjualan Sedang': 'orange',
        'Penjualan Tinggi': 'green'
    }

    fig = px.scatter(
        df,
        x='jumlah_transaksi',
        y='total_penjualan',
        color='kategori',
        color_discrete_map=color_map,
        hover_data=['kode_barang', 'nama_barang'],
        opacity=0.6,
    )
    st.plotly_chart(fig)

def run_kmeans(df, n_clusters=3):
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