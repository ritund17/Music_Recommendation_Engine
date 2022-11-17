import streamlit as st
import pickle
import pandas as pd
from tqdm import tqdm
import sklearn
import numpy as np

song_dict = pickle.load(open('song_dict.pkl','rb'))
songs = pd.DataFrame(song_dict)
st.title('Song Recommender System')
html_temp = """
      <div style="background-color:tomato;padding:10px">
      <h2 style="color:white;text-align:center;"> SONG RECOMMEDER SYSTEM </h2>
      </div>
      """


class SpotifyRecommender():
    def __init__(self, rec_data):
        # our class should understand which data to work with
        self.rec_data_ = rec_data

    # function which returns recommendations, we can also choose the amount of songs to be recommended
    def get_recommendations(self, track_name, amount=1):
        distances = []
        # choosing the data for our song
        song = self.rec_data_[(self.rec_data_.track_name.str.lower() == track_name.lower())].head(1).values[0]
        # dropping the data with our song
        res_data = self.rec_data_[self.rec_data_.track_name.str.lower() != track_name.lower()]
        for r_song in tqdm(res_data.values):
            dist = 0
            for col in np.arange(len(res_data.columns)):
                # indeces of non-numerical columns
                if not col in [0, 1]:
                    # calculating the manhettan distances for each numerical feature
                    dist = dist + np.absolute(float(song[col]) - float(r_song[col]))
            distances.append(dist)
        res_data['distance'] = distances
        # sorting our data to be ascending by 'distance' feature
        res_data = res_data.sort_values('distance')
        columns = ['artist_name', 'track_name']
        return res_data[columns][:amount]
recommender = SpotifyRecommender(songs)

def main():

    song = st.text_input("Type your song",)
    result=""
    
    if st.button("Recommend"):
        result=recommender.get_recommendations(song, 10)
        for i in (result['track_name']):
            st.write(i)
    else:
        print("Song not found")



if __name__=='__main__':
    main()

