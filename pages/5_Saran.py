import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from collections import defaultdict
from utils.visual import get_hari_libur_bulanan

# Layout penuh
st.set_page_config(layout="wide")

st.title("📋 Rekomendasi Persediaan & Penataan Barang")

st.markdown("""
<div class="highlight-box">
    <p class="note">
    Halaman ini memberikan <strong>rekomendasi persediaan stok dan penataan barang</strong> berdasarkan analisis pola penjualan saat hari libur.
    Rekomendasi dihasilkan secara otomatis dari produk-produk yang terbukti mengalami kenaikan signifikan saat hari libur tertentu.
    </p>
</div>
""", unsafe_allow_html=True)

# Style tambahan
st.markdown("""
    <style>
    .recommendation-box {
        background-color: #f0f8ff;
        padding: 16px;
        border-left: 6px solid #4682b4;
        border-radius: 6px;
        margin: 12px 0;
    }
    .recommendation-header {
        color: #2e5984;
        font-weight: bold;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk generate rekomendasi
def generate_recommendations(signifikan_products):
    current_year = datetime.now().year
    recommendations = []
    
    for libur, products in signifikan_products.items():
        # Rekomendasi persediaan
        rec_stock = f"""
        <div class='recommendation-box'>
            <div class='recommendation-header'>📦 Rekomendasi Persediaan untuk {libur}:</div>
            <ul style='margin-bottom:0;'>
        """
        
        gabung_produk = defaultdict(lambda: {'total': 0.0, 'count': 0})

        for p in products:
            nama = p['produk']
            try:
                kenaikan = float(str(p['kenaikan_penjualan']).strip())
                avg_global = float(str(p['avg_global']).strip())
                total = kenaikan + avg_global

                gabung_produk[nama]['total'] += total
                gabung_produk[nama]['count'] += 1
            except:
                pass  # biarkan nilai default 0.0

        # Buat list rekomendasi setelah digabung
        for nama, data in gabung_produk.items():
            if data['count'] > 0:
                estimated_avg = data['total'] / data['count']
                rec_stock += f"<li>Tambahkan stok <strong>{nama}</strong> sebanyak {estimated_avg:.0f} pcs</li>"
        
        rec_stock += "</ul></div>"
        
        recommendations.append({
            'libur': libur,
            'rec_stock': rec_stock,
        })
    
    return recommendations

# Ambil data dari session state jika ada
if 'signifikan_products' in st.session_state and st.session_state.signifikan_products:
    signifikan_products = st.session_state.signifikan_products
    
    # Generate rekomendasi
    all_recommendations = generate_recommendations(signifikan_products)
    
    # Tampilkan per hari libur
    st.markdown(f"## 🎯 Rekomendasi untuk Persediaan Stok Barang", unsafe_allow_html=True)

    for rec in all_recommendations:
        st.markdown(rec['rec_stock'], unsafe_allow_html=True)
        
    st.write("---")

    st.markdown("""
    <style>
    /* Style untuk rekomendasi keseluruhan */
    .penataan-box {
        background-color: #fff8e1;  /* kuning muda */
        padding: 16px;
        border-left: 6px solid #ff8f00;  /* kuning tua */
        border-radius: 8px;
        margin: 12px 0;
    }
    
    /* Style untuk rekomendasi tambahan */
    .tambahan-box {
        background-color: #fff8e1;  /* kuning muda */
        padding: 16px;
        border-left: 6px solid #ff8f00;  /* kuning tua */
        border-radius: 8px;
        margin: 12px 0;
    }
                
    /* Style untuk download */
    .download-box {
        background-color: #ffebee;  /* Merah muda */
        padding: 16px;
        border-left: 6px solid #c62828;  /* Merah tua */
        border-radius: 8px;
        margin: 12px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Rekomendasi penataan
    st.markdown("""
    ## 📝 Rekomendasi Penataan
    <div class='penataan-box'>
        <div class='recommendation-header'>🛍️ Rekomendasi Penataan Barang
            <ul>
                <li> Letakkan minuman kopi kemasan siap minum di area yang berdekatan dengan makanan ringan seperti roti, biskuit, atau snack</li>
                <li> Tambahkan label “Favorit Saat Istirahat” atau “Minuman Paling Dicari!” di sekitar produk.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # Rekomendasi umum
    st.markdown("""
    ## 📝 Rekomendasi Tambahan
    <div class='tambahan-box'>
        <ul>
            <li>🔄 Lakukan <strong>evaluasi stok</strong> seminggu setelah hari libur untuk menyesuaikan level persediaan</li>
            <li>📊 Lakukan perhitungan clustering menggunakan aplikasi ini untuk menganalisis pola penjualan</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")

    # Download
    st.markdown("""
    ## 📥 Download Hasil
    <div class='download-box'>
        <ul>
            <li> Pastikan untuk men-download hasil dari clustering yang telah dilakukan karena hasil tidak tersimpan pada database</li>
            <li> Hasil download berupa pdf akan digunakan untuk evaluasi pada waktu berikutnya</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("""
    ⚠️ Tidak ada data rekomendasi yang tersedia. 
    Silakan buka halaman **Hasil** terlebih dahulu untuk melihat produk dengan kenaikan signifikan saat hari libur.
    """)

# Fungsi buat PDF yang lebih rapi
def create_pdf(signifikan_products):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin_x = 40
    y = height - 40
    line_spacing = 14
    max_width = width - 2 * margin_x

    def draw_wrapped_text(text, font_name, font_size, x, y, indent=0):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        c.setFont(font_name, font_size)
        words = text.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}" if line else word
            if stringWidth(test_line, font_name, font_size) <= max_width - (x - margin_x):
                line = test_line
            else:
                c.drawString(x, y, line)
                y -= line_spacing
                line = word
                x += indent 
        if line:
            c.drawString(x, y, line)
            y -= line_spacing
        return y

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, "A. Kesimpulan: Produk dengan Kenaikan Signifikan per Hari Libur")
    y -= 25

    c.setFont("Helvetica", 11)
    for libur, products in signifikan_products.items():
        c.setFont("Helvetica-Bold", 11)
        y = draw_wrapped_text(f"- {libur}", "Helvetica-Bold", 11, margin_x + 18, y)
        c.setFont("Helvetica", 10)
        for p in products:
            nama = p.get('produk', '-')
            bulan = p.get('bulan', '-')
            penjualan = p.get('penjualan', '-')
            kenaikan_penjualan = p.get('kenaikan_penjualan', 0)

            teks = f"- {nama} ({bulan}): produk terjual= {penjualan} pcs (↑{kenaikan_penjualan:.2f} pcs)"
            y = draw_wrapped_text(teks, "Helvetica", 10, margin_x + 30, y)
            if y < 60:
                c.showPage()
                y = height - 40

        y -= 8

    y -= 12
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, "B. Rekomendasi Persediaan & Penataan Barang")
    y -= 25

    c.setFont("Helvetica-Bold", 11)
    y = draw_wrapped_text("1. Rekomendasi Penambahan Stok per Produk:", "Helvetica-Bold", 11, margin_x + 18, y)
    c.setFont("Helvetica", 10)

    for libur, products in signifikan_products.items():
        y = draw_wrapped_text(f"- {libur}", "Helvetica", 10, margin_x + 30, y)
        
        gabung_produk = defaultdict(lambda: {'total': 0.0, 'count': 0})
        for p in products:
            nama = p.get('produk', '-')
            try:
                kenaikan = float(p.get('kenaikan_penjualan', 0))
                avg = float(p.get('avg_global', 0))
                total = kenaikan + avg

                gabung_produk[nama]['total'] += total
                gabung_produk[nama]['count'] += 1
            except:
                continue

        # Kemudian render
        for nama, data in gabung_produk.items():
            if data['count'] > 0:
                rata = data['total'] / data['count']
                teks = f"• Tambahkan stok {nama} sebanyak {rata:.0f} pcs"
            y = draw_wrapped_text(teks, "Helvetica", 10, margin_x + 40, y, indent=10)
            if y < 60:  
                c.showPage()
                y = height - 40

        y -= 8

    y -= 12
    c.setFont("Helvetica-Bold", 11)
    y = draw_wrapped_text("2. Rekomendasi Penataan Barang:", "Helvetica-Bold", 11, margin_x + 18, y)
    penataan = [
        "Letakkan minuman kopi kemasan siap minum di area berdekatan dengan makanan ringan seperti roti, biskuit, atau snack",
        "Tambahkan label 'Favorit Saat Istirahat' atau 'Minuman Paling Dicari!' di sekitar produk."
    ]
    for p in penataan:
        y = draw_wrapped_text(f"- {p}", "Helvetica", 10, margin_x + 30, y)

    y -= 12
    c.setFont("Helvetica-Bold", 11)
    y = draw_wrapped_text("3. Rekomendasi Tambahan:", "Helvetica-Bold", 11, margin_x + 18, y)
    tambahan = [
        "Lakukan evaluasi stok seminggu setelah hari libur untuk menyesuaikan level persediaan",
        "Lakukan perhitungan clustering menggunakan aplikasi ini untuk menganalisis pola penjualan"
    ]
    for t in tambahan:
        y = draw_wrapped_text(f"- {t}", "Helvetica", 10, margin_x + 30, y)
        if y < 60:
            c.showPage()
            y = height - 40

    c.save()
    buffer.seek(0)
    return buffer

if 'signifikan_products' in st.session_state and st.session_state.signifikan_products:
    signifikan_products = st.session_state.signifikan_products

    pdf_file = create_pdf(signifikan_products)
    st.download_button(
        label="📥 Download PDF Rekomendasi & Kesimpulan",
        data=pdf_file,
        file_name="rekomendasi_penjualan_hari_libur.pdf",
        mime="application/pdf"
    )
