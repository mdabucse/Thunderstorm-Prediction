from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pickle 
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('final_data_set.csv')

# Dont Delete This code

def past_seven_days(date_string):
    given_date = datetime.strptime(date_string, '%Y-%m-%d')
    past_dates = []
    for i in range(7):
        past_dates.append((given_date - timedelta(days=i)).strftime('%Y-%m-%d'))

    return past_dates
result=past_seven_days('2023-01-05')


def dates_for_past(date):
        global humi,temp,wind
        humi = 0 
        temp = 0 
        wind = 0 
        for i in range(len(data.date)):
            if date[4:]==data['date'][i][4:]:
                humi=data['humidity'][i]
                temp=data['meantemp'][i]
                wind=data['wind_speed'][i]
        return temp,humi,wind





with open('final.pkl','rb') as file:
     model = pickle.load(file)

for i in result:
     temp = list(dates_for_past(i))
     print(model.predict([[temp[0],temp[1],temp[2]]]))