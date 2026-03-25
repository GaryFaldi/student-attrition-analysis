import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Student Dropout Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_models():
    model_dir = "models"
    models = {}
    model_files = {
        "Random Forest"      : "random_forest.pkl",
        "XGBoost"            : "xgboost.pkl",
        "Logistic Regression": "logistic_regression.pkl",
        "SVM"                : "svm.pkl",
    }
    for name, fname in model_files.items():
        path = os.path.join(model_dir, fname)
        if os.path.exists(path):
            models[name] = joblib.load(path)
    scaler        = joblib.load(os.path.join(model_dir, "scaler.pkl"))
    feature_names = joblib.load(os.path.join(model_dir, "feature_names.pkl"))
    return models, scaler, feature_names

try:
    models, scaler, feature_names = load_models()
    models_loaded = True
except Exception as e:
    models_loaded = False
    load_error    = str(e)

NEEDS_SCALING = {"Logistic Regression", "SVM"}

LABEL_MAP   = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}
LABEL_EMOJI = {0: "🚨", 1: "📚", 2: "🎓"}
LABEL_COLOR = {0: "#ef4444", 1: "#eab308", 2: "#22c55e"}

CSV_REQUIRED_COLS = [
    "Application_mode", "Application_order", "Course",
    "Previous_qualification_grade", "Mothers_qualification",
    "Fathers_qualification", "Mothers_occupation", "Fathers_occupation",
    "Admission_grade", "Debtor", "Tuition_fees_up_to_date", "Gender",
    "Scholarship_holder", "Age_at_enrollment",
    "Curricular_units_1st_sem_enrolled", "Curricular_units_1st_sem_evaluations",
    "Curricular_units_1st_sem_approved", "Curricular_units_1st_sem_grade",
    "Curricular_units_2nd_sem_enrolled", "Curricular_units_2nd_sem_evaluations",
    "Curricular_units_2nd_sem_approved", "Curricular_units_2nd_sem_grade",
]


with st.sidebar:
    st.title("🎓 Student Dropout Predictor")
    st.caption("Jaya Jaya Institut · 2024")
    st.divider()

    if models_loaded:
        selected_model = st.selectbox(
            "Model Prediksi",
            list(models.keys()),
        )
        st.divider()
        st.markdown("**Keterangan Status**")
        st.markdown("🎓 **Graduate** — Lulus normal")
        st.markdown("📚 **Enrolled** — Masih aktif")
        st.markdown("🚨 **Dropout** — Berisiko DO")
    else:
        st.error(f"Model tidak ditemukan: `{load_error}`")
        st.info("Pastikan folder `models/` berisi file `.pkl` hasil training.")


st.title("🎓 Student Dropout Predictor")
st.caption("Prediksi potensi dropout mahasiswa menggunakan Machine Learning")
st.divider()

if not models_loaded:
    st.error("Model belum dimuat. Jalankan notebook training terlebih dahulu.")
    st.stop()


def predict(model_name, input_df):
    model = models[model_name]
    X = input_df[feature_names]
    if model_name in NEEDS_SCALING:
        X_scaled = scaler.transform(X)
        proba = model.predict_proba(X_scaled)
    else:
        proba = model.predict_proba(X)
    preds = np.argmax(proba, axis=1)
    return preds, proba


