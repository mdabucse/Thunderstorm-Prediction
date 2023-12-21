import streamlit as st
import numpy as np
import pickle 
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import pyttsx3
import plotly.express as px
from datetime import datetime, timedelta
from datetime import date




def main():
    global engine
    

    #Data Loading And Preprocessing

    data=pd.read_csv('final_data_set.csv')
    for i in range(len(data.humidity)):
        data['date'][i]=data['date'][i].replace('-','')

    # Graph Data Collection
    for_graph ={
        'Year': [2013, 2014, 2015, 2016],
        'Humidity': [],
        'Temperature': [],  
        'Wind Speed': [],
    }

    # Past Seven Days Data Collection
    def dates_for_past(date):
        global humi,temp,wind
        humi = 0 
        temp = 0 
        wind = 0 
        for i in range(len(data.date)):
            if date[4:]==data['date'][i][4:]:
                humi_past=data['humidity'][i]
                temp_past=data['meantemp'][i]
                wind_past=data['wind_speed'][i]
        return temp_past,humi_past,wind_past
    
    def past_seven_days(date_string):
        date_format = '%Y%m%d'  

        try:
            given_date = datetime.strptime(date_string, date_format)
        except ValueError:
            return "Invalid date format. Please provide the date in YYYYMMDD format."

        past_dates = []
        for i in range(1, 8):
            delta = timedelta(days=i)
            past_date = given_date - delta
            past_dates.append(past_date.strftime('%Y%m%d'))

        return past_dates
    
    # Parameter Generator
    def dates(date):
        global humi,temp,wind
        humi = 0 
        temp = 0 
        wind = 0 
        for i in range(len(data.date)):
            if date[4:]==data['date'][i][4:]:
                temp=data['meantemp'][i]
                humi=data['humidity'][i]
                wind=data['wind_speed'][i]
        return temp,humi,wind


    def data_for_graph(date):
        for i in range(len(data.date)):
            if date[4:]==data['date'][i][4:]:
                for_graph['Humidity'].append(data['humidity'][i])
                for_graph['Temperature'].append(data['meantemp'][i])
                for_graph['Wind Speed'].append(data['wind_speed'][i])
        return 0

    # Frontend Development
    st.title('Thunderstorm Prediction ⛈️')

    with open('final.pkl','rb') as file:
        model_final = pickle.load(file)

    number = st.date_input("Select Date", date.today())
    button =st.button('Get Result')
    for_col=number
    number =str(number).replace('-','')
    past_seven_days_date = past_seven_days(number)
    predict=list(dates(number))
    result=model_final.predict([predict])
    if button:
        if result[0]==1:
            st.title("Thunderstorm Alert")
        else:
            st.title("Not Possible To Come")
    data_for_graph(number)

    # Columns For Todays Data
    data1,data2 = st.columns(2)

    if button:
        if result[0]==1:
            st.title("Todays Thunderstorm Factors Level\n")
            with data1:
                st.image('thunder.png',caption='Thunder',width=200)
            with data2:
                st.write('Thunderstorm alert in effect, urging immediate safety protocols and precautionary measures for all Air Force operations and personnel.')
                

        else:
            st.title("Todays Thunderstorm Factors Level\n")
            with data1:
                st.image('sunny.png',width=200)
            with data2:
                st.write('Due to Low level of Affecting Factors So ,Today Thunderstorm Not Possible To Come')
        
        col1,col2,col3= st.columns(3)
        st.title("Past 7 Days Predictions")
        # Columns For Past Datas
        col=['c1','c2','c3','c4','c5','c6','c7','c8']
        col = st.columns(8)

        # Past Data Colloction 
        with col[0]:
            st.write('\n\n')
            st.write('\n\n')
            st.write('\n\n')
            st.image('temperature.png',caption='Temperature',width=60)
            st.image('humidity.png',caption='Humidity',width=60)
            st.image('wind.png',caption='Wind ',width=60)
        st.title('\n')
        

        for i in range(1,7):
            number = past_seven_days_date[i]
            predict_past=list(dates(number))
            result_past=model_final.predict([predict_past])
            with col[i]:
                if result_past[0]==1:
                    st.image('thunder.png',caption='Thunder',width=100)
                    st.write('\n')
                    st.write(number)
                    st.write(f"{predict_past[0]:.2f}")
                    st.write(f"{predict_past[1]:.2f}")
                    st.write(f"{predict_past[2]:.2f}")


                else:
                    st.image('sunny.png',caption='Sunny',width=100)
                    st.write('\n')
                    st.write(number)
                    st.write(f"{predict_past[0]:.2f}")
                    st.write(f"{predict_past[1]:.2f}")
                    st.write(f"{predict_past[2]:.2f}")


        
        with col1:
            st.image('humidity.png',caption='Humidity',width=100)
            st.write('Humidity Level '+f"{predict[0]:.2f}")
        with col2:
            st.image('temperature.png',caption='Temperature',width=100)
            st.write('Temperature Level '+f"{predict[0]:.2f}")
        with col3:
            st.image('wind.png',caption='Wind Speed',width=100)
            st.write('Wind Speed Level '+f"{predict[0]:.2f}")
        
            
        # Plotting The Graph In The Streamlit Using Past Data 
        df= pd.DataFrame(for_graph)
        df_long = pd.melt(df, id_vars='Year', var_name='Measurement', value_name='Value')
        fig = px.line(df_long, x='Year', y='Value', color='Measurement',title='Thunderstorm Factors Past 5 Years', labels={'Value': 'Value'})
        st.plotly_chart(fig)

        # Voice Converter
        if result[0]==1:
            engine = pyttsx3.init()
            engine.setProperty('rate',150)
            engine.setProperty('volume',0.9)
            engine.say("Thunderstorm alert in effect, urging immediate safety protocols and precautionary measures for all Air Force operations and personnel.")
            engine.runAndWait()
            engine.stop()
        else:
            engine = pyttsx3.init()
            engine.setProperty('rate',150)
            engine.setProperty('volume',0.9)
            engine.say("Due to Low level of Affecting Factors So ,Today Thunderstorm Not Possible To Come ")
            engine.runAndWait()
            engine.stop()
        

if __name__ == "__main__":
    main()