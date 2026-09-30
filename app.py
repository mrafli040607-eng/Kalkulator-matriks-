import streamlit as st
import sympy as sp


# ============================================================
# KONFIGURASI
# ============================================================

st.set_page_config(
    page_title="Kalkulator Matriks",
    page_icon="🧮",
    layout="wide"
)


# ============================================================
# FUNGSI INPUT MATRIKS
# ============================================================

def input_matrix(nama, baris, kolom, prefix):
    data = []

    for i in range(baris):
        kolom_input = st.columns(kolom)
        baris_data = []

        for j in range(kolom):
            nilai = kolom_input[j].number_input(
                f"{nama}[{i+1},{j+1}]",
                value=0.0,
                step=1.0,
                format="%.4f",
                key=f"{prefix}_{i}_{j}"
            )

            nilai_sympy = sp.Rational(
                str(nilai)
            ).limit_denominator(100000)

            baris_data.append(nilai_sympy)

        data.append(baris_data)

    return sp.Matrix(data)


# ============================================================
# FUNGSI MENAMPILKAN MATRIKS
# ============================================================

def tampilkan_matriks(A, judul=None):
    if judul:
        st.subheader(judul)

    st.latex(sp.latex(A))


# ============================================================
# PENJUMLAHAN
# ============================================================

def langkah_penjumlahan(A, B):
    C = A + B
    langkah = []

    for i in range(A.rows):
        for j in range(A.cols):
            a = A[i, j]
            b = B[i, j]
            c = C[i, j]

            langkah.append(
                rf"""
                C_{{{i+1},{j+1}}}
                =
                ({sp.latex(a)})
                +
                ({sp.latex(b)})
                =
                \mathbf{{{sp.latex(c)}}}
                """
            )

    return C, langkah


# ============================================================
# PENGURANGAN
# ============================================================

def langkah_pengurangan(A, B):
    C = A - B
    langkah = []

    for i in range(A.rows):
        for j in range(A.cols):
            a = A[i, j]
            b = B[i, j]
            c = C[i, j]

            langkah.append(
                rf"""
                C_{{{i+1},{j+1}}}
                =
                ({sp.latex(a)})
                -
                ({sp.latex(b)})
                =
                \mathbf{{{sp.latex(c)}}}
                """
            )

    return C, langkah


# ============================================================
# PERKALIAN
# ============================================================

def langkah_perkalian(A, B):
    C = A * B
    langkah = []

    for i in range(A.rows):
        for j in range(B.cols):

            bagian = []

            for k in range(A.cols):
                bagian.append(
                    f"({sp.latex(A[i, k])})"
                    f"({sp.latex(B[k, j])})"
                )

            persamaan = " + ".join(bagian)

            langkah.append(
                rf"""
                C_{{{i+1},{j+1}}}
                =
                {persamaan}
                =
                \mathbf{{{sp.latex(C[i, j])}}}
                """
            )

    return C, langkah


# ============================================================
# DETERMINAN
# ============================================================

