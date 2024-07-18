import streamlit as st
import pickle
import pandas as pd
import requests

# Custom CSS for dark theme
st.markdown(
    """
    <style>
    /* Make the entire background black */
    body {
        background-color: #000000;
        color: white;
    }
    .reportview-container {
        background: #000000;
        color: white;
    }
    .main .block-container {
        background: #000000;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    .stTextInput input, .stSelectbox select {
        background-color: #333;
        color: white;
    }
    .stButton button {
        background-color: #1f77b4;
        color: white;
    }
    .stMarkdown, .stTitle, .stHeader, .stSubheader, .stCaption {
        color: #222222;
    }
    .stImage img {
        border: 1px solid #444;
    }
    h1 {
        color: red !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=feec64a94b167a2519e3e5547008876e&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_posters = []
    for i in movie_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie.append(movies.iloc[i[0]].title)

    return recommended_movie, recommended_movie_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    '.',
    movies['title'].values,
    key = 'selectbox'  # Assign a key to uniquely identify this select box

)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    if len(recommended_movie_names) == 5:  # Ensure exactly 5 recommendations
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)
