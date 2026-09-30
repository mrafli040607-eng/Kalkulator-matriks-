import streamlit as st
import sympy as sp

st.set_page_config(
    page_title="Kalkulator Matriks",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 Kalkulator Matriks")
st.write("Kalkulator matriks dengan langkah penyelesaian.")

st.sidebar.header("Pilih Operasi")

operasi = st.sidebar.selectbox(
    "Operasi",
    [
        "Penjumlahan",
        "Pengurangan",
        "Perkalian",
        "Transpose",
        "Determinan",
        "Invers",
        "Rank",
        "Trace"
    ]
)


def input_matrix(nama, baris, kolom, key_prefix):

    data = []

    for i in range(baris):

        cols = st.columns(kolom)

        row = []

        for j in range(kolom):

            nilai = cols[j].number_input(
                f"{nama}[{i+1},{j+1}]",
                value=0.0,
                step=1.0,
                key=f"{key_prefix}_{i}_{j}"
            )

            nilai = sp.Rational(
                str(nilai)
            ).limit_denominator(100000)

            row.append(nilai)

        data.append(row)

    return sp.Matrix(data)


# ============================================================
# TRANSPOSE
# ============================================================

if operasi == "Transpose":

    st.header("Transpose Matriks")

    baris = st.number_input(
        "Jumlah baris",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )

    kolom = st.number_input(
        "Jumlah kolom",
        min_value=1,
        max_value=8,
        value=2
    )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "transpose"
    )

    st.latex(
        sp.latex(A)
    )

    if st.button(
        "HITUNG",
        type="primary"
    ):

        hasil = A.T

        st.success("Transpose berhasil.")

        st.subheader("Hasil Aᵀ")

        st.latex(
            sp.latex(hasil)
        )


# ============================================================
# DETERMINAN
# ============================================================

elif operasi == "Determinan":

    st.header("Determinan Matriks")

    ukuran = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "determinan"
    )

    st.latex(
        sp.latex(A)
    )

    if st.button(
        "HITUNG",
        type="primary"
    ):

        hasil = A.det()

        st.success("Determinan berhasil.")

        st.latex(
            rf"\det(A) = {sp.latex(hasil)}"
        )


# ============================================================
# INVERS
# ============================================================

elif operasi == "Invers":

    st.header("Invers Matriks")

    ukuran = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "invers"
    )

    st.latex(
        sp.latex(A)
    )

    if st.button(
        "HITUNG",
        type="primary"
    ):

        det = A.det()

        if det == 0:

            st.error(
                "Matriks tidak memiliki invers karena determinan = 0."
            )

        else:

            hasil = A.inv()

            st.success("Invers berhasil.")

            st.latex(
                sp.latex(hasil)
            )


# ============================================================
# RANK
# ============================================================

elif operasi == "Rank":

    st.header("Rank Matriks")

    baris = st.number_input(
        "Jumlah baris",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )

    kolom = st.number_input(
        "Jumlah kolom",
        min_value=1,
        max_value=8,
        value=2
    )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "rank"
    )

    st.latex(
        sp.latex(A)
    )

    if st.button(
        "HITUNG",
        type="primary"
    ):

        hasil = A.rank()

        st.success("Rank berhasil.")

        st.latex(
            rf"\operatorname{{rank}}(A) = {hasil}"
        )


# ============================================================
# TRACE
# ============================================================

elif operasi == "Trace":

    st.header("Trace Matriks")

    ukuran = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "trace"
    )

    st.latex(
        sp.latex(A)
    )

    if st.button(
        "HITUNG",
        type="primary"
    ):

        hasil = A.trace()

        st.success("Trace berhasil.")

        st.latex(
            rf"\operatorname{{tr}}(A) = {sp.latex(hasil)}"
        )


# ============================================================
# PENJUMLAHAN
# ============================================================

elif operasi == "Penjumlahan":

    st.header("Penjumlahan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Matriks A")

        baris_a = st.number_input(
            "Baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

        kolom_a = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

    with col2:

        st.subheader("Matriks B")

        baris_b = st.number_input(
            "Baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

        kolom_b = st.number_input(
            "Kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1
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
        "HITUNG",
        type="primary"
    ):

        if A.shape != B.shape:

            st.error(
                "Ukuran A dan B harus sama."
            )

        else:

            hasil = A + B

            st.success(
                "Penjumlahan berhasil."
            )

            st.subheader("Hasil A + B")

            st.latex(
                sp.latex(hasil)
            )


# ============================================================
# PENGURANGAN
# ============================================================

elif operasi == "Pengurangan":

    st.header("Pengurangan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Matriks A")

        baris_a = st.number_input(
            "Baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

        kolom_a = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

    with col2:

        st.subheader("Matriks B")

        baris_b = st.number_input(
            "Baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

        kolom_b = st.number_input(
            "Kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

    col1, col2 = st.columns(2)

    with col1:

        A = input_matrix(
            "A",
            int(baris_a),
            int(kolom_a),
            "kurang_A"
        )

    with col2:

        B = input_matrix(
            "B",
            int(baris_b),
            int(kolom_b),
            "kurang_B"
        )

    if st.button(
        "HITUNG",
        type="primary"
    ):

        if A.shape != B.shape:

            st.error(
                "Ukuran A dan B harus sama."
            )

        else:

            hasil = A - B

            st.success(
                "Pengurangan berhasil."
            )

            st.subheader("Hasil A - B")

            st.latex(
                sp.latex(hasil)
            )


# ============================================================
# PERKALIAN
# ============================================================

elif operasi == "Perkalian":

    st.header("Perkalian Matriks")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Matriks A")

        baris_a = st.number_input(
            "Baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

        kolom_a = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

    with col2:

        st.subheader("Matriks B")

        baris_b = st.number_input(
            "Baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

        kolom_b = st.number_input(
            "Kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1
        )

    col1, col2 = st.columns(2)

    with col1:

        A = input_matrix(
            "A",
            int(baris_a),
            int(kolom_a),
            "kali_A"
        )

    with col2:

        B = input_matrix(
            "B",
            int(baris_b),
            int(kolom_b),
            "kali_B"
        )

    if st.button(
        "HITUNG",
        type="primary"
    ):

        if A.cols != B.rows:

            st.error(
                "Perkalian tidak dapat dilakukan."
            )

            st.write(
                "Jumlah kolom A harus sama "
                "dengan jumlah baris B."
            )

        else:

            hasil = A * B

            st.success(
                "Perkalian berhasil."
            )

            st.subheader("Hasil A × B")

            st.latex(
                sp.latex(hasil)
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Kalkulator Matriks | Python + Streamlit + SymPy"
                )
