import pandas as pd
import streamlit as st
import plotly_express as px

st.set_page_config(page_title="Video Games Statistics",
                   page_icon=":video_game:",
                   layout="wide")

@st.cache_resource
def get_excel():
    df = pd.read_csv("Video_Games.csv")
    return df

df = get_excel()

# --- TITLE ---
st.title(":video_game: Video Games Dashboard")
st.text("Spreadsheet:")
st.markdown("##")

# --- FILTERS ---
st.sidebar.title("Filters")

genre = st.sidebar.multiselect(
    "Choose the game genre:",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()
)

platform = st.sidebar.multiselect(
    "Choose the game platform:",
    options=df["Platform"].unique(),
    default=df["Platform"].unique()
)

filtered_df = df.query(
    "Genre == @genre & Platform == @platform"
)

st.dataframe(filtered_df)

# --- SALES BY YEAR GRAPH ---
sales_by_year = filtered_df.groupby(["Year_of_Release"]).sum()[["Global_Sales"]]
sales_by_year = sales_by_year.drop(sales_by_year.tail(2).index, axis=0)
average_annual_sales = sales_by_year.values.mean()

st.subheader("Average Annual Sales:")
st.subheader(f"${round(average_annual_sales, 2)} billion")
st.markdown("---")

# columns
left_column, right_column = st.columns(2)

sales_by_year_plot = px.bar(
    sales_by_year,
    x=sales_by_year.index,
    y="Global_Sales",
    title="Annual Game Sales (billion $)",
    template="plotly_white"
)
with left_column:
    st.plotly_chart(sales_by_year_plot)

# --- DISTRIBUTION BY GAME GRAPH ---
genre_platform = pd.crosstab(filtered_df["Genre"], filtered_df["Platform"]).T
genre_platform = pd.DataFrame(genre_platform.sum(axis=0))
genre_platform["Total"] = genre_platform.values

distribution_plot = px.pie(
    genre_platform,
    values="Total",
    names=genre_platform.index,
    title="Game Genre Distribution",
    color_discrete_sequence=px.colors.sequential.RdBu
)
with right_column:
    st.plotly_chart(distribution_plot)

# --- SALES BY PLATFORM GRAPH ---
sales_by_platform = filtered_df.groupby(["Platform"]).sum()[["Global_Sales"]]

sales_by_platform_plot = px.bar(
    sales_by_platform,
    x=sales_by_platform.index,
    y="Global_Sales",
    title="Sales by Platform (billion $)",
    template="plotly_white"
)
st.plotly_chart(sales_by_platform_plot)

# --- DISTRIBUTION BY RATING GRAPH ---
rating_distribution = filtered_df["Rating"].value_counts()

rating_distribution_plot = px.pie(
    names=rating_distribution.index,
    values=rating_distribution.values,
    title="Game Rating Distribution",
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(rating_distribution_plot)

# --- CRITIC SCORE VS USER SCORE SCATTER PLOT ---
scatter_plot = px.scatter(
    filtered_df,
    x="Critic_Score",
    y="User_Score",
    title="Critic Score vs User Score",
    template="plotly_white"
)
st.plotly_chart(scatter_plot)

# --- HIDE STUFF ---
hide = """
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)