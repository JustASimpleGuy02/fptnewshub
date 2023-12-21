import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
from Preprocess.clean_text import tien_xu_li
import numpy as np
from Utils.extract_news import prettify_week
import streamlit as st
from Model.model import sentiment
from termcolor import cprint
import pandas as pd
import altair as alt
from textwrap import wrap

dir_path = os.path.dirname(os.path.realpath(__file__))

text2color = {
    "Positive": "green",
    "Neutral": "violet",
    "Negative": "red"
}

def display_headings():
    st.set_page_config(page_title="FPT News Hub")
    st.title("Welcome to FPT News Hub 📈")
    # st.subheader("Created by Group 3 - DBP391 Project")
    st.write("**Created by Group 3 - DBP391 Project**")
    st.write("\n")


def display_mention_statistics(data: pd.DataFrame):
    st.subheader("Number of mentions by Week")
    data.sort_values(by="week", ascending=True, inplace=True, ignore_index=True)
    data["week"] = data["week"].apply(prettify_week)
            
    # Wrap on whitespace with a max line length of 11 chars
    # data["week"] = data["week"].apply(wrap, args=[11])
    
    chart = get_chart(data)
    st.altair_chart(chart.interactive(), use_container_width=True)
    
        
def display_wordcloud(df_recent, n=10):
    """
    Display wordcloud of n recent news
    """
    st.subheader("Word Cloud")
    
    # stopwords = open("Preprocess/stopword.txt", "r")
    stopwords = open("Preprocess/vietnamese-stopwords.txt", "r", encoding="UTF-8")
    stopwords_list = stopwords.read().split("\n")
    
    texts = []
    
    for _, row in df_recent.iterrows():
        title = row.title
        text = row.text
        if title is np.nan:
            title = ""
        if text is np.nan:
            text = ""
        texts.append(title + " " + text)
    
    texts = " ".join(texts)
    texts = tien_xu_li(texts)
    
    wordcloud = WordCloud(
        width=1600,
        height=800,
        stopwords=stopwords_list, 
        background_color="white"
    )
    wordcloud.generate(texts)
        
    fig = plt.figure( figsize=(40,20), facecolor="k")
    plt.imshow(wordcloud, interpolation="bilinear")
    # plt.title("Wordcloud")
    plt.axis("off")
    plt.tight_layout(pad=0)
    
    # plt.show()
    st.pyplot(fig)
    

def display_news(df: pd.DataFrame):
    df.sort_values(by=["time"], ascending=False, inplace=True)
    
    for _, row in df.iterrows():
        print("Time:", row.time)
        print("Link:", row.link)
        
        title = str(row.title).strip()
        if not isinstance(title, float) and len(title) > 0:
            print("Title: " + title)
        
        if isinstance(row.text, float):
            print()
            continue
        
        stm = sentiment(row)
        # cprint(f"Sentiment: {stm}", text2color[stm])
        print(f"Sentiment: {stm}")
                
        print()
        
        
def st_display_news(recent_news: pd.DataFrame):
    st.write("\n")
    st.subheader("**Recent News**")
    st.divider()
    
    for _, row in recent_news.iterrows():
        st.write("**Time**: " + str(prettify_date(row.time)))
        st.write("**Link**: " + row.link)
        
        title = str(row.title).strip()
        if not isinstance(title, float) and len(title) > 0:
            st.write("**Title**: " + title)
            
        stm = sentiment(row)
        st.markdown(f"**Sentiment**: :{text2color[stm]}[{stm}]")
            
        st.divider()

def prettify_date(date: str):
    """Change date to usual format: dd//mm/yyyy

    Args:
        date (str): input date

    Returns:
        date: the date changed to its format
    """
    # week = ['/'.join(w.split('-')[::-1]) for w in week.split('_')]
    date = '/'.join(date.split('-'))
    return date

# Define the base time-series chart.
def get_chart(data):
    hover = alt.selection_point(
        fields=["week"],
        nearest=True,
        on="mouseover",
        empty=False,
    )

    lines = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x="week",
            y="mentions",
        
            # x=alt.X(
            #     "week_readable", 
            #     axis=alt.Axis(labelFontSize=9),
            # ),
            # y=alt.Y("mentions:Q"),
            # order=alt.Order("week:Q")
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="week",
            y="mentions",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("week", title="Week"),
                alt.Tooltip("mentions", title="Number of mentions"),
            ],
        )
        .add_params(hover)
    )
    return (lines + points + tooltips).interactive()
    
    