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
    # print all columns of dataframe
    st.write('The input dataframe:')
    st.table(input_df)    
    print(input_df)
    #input_arr = np.array(input_df, dtype=object)
    return input_df

# Function for making prediction
def predict(model, input_df):
    prediction = model.predict(input_df)
    return prediction

# Function for displaying the predictions
def main():
    st.set_page_config(
        page_title="HYS Tahminleme Modeli",
        page_icon="🧊",
        #layout="wide",
        initial_sidebar_state="expanded"
    )

    st.sidebar.header('Choose your weightings')
    st.sidebar.markdown('You can change the weightings of the features in the model')
    st.sidebar.markdown('The default weightings are:')
    st.sidebar.markdown('**Hafta:** 0.1')
    st.sidebar.markdown('**Flukonazol alımı:** 0.1')
    st.sidebar.markdown('**Doğum kilosu_kategorik:** 0.1')
    st.sidebar.markdown('**TPN:** 0.1')

    st.title("Hastanede Yatış Süresi Tahminleme")
    qrcode = Image.open('qrcode.png')
    st.image(qrcode, width=300)
    st.subheader("Lütfen aşağıdaki hasta bilgilerini giriniz:")

    # html_temp = """
    # <div style="background-color:tomato;padding:10px">
    # <h2 style="color:white;text-align:center;">Streamlit XGBoost ML App </h2>
    # </div>
    # """

    bg_image = """
    <style>
    .stApp{{
    p {
    background-image: 
    url("https://cdn.pixabay.com/photo/2019/04/24/11/27/flowers-4151900_960_720.jpg");
    background-attachment: fixed;
    background-size: cover
    }}
    </style>
    """

    st.markdown(bg_image, unsafe_allow_html=True)



    input_df = get_user_input()
    print(input_df)

    model = xgb.XGBRegressor()

    with open("XGBoost.json", 'rb') as f:
        model = pkl.load(f)
    
    #model.load_model("XGBoost.json")
    
    

    if st.button("Tahminle"):
        output = predict(model, input_df)
        st.success(f'Hastanın hastanede yatış süresi tahmini {output[0]:.1f} gündür.')

if __name__ == '__main__':
    import xgboost as xgb
    import streamlit as st
    import pandas as pd
    import numpy as np
    from PIL import Image
    import pickle as pkl
    main()
    
#@st.cache