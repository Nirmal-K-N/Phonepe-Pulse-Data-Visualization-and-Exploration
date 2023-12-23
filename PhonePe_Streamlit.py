import pandas as pd
import json
import os
from pprint import pprint 
import mysql.connector
from dash import Dash,dcc,html,dash_table
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import plotly.express as px
import altair as alt
import plotly.graph_objects as go

# MYSql Connection
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Nirmal9699',
    database = 'phonepe_pulse_data_visualization')
cur = db.cursor()
db.commit()

with st.sidebar:
    selected = option_menu("Main Menu", ["Home","Questions","Geo Visualisation"], 
                icons=['house','question','map'], menu_icon="cast", default_index=0)
         
if selected == "Home":
    st.title("Phonepe Pulse Data Visualization and Exploration:")
    st.title("A User-Friendly Tool Using Streamlit and Plotly")
    st.divider()
    st.write("""**The result of this project will be a comprehensive and user-friendly solution for extracting, transforming, and visualizing data from the Phonepe pulse Github repository.**""")
    col1,col2 = st.columns(2)
    
    with col1:
        st.subheader(":blue[Skills take away From This Project]")
        st.divider()
        st.text("> Data extraction and processing,")
        st.text("> Database management,")
        st.text("> Visualization and dashboard creation,")
        st.text("> Geo visualization,")
        st.text("> Dynamic updating, &")
        st.text("> Project development and deployment&")
    
    with col2:
        st.subheader(":blue[Technologies Used]")
        st.divider()
        st.text("> Github Cloning,")
        st.text("> Python,")
        st.text("> Pandas,")
        st.text("> MySQL,")
        st.text("> mysql-connector-python,")
        st.text("> Streamlit, &")
        st.text("> Plotly")

    st.subheader('',divider='orange')

