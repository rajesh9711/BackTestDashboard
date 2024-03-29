import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import statistics as sta
import matplotlib.colors as mcolors
import base64
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import requests

# Configure default Streamlit theme
st.set_page_config(

    page_title="Multyfi Backtester",
    page_icon="🗓️",
    layout="wide",
)

import requests
import base64
import re
from PIL import Image
import io

url = 'https://drive.google.com/file/d/1-ABYp-BzXjjZTmkMGzjJz7jV1MHIfHH-/view?usp=sharing'

# Extract the file ID from the URL
file_id_match = re.match(r'^https://drive.google.com/file/d/([^/]+)/.*$', url)
if file_id_match:
    file_id = file_id_match.group(1)
else:
    raise ValueError('Invalid Google Drive file URL')

# Construct the file download URL
download_url = f'https://drive.google.com/uc?id={file_id}'

# Make a request to the file download URL
response = requests.get(download_url)

if response.status_code == 200:
    # Read the file data
    image_data = response.content

    # Open the image using PIL
    pil_image = Image.open(io.BytesIO(image_data))

    # Convert RGBA image to RGB
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')

    # Convert the image to a base64-encoded string
    buffered = io.BytesIO()
    pil_image.save(buffered, format='JPEG')  # Change the format as per your image type
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Display the image
    st.image(pil_image, width=500)
else:
    print('Failed to download the file')

x=0
# Apply CSS styling to the tables
table_style = """
    <style>
    table {
        color: #333;
        font-family: Arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        border: 1px solid #ccc;
    }

    table th {
        background-color: #f4f4f4;
        text-align: left;
        padding: 8px;
    }

    table td {
        padding: 8px;
    }

    table tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    table tr:hover {
        background-color: #f1f1f1;
    }

    </style>
"""
table_style += """
    <style>
    table th, table td {
        font-weight: bold;
    }
    </style>
"""
link = "https://drive.google.com/file/d/1Ts8yaB_MQdYNzzWTwEgJ4Qfi0OKrGj5Q/view?usp=sharing"
text = "Click here to visit the user guide"
samplef='https://docs.google.com/spreadsheets/d/11V8m6LhMwjxNrL_9vadOtdBYk-TPnh4Oe2mJqnXmOfY/edit?usp=sharing'
textf='Sample File'
link1,link2=st.columns([2,5])
with link1:
    st.markdown(f"[{text}]({link})")
