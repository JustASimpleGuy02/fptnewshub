import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
import requests as rq
from bs4 import BeautifulSoup as bs
import numpy as np
import PIL
from urllib.request import urlopen


# def generate_excel_download_link(df):
#     # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
#     towrite = BytesIO()
#     df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
#     towrite.seek(0)  # reset pointer
#     b64 = base64.b64encode(towrite.read()).decode()
#     href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
#     return st.markdown(href, unsafe_allow_html=True)

# def generate_html_download_link(fig):
#     # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
#     towrite = StringIO()
#     fig.write_html(towrite, include_plotlyjs="cdn")
#     towrite = BytesIO(towrite.getvalue().encode())
#     b64 = base64.b64encode(towrite.read()).decode()
#     href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
#     return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='CSV Plotter')
st.title('CSV Plotter 📈')
st.subheader('Feed me with your csv file')

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader('Choose a csv file', type='csv')
    if uploaded_file:
        st.markdown('---')
        df = pd.read_csv(uploaded_file, index_col=False)
        st.dataframe(df.head())
        groupby_column = st.selectbox(
            'What are you?',
            ('Male', 'Female', 'Email', 'Other'),
        )
        st.write('You are *' + groupby_column + '* :sunglasses:')

    # # -- GROUP DATAFRAME
    # output_columns = ['Sales', 'Profit']
    # df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    # # -- PLOT DATAFRAME
    # fig = px.bar(
    #     df_grouped,
    #     x=groupby_column,
    #     y='Sales',
    #     color='Profit',
    #     color_continuous_scale=['red', 'yellow', 'green'],
    #     template='plotly_white',
    #     title=f'<b>Sales & Profit by {groupby_column}</b>'
    # )
    # st.plotly_chart(fig)

    # -- DOWNLOAD SECTION
    # st.subheader('Downloads:')
    # generate_excel_download_link(df)
    # generate_html_download_link(fig)

with col2:
    uploaded_link = st.text_input('Enter the html link:', placeholder='Enter link here')
    if uploaded_link:
        try:
            resp = rq.get(uploaded_link)
            if resp.status_code:
                soup = bs(resp.content, features='lxml')
                tags = soup.findAll('img')
                imgs_link = [img['src'] for img in tags if img['src'][-3:] in ['jpg', 'png']]
                if len(imgs_link) == 0:
                    st.write('No png/jpg images found on this website!')
                else:
                    for img_link in imgs_link:
                        img = np.array(PIL.Image.open(urlopen(img_link)))
                        if img.shape[-1] == 3:
                            st.image(img)
                            break
        except:
            st.write("Incorrect html link, or this website cannot be crawled!")
    uploaded_img = st.file_uploader('Choose a image file', type=['png', 'jpg'])
    if uploaded_img:
        st.image(uploaded_img)


