import streamlit as st
import plotly.express as px
import pandas as pd

from collections import defaultdict

def get_hari_libur_bulanan(df):
    # Daftar hari libur nasional
    hari_libur = {
        '2022-04': 'Bulan Ramadhan',
        '2022-05': 'Bulan Ramadhan & Hari Buruh Internasional',
        '2022-07': 'Hari Raya Idul Adha',
        '2022-08': 'Hari Kemerdekaan RI',
        '2022-10': 'Maulid Nabi Muhammad SAW',
        '2022-12': 'Hari Raya Natal dan Malam Tahun Baru',

        '2023-04': 'Bulan Ramadhan',
        '2023-05': 'Hari Buruh Internasional',
        '2023-06': 'Hari Raya Idul Adha',
        '2023-08': 'Hari Kemerdekaan RI',
        '2023-09': 'Maulid Nabi Muhammad SAW',
        '2023-12': 'Hari Raya Natal dan Malam Tahun Baru',

        '2024-04': 'Bulan Ramadhan',
        '2024-05': 'Hari Buruh Internasional',
        '2024-06': 'Hari Raya Idul Adha',
        '2024-08': 'Hari Kemerdekaan RI',
        '2024-09': 'Maulid Nabi Muhammad SAW',
        '2024-12': 'Hari Raya Natal dan Malam Tahun Baru',

        '2025-03': 'Bulan Ramadhan',
        '2025-05': 'Hari Buruh Internasional',
        '2025-06': 'Hari Raya Idul Adha',
        '2025-08': 'Hari Kemerdekaan RI',
        '2025-09': 'Maulid Nabi Muhammad SAW',
        '2025-12': 'Hari Raya Natal dan Malam Tahun Baru',

        '2026-02': 'Bulan Ramadhan',
        '2026-03': 'Bulan Ramadhan & Hari Buruh Internasional',
        '2026-05': 'Hari Raya Idul Adha',
        '2026-08': 'Hari Kemerdekaan RI & Maulid Nabi Muhammad SAW',
        '2026-12': 'Hari Raya Natal dan Malam Tahun Baru',
        
        '2027-02': 'Bulan Ramadhan',
        '2027-03': 'Bulan Ramadhan',
        '2027-05': 'Hari Buruh Internasional & Hari Raya Idul Adha',
        '2027-08': 'Hari Kemerdekaan RI & Maulid Nabi Muhammad SAW',
        '2027-12': 'Hari Raya Natal dan Malam Tahun Baru',
    }

    bulan_libur = defaultdict(set)

    for tanggal_str, nama_libur in hari_libur.items():
        tahun, bulan= tanggal_str.split('-')
        key = f"{tahun}-{bulan}"
        bulan_libur[key].add(nama_libur)

    hari_libur_bulanan = {
        key: ', '.join(sorted(val)) if val else 'Tidak ada hari libur'
        for key, val in bulan_libur.items()
    }

    return hari_libur_bulanan

def show_summary_table(df, hari_libur_bulanan):
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

    summary_agg['hari_libur'] = summary_agg['bulan'].map(hari_libur_bulanan).fillna('-')

    summary_agg = summary_agg.reset_index(drop=True)
    summary_agg.index = summary_agg.index + 1

    st.dataframe(summary_agg[['bulan', 'kategori', 'jumlah_merek', 'qty_penjualan', 'produk_info', 'hari_libur']],
                 use_container_width=True)
    return summary_agg

def show_line_charts(df):
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

def hitung_statistik_kenaikan(df_all, df_sub, k=0.5):
    hasil = []
    produk_list = df_sub['nama_barang'].unique()
    df_all = df_all.copy()
    df_sub = df_sub.copy()

    df_all['total_penjualan'] = pd.to_numeric(df_all['total_penjualan'], errors='coerce')
    df_sub['total_penjualan'] = pd.to_numeric(df_sub['total_penjualan'], errors='coerce')
    df_all['jumlah_transaksi'] = pd.to_numeric(df_all['jumlah_transaksi'], errors='coerce')
    df_sub['jumlah_transaksi'] = pd.to_numeric(df_sub['jumlah_transaksi'], errors='coerce')

    for produk in produk_list:
        data_all_produk = df_all[df_all['nama_barang'] == produk].copy()
        data_sub_produk = df_sub[df_sub['nama_barang'] == produk].copy()

        if data_sub_produk.empty:
            continue

        mean = data_all_produk['total_penjualan'].mean()
        std = data_all_produk['total_penjualan'].std()
        threshold = mean + k * std

        data_sub_produk['avg_global'] = round(mean, 2)
        data_sub_produk['ambang_batas'] = round(threshold, 2)
        data_sub_produk['kenaikan_penjualan'] = (data_sub_produk['total_penjualan'] - mean).round(2)

        # data_sub_produk['persentase_kenaikan'] = (
        #     (data_sub_produk['total_penjualan'] - mean) / mean
        # ) * 100

        # Tangani pembagian 0
        # data_sub_produk['persentase_kenaikan'] = data_sub_produk['persentase_kenaikan'].replace([float('inf'), float('-inf')], 0).fillna(0)
        # data_sub_produk['persentase_kenaikan'] = data_sub_produk['persentase_kenaikan'].apply(lambda x: f"{x:.1f}%")

        data_sub_produk['kenaikan_signifikan'] = data_sub_produk['total_penjualan'] > threshold
        data_sub_produk['kenaikan_signifikan'] = data_sub_produk['kenaikan_signifikan'].apply(lambda x: "✅" if x else "❌")

        hasil.append(data_sub_produk)

    if hasil:
        return pd.concat(hasil).reset_index(drop=True)
    else:
        return pd.DataFrame(columns=['bulan', 'nama_barang', 'jumlah_transaksi', 'total_penjualan', 'avg_global', 'kenaikan_penjualan',
                                     'ambang_batas', 'kenaikan_signifikan'])

def get_brand(product_name):
    return " ".join(product_name.split()[:2])