with link2:
    st.markdown(f"[{textf}]({samplef})")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    but_summary,but_stats,but_charts,but_streaks,but_drawdown,but_datatable = st.columns(6)
    cost_col,capital_col=st.columns(2)
    data = pd.read_csv(uploaded_file)
    def color_negative_red(value):
        s=value
        value=''
        for i in s:
            if i.isnumeric() or i=='-':
                value+=i
        value=value.strip('%')
        if isinstance(value, str):
            value = float(value)
        else:
            value = float(value.item())
        if value < 0:
            return 'background-color: #ff6961'
        elif value > 0:
            return 'background-color: #77dd77'
        else:
            return ''
    def format_int_with_commas(value): 
        if isinstance(value, str):
            value=value.strip('%')
            value=float(value)
            return f'{value:,}'
        else:
            return value
    data = data.sort_values('ExitTime')
    #setting the cost
    with cost_col:
        cost = st.number_input('Insert the Cost')
    data['ExitPrice'] = pd.to_numeric(data['ExitPrice'], errors='coerce')
    data['EntryPrice'] = pd.to_numeric(data['EntryPrice'], errors='coerce')

    # Define a function to apply the calculations based on positionstatus
    def calculate_prices(row):
        if row['PositionStatus'] == -1:
            row['EntryPrice'] = row['EntryPrice'] * (1 - (cost / 100))
            row['ExitPrice'] = row['ExitPrice'] * (1 + (cost / 100))
        elif row['PositionStatus'] == 1:
            row['EntryPrice'] = row['EntryPrice'] * (1 + (cost / 100))
            row['ExitPrice'] = row['ExitPrice'] * (1 - (cost / 100))
        return row

    # Apply the calculations to the DataFrame
    data = data.apply(calculate_prices, axis=1)

    data['P&L']=(data['EntryPrice']-data['ExitPrice'])*data['Quantity']*data['PositionStatus']*-1

    # st.table(data)
    #running basics
    formats = ["%d/%m/%Y", "%Y-%m-%d %H:%M:%S",'%m/%d/%Y %H:%M',"%m/%d/%Y","%d/%m/%Y","%d/%m/%Y %H:%M", "%Y/%m/%d %H:%M",'%m/%d/%Y %H:%M',"%m/%d/%Y %H:%M:%S"]
    for fmt in formats:
        converted_dates = pd.to_datetime(data['ExitTime'], format=fmt, errors='coerce')
        if pd.isnull(converted_dates).any()==False:
            break
    # st.write(converted_dates)
    data['ExitTime'] = converted_dates
    data=data.dropna()

    data['year'] = data['ExitTime'].dt.year
    # data['year']=pd.to_datetime(data['year'].astype(int).astype(str), format='%Y')
    data['year']=data['year'].apply(lambda x: f'{x:.2f}' if isinstance(x, float) else x).apply(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x)
    data['month_name'] = data['ExitTime'].dt.month_name()
    data = data.sort_values('ExitTime')
    # Extract month and year from the date
    data['month_year'] = data['ExitTime'].dt.to_period('M')
    data['day_of_week'] = data['ExitTime'].dt.day_name()
    options1,options2=st.columns(2)
    with options1:
        options_year = st.multiselect('Years', data['year'].unique(), key='years_multiselect')
    with options2:
        options_days = st.multiselect('Days', day_order, key='days_multiselect')
    if options_year!=[]:
        data = data[data['ExitTime'].dt.year.isin(options_year)].reset_index(drop=True)
    if options_days!=[]:
        data = data[data['ExitTime'].dt.day_name().isin(options_days)].reset_index(drop=True)
    # =============================================================================STREAKS=========================================================================================
    # Calculate the streaks
    data['is_win'] = data['P&L'] > 0
    data['is_loss'] = data['P&L'] < 0

    # Calculate the streak ID for winning and losing streaks
    data['win_streak_id'] = (data['is_win'] != data['is_win'].shift()).cumsum()
    data['loss_streak_id'] = (data['is_loss'] != data['is_loss'].shift()).cumsum()

    win_streaks = data[data['is_win']].groupby('win_streak_id').agg(
        Days=('ExitTime', 'count'),
        Start=('ExitTime', 'first'),
        End=('ExitTime', 'last'),
        Profit=('P&L', 'sum')
    ).nlargest(5, 'Profit').reset_index(drop=True)
    win_streaks = win_streaks[['Days', 'Start', 'End', 'Profit']]
    
    # Calculate the streak details for losing streaks
    loss_streaks = data[data['is_loss']].groupby('loss_streak_id').agg(
        Days=('ExitTime', 'count'),
        Start=('ExitTime', 'first'),
        End=('ExitTime', 'last'),
        Loss=('P&L', 'sum')
    ).nsmallest(5, 'Loss').reset_index(drop=True)
    loss_streaks = loss_streaks[['Days', 'Start', 'End', 'Loss']]

