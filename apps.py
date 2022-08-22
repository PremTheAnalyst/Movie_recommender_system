#installing required libraries in the virtual environment
import streamlit as st
import pickle
import requests #to hit API i need this library
import pandas as pd


#function to fetch the path of the image of movie from the TMDB API
#it returns the path of the image
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=4af42ee1430d8e4e960c70ad56653120&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


#it is our ML model
#returns the recommended movies and their posters
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #Fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movies1=pickle.load(open('movies.pkl','rb'))
movies=pd.DataFrame(movies1)
similarity=pickle.load(open('similarity.pkl','rb'))

#title of the webpage
st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie_name=st.selectbox('Search for the movies',movies['title'].values)


if st.button('RECOMMEND'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

