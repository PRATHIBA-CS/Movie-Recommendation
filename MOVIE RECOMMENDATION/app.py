import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a7503f21611c6754658f64426ff0f146&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses 
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None

# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommendation System")

# Create a dropdown to select a movie
selected_movies = st.selectbox("Select a movie:", movies_list)

def recommend(selected_movie):
    index = movies[movies['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movies = []
    recommend_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        if poster:
            recommend_posters.append(poster)
        else:
            recommend_posters.append("No poster available")
    return recommend_movies, recommend_posters

if st.button("Show Recommendation"):
    recommend_movies, recommend_posters = recommend(selected_movies)
    cols = st.columns(5)
    for col, movie, poster in zip(cols, recommend_movies, recommend_posters):
        with col:
            st.text(movie)
            st.image(poster, use_column_width=True)



# streamlit run app.py
