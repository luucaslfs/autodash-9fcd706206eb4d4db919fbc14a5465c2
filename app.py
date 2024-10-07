import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    return df
df = load_data()
# Sidebar
st.sidebar.title('Movie Dashboard')
page = st.sidebar.radio('Select Page', ['Overview', 'Ratings Analysis', 'Genre Analysis', 'Release Year Analysis'])
# Main content
st.title('Movie Dataset Analysis')
if page == 'Overview':
    st.header('Dataset Overview')
    st.write(df.head())
    st.subheader('Dataset Info')
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    st.subheader('Missing Values')
    st.write(df.isnull().sum())
elif page == 'Ratings Analysis':
    st.header('Ratings Analysis')
    rating_cols = ['tomatometer_rating', 'audience_rating']
    selected_rating = st.selectbox('Select Rating Type', rating_cols)
    fig = px.histogram(df, x=selected_rating, nbins=20)
    st.plotly_chart(fig)
    st.subheader('Top 10 Movies by Rating')
    top_10 = df.nlargest(10, selected_rating)[['movie_title', selected_rating]]
    st.write(top_10)
elif page == 'Genre Analysis':
    st.header('Genre Analysis')
    genre_counts = df['genre'].value_counts()
    fig = px.bar(x=genre_counts.index, y=genre_counts.values)
    fig.update_layout(xaxis_title='Genre', yaxis_title='Count')
    st.plotly_chart(fig)
    st.subheader('Word Cloud of Genres')
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['genre']))
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
elif page == 'Release Year Analysis':
    st.header('Release Year Analysis')
    df['release_year'] = pd.to_datetime(df['in_theaters_date']).dt.year
    year_counts = df['release_year'].value_counts().sort_index()
    fig = px.line(x=year_counts.index, y=year_counts.values)
    fig.update_layout(xaxis_title='Release Year', yaxis_title='Number of Movies')
    st.plotly_chart(fig)
    st.subheader('Average Ratings by Year')
    yearly_avg = df.groupby('release_year')[['tomatometer_rating', 'audience_rating']].mean()
    fig = px.line(yearly_avg, x=yearly_avg.index, y=['tomatometer_rating', 'audience_rating'])
    fig.update_layout(xaxis_title='Release Year', yaxis_title='Average Rating')
    st.plotly_chart(fig)
st.sidebar.info('This dashboard analyzes movie data from Rotten Tomatoes.')