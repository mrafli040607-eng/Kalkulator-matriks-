import streamlit as st
import sympy as sp


# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Kalkulator Matriks",
    page_icon="🧮",
    layout="wide"
)


# ============================================================
# JUDUL APLIKASI
# ============================================================

st.title("🧮 Kalkulator Matriks")
st.write(
    "Kalkulator matriks dengan hasil dan langkah-langkah "
    "penyelesaian."
)

st.divider()


# ============================================================
# FUNGSI MEMBUAT INPUT MATRIKS
# ============================================================

def input_matrix(nama, baris, kolom, prefix):
    """
    Membuat input matriks menggunakan Streamlit.
    """

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

            # Mengubah angka desimal menjadi bentuk rasional
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
        st.markdown(f"### {judul}")

    st.latex(
        sp.latex(A)
    )


# ============================================================
# PENJUMLAHAN MATRIKS
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
                A_{{{i+1},{j+1}}}
                +
                B_{{{i+1},{j+1}}}
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
# PENGURANGAN MATRIKS
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
                A_{{{i+1},{j+1}}}
                -
                B_{{{i+1},{j+1}}}
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
# PERKALIAN MATRIKS
# ============================================================

def langkah_perkalian(A, B):

    C = A * B

    langkah = []

    for i in range(A.rows):

        for j in range(B.cols):

            bagian = []

            for k in range(A.cols):

                bagian.append(
                    f"({sp.latex(A[i,k])})"
                    f"({sp.latex(B[k,j])})"
                )

            persamaan = " + ".join(bagian)

            langkah.append(
                rf"""
                C_{{{i+1},{j+1}}}
                =
                {persamaan}
                =
                \mathbf{{{sp.latex(C[i,j])}}}
                """
            )

    return C, langkah


# ============================================================
# DETERMINAN
# ============================================================

