import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def summary(data,capital):
    # ----------------------------------------------------------------------------------quaterly breakup----------------------------------------------------------------------------------

    data["quarter"] = data["ExitTime"].dt.quarter
    
    # Calculate the total P&L for each quarter and year
    quarterly_PnL = data.groupby(["year", "quarter"])["P&L"].sum().unstack().fillna(0)
    quarterly_PnL["Net P&L"] = quarterly_PnL.sum(axis=1)
    total_PnL = quarterly_PnL.sum(axis=1)
    quarterly_PnL_percent = (quarterly_PnL / capital) * 100
    quarterly_PnL.rename(columns={1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}, inplace=True)
    quarterly_PnL_percent.rename(
        columns={1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}, inplace=True
    )

    bar_fig_quarterly = go.Figure()
    for col in quarterly_PnL.columns:
        bar_fig_quarterly.add_trace(
            go.Bar(x=quarterly_PnL.index, y=quarterly_PnL[col], name=f"{col}")
        )

    bar_fig_quarterly.update_layout(
        title="Quarterly P&L", xaxis_title="Year", yaxis_title="P&L"
    )

    # ----------------------------------------------------------------------------------cumulative P&L----------------------------------------------------------------------------------

    data["P&L_cumulative"] = data["P&L"].cumsum()
    # Create the area plot for cumulative P&L
    area_fig = go.Figure(
        data=go.Scatter(x=data["ExitTime"], y=data["P&L_cumulative"], fill="tozeroy")
    )

    # Set the layout for the area plot
    area_fig.update_layout(
        title="Cumulative P&L", xaxis_title="Date", yaxis_title="Cumulative P&L"
    )
    return total_PnL,bar_fig_quarterly,area_fig,quarterly_PnL_percent,quarterly_PnL

