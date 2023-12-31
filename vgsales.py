import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from urllib.error import URLError



@st.cache_data
def get_data():
    path_ = 'vgsales.csv'
    df = pd.read_csv(path_)
    # drop NAN on Year & Publisher
    df.dropna(inplace=True)
    # cleaning Year column
    df.Year = df.Year.astype('str')
    df.Year = df.Year.str.replace('.0','')
    return df

try:
    df = get_data()
    st.title("""Video games sales analysis""")

    # total sales metrics
    st.write("Sale metrics")
    st.dataframe(df.head(3))
    st.write()

    # total sales metrics
    global_sales = np.round(sum(df.Global_Sales),2)
    eu_sales = np.round(sum(df.EU_Sales),2)
    na_sales = np.round(sum(df.NA_Sales),2)
    jp_sales = np.round(sum(df.JP_Sales),2)
    other_sales = np.round(sum(df.Other_Sales),2)


    # creats a series of columns
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)


    # card
    col1.metric("Global Sales Total", global_sales,"USD")
    col2.metric("North America Sales", na_sales,"USD")
    col3.metric("European Union Sales",eu_sales,"USD")
    col4.metric("Japan Sales Total", jp_sales,"USD")
    col5.metric("Other Sales",other_sales, "USD")
    
    # filters (platforms)
    st.write("Select a Platform and Genre")
    col6, col7 = st.columns(2)
    platforms = df.Platform.unique()
    selected_platform = col6.multiselect(
        "Platforms",platforms,[platforms[0],
                     platforms[1]]
    )
   
   # filter 2 (genre)
    genre = df.Genre.unique()
    selected_genre = col7.multiselect(
        "Genre",genre,[genre[0],
                     genre[1]]
    )
    # filter 3 (publisher)
    publisher = df.Publisher.unique()
    selected_publisher = col7.multiselect(
        "Publisher",publisher,[publisher[0],
                     publisher[1]]
    )

    filtered_data = df[df["Platform"].isin(selected_platform) &
                       df["Genre"].isin(selected_genre)]

    # table
    if not selected_platform and selected_genre:
        st.error("Please select both filters from platform and genre")

    st.write("""Filtered result obtained""")
    st.table(filtered_data.head())

    # table end

    # plots
    # bar chart
    # Top 10
    st.write(""" ## Top Platform charts """)
    bar0 = df.groupby(['Platform'])['Global_Sales'].sum().nlargest(n=10).sort_values(ascending=True)
    st.write(bar0)
    st.bar_chart(bar0, color="#d4af37")

    st.write(""" # Global sales per platform """)
    bar1 = filtered_data.groupby(['Platform'])['Global_Sales'].sum().sort_values(ascending=True)
    st.write(bar1)
    st.bar_chart(bar1, color="#d4af37", width=20, height=400)

    # line chart
    st.write(""" ## Global sales over time(Line chart)""")
    chart = (
        alt.Chart(filtered_data)
        .mark_line()
        .encode(
            x="Year",
            y=alt.Y("Global_Sales", stack=None),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    # area chart
    st.write("""## Global Sales over Time(area chart)""")
    chart = (
        alt.Chart(filtered_data)
        .mark_area(opacity=0.8)
        .encode(
            x="Year",
            y=alt.Y("Global_Sales", stack=None),
        )
    )
    st.altair_chart(chart, use_container_width=True)


    # # countries = st.multiselect(
    #     "Choose countries", list(df.index), ["China", "United States of America"]
    # )
    # if not countries:
    #     st.error("Please select at least one country.")
    # else:
    #     data = df.loc[countries]
    #     data /= 1000000.0
    #     st.write("### Gross Agricultural Production ($B)", data.sort_index())

    #     data = data.T.reset_index()
    #     data = pd.melt(data, id_vars=["index"]).rename(
    #         columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    #     )
    #     chart = (
    #         alt.Chart(data)
    #         .mark_area(opacity=0.3)
    #         .encode(
    #             x="year:T",
    #             y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #             color="Region:N",
    #         )
    #     )
    #     st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