def langkah_determinan(A):

    det = sp.simplify(A.det())

    langkah = []

    # Matriks 1 x 1
    if A.rows == 1:

        langkah.append(
            rf"""
            \det(A)
            =
            {sp.latex(A[0,0])}
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    # Matriks 2 x 2
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

    # Matriks 3 x 3
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

    # Matriks lebih besar
    else:

        langkah.append(
            r"""
            Untuk matriks berukuran lebih dari 3 × 3,
            determinan dihitung menggunakan operasi aljabar
            matriks.
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
# INVERS MATRIKS
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

    # Invers 2 x 2
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

        langkah.append(
            r"""
            Untuk matriks berukuran 3 × 3 atau lebih,
            invers dihitung menggunakan metode Gauss-Jordan
            terhadap matriks augmented [A | I].
            """
        )

        augmented = A.row_join(
            sp.eye(A.rows)
        )

        rref, _ = augmented.rref()

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
# OPERASI BARIS UNTUK RANK DAN SPL
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

        # Tukar baris
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

        # Membuat pivot = 1
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

        # Membuat elemen lain di kolom pivot menjadi nol
        for r in range(M.rows):

            if r == baris:
                continue

            faktor = M[r, kolom]

            if faktor != 0:

                M.row_op(
                    r,
                    lambda nilai, j:
                    sp.simplify(
                        nilai
                        -
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
    Aplikasi ini menampilkan:
    
    • Hasil perhitungan
    • Rumus
    • Substitusi angka
    • Langkah penyelesaian
    """
)


# ============================================================
# OPERASI SATU MATRIKS
# ============================================================

if operasi in [
    "Transpose",
    "Determinan",
    "Invers",
    "Rank",
    "Trace"
]:

    st.header(f"📐 {operasi}")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="single_rows"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="single_cols"
        )

    st.write("### Masukkan Matriks A")

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "single_matrix"
    )

    st.divider()

    tampilkan_matriks(
        A,
        "Matriks A"
    )

    st.divider()

    tombol = st.button(
        "🔢 HITUNG",
        type="primary",
        use_container_width=True
    )

    if tombol:

        # ====================================================
        # TRANSPOSE
        # ====================================================

        if operasi == "Transpose":

            hasil = A.T

            st.success(
                "Transpose berhasil dihitung."
            )

            tampilkan_matriks(
                hasil,
                "Hasil Aᵀ"
            )

            st.subheader(
                "📖 Langkah-langkah"
            )

            st.write(
                "Transpose diperoleh dengan mengubah "
                "baris menjadi kolom."
            )

            st.latex(
                rf"A^T = {sp.latex(hasil)}"
            )

        # ====================================================
        # DETERMINAN
        # ====================================================

        elif operasi == "Determinan":

            if baris != kolom:

                st.error(
                    "Determinan hanya dapat dihitung "
                    "untuk matriks persegi."
                )

            else:

                hasil, langkah = langkah_determinan(A)

                st.success(
                    "Determinan berhasil dihitung."
                )

                st.subheader(
                    "✅ Hasil"
                )

                st.latex(
                    rf"\det(A) = \mathbf{{{sp.latex(hasil)}}}"
                )

                st.subheader(
                    "📖 Langkah-langkah"
                )

                for item in langkah:
                    st.latex(item)

        # ====================================================
        # INVERS
        # ====================================================

        elif operasi == "Invers":

            if baris != kolom:

                st.error(
                    "Invers hanya dapat dihitung "
                    "untuk matriks persegi."
                )

            else:

                determinan = sp.simplify(
                    A.det()
                )

                if determinan == 0:

                    st.error(
                        "Matriks tidak memiliki invers "
                        "karena determinannya = 0."
                    )

                    st.latex(
                        r"\det(A)=0"
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

                    st.subheader(
                        "📖 Langkah-langkah"
                    )

                    for item in langkah:
                        st.latex(item)

        # ====================================================
        # RANK
        # ====================================================

        elif operasi == "Rank":

            hasil = A.rank()

            rref, langkah = rref_dengan_langkah(A)

            st.success(
                "Rank berhasil dihitung."
            )

            st.subheader(
                "✅ Hasil"
            )

            st.latex(
                rf"\operatorname{{rank}}(A)"
                rf" = \mathbf{{{hasil}}}"
            )

            st.subheader(
                "📖 Langkah-langkah"
            )

            st.write(
                "Matriks diubah ke bentuk "
                "Reduced Row Echelon Form (RREF)."
            )

            for nomor, (deskripsi, matriks) in enumerate(
                langkah
            ):

                st.write(
                    f"**Langkah {nomor}: {deskripsi}**"
                )

                st.latex(
                    sp.latex(matriks)
                )

            st.write(
                "Rank adalah jumlah baris tidak nol "
                "pada bentuk eselon baris."
            )

        # ====================================================
        # TRACE
        # ====================================================

        elif operasi == "Trace":

            if baris != kolom:

                st.error(
                    "Trace hanya dapat dihitung "
                    "untuk matriks persegi."
                )

            else:

                hasil = sp.trace(A)

                st.success(
                    "Trace berhasil dihitung."
                )

                st.subheader(
                    "✅ Hasil"
                )

                st.latex(
                    rf"\operatorname{{tr}}(A)"
                    rf" = \mathbf{{{sp.latex(hasil)}}}"
                )

                st.subheader(
                    "📖 Langkah-langkah"
                )

                diagonal = []

                for i in range(A.rows):
                    diagonal.append(
                        sp.latex(A[i, i])
                    )

                persamaan = " + ".join(
                    diagonal
                )

                st.latex(
                    rf"\operatorname{{tr}}(A)"
                    rf" = {persamaan}"
                )

                st.latex(
                    rf"= \mathbf{{{sp.latex(hasil)}}}"
                )


# ============================================================
# OPERASI DUA MATRIKS
# ============================================================

elif operasi in [
    "Penjumlahan",
    "Pengurangan",
    "Perkalian"
]:

    st.header(
        f"📐 {operasi} Matriks"
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # UKURAN A
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "Ukuran Matriks A"
        )

        baris_a = st.number_input(
            "Baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="baris_a"
        )

        kolom_a = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="kolom_a"
        )

    # --------------------------------------------------------
    # UKURAN B
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "Ukuran Matriks B"
        )

        baris_b = st.number_input(
            "Baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="baris_b"
        )

        kolom_b = st.number_input(
            "Kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="kolom_b"
        )

    st.divider()

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # INPUT A
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "Matriks A"
        )

        A = input_matrix(
            "A",
            int(baris_a),
            int(kolom_a),
            "matrix_A"
        )

    # --------------------------------------------------------
    # INPUT B
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "Matriks B"
        )

        B = input_matrix(
            "B",
            int(baris_b),
            int(kolom_b),
            "matrix_B"
        )

    st.divider()

    tombol = st.button(
        "🔢 HITUNG",
        type="primary",
        use_container_width=True
    )

    if tombol:

        # ====================================================
        # PENJUMLAHAN
        # ================================================
