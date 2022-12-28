# Function for user input
def get_user_input():
    fluconazole = st.selectbox('Flukonazol tedavisi:', ['Evet','Hayır'])
    if fluconazole == 'Evet':
        fluconazole = 1
    else:
        fluconazole = 0
    
    tpn = st.selectbox('TPN ihtiyacı:', ['Yok','Var'])
    if tpn == 'Yok':
        tpn = 0
    else:
        tpn = 1
    
    age = st.number_input('Gestasyonel yaş (hafta):', min_value=21, max_value=45, value=38)
    
    weigth = st.selectbox('Doğum ağırlığı (kategorik):', ['≤1000','1001-1500','1501-2500','>2500'])
    if weigth == '≤1000':
        weigth = 1
    elif weigth == '1001-1500':
        weigth = 2
    elif weigth == '1501-2500':
        weigth = 3
    elif weigth == '>2500':
        weigth = 4
    
    uak = st.selectbox('UAK:', ['Evet','Hayır'])
    if uak == 'Evet':
        uak = 1
    else:
        uak = 0

    polisitemi = st.selectbox('Polisitemi:', ['Evet','Hayır'])
    if polisitemi == 'Evet':
        polisitemi = 1
    else:
        polisitemi = 0

    ventilation = st.selectbox('Ventilasyon tipi:', ['Yok','NIV','iMV'])
    if ventilation == 'Yok':
        ventilation = 0
    elif ventilation == 'NIV':
        ventilation = 1
    elif ventilation == 'iMV':
        ventilation = 2
    
    antibiotic = st.selectbox('İlk 24 saat antibiyoterapi:', ['Evet','Hayır'])
    if antibiotic == 'Evet':
        antibiotic = 1
    else:
        antibiotic = 0
    
    respiratory = st.selectbox('Solunumsal patolojiler:', ['Yok','Var'])
    if respiratory == 'Yok':
        respiratory = 0
    else:
        respiratory = 1
    
    maternal = st.selectbox('Maternal risk faktörü:', ['Yok','Var'])
    if maternal == 'Yok':
        maternal = 0
    else:
        maternal = 1
    
    chorioamnionitis = st.selectbox('Koryoamniyonit:', ['Evet','Hayır'])
    if chorioamnionitis == 'Evet':
        chorioamnionitis = 1
    else:
        chorioamnionitis = 0
    
    penicillin = st.selectbox('Penisilin antibiyoterapisi:', ['Evet','Hayır'])
    if penicillin == 'Evet':
        penicillin = 1
    else:
        penicillin = 0
    
    ampicillin = st.selectbox('Ampisilin antibiyoterapisi:', ['Evet','Hayır'])
    if ampicillin == 'Evet':
        ampicillin = 1
    else:
        ampicillin = 0
    
    amikacin = st.selectbox('Amikasin antibiyoterapisi:', ['Evet','Hayır'])
    if amikacin == 'Evet':
        amikacin = 1
    else:
        amikacin = 0
    
    input_df = pd.DataFrame([[fluconazole, tpn, age, weigth, uak, polisitemi, ventilation, antibiotic, respiratory, maternal, chorioamnionitis, penicillin, ampicillin, amikacin]],
                            columns=['fluconazole', 'tpn', 'age', 'weigth', 'uak', 'polisitemi', 'ventilation', 'antibiotic', 'respiratory', 'maternal', 'chorioamnionitis', 'penicillin', 'ampicillin', 'amikacin'],
                            dtype=float,
                            index=['input'])

    return input_df

# Function for making prediction
def predict(model, input_df):
    prediction = model.predict(input_df)
    return prediction

# Function for displaying the predictions
def main():
    st.title("Hastanede Yatış Süresi Tahminleme")
    st.image("https://www.oreilly.com/library/view/python-data-science/9781491912126/assets/pds_0101.png", width=300)
    st.header("Lütfen aşağıdaki hasta bilgilerini giriniz:")

    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit XGBoost ML App </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    input_df = get_user_input()

    model = xgb.XGBRegressor()
    model.load_model('XGBoost.sav')

    if st.button("Tahminle"):
        output = predict(model, input_df)
        st.success(f'Hastanın tahmini hastanede yatış süresi {output[0]:.1f} gündür')

if __name__ == '__main__':
    import xgboost as xgb
    import streamlit as st
    import pandas as pd
    main()
    
#@st.cache