def langkah_determinan(A):

    det = sp.simplify(A.det())
    langkah = []

    if A.rows == 1:

        langkah.append(
            rf"""
            \det(A)
            =
            {sp.latex(A[0, 0])}
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    elif A.rows == 2:

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        langkah.append(
            rf"""
            \det(A)
            =
            ({sp.latex(a)})({sp.latex(d)})
            -
            ({sp.latex(b)})({sp.latex(c)})
            """
        )

        langkah.append(
            rf"""
            =
            {sp.latex(a*d)}
            -
            {sp.latex(b*c)}
            """
        )

        langkah.append(
            rf"""
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    elif A.rows == 3:

        a = A[0, 0]
        b = A[0, 1]
        c = A[0, 2]

        d = A[1, 0]
        e = A[1, 1]
        f = A[1, 2]

        g = A[2, 0]
        h = A[2, 1]
        i = A[2, 2]

        langkah.append(
            rf"""
            \det(A)
            =
            ({sp.latex(a)})
            [({sp.latex(e)})({sp.latex(i)})
            -
            ({sp.latex(f)})({sp.latex(h)})]
            -
            ({sp.latex(b)})
            [({sp.latex(d)})({sp.latex(i)})
            -
            ({sp.latex(f)})({sp.latex(g)})]
            +
            ({sp.latex(c)})
            [({sp.latex(d)})({sp.latex(h)})
            -
            ({sp.latex(e)})({sp.latex(g)})]
            """
        )

        langkah.append(
            rf"""
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    else:

        langkah.append(
            r"""
            Determinan untuk matriks berukuran lebih dari
            3 × 3 dihitung menggunakan metode aljabar matriks.
            """
        )

        langkah.append(
            rf"""
            \det(A)
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    return det, langkah


# ============================================================
# INVERS
# ============================================================

def langkah_invers(A):

    det = sp.simplify(A.det())

    if det == 0:
        return None, []

    invers = A.inv()
    langkah = []

    langkah.append(
        rf"""
        \det(A)
        =
        {sp.latex(det)}
        """
    )

    if A.rows == 2:

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        langkah.append(
            rf"""
            A^{{-1}}
            =
            \frac{{1}}{{\det(A)}}
            \begin{{bmatrix}}
            d & -b \\
            -c & a
            \end{{bmatrix}}
            """
        )

        langkah.append(
            rf"""
            A^{{-1}}
            =
            \frac{{1}}{{{sp.latex(det)}}}
            \begin{{bmatrix}}
            {sp.latex(d)} & -{sp.latex(b)} \\
            -{sp.latex(c)} & {sp.latex(a)}
            \end{{bmatrix}}
            """
        )

        langkah.append(
            rf"""
            A^{{-1}}
            =
            {sp.latex(invers)}
            """
        )

    else:

        augmented = A.row_join(
            sp.eye(A.rows)
        )

        rref, _ = augmented.rref()

        langkah.append(
            r"""
            Invers dihitung menggunakan metode
            Gauss-Jordan pada matriks augmented [A | I].
            """
        )

        langkah.append(
            rf"""
            [A|I]
            =
            {sp.latex(augmented)}
            """
        )

        langkah.append(
            rf"""
            RREF([A|I])
            =
            {sp.latex(rref)}
            """
        )

        langkah.append(
            rf"""
            A^{{-1}}
            =
            {sp.latex(invers)}
            """
        )

    return invers, langkah


# ============================================================
# RREF DENGAN LANGKAH
# ============================================================

def rref_dengan_langkah(A):

    M = A.copy()
    langkah = []

    langkah.append(
        (
            "Matriks awal",
            M.copy()
        )
    )

    baris = 0

    for kolom in range(M.cols):

        if baris >= M.rows:
            break

        pivot = None

        for r in range(baris, M.rows):

            if M[r, kolom] != 0:
                pivot = r
                break

        if pivot is None:
            continue

        if pivot != baris:

            M.row_swap(
                pivot,
                baris
            )

            langkah.append(
                (
                    f"R{baris+1} ↔ R{pivot+1}",
                    M.copy()
                )
            )

        nilai_pivot = M[baris, kolom]

        if nilai_pivot != 1:

            M.row_op(
                baris,
                lambda nilai, j:
                sp.simplify(
                    nilai / nilai_pivot
                )
            )

            langkah.append(
                (
                    f"R{baris+1} → "
                    f"R{baris+1}/({sp.latex(nilai_pivot)})",
                    M.copy()
                )
            )

        for r in range(M.rows):

            if r == baris:
                continue

            faktor = M[r, kolom]

            if faktor != 0:

                M.row_op(
                    r,
                    lambda nilai, j:
                    sp.simplify(
                        nilai -
                        faktor * M[baris, j]
                    )
                )

                langkah.append(
                    (
                        f"R{r+1} → "
                        f"R{r+1} - "
                        f"({sp.latex(faktor)})R{baris+1}",
                        M.copy()
                    )
                )

        baris += 1

    return M, langkah


# ============================================================
# SPL GAUSS-JORDAN
# ============================================================

def tampilkan_spl(A, b):

    n = A.rows

    for i in range(n):

        suku = []

        for j in range(n):

            koefisien = A[i, j]

            if koefisien == 0:
                continue

            if j == 0:

                suku.append(
                    f"{sp.latex(koefisien)}x_1"
                )

            else:

                if koefisien > 0:

                    suku.append(
                        f"+ {sp.latex(koefisien)}x_{j+1}"
                    )

                else:

                    suku.append(
                        f"- {sp.latex(abs(koefisien))}"
                        f"x_{j+1}"
                    )

        if suku:
            ruas_kiri = " ".join(suku)
        else:
            ruas_kiri = "0"

        st.latex(
            rf"{ruas_kiri} = {sp.latex(b[i])}"
        )


# ============================================================
# HEADER
# ============================================================

st.title("🧮 Kalkulator Matriks")

st.write(
    "Kalkulator matriks dengan hasil dan "
    "langkah-langkah penyelesaian."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Pilih Operasi")

operasi = st.sidebar.selectbox(
    "Operasi Matriks",
    [
        "Penjumlahan",
        "Pengurangan",
        "Perkalian",
        "Transpose",
        "Determinan",
        "Invers",
        "Rank",
        "Trace",
        "SPL - Gauss-Jordan"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    """
    Aplikasi menyediakan:

    • Hasil perhitungan
    • Rumus
    • Substitusi
    • Langkah penyelesaian
    """
)


# ============================================================
# TRANSPOSE
# ============================================================

if operasi == "Transpose":

    st.header("📐 Transpose Matriks")

    baris = st.number_input(
        "Jumlah baris",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="transpose_baris"
    )

    kolom = st.number_input(
        "Jumlah kolom",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="transpose_kolom"
    )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "transpose"
    )

    tampilkan_matriks(
        A,
        "Matriks A"
    )

    if st.button(
        "🔢 HITUNG TRANSPOSE",
        type="primary"
    ):

        hasil = A.T

        st.success(
            "Transpose berhasil dihitung."
        )

        tampilkan_matriks(
            hasil,
            "Hasil Aᵀ"
        )

        st.subheader("📖 Langkah")

        st.write(
            "Transpose dilakukan dengan mengubah "
            "baris menjadi kolom."
        )

        st.latex(
            rf"A^T = {sp.latex(hasil)}"
        )


# ============================================================
# DETERMINAN
# ============================================================

elif operasi == "Determinan":

    st.header("📐 Determinan Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="det_ukuran"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "determinan"
    )

    tampilkan_matriks(
        A,
        "Matriks A"
    )

    if st.button(
        "🔢 HITUNG DETERMINAN",
        type="primary"
    ):

        hasil, langkah = langkah_determinan(A)

        st.success(
            "Determinan berhasil dihitung."
        )

        st.latex(
            rf"\det(A) = \mathbf{{{sp.latex(hasil)}}}"
        )

        st.subheader("📖 Langkah-langkah")

        for item in langkah:
            st.latex(item)


# ============================================================
# INVERS
# ============================================================

elif operasi == "Invers":

    st.header("📐 Invers Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="invers_ukuran"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "invers"
    )

    tampilkan_matriks(
        A,
        "Matriks A"
    )

    if st.button(
        "🔢 HITUNG INVERS",
        type="primary"
    ):

        det = sp.simplify(A.det())

        if det == 0:

            st.error(
                "Matriks tidak memiliki invers "
                "karena determinannya = 0."
            )

        else:

            hasil, langkah = langkah_invers(A)

            st.success(
                "Invers berhasil dihitung."
            )

            tampilkan_matriks(
                hasil,
                "Hasil A⁻¹"
            )

            st.subheader("📖 Langkah-langkah")

            for item in langkah:
                st.latex(item)


# ============================================================
# RANK
# ============================================================

elif operasi == "Rank":

    st.header("📐 Rank Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="rank_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="rank_kolom"
        )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "rank"
    )

    tampilkan_matriks(
        A,
        "Matriks A"
    )

    if st.button(
        "🔢 HITUNG RANK",
        type="primary"
    ):

        hasil = A.rank()

        rref, langkah = rref_dengan_langkah(A)

        st.success(
            "Rank berhasil dihitung."
        )

        st.latex(
            rf"\operatorname{{rank}}(A)"
            rf" = \mathbf{{{hasil}}}"
        )

        st.subheader(
            "📖 Langkah-langkah RREF"
        )

        for nomor, (deskripsi, matriks) in enumerate(
            langkah,
            start=1
        ):

            st.write(
                f"**Langkah {nomor}: {deskripsi}**"
            )

            st.latex(
                sp.latex(matriks)
            )


# ============================================================
# TRACE
# ============================================================

elif operasi == "Trace":

    st.header("📐 Trace Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="trace_ukuran"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "trace"
    )

    tampilkan_matriks(
        A,
        "Matriks A"
    )

    if st.button(
        "🔢 HITUNG TRACE",
        type="primary"
    ):

        hasil = sp.trace(A)

        diagonal = []

        for i in range(A.rows):
            diagonal.append(
                sp.latex(A[i, i])
            )

        persamaan = " + ".join(diagonal)

        st.success(
            "Trace berhasil dihitung."
        )

        st.latex(
            rf"\operatorname{{tr}}(A)"
            rf" = {persamaan}"
        )

        st.latex(
            rf"= \mathbf{{{sp.latex(hasil)}}}"
        )


# ============================================================
# PENJUMLAHAN
# ============================================================

elif operasi == "Penjumlahan":

    st.header("📐 Penjumlahan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Ukuran A")

        baris_a = st.number_input(
            "Baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="tambah_baris_a"
        )

        kolom_a = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="tambah_kolom_a"
        )

    with col2:

        st.subheader("Ukuran B")

        baris_b = st.number_input(
            "Baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="tambah_baris_b"
        )

        kolom_b = st.number_input(
            "Kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="tambah_kolom_b"
        )

    col1, col2 = st.columns(2)

    with col1:

        A = input_matrix(
            "A",
            int(baris_a),
            int(kolom_a),
            "tambah_A"
        )

    with col2:

        B = input_matrix(
            "B",
            int(baris_b),
            int(kolom_b),
            "tambah_B"
        )

    if st.button(
        "🔢 HITUNG PENJUMLAHAN",
        type="primary"
    ):

        if A.shape != B.shape:

            st.error(
                "Ukuran A dan B harus sama."
            )

        else:

            hasil, langkah = langkah_penjumlahan(
                A,
                B
            )

            st.success(
                "Penjumlahan berhasil."
            )

            tampilkan_matriks(
                hasil,
                "Hasil A + B"
            )

            st.subheader("📖 Langkah-langkah")

            for item in langkah:
                st.latex(item)


# ============================================================
# PENGURANGAN
# ============================================================

elif operasi == "Pengurangan":

    st.header("📐 Pengurangan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Ukuran A")

        baris_a = st.number_input(
            "Baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="kurang_baris_a"
        )

        kolom_a = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="kurang_kolom_a"
        )

    with col2:

        st.subheader("Ukuran B")

        baris_b = st.number_input(
            "Baris B",
            min_value=1,
            max_value=8
