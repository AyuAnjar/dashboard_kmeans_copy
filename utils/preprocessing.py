import pandas as pd

def preprocess_data(df):
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
