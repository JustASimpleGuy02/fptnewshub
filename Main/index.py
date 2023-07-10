import streamlit as st  # pip install streamlit
from icecream import ic
from Utils import *
import random

def main():
    st.set_page_config(page_title='FPT News Hub')
    st.title('Welcome to FPT News Hub 📈')
    st.subheader('Created by Group 3 - DBP391 Project')

    # count number of articles by past n weeks, default n = 5
    recent_news, week2mentions = get_news_by_week()

    # display number of mentions in line graph by week
    display_mention_statistics(week2mentions)

    # display most recent news' word cloud
    display_wordcloud(recent_news)

    # display details about news
    display_news(recent_news)

def test():
    # Set header for website
    st.set_page_config(page_title='FPT News Hub')
    st.title('Welcome to FPT News Hub 📈')
    st.subheader('Created by Group 3 - DBP391 Project')

    # Create some sample text
    text = "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. Jackdaws love my big sphinx of quartz. The five boxing wizards jump quickly. How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack. Quick wafting zephyrs vex bold Jim."

    # Create and generate a word cloud image:
    wordcloud = WordCloud(background_color='white').generate(text)

    # Display the generated image:
    def display_wordcloud(wordcloud):
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    
    display_wordcloud(wordcloud)

    def generate_dataset(num_points, x_min, x_max, y_min, y_max):
        dataset = []
        for _ in range(num_points):
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            dataset.append((x, y))
        return dataset

    # Set the parameters for the dataset
    num_points = 10  # Number of data points
    x_min = 0       # Minimum x-value
    x_max = 100     # Maximum x-value
    y_min = 0       # Minimum y-value
    y_max = 50      # Maximum y-value

    # Generate the dataset
    dataset = generate_dataset(num_points, x_min, x_max, y_min, y_max)
    st.bar_chart(dataset)
    st.line_chart(dataset)
        
if __name__ == '__main__':
    test()