#=========================================================================DRAWDOWN=======================================================================================
    # Calculate drawdownimport pandas as pd

    data['cumulative_P&L'] = data['P&L'].cumsum()
    data['previous_peak'] = data['cumulative_P&L'].cummax()
    data['drawdown'] = data['cumulative_P&L'] - data['previous_peak']
    drawdown_periods = []
    current_drawdown = None
    for i in range(len(data)):
        if current_drawdown is None:
            if data['drawdown'][i] < 0:
                current_drawdown = {'Start Date': data['ExitTime'][i], 'Max Date': data['ExitTime'][i], 'End Date': None, 'Drawdown': float('inf')}
        else:
            if data['drawdown'][i] >= 0:
                current_drawdown['End Date'] = data['ExitTime'][i-1]
                if current_drawdown['Start Date'] != current_drawdown['End Date'] and current_drawdown['Drawdown']!=float('inf'):
                    drawdown_periods.append(current_drawdown)
                    current_drawdown = None
            else:
                if data['drawdown'][i] < current_drawdown['Drawdown']:
                    current_drawdown['Drawdown'] = data['drawdown'][i]
                    current_drawdown['Max Date'] = data['ExitTime'][i]

    if current_drawdown is not None and current_drawdown['Start Date'] != current_drawdown['End Date'] and current_drawdown['Drawdown']!=float('inf'):
        current_drawdown['End Date'] = data['ExitTime'][len(data)-1]
        drawdown_periods.append(current_drawdown)

    drawdown_df = pd.DataFrame(drawdown_periods)
    drawdown_graph=px.bar(drawdown_df,y='Drawdown',title="Drawdown")
#======================================================================================Stats======================================================================================

# ----------------------------------------------------------------------------------Monthly Breakup----------------------------------------------------------------------------------
    monthly_PnL = data.groupby('month_year')['P&L'].sum().reset_index().astype(str)

# ----------------------------------------------------------------------------------Daily Breakup----------------------------------------------------------------------------------
    # Group the data by year and day of the week and calculate the sum of profit for each combination
    daywise_breakup = data.groupby(['year', 'day_of_week'])['P&L'].sum().unstack().reindex(day_order,axis=1).fillna(0)

# --------------------------------------------------------------------------------Ratios--------------------------------------------------------------------------------

    # Calculate the overall profit
    overall_profit = data['P&L'].sum()

    # Calculate the average day profit
    average_day_profit = data['P&L'].mean()

    # Calculate the maximum profit
    max_profit = data['P&L'].max()

    # Calculate the maximum loss
    max_loss = data['P&L'].min()

    # Calculate the win percentage (days)
    win_percentage = (data[data['P&L'] > 0].shape[0] / data.shape[0]) * 100

    # Calculate the loss percentage (days)
    loss_percentage = (data[data['P&L'] <= 0].shape[0] / data.shape[0]) * 100

    # Calculate the average monthly profit
    data['month'] = pd.to_datetime(data['ExitTime']).dt.to_period('M')
    average_monthly_profit = data.groupby('month')['P&L'].sum().mean()

    # Calculate the average profit on win days
    average_profit_win_days = data[data['P&L'] > 0]['P&L'].mean()

    # Calculate the average loss on loss days
    average_loss_loss_days = data[data['P&L'] < 0]['P&L'].mean()
    avg_yearly_profit = data.groupby(data['ExitTime'].dt.year)['P&L'].sum().mean()
    median_monthly_profit = data.groupby(data['ExitTime'].dt.to_period('M'))['P&L'].sum().median()
    # Calculate Average Weekly Profit
    avg_weekly_profit = data.groupby(data['ExitTime'].dt.to_period('W'))['P&L'].sum().mean()

    # Calculate Average Trades Per Day
    avg_trades_per_day = data.groupby(data['ExitTime'].dt.date)['ExitTime'].count().mean()
    data["Month"] = data["ExitTime"].dt.month
    data['Date']=data['ExitTime'].dt.date
    max_drawdown=abs(data['drawdown'].min())
    max_entries_day = data["Date"].value_counts().max()
    capital=(150000*abs(max_entries_day)+max_drawdown)*1.2
    with capital_col:
        capital_=st.number_input('Capital, Pre-set Capital: '+str(int(capital)))
    if capital_!=0:
        capital=capital_
    data['NAv']=data["cumulative_P&L"].add(capital)
    data['NAv'] = pd.to_numeric(data['NAv'], errors='coerce')
    ddpercentage=(max_drawdown/capital)
    number_of_years=data['year'].nunique()
    cagr=(data['NAv'].iloc[-1]/capital)**(1/number_of_years)-1
    calmar=(cagr*capital)/max_drawdown
    average_points=overall_profit/(data['cumulative_P&L'].count())/data['Quantity'].max()
    roi_percentage=(overall_profit/capital)*100
    yearly_roi_percentage=(roi_percentage/number_of_years)
    data['std']=pd.to_numeric(data['P&L'])/capital
    std=data['std'].values.tolist()
    stdev = np.std(std)*np.sqrt(252)
    sharpe_ratio=(cagr-.02)/stdev
    Ratios={
        'Maximum Drawdown':round(max_drawdown,2),
        'Overall Drawdown Percentage':str(round(ddpercentage*100,2))+' %',
        'Overall Cagr':round(cagr*100,2),
        'Calmar':round(calmar,2),
        'Overall ROI Percentage':str(round(roi_percentage,2))+' %',
        'Yearly ROI Percentage':str(round(yearly_roi_percentage,2))+' %',
        'Sharpe Ratio (Yearly)':round(sharpe_ratio,2)
    }
    statistics = {
        'Overall Profit': round(overall_profit,2),
        'Average Day Profit': round(average_day_profit,2),
        'Avg Monthly Profit': round(average_monthly_profit,2),
        "Avg Yearly Profit": round(avg_yearly_profit,2),
        "Median Monthly Profit": round(median_monthly_profit,2),
        'Average points':round(average_points,2),
        "Avg Trades Per Day": round(avg_trades_per_day,2)
    }
    Stats2={
        'Max Profit': max_profit,
        'Max Loss': max_loss,
        'Win% (Days)': win_percentage,
        'Loss% (Days)': loss_percentage,
        'Avg Profit On Win Days': average_profit_win_days,
        'Avg Loss On Loss Days': average_loss_loss_days,
        "Avg Weekly Profit": avg_weekly_profit,
    }
