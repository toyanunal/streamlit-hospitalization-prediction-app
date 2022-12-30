import xgboost as xgb
import streamlit as st
import pandas as pd
import numpy as np
import pickle as pkl
import base64
import time
from PIL import Image

# Function for user input
def get_user_input():
    week = st.slider('Gestasyonel yaş (hafta):', min_value=21, max_value=45, value=33, step=1)
    #week = st.number_input('Gestasyonel yaş (hafta):', min_value=21, max_value=45, value=30, step=1)
    day = st.slider('Gestasyonel yaş (gün):', min_value=0, max_value=6, value=3, step=1)
    day = int(day)
    age = week + day/7

    weight = st.radio('Doğum ağırlığı (kategorik):', ['≤1000 gr','1001-1500 gr','1501-2500 gr','>2500 gr'])
    if weight == '≤1000 gr':
        weight = 1
    elif weight == '1001-1500 gr':
        weight = 2
    elif weight == '1501-2500 gr':
        weight = 3
    elif weight == '>2500 gr':
        weight = 4
    
    birth = st.radio('Doğum şekli:', ['C/S','NSVY'])
    if birth == 'C/S':
        birth = 1
    else:
        birth = 0

    antibiotic = st.radio('Maternal risk faktörü:', ['Yok','Var'])
    if antibiotic == 'Yok':
        antibiotic = 0
    else:
        antibiotic = 1

    chorioamnionitis = st.radio('Koryoamniyonit:', ['Yok','Var'])
    if chorioamnionitis == 'Yok':
        chorioamnionitis = 0
    else:
        chorioamnionitis = 1

    respiratory = st.radio('Solunumsal patolojiler:', ['Yok','Var'])
    if respiratory == 'Yok':
        respiratory = 0
    else:
        respiratory = 1

    polisitemia = st.radio('Polisitemi:', ['Yok','Var'])
    if polisitemia == 'Yok':
        polisitemia = 0
    else:
        polisitemia = 1

    uak = st.radio('UAK:', ['Yok','Var'])
    if uak == 'Yok':
        uak = 0
    else:
        uak = 1

    ventilation = st.radio('Ventilasyon tipi:', ['Yok','NIV','iMV'])
    if ventilation == 'Yok':
        ventilation = 0
    elif ventilation == 'NIV':
        ventilation = 1
    elif ventilation == 'iMV':
        ventilation = 2

    tpn = st.radio('TPN ihtiyacı:', ['Yok','Var'])
    if tpn == 'Yok':
        tpn = 0
    else:
        tpn = 1

    fluconazole = st.radio('Flukonazol tedavisi:', ['Yok','Var'])
    if fluconazole == 'Yok':
        fluconazole = 0
    else:
        fluconazole = 1
    
    antibiotic_24h = st.radio('İlk 24 saat antibiyoterapi:', ['Yok','Var'])
    if antibiotic_24h == 'Yok':
        antibiotic_24h = 0
    else:
        antibiotic_24h = 1
    
    ampicillin = st.radio('Ampisilin antibiyoterapisi:', ['Yok','Var'])
    if ampicillin == 'Yok':
        ampicillin = 0
    else:
        ampicillin = 1

    penicillin = st.radio('Penisilin antibiyoterapisi:', ['Yok','Var'])
    if penicillin == 'Yok':
        penicillin = 0
    else:
        penicillin = 1
    
    amikacin = st.radio('Amikasin antibiyoterapisi:', ['Yok','Var'])
    if amikacin == 'Yok':
        amikacin = 0
    else:
        amikacin = 1

    input_df = pd.DataFrame([[age, fluconazole, weight, tpn, uak, polisitemia, antibiotic, amikacin, antibiotic_24h, chorioamnionitis, birth, respiratory, ampicillin, penicillin, ventilation]],
                            columns=['Hafta', 'Flukonazol alımı', 'Doğum kilosu_kategorik', 'TPN', 'Umblikal Arter', 'Tanı-4', 'Ab var/yok', 'Ab-8', 'İlk 24 saat Ab', 'Mr-40', 'Doğum şekli', 'Tanı-1', 'Ab-14', 'Ab-12', 'Ventilasyon tipi (ilk yatış)'],
                            dtype=float,
                            index=['input'])

    st.write('The input dataframe:')
    st.dataframe(input_df)
    return input_df

# Function for making prediction
def predict(model, input_df):
    prediction = model.predict(input_df)
    return prediction

# Functions for background image from local
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# Function for displaying the predictions
def main():
    st.set_page_config(
        page_title="HYS Tahminleme Modeli",
        page_icon="random",
        #layout="wide",
        #initial_sidebar_state="expanded"
        )

    st.title("Hastanede Yatış Süresi Tahminleme")
    st.write("[![Star](https://img.shields.io/github/stars/toyanunal/streamlit-hospitalization-prediction-app.svg?logo=github&style=social)](https://gitHub.com/toyanunal/streamlit-hospitalization-prediction-app)")
    qrcode = Image.open('qrcode.png')
    st.image(qrcode, width=300)
    st.subheader("Lütfen aşağıdaki hasta bilgilerini giriniz:")

    set_png_as_page_bg("background.png")

    input_df = get_user_input()

    model = xgb.XGBRegressor()
    with open("XGBoost.json", 'rb') as f:
        model = pkl.load(f)

    if st.button("Tahminle"):
        output = predict(model, input_df)
        st.spinner()
        with st.spinner(text='In progress'):
            time.sleep(1)
            st.success(f'Hastanın hastanede yatış süresi tahmini {output[0]:.0f} gündür.')
    
    
    my_bar = st.progress(0)
    for percent_complete in range(20):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    # st.spinner()
    # with st.spinner(text='In progress'):
    #     time.sleep(5)
    #     st.success('Done')

if __name__ == '__main__':
    main()