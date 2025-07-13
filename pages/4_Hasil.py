import streamlit as st
import pandas as pd

from utils.visual import (
    show_summary_table,
    show_line_charts,
    get_hari_libur_bulanan,
    hitung_statistik_kenaikan
)

# Layout penuh
st.set_page_config(layout="wide")

# Tambahan styling
st.markdown("""
    <style>
    .highlight-box {
        background-color: #fffaf0;
        padding: 16px;
        border-left: 6px solid #ffa500;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .note {
        font-size: 16px;
        color: #444;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Hasil Visualisasi Penjualan & Analisis")

st.markdown("""
<div class="highlight-box">
    <p class="note">
    Halaman ini menampilkan <strong>analisis penjualan bulanan</strong> berdasarkan hasil clustering, 
    serta mengevaluasi <strong>pengaruh hari libur nasional</strong> terhadap produk.
    </p>
</div>
""", unsafe_allow_html=True)

# Pastikan data sudah di-cluster
if 'clustered_df' in st.session_state:
    df = st.session_state.clustered_df

    if 'bulan' not in df.columns:
        df['bulan'] = pd.to_datetime(df['tanggal']).dt.to_period('M').astype(str)

    hari_libur = get_hari_libur_bulanan(df)

    # Daftar hari libur
    with st.expander("📅 Daftar Hari Libur Nasional"):
        if hari_libur:
            for bulan, libur in hari_libur.items():
                st.write(f"📌 {bulan}: {libur}")
        else:
            st.write("❌ Tidak ada hari libur yang terdeteksi.")

    st.info("ℹ️ Data hari libur hanya mencakup tahun 2022 hingga 2027.")
    st.write("---")

    # Tabel ringkasan penjualan
    st.subheader("📋 Ringkasan Penjualan Bulanan")
    summary_df = show_summary_table(df, hari_libur)
    st.write("---")

    st.subheader("📈 Grafik Penjualan Tiap Produk")
    with st.expander("📈 Grafik Penjualan Tiap Produk"):
        show_line_charts(df)
    st.write("---")

    # Insight produk dengan penjualan tinggi saat hari libur
    st.subheader("⭐ Analisis Produk Penjualan Tinggi Terkait Hari Libur")
    # st.markdown("""
    #     #### 📘 Penjelasan Kolom Interpretasi
    #     Analisis ini bertujuan untuk melihat apakah terdapat **lonjakan penjualan** yang signifikan pada momen hari libur nasional. Untuk itu, digunakan perhitungan berbasis statistik dari rata-rata penjualan tiap produk.
    #     - **`avg_global`**: Rata-rata total penjualan per bulan dari suatu produk sepanjang data yang tersedia.
    #     - **`ambang_batas`**: Batas atas normal penjualan. Jika penjualan di bulan tertentu melebihi nilai ini, maka penjualan dianggap mengalami **peningkatan signifikan**.
    #     - **`kenaikan_penjualan`**: Kenaikan penjualan produk pada bulan tersebut.
    #     > Dengan pendekatan ini, Anda dapat melihat **produk mana yang benar-benar mengalami lonjakan penjualan** saat hari libur nasional tertentu, dan bukan hanya naik secara alami atau karena fluktuasi kecil.
    #     """, unsafe_allow_html=True)
    st.markdown("#### 📘 Penjelasan Kolom Interpretasi")
    st.markdown(
        "Analisis ini bertujuan untuk melihat apakah terdapat **lonjakan penjualan** "
        "yang signifikan pada momen hari libur nasional. Untuk itu, digunakan perhitungan "
        "berbasis statistik dari rata-rata penjualan tiap produk."
    )

    st.markdown("- `avg_global`: Rata-rata total penjualan per bulan dari suatu produk sepanjang data yang tersedia.")
    st.markdown("- `ambang_batas`: Batas atas normal penjualan. Jika melebihi nilai ini, dianggap **peningkatan signifikan**.")
    st.markdown("- `kenaikan_penjualan`: Kenaikan penjualan produk pada bulan tersebut.")

    st.info(
        "📌 Dengan pendekatan ini, Anda dapat melihat **produk mana yang benar-benar mengalami lonjakan penjualan** "
        "saat hari libur nasional tertentu, dan bukan hanya naik secara alami atau karena fluktuasi kecil."
    )

    df_high_sales = df[df['kategori'] == 'Penjualan Tinggi'].copy()
    df_high_sales['hari_libur'] = df_high_sales['bulan'].map(hari_libur).fillna('Tidak ada hari libur')
    df_high_sales_with_holidays = df_high_sales[df_high_sales['hari_libur'] != 'Tidak ada hari libur']

    if not df_high_sales_with_holidays.empty:
        grouped = df_high_sales_with_holidays.groupby('hari_libur')

        for nama_libur, grup in grouped:
            summary = hitung_statistik_kenaikan(df, grup)

            st.markdown(f"### 📌 {nama_libur}")

            # # Hitung persentase kenaikan
            # def calculate_percentage(row):
            #     try:
            #         if row['avg_global'] == 0:
            #             return 0
            #         return ((row['total_penjualan'] - row['avg_global']) / row['avg_global']) * 100
            #     except:
            #         return 0

            # summary['persentase_kenaikan_num'] = summary.apply(calculate_percentage, axis=1).round(1)

            # def format_percent(x):
            #     try:
            #         return f"{float(x):.1f}%"
            #     except:
            #         return "0.0%"

            # summary['persentase_kenaikan'] = summary['persentase_kenaikan_num'].apply(format_percent)

            # Tentukan apakah kenaikan signifikan
            summary['kenaikan_signifikan'] = summary['total_penjualan'] > summary['ambang_batas']
            summary['kenaikan_signifikan'] = summary['kenaikan_signifikan'].apply(lambda x: "✅" if x else "❌")

            # Tampilkan tabel hasil analisis
            st.dataframe(
                summary[['bulan', 'nama_barang', 'jumlah_transaksi', 'total_penjualan', 'avg_global', 'kenaikan_penjualan',
                        'ambang_batas', 'kenaikan_signifikan']],
                use_container_width=True
            )
    else:
        st.info("📭 Tidak ditemukan produk penjualan tinggi yang berkaitan dengan hari libur.")
    st.write("---")

    # Kesimpulan produk dengan kenaikan signifikan (dikelompokkan per hari libur)
    st.subheader("📌 Kesimpulan: Produk dengan Kenaikan Signifikan per Hari Libur")
    
    # Dictionary untuk menyimpan produk signifikan per hari libur
    libur_products = {}

    if not df_high_sales_with_holidays.empty:
        grouped = df_high_sales_with_holidays.groupby('hari_libur')

        for nama_libur, grup in grouped:
            summary = hitung_statistik_kenaikan(df, grup)
            produk_signifikan = summary[summary['kenaikan_signifikan'] == "✅"]

            if not produk_signifikan.empty:
                libur_products[nama_libur] = []
                for _, row in produk_signifikan.iterrows():
                    libur_products[nama_libur].append({
                        'bulan': row['bulan'],
                        'produk': row['nama_barang'],
                        'penjualan': row['total_penjualan'],
                        'kenaikan_penjualan': row['kenaikan_penjualan'],
                        'avg_global': row['avg_global']
                    })
    
    if libur_products:
        st.success("✅ Produk berikut mengalami kenaikan signifikan saat hari libur:")
        
        for libur, products in libur_products.items():
            # Urutkan berdasarkan persentase tertinggi
            products_sorted = sorted(products, key=lambda x: x['kenaikan_penjualan'], reverse=True)
            
            st.markdown(f"#### 📅 {libur}")
            for product in products_sorted:
                st.markdown(
                    f"- **{product['produk']}** ({product['bulan']}): "
                    f"produk terjual= {product['penjualan']:.0f} pcs (↑{product['kenaikan_penjualan']:.2f} pcs)"
                )
            st.write("")
    else:
        st.info("📭 Tidak ada produk yang mengalami kenaikan signifikan saat hari libur.")

    if libur_products:
        # Simpan ke session state untuk digunakan di halaman Saran
        st.session_state.signifikan_products = libur_products
        st.success("✅ Data kesimpulan telah disimpan untuk halaman Saran")

else:
    st.warning("⚠️ Silakan lakukan preprocessing dan clustering data terlebih dahulu.")