# --------------------------------------------------------------------------------minimum_PnL--------------------------------------------------------------------------------
    month_order = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
    data['monthly_PnL_unstyled'] = data.groupby(['year', 'month_name'])['P&L'].cumsum()
    minimum_PnL = data.groupby(['year', 'month_name'])['monthly_PnL_unstyled'].min().unstack().reindex(month_order, axis=1).fillna(0)

# --------------------------------------------------------------------------------monthly_trades--------------------------------------------------------------------------------
    # Group the trades by month and calculate the win rate
    monthly_trades_overview = data.groupby(['year', 'month_name']).apply(lambda x: (x['P&L'] > 0).sum() / len(x) * 100).unstack().reindex(month_order, axis=1).fillna(0)

# ==========================================================================but_summary======================================================================================
    
    #----------------------------------------------------------------------------------quaterly breakup----------------------------------------------------------------------------------

    data['quarter'] = data['ExitTime'].dt.quarter

    # Calculate the total P&L for each quarter and year
    quarterly_PnL = data.groupby(['year', 'quarter'])['P&L'].sum().unstack().fillna(0)
    quarterly_PnL['Net P&L'] = quarterly_PnL.sum(axis=1)
    total_PnL = quarterly_PnL.sum(axis=1)
    quarterly_PnL_percent = (quarterly_PnL / capital) * 100
    quarterly_PnL.rename(columns={1:'Q1',2:'Q2',3:'Q3',4:'Q4'},inplace=True)
    quarterly_PnL_percent.rename(columns={1:'Q1',2:'Q2',3:'Q3',4:'Q4'},inplace=True)
    
    bar_fig_quarterly = go.Figure()
    for col in quarterly_PnL.columns:
        bar_fig_quarterly.add_trace(go.Bar(x=quarterly_PnL.index, y=quarterly_PnL[col], name=f"{col}"))

    bar_fig_quarterly.update_layout(
        title='Quarterly P&L',
        xaxis_title='Year',
        yaxis_title='P&L'
    )