elif selected == "Questions":
    t1,t2,t3,t4,t5,t6,t7,t8,t9,t10 = st.tabs(['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10'])

    with t1:
        st.write(":orange[1. Show the Total Transaction of the chosen State, Year wise]")    
        def qust_1(s):
            sql = """SELECT state State, year Year, ROUND(sum(Transaction_Amount)) Transaction_Year 
                FROM phonepe_pulse_data_visualization.agg_trans  
                WHERE state = %s 
                GROUP BY year"""
            cur.execute(sql,(s,))
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'Year','Transaction_Amount_By_Year']).reset_index(drop=True)
            data_df.index += 1
            return data_df

        sql = """select distinct State from agg_trans"""
        cur.execute(sql)
        states = cur.fetchall()
        states = [item[0] for item in states]
        option = st.selectbox('Select State',states, index=None, placeholder="State",key='t1_state')
        st.write('Your selected state:', option)
        Q1 = qust_1(option)
        
        # Plotting the line chart
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(Q1['Year'], Q1['Transaction_Amount_By_Year'], marker='o', linestyle='-')
        # Adding labels and title
        ax.set_title(f'Transaction Amount by Year in {option}',fontweight='bold', fontsize=18)
        ax.set_xlabel('Year', fontweight='bold',fontsize = 14)
        ax.set_ylabel('Transaction Amount', fontweight='bold',fontsize = 14)
        # Display the chart in Streamlit
        if option is not None:
            st.pyplot(fig)
        else:
            st.empty()
    
    with t2:
        st.write(":orange[2. Show Top 8 States w.r.t. Transaction Count]")
        def qust_2():
            sql = """SELECT state, SUM(Transaction_Count) AS Transaction_Count_By_State 
                    FROM phonepe_pulse_data_visualization.agg_trans 
                    GROUP BY state 
                    ORDER BY Transaction_Count_By_State DESC 
                    LIMIT 8"""
            cur.execute(sql)
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'Transaction_Count_By_State']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        Q2 = qust_2()

        # Plotting the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(Q2['State'], Q2['Transaction_Count_By_State'], color='#026ab5')
        # Adding labels and title
        ax.set_xlabel('State',fontweight='bold',fontsize = 14)
        ax.set_ylabel('Transaction Count',fontweight='bold',fontsize = 14)
        ax.set_title('Transaction Count by State',fontweight='bold', fontsize=18)
        # Display the chart in Streamlit
        st.pyplot(fig)

    with t3:
        st.write(":orange[3. Show Top 3 Brands w.r.t. Percentage Users, Quarter wise for selected State and Year]")
        def qust_3(s,y):
            sql = """WITH SQ AS ( SELECT State,Quarter,Brand,ROUND(User_Percentage * 100) AS Percentage,
                    ROW_NUMBER() OVER (PARTITION BY Quarter ORDER BY User_Percentage DESC) AS RowNum
                    FROM phonepe_pulse_data_visualization.agg_user
                    WHERE State = %s AND Year = %s)
                    SELECT State,Quarter,Brand,Percentage
                    FROM SQ
                    WHERE RowNum <= 3;"""
            cur.execute(sql,(s,y))
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'Quarter','Brand','Percentage']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        sql1 = """select distinct State from agg_user"""
        sql2 = """select distinct Year from agg_user"""
        cur.execute(sql1)
        states = cur.fetchall()
        cur.execute(sql2)
        years = cur.fetchall()

        states = [item[0] for item in states]
        years = [item[0] for item in years]

        option1 = st.selectbox('Select State', states, index=None, placeholder="State",key='t3_state')
        option2 = st.selectbox('Select Year', years, index=None, placeholder="Year",key='t3_year')

        st.write("Your selected state:",option1)
        st.write("Your selected year:",option2)

        Q3 = qust_3(option1,option2)
        
        # Plotting the grouped bar chart
        fig, ax = plt.subplots(figsize=(12,8))

        sns.barplot(x=Q3['Quarter'], y=Q3['Percentage'], hue=Q3['Brand'], data=Q3, palette='viridis')
        # Adding labels and title
        ax.set_xlabel('Quarter',fontweight='bold',fontsize = 14)
        ax.set_ylabel('Percentage',fontweight='bold',fontsize = 14)
        ax.set_title(f'Brand Percentage Distribution by Quarter in {option1} in {option2}',fontweight='bold',fontsize = 18)
        # Display the chart in Streamlit
        if option1 is not None and option2 is not None:
            st.pyplot(fig)
        else:
            st.empty()

    with t4:
        st.write(":orange[4. Show the Top Region w.r.t. Amount for the selected State and Year]")
        def qust_4(s,y):
            sql = """WITH SQ AS (
                    SELECT State, Quarter, Year, Region, Amount,
                    ROW_NUMBER() OVER (PARTITION BY Year, Quarter
                    ORDER BY Amount DESC) AS RowNum
                    FROM phonepe_pulse_data_visualization.map_trans
                    WHERE State = %s
                    )
                    SELECT State, Quarter, Year, Region, Amount
                    FROM SQ
                    WHERE RowNum = 1 and YEAR = %s"""
            cur.execute(sql,(s,y))
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'Quarter','Year','Region','Amount']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        sql1 = """select distinct State from map_trans"""
        sql2 = """select distinct Year from map_trans"""
        cur.execute(sql1)
        states = cur.fetchall()
        cur.execute(sql2)
        years = cur.fetchall()

        states = [item[0] for item in states]
        years = [item[0] for item in years]

        option1 = st.selectbox('Select State', states, index=None, placeholder="State",key='t4_state')
        option2 = st.selectbox('Select Year', years, index=None, placeholder="Year",key='t4_year')

        st.write("Your selected state:",option1)
        st.write("Your selected state:",option2)

        Q4 = qust_4(option1,option2)

        # Plotly chart
        custom_color_scale = px.colors.qualitative.Set2
        fig = px.area(Q4, x='Quarter', y='Amount', color='Region', title=f'Amount by Quarter for {option1} in {option2}',
                      color_discrete_sequence=custom_color_scale,)
        # Add grid
        fig.update_layout(
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#2e2d2d'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#2e2d2d'))
        
        if option1 is not None and option2 is not None:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.empty()

    with t5:
        st.write(":orange[5. Show Top District & Count by Amount, Year wise for the selected State]")
        def qust_5(s):
            sql = """WITH SQ AS (
                    SELECT State, Year, District, sum(Count) AS Count, sum(Amount) AS Amount,
                    ROW_NUMBER() OVER (PARTITION BY State, Year ORDER BY sum(Amount) DESC) AS RowNum
                    FROM phonepe_pulse_data_visualization.top_trans_dis 
                    GROUP BY State,Year, District)
                    SELECT State, District, Year, Count, Amount
                    FROM SQ
                    WHERE State = %s and RowNum = 1"""
            cur.execute(sql,(s,))
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'District','Year','Count','Amount']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        sql = """select distinct State from top_trans_dis"""
        cur.execute(sql)
        states = cur.fetchall()
        states = [item[0] for item in states]
        option = st.selectbox('Select State',states, index=None, placeholder="State",key='t5_state')
        st.write('Your selected state:', option)
        Q5 = qust_5(option)
        
        Q5['Count'] = Q5['Count'].astype(float)
        Q5['Amount'] = Q5['Amount'].astype(float)

        fig = go.Figure()

        # Add left Y-axis
        fig.add_trace(go.Bar(
            x=Q5['Year'],
            y=Q5['Count'],
            name='Count',
            marker_color='blue',
            offsetgroup=1  # Use offsetgroup to place bars side by side
        ))

        # Add right Y-axis
        fig.add_trace(go.Bar(
            x=Q5['Year'],
            y=Q5['Amount'],
            name='Amount',
            marker_color='orange',
            offsetgroup=2,  # Use offsetgroup to place bars side by side
            yaxis='y2'
        ))

        # Update layout to include two Y-axes
        fig.update_layout(
            title=f'Count and Amount by Year for {option}',
            yaxis=dict(title='Count', side='left', showgrid=False),
            yaxis2=dict(title='Amount', overlaying='y', side='right', showgrid=False),
            xaxis=dict(title='Year'),
            barmode='group',
            bargap=0.1,  # Adjust the bargap as needed
            legend=dict(x=0, y=1.0, traceorder='normal', orientation='v')
        )

        # Show the plot
        if option is not None:
            st.plotly_chart(fig)
        else:
            st.empty()
        
        

    with t6:
        st.write(":orange[6. Show Top 6th to 8th Region w.r.t. to Count, Year wise for the selected State]")
        def qust_6(s):
            sql = """WITH SQ AS (
                    SELECT State, Year, Region, SUM(Count) AS Count,
                    ROW_NUMBER() OVER (PARTITION BY Year ORDER BY SUM(Count) DESC) AS RowNum
                    FROM phonepe_pulse_data_visualization.map_user
                    WHERE State = %s
                    GROUP BY State, Year, Region)
                    SELECT State, Year, RowNum, Region, Count
                    FROM SQ 
                    WHERE RowNum > 5 AND RowNum <= 8"""
            cur.execute(sql,(s,))
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'Year','RowNum','Region','Count']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        sql = """select distinct State from map_user"""
        cur.execute(sql)
        states = cur.fetchall()
        states = [item[0] for item in states]
        option = st.selectbox('Select State',states, index=None, placeholder="State",key='t6_state')
        st.write('Your selected state:', option)
        Q6 = qust_6(option)

        # Streamlit app
        if option is not None:
            def main():
                st.subheader('Users Count in Top 6-8th Position')
                # Create a line chart using Plotly Express
                fig = px.line(Q6, x='Year', y='Count', color='Region', line_group='Region',
                            labels={'Value': 'Count'})
                # Update the layout to increase the graph size
                fig.update_layout(width=900, height=700)
                # Display the chart using Streamlit
                st.plotly_chart(fig)
                # Display the data table
                st.write("Data Table:")
                st.table(Q6)
            # Run the Streamlit app
            main()
        else:
            st.empty()
        

    with t7:
        st.write(":orange[7. Display complete details from Top Transaction Pincode]")
        def qust_7():
            sql = """SELECT * FROM phonepe_pulse_data_visualization.top_trans_pin"""
            cur.execute(sql)
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'Year','Quarter','Pincode','Amount','Count']).reset_index(drop=True)
            data_df.index += 1
            return data_df
       
        Q7 = qust_7()
        
        #Inserting search bar
        def search_table():
            #st.title("Search Bar for Table")
            search_term = st.text_input("Search by Pincode:", "")
            # Filter the dataframe based on the search term
            filtered_df = Q7[Q7['Pincode'].astype(str).str.contains(search_term)]
            if not search_term:
                st.table(Q7)
            else:
                if not filtered_df.empty:
                    st.table(filtered_df)
                else:
                    st.error("Data Not Found !!!")
        search_table()

    with t8:
        st.write(":orange[8. Show Top 10 Districts w.r.t. Count]")
        def qust_8():
            sql = """SELECT CONCAT(District,", ",State) AS Place, Round(Count)
                    FROM phonepe_pulse_data_visualization.top_user_dis
                    WHERE Year = 2023 and Quarter = 3
                    ORDER BY Count DESC
                    LIMIT 10;"""
            cur.execute(sql)
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['Place','Count']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        Q8 = qust_8()

        # Plotting the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(Q8['Place'], Q8['Count'])
        # Adding labels and title
        ax.set_xlabel('District',fontweight='bold',fontsize = 14)
        # Rotate x-axis labels by 45 degrees
        plt.xticks(rotation=45, ha='right')
        ax.set_ylabel('Count',fontweight='bold',fontsize = 14)
        ax.set_title('Top 10 Districts in India by Count',fontweight='bold', fontsize=18)
        # Display the chart in Streamlit
        st.pyplot(fig)

    with t9:
        st.write(":orange[9. Show Pincode of each State which has less Count]")
        def qust_9():
            sql = """WITH SQ as (
                    SELECT State, Pincode, Round(Count) AS Count, Year, Quarter,
                    ROW_NUMBER() OVER (PARTITION BY State ORDER BY Count) AS RowNum
                    FROM phonepe_pulse_data_visualization.top_user_pin
                    WHERE Year = 2023 and Quarter = 3)
                    SELECT State, Pincode, Count
                    FROM SQ
                    WHERE RowNum = 1"""
            cur.execute(sql)
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State', 'Pincode','Count']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        Q9 = qust_9()
        Q9['Count'] = Q9['Count'].astype(int)

        fig = px.choropleth(
                Q9,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Count',
                hover_data=['Pincode', 'Count'],
                color_continuous_scale='Viridis'
            )

        fig.update_geos(
            visible=False,
            projection=dict(
                type='conic conformal',
                parallels=[12.472944444, 35.172805555556],
                rotation={'lat': 24, 'lon': 80}
            ),
            lonaxis={'range': [68, 98]},
            lataxis={'range': [6, 38]}
        )

        fig.update_layout(
            title=dict(
                text="*Least Users By Pincode In Each State*",
                xanchor='center',
                x=0.4,
                yref='paper',
                yanchor='top',
                y=1,
                pad={'b': 10},
                font=dict(
                size=20)),
            margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
            height=650,
            width=700
        )

        st.plotly_chart(fig)

    with t10:
        st.write(":orange[10. Show States in Percentage w.r.t. Amount]")
        def qust_10():
            sql = """SELECT State, ROUND((Sum(Amount)/Total_Amount),2)*100 AS Percentage
                    FROM (SELECT Sum(Amount) AS Total_Amount 
                    FROM phonepe_pulse_data_visualization.top_trans_dis
                    WHERE Year = 2023) AS SQ
                    JOIN phonepe_pulse_data_visualization.top_trans_dis AS M
                    GROUP BY State, Total_Amount
                    ORDER BY Percentage DESC
                    LIMIT 15"""
            cur.execute(sql)
            data = cur.fetchall()
            data_df = pd.DataFrame(data, columns=['State','Percentage']).reset_index(drop=True)
            data_df.index += 1
            return data_df
        
        Q10 = qust_10()

        # Plotting the tree map
        fig = px.treemap(Q10, path=['State'], values='Percentage', title='State Percentages',
                         hover_data=['Percentage','State'], color='Percentage')
        # Display the chart in Streamlit
        st.plotly_chart(fig)

