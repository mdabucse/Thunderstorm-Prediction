import streamlit as st
import numpy as np
import pickle 
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
# import pyttsx3
import plotly.express as px



def main():
    # global engine
    # engine = pyttsx3.init()
    # engine.setProperty('rate',150)
    # engine.setProperty('volume',0.9)

    data=pd.read_csv('final_data_set.csv')
    for i in range(len(data.humidity)):
        data['date'][i]=data['date'][i].replace('-','')


    for_graph ={
        'Year': [2013, 2014, 2015, 2016],
        'Humidity': [],
        'Temperature': [],  
        'Wind Speed': [],
    }


    def dates(date):
        global humi,temp,wind
        humi = 0 
        temp = 0 
        wind = 0 
        for i in range(len(data.date)):
            if date[4:]==data['date'][i][4:]:
                for_graph['Humidity'].append(data['humidity'][i])
                for_graph['Temperature'].append(data['meantemp'][i])
                for_graph['Wind Speed'].append(data['wind_speed'][i])
                temp=data['meantemp'][i]
                humi=data['humidity'][i]
                wind=data['wind_speed'][i]
        return temp,humi,wind
    

    
    st.title('Thunderstorm Prediction ⛈️')

    with open('final.pkl','rb') as file:
        model_final = pickle.load(file)

    number = st.text_input('Enter Date YYYYMMDD')
    predict=list(dates(number))
    result=model_final.predict([predict])


    if st.button('Get Result'):
        if result[0]==1:
            st.write("ThunderStorm Alert ⛈️")
            st.image('thunder.png',caption='Thunder',width=200)
        else:
            st.write("Not Possible to come")
            st.image('sunny.png',width=200)
        
        col1,col2,col3= st.columns(3)

        with col1:
            st.image('humidity.png',caption='Humidity',width=100)
            st.write('Humidity Level '+str(predict[0]))
        with col2:
            st.image('temperature.png',caption='Temperature',width=100)
            st.write('Temperature Level '+str(predict[1]))
        with col3:
            st.image('humidity.png',caption='Wind Speed',width=100)
            st.write('Wind Speed Level '+str(predict[2]))
            
        # engine.say("Thunderstorm Varuthu")
        # engine.runAndWait()
        df= pd.DataFrame(for_graph)
        df_long = pd.melt(df, id_vars='Year', var_name='Measurement', value_name='Value')
        fig = px.line(df_long, x='Year', y='Value', color='Measurement',title='Thunderstorm Factors Past 5 Years', labels={'Value': 'Value'})
        st.plotly_chart(fig)
        

if __name__ == "__main__":
    main()