#----------------------------------------------------------------------------------cumulative P&L----------------------------------------------------------------------------------

    data['P&L_cumulative'] = data['P&L'].cumsum()
    # Create the area plot for cumulative P&L
    area_fig = go.Figure(data=go.Scatter(x=data['ExitTime'], y=data['P&L_cumulative'], fill='tozeroy'))

    # Set the layout for the area plot
    area_fig.update_layout(
        title='Cumulative P&L',
        xaxis_title='Date',
        yaxis_title='Cumulative P&L'
    )


# ======================================================================================but_charts======================================================================================

    data['P&L_cumulative'] = data['P&L'].cumsum()
    # Create the area plot for cumulative P&L
    area_fig = go.Figure(data=go.Scatter(x=data['ExitTime'], y=data['P&L_cumulative'], fill='tozeroy'))

    # Set the layout for the area plot
    area_fig.update_layout(
        title='Cumulative P&L',
        xaxis_title='Date',
        yaxis_title='Cumulative P&L'
    )

    # Calculate the total P&L for each month
    monthly_PnL = data.groupby('month_year')['P&L'].sum().reset_index().astype(str)

    # Create a bar graph for monthly P&L using Plotly
    bar_fig_monthly = go.Figure(data=go.Bar(x=monthly_PnL['month_year'], y=monthly_PnL['P&L']))
    bar_fig_monthly.update_layout(
        title='Monthly P&L',
        xaxis_title='Month',
        yaxis_title='P&L'
    )

    # Calculate the cumulative P&L on a daily basis
    data['Daily P&L'] = data.groupby(data['ExitTime'].dt.date)['P&L'].cumsum()
    daily_fig = px.bar(data, x='Date', y='Daily P&L', title='Daily P&L Cumulative')

    # Calculate the cumulative P&L on a weekly basis
    data['Week'] = data['ExitTime'].dt.to_period('W').astype(str)
    data['Weekly P&L'] = data.groupby('Week')['P&L'].cumsum()
    weekly_fig = px.bar(data, x='Week', y='Weekly P&L', title='Weekly P&L Cumulative')


    #monthly trades
    monthly_trades = data.groupby('month_year').size().reset_index(name='Number of Trades').astype(str)

    # Create a bar graph for monthly number of trades using Plotly
    bar_fig_trades = go.Figure(data=go.Bar(x=monthly_trades['month_year'], y=monthly_trades['Number of Trades']))
    bar_fig_trades.update_layout(
        title='Monthly Number of Trades',
        xaxis_title='Month',
        yaxis_title='Number of Trades'
    )

# =========================================================DATA TABLE=====================================================================================================================================================
        # Apply color formatting to P&L values

    # Apply color formatting to the entire DataFrame
    selected_headers = [ 'ExitTime', 'EntryPrice', 'ExitPrice', 'P&L', 'PositionStatus', 'Quantity', 'Symbol']

    # Subset the data with selected headers
    subset_data = data[selected_headers]
    styled_data_table = subset_data.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).reset_index(drop=True).apply(lambda x: x.apply(format_int_with_commas) if x.name == 'P&L' else x).style.applymap(color_negative_red, subset=['P&L'])

    # Calculate the total P&L for each month and year
    monthly_PnL_unstyled = data.groupby(['year', 'month_name'])['P&L'].sum().unstack()
    monthly_PnL_unstyled['Net P&L'] = monthly_PnL_unstyled.sum(axis=1)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December','Net P&L']
    monthly_PnL = monthly_PnL_unstyled.reindex(month_order, axis=1).fillna(0).applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(color_negative_red)



