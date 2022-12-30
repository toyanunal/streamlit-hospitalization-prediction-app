# Function for user input
def get_user_input():
    deneme = st.slider('Deneme:', min_value=21, max_value=45, value=30, step=1)
    week = st.number_input('Gestasyonel yaş (hafta):', min_value=21, max_value=45, value=30, step=1)
    day = st.radio('Gestasyonel yaş (gün):', ['0','1','2','3','4','5','6'])
    day = int(day)
    age = week + day/7

    fluconazole = st.radio('Flukonazol tedavisi:', ['Yok','Var'])
    if fluconazole == 'Yok':
        fluconazole = 0
    else:
        fluconazole = 1
    
    weigth = st.radio('Doğum ağırlığı (kategorik):', ['≤1000 gr','1001-1500 gr','1501-2500 gr','>2500 gr'])
    if weigth == '≤1000 gr':
        weigth = 1
    elif weigth == '1001-1500 gr':
        weigth = 2
    elif weigth == '1501-2500 gr':
        weigth = 3
    elif weigth == '>2500 gr':
        weigth = 4

    tpn = st.radio('TPN ihtiyacı:', ['Yok','Var'])
    if tpn == 'Yok':
        tpn = 0
    else:
        tpn = 1
    
    uak = st.radio('UAK:', ['Yok','Var'])
    if uak == 'Yok':
        uak = 0
    else:
        uak = 1

    polisitemia = st.radio('Polisitemi:', ['Yok','Var'])
    if polisitemia == 'Yok':
        polisitemia = 0
    else:
        polisitemia = 1

    antibiotic = st.radio('Maternal risk faktörü:', ['Yok','Var'])
    if antibiotic == 'Yok':
        antibiotic = 0
    else:
        antibiotic = 1

    amikacin = st.radio('Amikasin antibiyoterapisi:', ['Yok','Var'])
    if amikacin == 'Yok':
        amikacin = 0
    else:
        amikacin = 1

    antibiotic_24h = st.radio('İlk 24 saat antibiyoterapi:', ['Yok','Var'])
    if antibiotic_24h == 'Yok':
        antibiotic_24h = 0
    else:
        antibiotic_24h = 1
    
    chorioamnionitis = st.radio('Koryoamniyonit:', ['Yok','Var'])
    if chorioamnionitis == 'Yok':
        chorioamnionitis = 0
    else:
        chorioamnionitis = 1
    
    birth = st.radio('Doğum şekli:', ['C/S','NSVY'])
    if birth == 'C/S':
        birth = 1
    else:
        birth = 0

    respiratory = st.radio('Solunumsal patolojiler:', ['Yok','Var'])
    if respiratory == 'Yok':
        respiratory = 0
    else:
        respiratory = 1
    
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
    
    ventilation = st.radio('Ventilasyon tipi:', ['Yok','NIV','iMV'])
    if ventilation == 'Yok':
        ventilation = 0
    elif ventilation == 'NIV':
        ventilation = 1
    elif ventilation == 'iMV':
        ventilation = 2
     
    input_df = pd.DataFrame([[age, fluconazole, weigth, tpn, uak, polisitemia, antibiotic, amikacin, antibiotic_24h, chorioamnionitis, birth, respiratory, ampicillin, penicillin, ventilation]],
                            columns=['age', 'fluconazole', 'weigth', 'tpn', 'uak', 'polisitemia', 'antibiotic', 'amikacin', 'antibiotic_24h', 'chorioamnionitis', 'birth', 'respiratory', 'ampicillin', 'penicillin', 'ventilation'],
                            dtype=float,
                            index=['input'])

    input_arr = np.array(input_df, dtype=object)
    return input_arr

# Function for making prediction
def predict(model, input_df):
    prediction = model.predict(input_df)
    return prediction

# Function for displaying the predictions
def main():
    st.title("Hastanede Yatış Süresi Tahminleme")
    qrcode = Image.open('qrcode.png')
    st.image(qrcode, width=300)
    st.header("Lütfen aşağıdaki hasta bilgilerini giriniz:")

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