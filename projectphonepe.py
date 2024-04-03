import pandas as pd 
import json
import os
import mysql.connector
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
#database connection 
mydb= mysql.connector.connect(
    host='your database',
    user="admin",
    password="yourpassword ",
    database='phonepeproject')
mycursor= mydb.cursor()
# state name based on geo map 
State_name=['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
       'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
       'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
       'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
       'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh',"Lakshadweep", 'Madhya Pradesh',
       'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
       'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
       'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand',
       'Uttar Pradesh', 'West Bengal']
#Aggregate Transaction 
path= r"D:\Users\Admin\Desktop\datasciene\DemoMongoDB\phonepe\pulse\data\aggregated\transaction\country\india\state/"
agg_state_list=os.listdir(path)
data_name={"state":[],'year':[],'quater':[],'Transaction_type':[], "Transaction_count":[],"Transaction_amount":[] }
for i in agg_state_list:
    p_i=path+i+"/"
    agg_yr=os.listdir(p_i)
    for j in agg_yr:
        p_j=p_i+j+"/"
        agg_yr_list=os.listdir(p_j)
        for k in agg_yr_list:
            p_k=p_j+k
            data=open(p_k,"r")
            data_data=json.load(data)
            for l in data_data["data"]["transactionData"]:
              Name=l["name"]
              count=l['paymentInstruments'][0]['count']
              amount=l['paymentInstruments'][0]['amount']
              data_name['Transaction_type'].append(Name)
              data_name["Transaction_count"].append(count)
              data_name["Transaction_amount"].append(amount)
              data_name['state'].append(i)
              data_name['year'].append(j)
              data_name['quater'].append(int(k.strip('.json')))
data1=pd.DataFrame(data_name)
Agg_trans=data1.sort_values(by=["state"],ascending=True)
stat1=Agg_trans.state.unique()
Agg_trans.replace(stat1,State_name, inplace=True)



#Aggregate User
path_2=r"D:\Users\Admin\Desktop\datasciene\DemoMongoDB\phonepe\pulse\data\aggregated\user\country\india\state/"
user_list=os.listdir(path_2)

user_data={"state":[],'year':[],'quater':[],'Brands':[], "Transaction_count":[],"percentage":[] }
for i in user_list:
    p_i=path_2+i+"/"
    us_yr=os.listdir(p_i)
    for j in us_yr:
        p_j=p_i+j+"/"
        us_yr_list=os.listdir(p_j)
        for k in us_yr_list:
            p_k=p_j+k
            userdata=open(p_k,"r")
            user_da_ta=json.load(userdata)
            if user_da_ta["data"]["usersByDevice"]:
               for l in user_da_ta["data"]["usersByDevice"]:
                  brands=l['brand']
                  Count=l['count']
                  Percentage=l['percentage']
                  user_data['Brands'].append(brands)
                  user_data["Transaction_count"].append(Count)
                  user_data["percentage"].append(Percentage)
                  user_data["state"].append(i)
                  user_data['year'].append(j)
                  user_data['quater'].append(int(k.strip('.json')))
data2=pd.DataFrame(user_data) 
agg_user =data2.sort_values(by=['state'],ascending=True) 
stat2=agg_user.state.unique()
agg_user.replace(stat2,State_name,inplace=True)

# path3 Map Transaction
path_3=r"D:\Users\Admin\Desktop\datasciene\DemoMongoDB\phonepe\pulse\data\map\transaction\hover\country\india\state/"
map_agg_trans=os.listdir(path_3)

maptrans_data={"state":[],'year':[],'quater':[],'District':[], "Transaction_count":[],"Transaction_amount":[] }
for i in map_agg_trans:
  p_i=path_3+i+'/'
  map_trans_yr=os.listdir(p_i)
  for j in map_trans_yr:
        p_j=p_i+j+"/"
        map_trans_yr_list=os.listdir(p_j)
        for k in map_trans_yr_list:
          p_k=p_j+k
          map_t_data=open(p_k,"r")
          map_trans_data= json.load(map_t_data)
          for l in map_trans_data["data"]["hoverDataList"]:
            district=l['name']
            count=l['metric'][0]['count']
            amount=l['metric'][0]["amount"]
            maptrans_data["District"].append(district)
            maptrans_data["Transaction_count"].append(count)
            maptrans_data["Transaction_amount"].append(amount)
            maptrans_data["state"].append(i)
            maptrans_data["year"].append(j)
            maptrans_data["quater"].append(int(k.strip('.json')))

data3=pd.DataFrame(maptrans_data)
map_trans=data3.sort_values(by=["state"],ascending=True)
stat3=map_trans.state.unique()
map_trans.replace(stat3,State_name, inplace=True)
q=map_trans.District.unique()
q1=[]
for j in q:
  if "district" in j:
   a1= j.replace('district','')
   b1=a1.title()
   q1.append(b1)
map_trans.replace(q,q1,inplace=True)