# ====================================================running the code===============================================================================================
    def display(x):
        if x==3:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Display the area plot
                st.plotly_chart(area_fig)
                st.divider()
                st.plotly_chart(bar_fig_monthly)
                st.divider()
                st.plotly_chart(weekly_fig)
                st.divider()
                st.plotly_chart(daily_fig)
                st.divider()
                st.plotly_chart(bar_fig_trades)
        if x==4:
            col1, col2 = st.columns(2)

            with col1:
                st.write("Top 5 Maximum Winning Streaks (Moneywise):")
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(win_streaks.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(lambda x: 'color: #77dd77')) 
                st.write("Top 5 Maximum Losing Streaks (Moneywise):")
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(loss_streaks.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(lambda x: 'color: #ff6961'))      

            with col2:
                st.write("Top 5 Longest Winning Streaks (Timewise):")
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(win_streaks.nlargest(5, 'Days').reset_index(drop=True).applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(lambda x: 'color: #77dd77')) 

                st.write("Top 5 Longest Losing Streaks (Timewise):")
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(loss_streaks.nlargest(5, 'Days').reset_index(drop=True).applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(lambda x: 'color: #ff6961'))
        if x==6:
            st.markdown(table_style, unsafe_allow_html=True)
            st.table(styled_data_table)
        if x==2:
            st.header('Monthly Breakup')
            # Display the monthly P&L breakup
            st.table(monthly_PnL)
            st.divider()
            s1,s2,s3=st.columns(3)
            with s1:
                # Display the table with custom styling
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(pd.DataFrame.from_dict(statistics, orient='index', columns=['Value']).applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas))

            with s2:
                # Display the table with custom styling
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(pd.DataFrame.from_dict(Stats2, orient='index', columns=['Value']).applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas))

            with s3:
                # Display the table with custom styling
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(pd.DataFrame.from_dict(Ratios, orient='index', columns=['Value']).applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas))

            st.divider()
            st.header('Day- Wise Breakup')
            # Display the day=wise breakup as a table
            st.markdown(table_style, unsafe_allow_html=True)
            st.table(daywise_breakup.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(color_negative_red))
            st.divider()
            st.markdown(table_style, unsafe_allow_html=True)
            st.subheader('Monthly Win Rate')
            st.table(monthly_trades_overview.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).applymap(lambda x: f'{x}%').style.applymap(color_negative_red))
            st.divider()
            st.subheader('Minimum P&L')
            st.markdown(table_style, unsafe_allow_html=True)
            st.table(minimum_PnL.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(color_negative_red))
        if x==1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.subheader("Quarterly P&L Breakup (Absolute Values)")
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(quarterly_PnL.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(color_negative_red))
                st.subheader("Quarterly P&L Breakup (Percentages)")
                st.markdown(table_style, unsafe_allow_html=True)
                st.table(quarterly_PnL_percent.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).applymap(lambda x: f'{x}%').style.applymap(color_negative_red))
                st.divider()
            with col2:
                st.plotly_chart(area_fig)
                st.divider() 
            with col2:
                st.header('Quarterly Bar Chart')
                st.plotly_chart(bar_fig_quarterly)

        if x==5:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.plotly_chart(drawdown_graph)
            st.markdown(table_style, unsafe_allow_html=True)
            st.table(drawdown_df.sort_values(by='Drawdown').reset_index(drop=True).applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else x).applymap(lambda x: x.rstrip('0').rstrip('.') if isinstance(x, str) else x).applymap(format_int_with_commas).style.applymap(lambda x: 'color: #ff6961',subset=['Drawdown']))
    with but_charts:
        if st.button('Charts'):
            x=3
    with but_streaks:
        if st.button('Streaks'):
            x=4
    with but_stats:
        if st.button('Stats'):
            x=2
    with but_summary:
        if st.button('Summary'):
            x=1
    with but_datatable:
        if st.button('Data Table'):
            x=6
    with but_drawdown:
        if st.button('Drawdown'):
            x=5
    # st.table(data)
    display(x)