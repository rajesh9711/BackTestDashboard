import streamlit as st
import pandas as pd
import numpy as np
from pyecharts.charts import Calendar
from pyecharts import options as opts
def stats(data,day_order,capital_col):
    

    #-----------Yearly DayWise Total Pnl------------
    data['ExitTime'] = pd.to_datetime(data['ExitTime'])
    data['Year'] = data['ExitTime'].dt.year
    data['Date'] = data['ExitTime'].dt.day
    grouped = data.groupby(['Year', 'Date'])['P&L'].sum().reset_index()
    year_Daywise = pd.pivot_table(grouped, values='P&L', index='Year', columns='Date', aggfunc='sum')
    year_Daywise = year_Daywise.applymap(lambda x: '{:.2f}'.format(x))

    #-------------- Month and Day Wise total pnl
    data['ExitTime'] = pd.to_datetime(data['ExitTime'])
    data['Month'] = data['ExitTime'].dt.month_name()
    data['Day'] = data['ExitTime'].dt.day
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)
    grouped = data.groupby(['Month', 'Day'])['P&L'].sum().reset_index()
    month_Daywise = pd.pivot_table(grouped, values='P&L', index='Month', columns='Day', aggfunc='sum')
    month_Daywise = month_Daywise.fillna(0)
    month_Daywise = month_Daywise.applymap(lambda x: '{:.2f}'.format(x))

    monthly_PnL = data.groupby("month_year")["P&L"].sum().reset_index().astype(str)
    # ----------------------------------------------------------------------------------Daily Breakup----------------------------------------------------------------------------------
    # Group the data by year and day of the week and calculate the sum of profit for each combination
    daywise_breakup = (
        data.groupby(["year", "day_of_week"])["P&L"]
        .sum()
        .unstack()
        .reindex(day_order, axis=1)
        .fillna(0)
    )

    # --------------------------------------------------------------------------------Ratios--------------------------------------------------------------------------------

    # Calculate the overall profit
    overall_profit = data["P&L"].sum()
   

    # Calculate the average day profit
    average_day_profit = data["P&L"].mean()

    # Calculate the maximum profit
    max_profit = data["P&L"].max()

    # Calculate the maximum loss
    max_loss = data["P&L"].min()

    # Calculate the win percentage (days)
    win_percentage = (data[data["P&L"] > 0].shape[0] / data.shape[0]) * 100

    # Calculate the loss percentage (days)
    loss_percentage = (data[data["P&L"] <= 0].shape[0] / data.shape[0]) * 100

    # Calculate the average monthly profit
    data["month"] = pd.to_datetime(data["ExitTime"]).dt.to_period("M")
    average_monthly_profit = data.groupby("month")["P&L"].sum().mean()
    # Calculate the average profit on win days
    average_profit_win_days = data[data["P&L"] > 0]["P&L"].mean()

    # Calculate the average loss on loss days
    average_loss_loss_days = data[data["P&L"] < 0]["P&L"].mean()
    avg_yearly_profit = data.groupby(data["ExitTime"].dt.year)["P&L"].sum().mean()
    median_monthly_profit = (
        data.groupby(data["ExitTime"].dt.to_period("M"))["P&L"].sum().median()
    )
    # Calculate Average Weekly Profit
    avg_weekly_profit = (
        data.groupby(data["ExitTime"].dt.to_period("W"))["P&L"].sum().mean()
    )

    # Calculate Average Trades Per Day
    avg_trades_per_day = (
        data.groupby(data["ExitTime"].dt.date)["ExitTime"].count().mean()
    )
    data["Month"] = data["ExitTime"].dt.month
    data["Date"] = data["ExitTime"].dt.date
    max_drawdown = abs(data["drawdown"].min())
    max_entries_day = data["Date"].value_counts().max()
    capital = (150000 * abs(max_entries_day) + max_drawdown) * 1.2
    with capital_col:
        capital_ = st.number_input("Capital, Pre-set Capital: " + str(int(capital)))
    if capital_ != 0:
        capital = capital_
    data["NAv"] = data["cumulative_P&L"].add(capital)
    data["NAv"] = pd.to_numeric(data["NAv"], errors="coerce")
    ddpercentage = max_drawdown / capital
    number_of_years = data["year"].nunique()
    cagr = (data["NAv"].iloc[-1] / capital) ** (1 / number_of_years) - 1
    calmar = (cagr * capital) / max_drawdown
    average_points = (
        overall_profit / (data["cumulative_P&L"].count()) / data["Quantity"].max()
    )
    roi_percentage = (overall_profit / capital) * 100
    yearly_roi_percentage = roi_percentage / number_of_years
    data["std"] = pd.to_numeric(data["P&L"]) / capital
    std = data["std"].values.tolist()
    stdev = np.std(std) * np.sqrt(252)
    sharpe_ratio = (cagr - 0.02) / stdev
    Ratios = {
        "Maximum Drawdown": round(max_drawdown, 2),
        "Overall Drawdown Percentage": str(round(ddpercentage * 100, 2)) + " %",
        "Overall Cagr": round(cagr * 100, 2),
        "Calmar": round(calmar, 2),
        "Overall ROI Percentage": str(round(roi_percentage, 2)) + " %",
        "Yearly ROI Percentage": str(round(yearly_roi_percentage, 2)) + " %",
        "Sharpe Ratio (Yearly)": round(sharpe_ratio, 2),
    }
    statistics = {
        "Overall Profit": round(overall_profit, 2),
        "Average Day Profit": round(average_day_profit, 2),
        "Avg Monthly Profit": round(average_monthly_profit, 2),
        "Avg Yearly Profit": round(avg_yearly_profit, 2),
        "Median Monthly Profit": round(median_monthly_profit, 2),
        "Average points": round(average_points, 2),
        "Avg Trades Per Day": round(avg_trades_per_day, 2),
    }
    Stats2 = {
        "Max Profit": max_profit,
        "Max Loss": max_loss,
        "Win% (Days)": win_percentage,
        "Loss% (Days)": loss_percentage,
        "Avg Profit On Win Days": average_profit_win_days,
        "Avg Loss On Loss Days": average_loss_loss_days,
        "Avg Weekly Profit": avg_weekly_profit,
    }
    # --------------------------------------------------------------------------------minimum_PnL--------------------------------------------------------------------------------
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    data["monthly_PnL_unstyled"] = data.groupby(["year", "month_name"])["P&L"].cumsum()
    minimum_PnL = (
        data.groupby(["year", "month_name"])["monthly_PnL_unstyled"]
        .min()
        .unstack()
        .reindex(month_order, axis=1)
        .fillna(0)
    )

    # --------------------------------------------------------------------------------monthly_trades--------------------------------------------------------------------------------
    # Group the trades by month and calculate the win rate
    monthly_trades_overview = (
        data.groupby(["year", "month_name"])
        .apply(lambda x: (x["P&L"] > 0).sum() / len(x) * 100)
        .unstack()
        .reindex(month_order, axis=1)
        .fillna(0)
    )
    return monthly_PnL,daywise_breakup,Ratios,statistics,Stats2,minimum_PnL,monthly_trades_overview,capital,year_Daywise,month_Daywise