import pandas as pd 
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title= "CARS24 DASHBOARD" ,
                page_icon= " Plots :" ,
                layout= "wide")

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://feeds.abplive.com/onecms/images/uploaded-images/2022/08/25/5523d0a239ac8132bf8cdd31dbd2b0e51661436955376456_original.jpg?impolicy=abp_cdn&amp;imwidth=720");
             background-attachment: fixed;
	     background-position:75%;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()



cars = pd.read_csv("carsEDA.csv")

st.dataframe(cars)

#-------SIDEBAR---------
city = st.sidebar.multiselect(
     "Select the City :", 
     options= cars["City"].unique()

)

Transmission = st.sidebar.multiselect(
     "Select the Transmission :", 
     options= cars["Transmission"].unique()
)

fuel = st.sidebar.multiselect(
     "Select the fuel :", 
     options= cars["Fuel_Type"].unique()
)

owner = st.sidebar.multiselect(
     "Select the Owner :", 
     options= cars["Owner"].unique()
)

Company = st.sidebar.multiselect(
     "Select the Company :",
     options= cars["Company"].unique()
)


cars_selection = cars.query(
    "City == @city & Transmission == @Transmission & Fuel_Type == @fuel & Owner == @owner & Company == @Company"
)

#--------MAINPAGE---------
st.title("Plots: CARS24 DASHBOARD")
st.markdown("##")

#TOP KPI'S
Max_price = (cars["Sales_Price"].max())
average_Price = round(cars["Sales_Price"].mean(),1)
Average_Km = round(cars["KM_Driven"].mean(),1)

left_column , middle_column , right_column = st.columns(3)
with left_column:
    st.subheader("Maximum Price :")
    st.subheader(f"Rs {Max_price:,}")
with middle_column:
    st.subheader("Average Price :")
    st.subheader(f"Rs {average_Price:,}")
with right_column:
    st.subheader("Average_KM_DRIVEN:")
    st.subheader( f"km{Average_Km:,}")

st.markdown("____")


#--------- Charts------------

fig_1 = px.bar(
    cars , x = "Sales_Price", y = "Fuel_Type",
    orientation="h",
    title="<b>Fuel Vs Selling_Price</b>",

    color_discrete_sequence=["#0083B8"]*len(cars)
)



fig_2 = px.pie(cars , values = "Sales_Price" ,names = "Owner", title= "<b>Contribution of owner type</b>")

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_1 , use_container_width= True)
right_column.plotly_chart(fig_2 , use_container_width= True)

fig = px.scatter (cars , x= "Sales_Price" , y = "EMI(₹)" , color= "Company", symbol= "Fuel_Type"
, title="<b>Correlation between Variables</b>")

st.plotly_chart(fig)

fig_3 = px.box(cars ,x='Company',y='Sales_Price',  title= "<b>Company and Price</b>")
st.plotly_chart(fig_3)

fig_4 = px.violin(cars , x = "Company" , y = "KM_Driven" , title = "<b>Company and km_driven</b>" , orientation= "v")


fig_5= px.histogram(cars , x = "Year" , y = "Sales_Price",
                 title= "Year vs Price" )
                 

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_4 , use_container_width= True)
right_column.plotly_chart(fig_5 , use_container_width= True)

# ----------- HIDE STREAMLIT STYLE--------------
hide_st_style = """ 
               <style>
               #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                </style>
                """
st.markdown(hide_st_style , unsafe_allow_html = True)               