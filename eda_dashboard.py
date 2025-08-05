import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- App Title ----
st.title("📊 Mini EDA Dashboard")
st.text("Upload a CSV file and explore your dataset!")

# ---- Sidebar Section ----
st.sidebar.header("📁 Upload your data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# ---- Main App Logic ----
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ---- Basic Metadata ----
    st.markdown("## 📌 Dataset Preview")
    with st.expander("📋 Show Raw Data"):
        st.dataframe(df)

    st.markdown("### 📈 Basic Info")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Shape of data:**", df.shape)
        st.write("**Column names:**", df.columns.tolist())

    with col2:
        st.write("**Data Types:**")
        st.write(df.dtypes)

    # ---- Filtering Options ----
    st.sidebar.markdown("### 🔍 Filter Data")
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    if categorical_cols:
        selected_col = st.sidebar.selectbox("Select categorical column to filter", categorical_cols)
        unique_values = df[selected_col].dropna().unique().tolist()
        selected_values = st.sidebar.multiselect("Choose values", unique_values, default=unique_values)

        filtered_df = df[df[selected_col].isin(selected_values)]
    else:
        filtered_df = df

    # ---- Visualizations ----
    st.markdown("## 📊 Visualizations")

    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if num_cols:
        selected_num = st.selectbox("Choose numerical column for Histogram", num_cols)
        fig1, ax1 = plt.subplots()
        sns.histplot(filtered_df[selected_num], kde=True, ax=ax1)
        st.pyplot(fig1)

        # Bar chart
        if categorical_cols:
            selected_cat = st.selectbox("Choose categorical column for Bar Chart", categorical_cols)
            st.bar_chart(filtered_df[selected_cat].value_counts())
    else:
        st.warning("No numerical columns found for plotting.")
else:
    st.info("👈 Upload a CSV file to begin.")
