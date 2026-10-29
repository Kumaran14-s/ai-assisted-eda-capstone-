import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from eda_utils import data_quality_summary, clean_dataframe, numeric_summary, outlier_summary

st.set_page_config(page_title="Open Dataset EDA Lab", page_icon="📊", layout="wide")
st.title("📊 AI-Assisted Exploratory Data Analysis")
st.caption("CSE Capstone • Transparent data quality checks • Reproducible Python analysis")

with st.sidebar:
    st.header("Dataset")
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    st.markdown("**Offline demo:** bundled illustrative sample")
    st.caption("The bundled sample is synthetic and is not a subset of the official Palmer Penguins dataset.")
    st.divider()
    st.header("Cleaning options")
    drop_duplicates = st.checkbox("Remove duplicate rows", value=False)
    missing_action = st.selectbox("Missing numeric values", ["Keep unchanged", "Drop rows with missing values", "Fill numeric missing values with median"])
    trim_text = st.checkbox("Trim whitespace in text columns", value=True)
    st.caption("Cleaning changes are optional. Review the before/after comparison before downloading.")

if uploaded:
    try:
        original = pd.read_csv(uploaded)
        source_label = uploaded.name
    except Exception as exc:
        st.error(f"Could not read this CSV: {exc}")
        st.stop()
else:
    original = pd.read_csv(ROOT / "data" / "sample_penguins_demo.csv")
    source_label = "Bundled synthetic demo sample"

if original.empty:
    st.warning("The selected dataset has no rows.")
    st.stop()

cleaned, cleaning_log = clean_dataframe(
    original,
    drop_duplicates=drop_duplicates,
    missing_action=missing_action,
    trim_text=trim_text
)

st.info(f"Current source: **{source_label}** · {len(original):,} rows · {len(original.columns):,} columns. "
        "For research submissions, use a documented public dataset and record its source, licence and limitations.")

tabs = st.tabs(["Overview", "Data quality", "Visual exploration", "Clean & export", "Methods & ethics"])
with tabs[0]:
    a, b, c, d = st.columns(4)
    a.metric("Rows", f"{len(original):,}")
    b.metric("Columns", f"{len(original.columns):,}")
    c.metric("Missing cells", f"{int(original.isna().sum().sum()):,}")
    d.metric("Duplicate rows", f"{int(original.duplicated().sum()):,}")
    st.subheader("Data preview")
    st.dataframe(original.head(100), use_container_width=True)
    st.subheader("Summary statistics")
    st.dataframe(original.describe(include="all").transpose(), use_container_width=True)

with tabs[1]:
    st.subheader("Data-quality summary")
    quality = data_quality_summary(original)
    st.dataframe(quality, use_container_width=True)
    st.subheader("Column data types")
    dtypes = pd.DataFrame({"column": original.columns, "dtype": [str(t) for t in original.dtypes],
                           "unique_values": [original[c].nunique(dropna=True) for c in original.columns]})
    st.dataframe(dtypes, use_container_width=True)
    st.subheader("Potential numeric outliers")
    st.caption("IQR flags are diagnostics, not proof that a value is wrong. Domain knowledge is required.")
    outliers = outlier_summary(original)
    st.dataframe(outliers, use_container_width=True)

with tabs[2]:
    st.subheader("Interactive visualizations")
    numeric_cols = original.select_dtypes(include="number").columns.tolist()
    categorical_cols = original.select_dtypes(exclude="number").columns.tolist()
    if numeric_cols:
        chosen_num = st.selectbox("Numeric variable", numeric_cols, key="hist_col")
        fig = px.histogram(original, x=chosen_num, marginal="box", title=f"Distribution of {chosen_num}")
        st.plotly_chart(fig, use_container_width=True)
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("X-axis", numeric_cols, index=0, key="scatter_x")
            y_col = st.selectbox("Y-axis", numeric_cols, index=min(1, len(numeric_cols)-1), key="scatter_y")
            color_col = st.selectbox("Colour grouping (optional)", ["None"] + categorical_cols)
            fig = px.scatter(original, x=x_col, y=y_col,
                             color=None if color_col == "None" else color_col,
                             title=f"{y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)
            corr = original[numeric_cols].corr(numeric_only=True)
            st.plotly_chart(px.imshow(corr, text_auto=".2f", aspect="auto", title="Numeric correlation heatmap"),
                            use_container_width=True)
        if categorical_cols:
            cat_col = st.selectbox("Group by category", categorical_cols)
            fig = px.box(original, x=cat_col, y=chosen_num, points="all", title=f"{chosen_num} by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
            counts = original[cat_col].fillna("(Missing)").value_counts().rename_axis(cat_col).reset_index(name="count")
            st.plotly_chart(px.bar(counts, x=cat_col, y="count", title=f"Counts by {cat_col}"),
                            use_container_width=True)
    else:
        st.warning("No numeric columns found. Upload a dataset with at least one numeric column for the full chart set.")
        if categorical_cols:
            cat_col = st.selectbox("Categorical column", categorical_cols)
            counts = original[cat_col].fillna("(Missing)").value_counts().rename_axis(cat_col).reset_index(name="count")
            st.plotly_chart(px.bar(counts, x=cat_col, y="count"), use_container_width=True)
    st.caption("Charts are generated from the currently selected data. Association/correlation does not establish causation.")

with tabs[3]:
    st.subheader("Transparent cleaning")
    st.write("The selected options are applied to a working copy. The uploaded/original data is not overwritten.")
    st.dataframe(pd.DataFrame({"Step": list(cleaning_log.keys()), "Result": list(cleaning_log.values())}), use_container_width=True)
    before, after = st.columns(2)
    before.metric("Rows before", len(original))
    after.metric("Rows after", len(cleaned))
    before.metric("Missing cells before", int(original.isna().sum().sum()))
    after.metric("Missing cells after", int(cleaned.isna().sum().sum()))
    st.dataframe(cleaned.head(100), use_container_width=True)
    st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode("utf-8"),
                       file_name="cleaned_dataset.csv", mime="text/csv")
    st.download_button("Download data-quality summary CSV", quality.to_csv(index=False).encode("utf-8"),
                       file_name="data_quality_summary.csv", mime="text/csv")

with tabs[4]:
    st.subheader("Methods, source and ethics")
    st.markdown("""
- **Default data:** synthetic teaching sample bundled for offline operation; not suitable for scientific claims.
- **Suggested public research dataset:** Palmer Penguins, documented by the Palmer Station Long-Term Ecological Research (LTER) program and distributed through the `palmerpenguins` project. See `docs/DATASET_NOTE.md` for source and licence notes.
- **Data minimisation:** use open, non-personal data only; do not upload confidential or identifiable records.
- **Missing values:** never assume missing means zero. The app leaves data unchanged unless a cleaning option is selected.
- **Outliers:** IQR flags are prompts for review, not automatic deletion rules.
- **AI safety:** any AI-generated interpretation must be checked against calculations and the source. This demo does not make external AI calls.
- **Inference:** descriptive patterns and correlation do not prove causation.
""")
    st.subheader("Reproducibility")
    st.code("python -m pip install -r requirements.txt\nstreamlit run app.py\npython -m unittest discover -s tests -v", language="bash")