#path4 Map user 
path_4= r"D:\Users\Admin\Desktop\datasciene\DemoMongoDB\phonepe\pulse\data\map\user\hover\country\india\state/"
map_agg_user=os.listdir(path_4)

mapuser_data={"state":[],'year':[],'quater':[],'District':[], "RegisteredUser":[],"AppOpens":[] }

for i in map_agg_user:
  p_i=path_4+i+'/'
  map_user_yr=os.listdir(p_i)
  for j in map_user_yr:
        p_j=p_i+j+"/"
        map_user_yr_list=os.listdir(p_j)
        for k in map_user_yr_list:
          p_k=p_j+k
          map_u_data=open(p_k,"r")
          map_user_data= json.load(map_u_data)
          for l in map_user_data["data"]['hoverData'].items():
            district= l[0]
            registerUsers=l[1]['registeredUsers']
            appoens=l[1]['appOpens']
            mapuser_data["District"].append(district)
            mapuser_data["RegisteredUser"].append(registerUsers)
            mapuser_data["AppOpens"].append(appoens)
            mapuser_data["state"].append(i)
            mapuser_data["year"].append(j)
            mapuser_data["quater"].append(int(k.strip('.json')))
data4=pd.DataFrame(mapuser_data)
map_users=data4.sort_values(by=["state"],ascending=True)
stat4=map_users.state.unique()
map_users.replace(stat4,State_name, inplace=True)
w=map_users.District.unique()
w1=[]
for i in w:
  if "district" in i:
   a= i.replace('district','')
   b=a.title()
   w1.append(b)
map_users.replace(w,w1,inplace=True)

#path5 Top Transaction

path_5= r"D:\Users\Admin\Desktop\datasciene\DemoMongoDB\phonepe\pulse\data\top\transaction\country\india\state/"
top_trans=os.listdir(path_5)
toptrans_data={"state":[],'year':[],'quater':[],'postalcode':[], "Transaction_count":[],"Transaction_amount":[] }

for i in top_trans:
  p_i=path_5+i+'/'
  top_trans_yr=os.listdir(p_i)
  for j in top_trans_yr:
        p_j=p_i+j+"/"
        top_trans_yr_list=os.listdir(p_j)
        for k in top_trans_yr_list:
          p_k=p_j+k
          top_t_data=open(p_k,"r")
          top_trans_data= json.load(top_t_data)
          for l in top_trans_data['data']['pincodes']:
             pincode= l["entityName"]
             count=l['metric']['count']
             amount=l['metric']['amount']
             toptrans_data["postalcode"].append(pincode)
             toptrans_data["Transaction_count"].append(count)
             toptrans_data["Transaction_amount"].append(amount)
             toptrans_data["state"].append(i)
             toptrans_data["year"].append(j)
             toptrans_data["quater"].append(int(k.strip('.json')))

data5=pd.DataFrame(toptrans_data)
top_transaction=data5.sort_values(by=['state'],ascending=True)
stat5=top_transaction.state.unique()
top_transaction.replace(stat5,State_name,inplace=True)

#path 6 Top User 

path_6= r"D:\Users\Admin\Desktop\datasciene\DemoMongoDB\phonepe\pulse\data\top\user\country\india\state/"
top_user=os.listdir(path_6)
topuser_data={"state":[],'year':[],'quater':[],'Pincode':[], "RegisteredUser":[]}
for i in top_user:
  p_i=path_6+i+'/'
  top_user_yr=os.listdir(p_i)
  for j in top_user_yr:
        p_j=p_i+j+"/"
        top_user_yr_list=os.listdir(p_j)
        for k in top_user_yr_list:
          p_k=p_j+k
          top_u_data=open(p_k,"r")
          top_user_data= json.load(top_u_data)
          for l in top_user_data['data']['pincodes']:
            pincode=l['name']
            registeruser=l['registeredUsers']
            topuser_data["Pincode"].append(pincode)
            topuser_data["RegisteredUser"].append(registeruser)
            topuser_data["state"].append(i)
            topuser_data["year"].append(j)
            topuser_data["quater"].append(int(k.strip('.json')))

data6= pd.DataFrame(topuser_data)
topus_er=data6.sort_values(by=["state"],ascending=True)
stat6=topus_er.state.unique()
topus_er.replace(stat6,State_name,inplace=True)
#Migrate to sql 
engine= create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(user="admin",pw="yourpassword",host="yourdatabase",db="phonepeproject"));
Agg_trans.to_sql('Agg_trans', con=engine, if_exists="replace", chunksize=1000, index=False)
agg_user.to_sql('agg_user',con=engine, if_exists="replace", chunksize=1000, index=False)
map_trans.to_sql('map_trans',con=engine, if_exists="replace", chunksize=1000, index=False)
map_users.to_sql('map_users',con=engine, if_exists="replace", chunksize=1000, index=False)
top_transaction.to_sql('top_transaction',con=engine, if_exists="replace", chunksize=1000, index=False)
topus_er.to_sql('topus_er',con=engine, if_exists="replace", chunksize=1000, index=False)

