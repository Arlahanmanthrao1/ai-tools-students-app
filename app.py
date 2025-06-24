import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Page config
st.set_page_config(page_title="AI Tools Usage Among Students", layout="wide")
st.title("🤖 AI Tools Usage Among Global High School Students")

# Load data
@st.cache_data
def load_data():
    base = "dataset"
    files = {
        "AI Adoption by Country": pd.read_csv(os.path.join(base, "ai_adoption_by_country.csv")),
        "Tool Usage Breakdown": pd.read_csv(os.path.join(base, "ai_tool_usage_breakdown.csv")),
        "Tool Usefulness Scores": pd.read_csv(os.path.join(base, "ai_tool_usefulness_scores.csv")),
        "Global Tool Usage": pd.read_csv(os.path.join(base, "global_ai_tools_students_use.csv")),
    }
    return files

data = load_data()

# Sidebar navigation
st.sidebar.title("📂 Choose Dataset to Explore")
selection = st.sidebar.radio("Select a dataset", list(data.keys()))

df = data[selection]
st.subheader(f"📄 Preview: {selection}")
st.dataframe(df.head(), use_container_width=True)

# Explore and visualize
st.markdown("### 🔍 Filter and Visualize")

if st.checkbox("Show basic info and stats"):
    st.write("Shape:", df.shape)
    st.write("Columns:", df.columns.tolist())
    st.write("Description:")
    st.write(df.describe(include="all"))

if st.checkbox("Visualize column values"):
    col = st.selectbox("Select a column to visualize", df.select_dtypes(include=["object", "category", "int64", "float64"]).columns)
    chart_type = st.radio("Chart type", ["Bar", "Pie"])
    value_counts = df[col].value_counts()

    if chart_type == "Bar":
        st.bar_chart(value_counts)
    else:
        fig, ax = plt.subplots()
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

# Grouped summaries
if st.checkbox("📊 Group & Summarize"):
    group_col = st.selectbox("Group by", df.columns)
    agg_col = st.selectbox("Aggregate", df.select_dtypes(include=["int64", "float64"]).columns)
    agg_type = st.radio("Aggregation", ["mean", "sum", "count"])

    if agg_type == "mean":
        result = df.groupby(group_col)[agg_col].mean().reset_index()
    elif agg_type == "sum":
        result = df.groupby(group_col)[agg_col].sum().reset_index()
    else:
        result = df.groupby(group_col)[agg_col].count().reset_index()

    st.dataframe(result)
    st.bar_chart(result.set_index(group_col))

st.markdown("---")
st.caption("Built with ❤️ by Hanmanth using Streamlit")

