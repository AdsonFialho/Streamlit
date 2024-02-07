import streamlit as st
import pandas as pd
import time

st.set_page_config(
    layout='wide',
    page_title='Spotify Songs'
)

@st.cache_data
def load_data():
    df = pd.read_csv('01 Spotify.csv')
    # Operação pesada
    time.sleep(10)
    return df

df = load_data()
st.session_state['df_spotify'] = df

# df.set_index('Artist', inplace=True)
# st.write(df[df['Stream'] > 1000000000])
# st.line_chart(df[df['Stream'] > 1000000000]['Stream'])

df.set_index('Track', inplace=True)

# artists = df['Artist'].unique()
artists = df['Artist'].value_counts().index
artist = st.sidebar.selectbox('Artista', artists)
df_filtered = df[df['Artist'] == artist]

albuns = df_filtered['Album'].value_counts().index
album = st.selectbox('Album', albuns)

df_filtered2 = df[df['Album'] == album]

# display = st.sidebar.checkbox('Display')
# if display:
#     st.bar_chart(df_filtered2['Stream'])

col1, col2 = st.columns([0.7, 0.3])
col1.bar_chart(df_filtered2['Stream'])
col2.line_chart(df_filtered2['Danceability'])

st.write(artist)
