import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

mydb= mysql.connector.connect(
    host='database-1.cxe2c4iqum5i.ap-south-1.rds.amazonaws.com',
    user="admin",
    password="Surya0807sada",
    database='phonepeproject')
mycursor= mydb.cursor()
st.set_page_config(
   page_title="PhonePe Dashboard",
   layout="wide",
   initial_sidebar_state='expanded'
) 

years_list=[]
mycursor.execute("SELECT year from Agg_trans;")
y=mycursor.fetchall()
ye=pd.DataFrame(y,columns=["year"])
yy=ye.year.unique()
for i in yy:
  years_list.append(int(i))
  
Quat_list=[]
mycursor.execute("SELECT quater from Agg_trans;")
q=mycursor.fetchall()
qe=pd.DataFrame(q,columns=["quater"])
qq=qe.quater.unique()
for i in qq:
   Quat_list.append(int(i))

state_list=["All"]
mycursor.execute("SELECT state from Agg_trans;")
s=mycursor.fetchall()
se=pd.DataFrame(s,columns=["state"])
ss=se.state.unique()
for i in ss:
   state_list.append(i)




## Transaction Analysis
stat= 'All'
#1
def transaction_type(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT Transaction_type,sum(Transaction_count) from Agg_trans where year=%s and quater=%s group by Transaction_type;",(yr,quat))
    res1=mycursor.fetchall()
    result1=pd.DataFrame(res1,columns=["Name","transaction_count"])
    fig1=px.pie(result1,names="Name",values='transaction_count')
    fig1.update_layout(autosize=False,width=400,height=350)
    return fig1
    
  else:
    mycursor.execute("SELECT Transaction_type,sum(Transaction_count) from Agg_trans where year=%s and quater=%s and state=%s group by Transaction_type;",(yr,quat,state))
    res1=mycursor.fetchall()
    result1=pd.DataFrame(res1,columns=["Name","transaction_count"])
    fig1=px.pie(result1,names="Name",values='transaction_count')
    fig1.update_layout(autosize=False,width=300,height=250)
    return fig1

def transaction_count(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT * from Agg_trans where year=%s and quater=%s;",(yr,quat))
    res2=mycursor.fetchall()
    result2=pd.DataFrame(res2,columns=["state","year","quater","Name","transaction_count","transaction amount"])
    total_count_transaction=result2['transaction_count'].sum()
    data_card=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=total_count_transaction,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card.update_layout(width=100,height=100)
    return data_card
  else:
    mycursor.execute("SELECT * from Agg_trans where year=%s and quater=%s and state=%s;",(yr,quat,state))
    res2=mycursor.fetchall()
    result2=pd.DataFrame(res2,columns=["state","year","quater","Name","transaction_count","transaction amount"])
    total_count_transaction=result2['transaction_count'].sum()
    data_card=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=total_count_transaction,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card.update_layout(width=100,height=100)
    return data_card
 
def transaction_amount(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT * from Agg_trans where year=%s and quater=%s;",(yr,quat))
    res3=mycursor.fetchall()
    result3=pd.DataFrame(res3,columns=["state","year","quater","Name","transaction_count","transaction amount"])
    total_transaction_value=result3['transaction amount'].sum()
    data_card1=go.Figure(go.Indicator(
        mode="number",
        value=total_transaction_value,
        number={'prefix': "₹",'font':{'size':30,'color':colour}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card1.update_layout(width=100,height=100)
    return data_card1
  else:
    mycursor.execute("SELECT * from Agg_trans where year=%s and quater=%s and state=%s;",(yr,quat,state))
    res3=mycursor.fetchall()
    result3=pd.DataFrame(res3,columns=["state","year","quater","Name","transaction_count","transaction amount"])
    total_transaction_value=result3['transaction amount'].sum()
    data_card1=go.Figure(go.Indicator(
        mode="number",
        value=total_transaction_value,
        number={'prefix': "₹",'font':{'size':30,'color':colour}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card1.update_layout(width=100,height=100)
    return data_card1
 
def transaction_amount_avg(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT * from Agg_trans where year=%s and quater=%s;",(yr,quat))
    res4=mycursor.fetchall()
    result4=pd.DataFrame(res4,columns=["state","year","quater","Name","transaction_count","transaction amount"])
    total_transaction_avg=(result4['transaction amount'].sum()/result4['transaction_count'].sum())
    data_card2=go.Figure(go.Indicator(
        mode="number",
        value=total_transaction_avg,
        number={'prefix': "₹",'font':{'size':30,'color':colour}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card2.update_layout(width=100,height=100)
    return data_card2
  else:
    mycursor.execute("SELECT * from Agg_trans where year=%s and quater=%s and state=%s;",(yr,quat,state))
    res4=mycursor.fetchall()
    result4=pd.DataFrame(res4,columns=["state","year","quater","Name","transaction_count","transaction amount"])
    total_transaction_avg=(result4['transaction amount'].sum()/result4['transaction_count'].sum())
    data_card2=go.Figure(go.Indicator(
        mode="number",
        value=total_transaction_avg,
        number={'prefix': "₹",'font':{'size':30,'color':colour}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card2.update_layout(width=100,height=100)
    return data_card2
 
def top_10_transaction_state(yr,quat,colour):
    mycursor.execute("SELECT state,sum(Transaction_count) from Agg_trans where year=%s and quater=%s group by state order by sum(Transaction_count) desc limit 10;",(yr,quat))
    res5=mycursor.fetchall()
    result5=pd.DataFrame(res5,columns=["state","transaction count"])
    fig2=px.bar(result5,x='state',y='transaction count')
    fig2.update_traces(marker_color=colour)
    fig2.update_layout(width=400,height=250)
    return fig2
def transaction_district_wise(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT District,sum(Transaction_count) from map_trans  where year=%s and quater=%s group by state,District order by sum(Transaction_count) desc limit 10;",(yr,quat))
    res6=mycursor.fetchall()
    result6=pd.DataFrame(res6,columns=["District","transaction_count"])
    fig3=px.bar(result6,x='District',y='transaction_count')
    fig3.update_traces(marker_color=colour)
    fig3.update_layout(width=400,height=250)
    return fig3

  else:
    mycursor.execute("SELECT District,sum(Transaction_count) from map_trans  where year=%s and quater=%s and state =%s group by District order by sum(Transaction_count) desc limit 10;",(yr,quat,state))
    res6=mycursor.fetchall()
    result6=pd.DataFrame(res6,columns=["District","transaction_count"])
    fig3=px.bar(result6,x='District',y='transaction_count')
    fig3.update_traces(marker_color=colour)
    fig3.update_layout(width=400,height=250)
    return fig3
def transaction_postalcode_wise(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT postalcode,sum(Transaction_count) from top_transaction  where year=%s and quater=%s group by state,postalcode order by sum(Transaction_count) desc limit 10;",(yr,quat))
    res7=mycursor.fetchall()
    result7=pd.DataFrame(res7,columns=["PostalCode","transaction_count"])
    return result7

  else:
    mycursor.execute("SELECT postalcode,sum(Transaction_count) from top_transaction  where year=%s and quater=%s and state =%s group by postalcode order by sum(Transaction_count) desc limit 10;",(yr,quat,state))
    res7=mycursor.fetchall()
    result7=pd.DataFrame(res7,columns=["PostalCode","transaction_count"])
    return result7
  
#8 Map
def Map_display(yr,quat,colour):
  mycursor.execute("SELECT state,sum(Transaction_count),sum(Transaction_amount),(sum(Transaction_amount)/sum(Transaction_count)) from Agg_trans WHERE year = %s AND quater = %s	group by state  order by state desc;",(yr,quat))
  res8=mycursor.fetchall()
  result8=pd.DataFrame(res8,columns=["state","transaction_count","transaction amount",'Avg_in_rs'])
  result8['transaction amount'] = '₹'+ ' ' +result8['transaction amount'].astype(str)
  fig4 = px.choropleth(result8,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color="Avg_in_rs",
                    range_color=(500,4000),
                    hover_data={"transaction_count","transaction amount"},
                    color_continuous_scale=colour
                   )
  fig4.update_geos(fitbounds="locations", visible=False)
  fig4.update_layout(template="plotly_dark")
  return fig4

#
#9 
def lowest_10_transaction_state(yr,quat,colour):
    mycursor.execute("SELECT state,sum(Transaction_count) from Agg_trans where year=%s and quater=%s group by state order by sum(Transaction_count) asc limit 10;",(yr,quat))
    res9=mycursor.fetchall()
    result9=pd.DataFrame(res9,columns=["state","transaction count"])
    fig5=px.bar(result9,x='state',y='transaction count')
    fig5.update_traces(marker_color=colour)
    fig5.update_layout(width=400,height=250)
    return fig5  
def transaction_district_lowest (yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT District,sum(Transaction_count) from map_trans  where year=%s and quater=%s group by state,District order by sum(Transaction_count) Asc limit 7;",(yr,quat))
    res10=mycursor.fetchall()
    result10=pd.DataFrame(res10,columns=["District","transaction_count"])
    return result10

  else:
    mycursor.execute("SELECT District,sum(Transaction_count) from map_trans  where year=%s and quater=%s and state =%s group by District order by sum(Transaction_count) Asc limit 7;",(yr,quat,state))
    res10=mycursor.fetchall()
    result10=pd.DataFrame(res10,columns=["District","transaction_count"])
    return result10
  
#USER ANALYSIS
def user_transactioncount(yr, quat, state,colour):
  if stat==state:
    mycursor.execute("SELECT Transaction_count from agg_user where year=%s and quater=%s;",(yr,quat))
    res11=mycursor.fetchall()
    result11=pd.DataFrame(res11,columns=["transaction_count"])
    user_count_transaction=result11['transaction_count'].sum()
    data_card6=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=user_count_transaction,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card6.update_layout(width=100,height=100)
    return data_card6
  else:
    mycursor.execute("SELECT Transaction_count from agg_user where year=%s and quater=%s and state=%s;",(yr,quat,state))
    res11=mycursor.fetchall()
    result11=pd.DataFrame(res11,columns=["transaction_count"])
    user_count_transaction=result11['transaction_count'].sum()
    data_card6=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=user_count_transaction,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card6.update_layout(width=100,height=100)
    return data_card6

def user_appopen(yr, quat, state,colour):
  if stat==state:
    mycursor.execute("SELECT AppOpens from map_users where year=%s and quater=%s;",(yr,quat))
    res12=mycursor.fetchall()
    result12=pd.DataFrame(res12,columns=["appopens"])
    user_appopen=result12['appopens'].sum()
    data_card7=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=user_appopen,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card7.update_layout(width=100,height=100)
    return data_card7
  else:
    mycursor.execute("SELECT AppOpens from map_users where year=%s and quater=%s and state=%s;",(yr,quat,state))
    res12=mycursor.fetchall()
    result12=pd.DataFrame(res12,columns=["AppOpens"])
    user_appopen=result12['AppOpens'].sum()
    data_card7=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=user_appopen,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    data_card7.update_layout(width=100,height=100)
    return data_card7
def pincode(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT Pincode,sum(RegisteredUser) from topus_er  where year=%s and quater=%s group by pincode order by sum(RegisteredUser) desc limit 10;",(yr,quat))
    res13=mycursor.fetchall()
    result13=pd.DataFrame(res13,columns=["Pincode","RegisteredUser"])
    return result13

  else:
    mycursor.execute("SELECT Pincode,sum(RegisteredUser) from topus_er where year=%s and quater=%s and state =%s group by pincode order by sum(RegisteredUser) desc limit 10;",(yr,quat,state))
    res13=mycursor.fetchall()
    result13=pd.DataFrame(res13,columns=["Pincode","RegisteredUser"])
    return result13
def brands(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT Brands,sum(Transaction_count) from agg_user where year=%s and quater=%s group by Brands order by sum(transaction_count) desc limit 5;",(yr,quat))
    res14=mycursor.fetchall()
    result14=pd.DataFrame(res14,columns=["Brand","transaction_count"])
    fig14=px.pie(result14,names="Brand",values='transaction_count')
    fig14.update_layout(autosize=False,width=300,height=350)
    return fig14
    
  else:
    mycursor.execute("SELECT Brands,sum(Transaction_count) from agg_user where year=%s and quater=%s and state=%s group by Brands order by sum(transaction_count) desc limit 5;",(yr,quat,state))
    res14=mycursor.fetchall()
    result14=pd.DataFrame(res14,columns=["Brands","transaction_count"])
    fig14=px.pie(result14,names="Brands",values='transaction_count')
    fig14.update_layout(autosize=False,width=300,height=350)
    return fig14
  
def state_register(yr,quat,colour):
    mycursor.execute("SELECT state,sum(RegisteredUser) from map_users where year=%s and quater=%s group by state order by sum(RegisteredUser) desc limit 10;",(yr,quat))
    res15=mycursor.fetchall()
    result15=pd.DataFrame(res15,columns=["state","user_count"])
    fig15=px.bar(result15,x='state',y='user_count')
    fig15.update_traces(marker_color=colour)
    fig15.update_layout(width=400,height=250)
    return fig15
def state_appopen(yr,quat,colour):
    mycursor.execute("SELECT state,sum(AppOpens) from map_users where year=%s and quater=%s group by state order by sum(AppOpens) desc limit 10;",(yr,quat))
    res16=mycursor.fetchall()
    result16=pd.DataFrame(res16,columns=["state","app_count"])
    fig16=px.bar(result16,x='state',y='app_count')
    fig16.update_traces(marker_color=colour)
    fig16.update_layout(width=400,height=250)
    return fig16
def district_user(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT District,sum(RegisteredUser) from map_users  where year=%s and quater=%s group by District order by sum(RegisteredUser) desc limit 10;",(yr,quat))
    res17=mycursor.fetchall()
    result17=pd.DataFrame(res17,columns=["District","User"])
    fig17=px.bar(result17,x='District',y='User')
    fig17.update_traces(marker_color=colour)
    fig17.update_layout(width=400,height=250)
    return fig17

  else:
    mycursor.execute("SELECT District,sum(RegisteredUser) from map_users  where year=%s and quater=%s and state =%s group by District order by sum(RegisteredUser) desc limit 10;",(yr,quat,state))
    res17=mycursor.fetchall()
    result17=pd.DataFrame(res17,columns=["District","transaction_count"])
    fig17=px.bar(result17,x='District',y='transaction_count')
    fig17.update_traces(marker_color=colour)
    fig17.update_layout(width=400,height=250)
    return fig17
def district_open(yr,quat,state,colour):
  if stat==state:
    mycursor.execute("SELECT District,sum(AppOpens) from map_users  where year=%s and quater=%s group by District order by sum(AppOpens) desc limit 10;",(yr,quat))
    res18=mycursor.fetchall()
    result18=pd.DataFrame(res18,columns=["District","appopen"])
    fig18=px.bar(result18,x='District',y='appopen')
    fig18.update_traces(marker_color=colour)
    fig18.update_layout(width=400,height=250)
    return fig18

  else:
    mycursor.execute("SELECT District,sum(AppOpens) from map_users  where year=%s and quater=%s and state =%s group by District order by sum(AppOpens) desc limit 10;",(yr,quat,state))
    res18=mycursor.fetchall()
    result18=pd.DataFrame(res18,columns=["District","appopen"])
    fig18=px.bar(result18,x='District',y='appopen')
    fig18.update_traces(marker_color=colour)
    fig18.update_layout(width=400,height=250)
    return fig18
  
def low_state_register(yr,quat,colour):
    mycursor.execute("SELECT state,sum(RegisteredUser) from map_users where year=%s and quater=%s group by state order by sum(RegisteredUser) Asc limit 10;",(yr,quat))
    res19=mycursor.fetchall()
    result19=pd.DataFrame(res19,columns=["state","user_count"])
    fig19=px.bar(result19,x='state',y='user_count')
    fig19.update_traces(marker_color=colour)
    fig19.update_layout(width=400,height=250)
    return fig19
  
def Map_user(yr,quat,colour):
  mycursor.execute("SELECT state,sum(RegisteredUser),sum(AppOpens) from map_users WHERE year = %s AND quater = %s	group by state  order by state desc;",(yr,quat))
  res20=mycursor.fetchall()
  result20=pd.DataFrame(res20,columns=["state","RegistereUser","AppOpens"])
  fig20 = px.choropleth(result20,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    hover_data={"RegistereUser","AppOpens"}
                                   )
  fig20.update_geos(fitbounds="locations", visible=False)
  fig20.update_layout(template="plotly_dark")
  fig20.update_traces(colorscale=colour)
  return fig20
   

page = st.sidebar.selectbox("Select", ["About","Transaction", "User"], index=0)

if page=="About":
  st.title("Welcome to the PhonePe Data Visualization and Exploration tool")
  if st.button("Overview"):
    st.write(''' The Phonepe Pulse Data Visualization and Exploration tool is a user-friendly
             web application built to visualize and explore data 
             elated to transactions processed through Phonepe. 
             Leveraging the power of Streamlit and Plotly, 
             this tool provides an interactive and intuitive interface 
             for users to gain insights into transaction data and trends.''')
    st.header("Key Features")
    st.markdown(''' 
                - Data Visualization
                - User-Friendly Interface
                - Customization
                - Insightful Analytics''')
    st.header("Technology List ")
    st.markdown(''' 
                - Python
                - Plotly
                - MYSQL(AWS)
                - Streamlit''')
    st.header("Tutorial")
    st.write('''To start exploring transaction data with 
             the Phonepe Pulse Data Visualization and Exploration tool, 
             simply navigate through the various visualization options 
             available in the sidebar menu. Use the provided filters to 
             customize your analysis and gain valuable insights into 
             transaction trends and patterns.''')
    
    
    
if page=="Transaction":
  with st.sidebar:
   st.title('PhonePe Dashboard')
   selected_year=st.selectbox('select a year',years_list, index=0)
   selected_Quater=st.selectbox('select a quater',Quat_list, index=0)
   selected_state=st.selectbox('select a state',state_list, index=0)
   color_theme_list = ['blue', 'tan', 'green', 'HotPink', 'Indigo', 'steelblue', 'red', 'orange', 'aqua',"Reds"]
   selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
   query_list=["Count","Amount","Average Amount","Top State","Top District","Category","Postalcode","Lowest State","Lowest District","Map"]
   Query=st.selectbox('select the question',query_list)
  
  col=st.columns((1.5,3.5,2),gap='medium')
  with col[2]:
    st.markdown("### category")
    graph1=transaction_type(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.plotly_chart(graph1)
    st.markdown("Top Transaction by postalcode")
    graph7=transaction_postalcode_wise(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.table(graph7)
  with col[1]:
    st.markdown("Top Transaction by State")
    graph5=top_10_transaction_state(selected_year,selected_Quater,selected_color_theme)
    st.plotly_chart(graph5)
    st.markdown("Top Transaction by District")
    graph6=transaction_district_wise(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.plotly_chart(graph6)
    st.markdown("Lowest Transaction by state")
    graph9=lowest_10_transaction_state(selected_year,selected_Quater,selected_color_theme)
    st.plotly_chart(graph9)
  with col[0]:
    st.markdown('Transaction count')
    graph2=transaction_count(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.plotly_chart(graph2)
    st.markdown('Transaction Amount')
    graph3=transaction_amount(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.plotly_chart(graph3)
    st.markdown('Average Transaction Amount per Transaction')
    graph4=transaction_amount_avg(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.plotly_chart(graph4)
    st.markdown("Lowest Transaction by District")
    graph10=transaction_district_lowest(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.table(graph10)
  st.title('Transaction Map Analysis')
  col1=st.columns((.6,3.5,2),gap='small')
  with col1[0]:
     color_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
     option4=st.selectbox('Pick a Colour',color_list, index=0)
  graph8=Map_display(selected_year,selected_Quater,option4)
  st.plotly_chart(graph8)
  

if page=="User":
  with st.sidebar:
   st.title('PhonePe Dashboard')
   selected_year=st.selectbox('select a year',years_list, index=0)
   selected_Quater=st.selectbox('select a quater',Quat_list, index=0)
   selected_state=st.selectbox('select a state',state_list, index=0)
   color_theme_list = ['blue', 'tan', 'green', 'HotPink', 'Indigo', 'steelblue', 'red', 'orange', 'aqua',"Reds"]
   selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
   query_list=["User Count","AppOpen Count","Top user State","Top AppOpens State","Brands","Pincode","Lowest state appopen","Top district user","Top District AppOpen","Map"]
   Query=st.selectbox('select the question',query_list)
   
  col=st.columns((1.5,3.5,2),gap='medium') 
  with col[0]:
    st.markdown('Transaction user count')
    graph11= user_transactioncount(selected_year,selected_Quater, selected_state,selected_color_theme)
    st.plotly_chart(graph11)
    st.markdown('AppOpens count')
    graph12=user_appopen(selected_year,selected_Quater, selected_state,selected_color_theme)
    st.plotly_chart(graph12)
    st.markdown("Pincode by User")
    graph13=pincode(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.table(graph13)
    
  with col[2]:
    st.markdown("### Brands")
    graph14=brands(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.plotly_chart(graph14)
    st.markdown("Top Registered appopen by District")
    graph18=district_open(selected_year,selected_Quater,selected_state,selected_color_theme)
    st.plotly_chart(graph18)
  with col[1]:
     st.markdown("Top User by State")
     graph15=state_register(selected_year,selected_Quater,selected_color_theme)
     st.plotly_chart(graph15)
     st.markdown("Lowest User by State")
     graph19=low_state_register(selected_year,selected_Quater,selected_color_theme)
     st.plotly_chart(graph19)
     st.markdown("Top Appopen by State")
     graph16=state_appopen(selected_year,selected_Quater,selected_color_theme)
     st.plotly_chart(graph16)
     st.markdown("Top User by District")
     graph17=district_user(selected_year,selected_Quater,selected_state,selected_color_theme)
     st.plotly_chart(graph17)
  st.title('User Map Analysis')
  col4=st.columns((.6,3.5,2),gap='small')
  with col4[0]:
     color_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
     option5=st.selectbox('Pick a Colour',color_list, index=0)
  graph20=Map_user(selected_year,selected_Quater,option5)
  st.plotly_chart(graph20)

 
