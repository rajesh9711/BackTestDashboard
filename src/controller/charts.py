import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def charts(data):
    
    data["P&L_cumulative"] = data["P&L"].cumsum()
    # Create the area plot for cumulative P&L
    area_fig = go.Figure(
        data=go.Scatter(x=data["ExitTime"], y=data["P&L_cumulative"], fill="tozeroy")
    )

    # Set the layout for the area plot
    area_fig.update_layout(
        title="Cumulative P&L", xaxis_title="Date", yaxis_title="Cumulative P&L",
        font=dict(family="Arial", size=15, color="black"),  # Font style and color
        margin=dict(l=50, r=50, t=50, b=50),  # Margins around the plot area
        width=800,  # Width of the figure
        height=400,
    )

    # Calculate the total P&L for each month
    monthly_PnL = data.groupby("month_year")["P&L"].sum().reset_index().astype(str)

    # Create a bar graph for monthly P&L using Plotly
    monthly_PnL["p&l"] = pd.to_numeric(monthly_PnL["P&L"])
    colors = ['red' if val < 0 else 'green' for val in monthly_PnL["p&l"]]
    bar_fig_monthly = go.Figure(
        data=go.Bar(
            x=monthly_PnL["month_year"], 
            y=monthly_PnL["P&L"],
            marker=dict(color=colors)  # Specify the colors based on the list
        )
    )
    bar_fig_monthly.update_layout(
        title="Monthly P&L", xaxis_title="Month", yaxis_title="P&L"
    )

    # Calculate the cumulative P&L on a daily basis
    data["Daily P&L"] = data.groupby(data["ExitTime"].dt.date)["P&L"].cumsum()
    data["Daily p&l"] = pd.to_numeric(data["Daily P&L"])

    # Define the color column based on the sign of the y-axis values
    data['color'] = ['green' if val >= 0 else 'red' for val in data['Daily p&l']]

    # Create the bar figure with conditional coloring
    daily_fig = px.bar(
        data, 
        x="Date", 
        y="Daily P&L", 
        title="Daily P&L Cumulative",
        color="color",
        color_discrete_map={"green": "green", "red": "red"}  
    )


    # Calculate the cumulative P&L on a weekly basis
    data["Week"] = data["ExitTime"].dt.to_period("W").astype(str)
    data["Weekly P&L"] = data.groupby("Week")["P&L"].cumsum()
    data["Weekly p&l"] = pd.to_numeric(data["Weekly P&L"])

    data['color'] = ['green' if val >= 0 else 'red' for val in data['Weekly p&l']]
    weekly_fig = px.bar(
        data, 
        x="Week", 
        y="Weekly P&L", 
        title="Weekly P&L Cumulative",
        color="color",
        color_discrete_map={"green": "green", "red": "red"}  
        )

    # monthly trades
    monthly_trades = (
        data.groupby("month_year")
        .size()
        .reset_index(name="Number of Trades")
        .astype(str)
    )

    # Create a bar graph for monthly number of trades using Plotly
    bar_fig_trades = go.Figure(
        data=go.Bar(
            x=monthly_trades["month_year"], y=monthly_trades["Number of Trades"]
        )
    )
    bar_fig_trades.update_layout(
        title="Monthly Number of Trades",
        xaxis_title="Month",
        yaxis_title="Number of Trades",
    )
    return bar_fig_monthly,bar_fig_trades,monthly_trades,weekly_fig,daily_fig,area_fig