def make_gauge(prob, label_idx):
    color = LABEL_COLOR[label_idx]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob * 100, 1),
        number={"suffix": "%", "font": {"size": 28}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 10}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#f1f5f9",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 33],   "color": "#fef2f2"},
                {"range": [33, 66],  "color": "#fefce8"},
                {"range": [66, 100], "color": "#f0fdf4"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.8,
                "value": prob * 100
            }
        }
    ))
    fig.update_layout(
        height=180,
        margin=dict(t=20, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


tab1, tab2 = st.tabs(["✏️ Prediksi Manual", "📂 Prediksi Batch (CSV)"])


with tab1:
    st.subheader("Input Data Mahasiswa")

    with st.form("manual_form"):
        st.markdown("#### 📚 Latar Belakang Akademik")
        c1, c2, c3 = st.columns(3)
        with c1:
            prev_qual = st.selectbox("Previous Qualification", [
                (1, "Secondary education"),
                (2, "Bachelor's degree"),
                (3, "Higher ed - degree"),
                (4, "Master's"),
                (5, "Doctorate"),
                (6, "Freq. of higher ed"),
                (9, "12th year - not completed"),
                (10, "11th year - not completed"),
                (19, "Basic education 3rd cycle"),
            ], format_func=lambda x: x[1])
            prev_qual_grade = st.number_input("Prev. Qual. Grade (0–200)", 0.0, 200.0, 130.0, 1.0)
        with c2:
            admission_grade = st.number_input("Admission Grade (0–200)", 0.0, 200.0, 127.0, 1.0)
            course = st.selectbox("Course", [
                (33,   "Biofuel Production Tech"),
                (171,  "Animation & Multimedia"),
                (9003, "Agronomy"),
                (9070, "Communication Design"),
                (9085, "Veterinary Nursing"),
                (9119, "Informatics Engineering"),
                (9147, "Management"),
                (9238, "Social Service"),
                (9254, "Tourism"),
                (9500, "Nursing"),
                (9853, "Basic Education"),
                (9991, "Management (evening)"),
            ], format_func=lambda x: x[1])
        with c3:
            application_mode = st.selectbox("Application Mode", [
                (1,  "1st phase - general"),
                (7,  "Holders other higher courses"),
                (10, "Ordinance 854-B/99"),
                (17, "2nd phase - general"),
                (18, "3rd phase - general"),
                (39, "Over 23 years old"),
                (42, "Transfer"),
                (43, "Change of course"),
            ], format_func=lambda x: x[1])
            application_order = st.slider("Application Order", 0, 9, 1)

        st.markdown("#### 📊 Performa Akademik Semester")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Semester 1**")
            cu1_enrolled    = st.number_input("Enrolled (Sem 1)",     0, 20, 6)
            cu1_approved    = st.number_input("Approved (Sem 1)",     0, 20, 5)
            cu1_grade       = st.number_input("Grade (Sem 1, 0–20)",  0.0, 20.0, 12.0, 0.5)
            cu1_evaluations = st.number_input("Evaluations (Sem 1)",  0, 30, 6)
            cu1_credited    = st.number_input("Credited (Sem 1)",     0, 20, 0)
            cu1_no_eval     = st.number_input("Without Eval (Sem 1)", 0, 20, 0)
        with c2:
            st.markdown("**Semester 2**")
            cu2_enrolled    = st.number_input("Enrolled (Sem 2)",     0, 20, 6)
            cu2_approved    = st.number_input("Approved (Sem 2)",     0, 20, 5)
            cu2_grade       = st.number_input("Grade (Sem 2, 0–20)",  0.0, 20.0, 12.0, 0.5)
            cu2_evaluations = st.number_input("Evaluations (Sem 2)",  0, 30, 6)
            cu2_credited    = st.number_input("Credited (Sem 2)",     0, 20, 0)
            cu2_no_eval     = st.number_input("Without Eval (Sem 2)", 0, 20, 0)

        st.markdown("#### 👤 Demografi & Sosial Ekonomi")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            age      = st.number_input("Age at Enrollment", 17, 70, 20)
            gender   = st.selectbox("Gender", [(1, "Male"), (0, "Female")], format_func=lambda x: x[1])
            marital  = st.selectbox("Marital Status", [
                (1,"Single"),(2,"Married"),(3,"Widower"),
                (4,"Divorced"),(5,"Facto union"),(6,"Legally separated")
            ], format_func=lambda x: x[1])
        with c2:
            scholarship = st.selectbox("Scholarship Holder", [(1,"Yes"),(0,"No")], format_func=lambda x: x[1])
            debtor      = st.selectbox("Debtor",              [(1,"Yes"),(0,"No")], format_func=lambda x: x[1])
            tuition_ok  = st.selectbox("Tuition Fees Up to Date", [(1,"Yes"),(0,"No")], format_func=lambda x: x[1])
        with c3:
            displaced     = st.selectbox("Displaced",                  [(1,"Yes"),(0,"No")], format_func=lambda x: x[1])
            international = st.selectbox("International",              [(1,"Yes"),(0,"No")], format_func=lambda x: x[1])
            sp_needs      = st.selectbox("Educational Special Needs",  [(1,"Yes"),(0,"No")], format_func=lambda x: x[1])
        with c4:
            daytime      = st.selectbox("Attendance", [(1,"Daytime"),(0,"Evening")], format_func=lambda x: x[1])
            mothers_qual = st.number_input("Mother's Qualification", 1, 44, 19)
            fathers_qual = st.number_input("Father's Qualification", 1, 44, 19)
            mothers_occ  = st.number_input("Mother's Occupation",    0, 194, 5)
            fathers_occ  = st.number_input("Father's Occupation",    0, 194, 5)

        submitted = st.form_submit_button("🔮 Prediksi Sekarang", use_container_width=True)

    if submitted:
        input_data = {
            "Marital_status"                              : marital[0],
            "Application_mode"                            : application_mode[0],
            "Application_order"                           : application_order,
            "Course"                                      : course[0],
            "Daytime_evening_attendance"                  : daytime[0],
            "Previous_qualification"                      : prev_qual[0],
            "Previous_qualification_grade"                : prev_qual_grade,
            "Nacionality"                                 : 1,
            "Mothers_qualification"                       : mothers_qual,
            "Fathers_qualification"                       : fathers_qual,
            "Mothers_occupation"                          : mothers_occ,
            "Fathers_occupation"                          : fathers_occ,
            "Admission_grade"                             : admission_grade,
            "Displaced"                                   : displaced[0],
            "Educational_special_needs"                   : sp_needs[0],
            "Debtor"                                      : debtor[0],
            "Tuition_fees_up_to_date"                     : tuition_ok[0],
            "Gender"                                      : gender[0],
            "Scholarship_holder"                          : scholarship[0],
            "Age_at_enrollment"                           : age,
            "International"                               : international[0],
            "Curricular_units_1st_sem_credited"           : cu1_credited,
            "Curricular_units_1st_sem_enrolled"           : cu1_enrolled,
            "Curricular_units_1st_sem_evaluations"        : cu1_evaluations,
            "Curricular_units_1st_sem_approved"           : cu1_approved,
            "Curricular_units_1st_sem_grade"              : cu1_grade,
            "Curricular_units_1st_sem_without_evaluations": cu1_no_eval,
            "Curricular_units_2nd_sem_credited"           : cu2_credited,
            "Curricular_units_2nd_sem_enrolled"           : cu2_enrolled,
            "Curricular_units_2nd_sem_evaluations"        : cu2_evaluations,
            "Curricular_units_2nd_sem_approved"           : cu2_approved,
            "Curricular_units_2nd_sem_grade"              : cu2_grade,
            "Curricular_units_2nd_sem_without_evaluations": cu2_no_eval,
        }

        input_df = pd.DataFrame([input_data])
        for col in [c for c in feature_names if c not in input_df.columns]:
            input_df[col] = 0

        pred, proba = predict(selected_model, input_df)
        pred_idx    = pred[0]
        pred_label  = LABEL_MAP[pred_idx]

        prob_dropout    = proba[0][0]
        prob_not_dropout = proba[0][1] + proba[0][2]
        is_dropout      = pred_idx == 0

        st.divider()
        st.subheader("🎯 Hasil Prediksi")

        col_main, col_gauge = st.columns([3, 2])

        with col_main:
            if is_dropout:
                st.error(
                    f"### 🚨 BERISIKO DROPOUT\n\n"
                    f"Model **{selected_model}** memprediksi mahasiswa ini **berpotensi tidak menyelesaikan studi**."
                )
            else:
                st.success(
                    f"### ✅ TIDAK BERISIKO DROPOUT\n\n"
                    f"Model **{selected_model}** memprediksi mahasiswa ini **berpotensi menyelesaikan studi**."
                )

            st.caption(
                "ℹ️ **Tentang prediksi ini:** Model dilatih dengan 3 kelas — *Dropout*, *Enrolled* (masih aktif), "
                "dan *Graduate* (lulus). Untuk fokus deteksi risiko, hasil di atas menyederhanakan menjadi: "
                "**Dropout** vs **Tidak Dropout** (gabungan Enrolled + Graduate). "
                "Detail probabilitas masing-masing kelas tersedia di bawah."
            )

        with col_gauge:
            fig_main = make_gauge(prob_dropout, 0)
            st.markdown("<center><b>Probabilitas Dropout</b></center>", unsafe_allow_html=True)
            st.plotly_chart(fig_main, use_container_width=True, key="gauge_main")


        with st.expander("📊 Lihat detail probabilitas per kelas (Dropout / Enrolled / Graduate)"):
            st.caption(
                "Model aslinya memprediksi 3 kemungkinan status mahasiswa:\n\n"
                "- 🚨 **Dropout** — Mahasiswa tidak menyelesaikan studi\n"
                "- 📚 **Enrolled** — Mahasiswa masih aktif kuliah (belum ada keputusan akhir)\n"
                "- 🎓 **Graduate** — Mahasiswa berhasil lulus\n\n"
                f"Prediksi detail model: **{pred_label}** (kelas dengan probabilitas tertinggi)"
            )
            g1, g2, g3 = st.columns(3)
            for col_g, (lbl, emoji) in zip([g1, g2, g3], [(0,"🚨"),(1,"📚"),(2,"🎓")]):
                with col_g:
                    st.markdown(f"<center>{emoji} <b>{LABEL_MAP[lbl]}</b></center>", unsafe_allow_html=True)
                    st.plotly_chart(
                        make_gauge(proba[0][lbl], lbl),
                        use_container_width=True, key=f"gauge_{lbl}"
                    )


with tab2:
    st.subheader("Prediksi Batch via CSV")

    with st.expander("📋 Lihat kolom yang wajib ada di CSV", expanded=True):
        st.markdown(
            "CSV yang diupload **harus memiliki kolom berikut** (sesuai data training). "
            "Kolom `Status` dan `Dropout` akan diabaikan jika ada."
        )
        col_df = pd.DataFrame({
            "No": range(1, len(CSV_REQUIRED_COLS) + 1),
            "Nama Kolom": CSV_REQUIRED_COLS,
        })
        st.dataframe(col_df, use_container_width=True, hide_index=True)
        st.code(
            ",".join(CSV_REQUIRED_COLS),
            language="text"
        )

    st.divider()

    template_df = pd.DataFrame(columns=CSV_REQUIRED_COLS)
    template_df.loc[0] = [0] * len(CSV_REQUIRED_COLS)
    csv_template = template_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Template CSV",
        csv_template,
        "template_input.csv",
        "text/csv"
    )

    uploaded = st.file_uploader("Upload file CSV", type=["csv"])

    if uploaded:
        try:
            df_upload = pd.read_csv(uploaded)
            st.success(f"**{len(df_upload)} baris** berhasil dibaca.")

            missing_required = [c for c in CSV_REQUIRED_COLS if c not in df_upload.columns]
            if missing_required:
                st.warning(f"⚠️ Kolom berikut tidak ditemukan di CSV dan akan diisi 0:\n`{missing_required}`")

            st.dataframe(df_upload.head(5), use_container_width=True)

            missing_feat = [c for c in feature_names if c not in df_upload.columns]
            for c in missing_feat:
                df_upload[c] = 0

            if st.button("🚀 Jalankan Prediksi Batch", use_container_width=True):
                with st.spinner("Memproses prediksi..."):
                    preds, probas = predict(selected_model, df_upload)

                df_result = df_upload.copy()
                df_result["Predicted_Status"]  = [LABEL_MAP[p] for p in preds]
                df_result["Risiko_Dropout"]     = ["🚨 Berisiko" if p == 0 else "✅ Tidak Berisiko" for p in preds]
                df_result["Prob_Dropout"]       = (probas[:, 0] * 100).round(2)
                df_result["Prob_Enrolled"]      = (probas[:, 1] * 100).round(2)
                df_result["Prob_Graduate"]      = (probas[:, 2] * 100).round(2)

                n_dropout     = int((np.array(preds) == 0).sum())
                n_not_dropout = len(preds) - n_dropout
                counts        = pd.Series([LABEL_MAP[p] for p in preds]).value_counts()

                st.success(f"✅ Prediksi selesai untuk **{len(df_result)} mahasiswa**.")

                st.markdown("**Ringkasan Risiko Dropout**")
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("🚨 Berisiko Dropout",    n_dropout)
                mc2.metric("✅ Tidak Berisiko",       n_not_dropout)
                mc3.metric("📊 Total Mahasiswa",      len(preds))

                st.caption(
                    "ℹ️ *Tidak Berisiko* = gabungan mahasiswa yang diprediksi **Enrolled** (masih aktif) "
                    "dan **Graduate** (lulus). Detail per kelas tersedia di pie chart dan tabel di bawah."
                )

                st.divider()

                col_pie, col_table = st.columns([1, 2])
                with col_pie:
                    fig_pie = px.pie(
                        values=counts.values,
                        names=counts.index,
                        color=counts.index,
                        color_discrete_map={
                            "Dropout" : "#ef4444",
                            "Enrolled": "#eab308",
                            "Graduate": "#22c55e"
                        },
                        hole=0.45,
                        title="Distribusi Prediksi (3 Kelas)"
                    )
                    fig_pie.update_layout(
                        height=300,
                        margin=dict(t=40, b=0, l=0, r=0),
                        legend=dict(orientation="h", y=-0.1)
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col_table:
                    display_cols = ["Risiko_Dropout", "Predicted_Status", "Prob_Dropout", "Prob_Enrolled", "Prob_Graduate"]
                    st.dataframe(
                        df_result[display_cols].style
                            .background_gradient(subset=["Prob_Dropout"],  cmap="Reds")
                            .background_gradient(subset=["Prob_Graduate"], cmap="Greens")
                            .format({
                                "Prob_Dropout" : "{:.1f}%",
                                "Prob_Enrolled": "{:.1f}%",
                                "Prob_Graduate": "{:.1f}%",
                            }),
                        use_container_width=True,
                        height=280
                    )

                output_csv = df_result.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download Hasil Prediksi CSV",
                    output_csv,
                    "hasil_prediksi.csv",
                    "text/csv",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Error memproses file: {e}")