if selected == "Geo Visualisation":
    def gv():
        sql = """SELECT State, Sum(Count) as T_Count
                FROM phonepe_pulse_data_visualization.map_user
                WHERE Year = 2023 and Quarter = 3
                GROUP BY State
                ORDER BY T_Count DESC;"""
        cur.execute(sql)
        data = cur.fetchall()
        data_df = pd.DataFrame(data, columns=['State', 'Total_Count']).reset_index(drop=True)
        data_df.index += 1
        return data_df

    GV = gv()
    GV['Total_Count'] = GV['Total_Count'].astype(int)
    df=GV
    print(df.info())

    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Total_Count',
        color_continuous_scale='Reds'
    )

    fig.update_geos(
        visible=False,
        projection=dict(
            type='conic conformal',
            parallels=[12.472944444, 35.172805555556],
            rotation={'lat': 24, 'lon': 80}
        ),
        lonaxis={'range': [68, 98]},
        lataxis={'range': [6, 38]}
    )

    fig.update_layout(
        title=dict(
            text="*Users By State in India*",
            xanchor='center',
            x=0.4,
            yref='paper',
            yanchor='top',
            y=1,
            pad={'b': 10},
            font=dict(
            size=20)),
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        height=650,
        width=700
    )

    st.plotly_chart(fig)