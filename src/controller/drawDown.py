import pandas as pd
import streamlit as st
import plotly.express as px
def drawnDown(data):
    
    # Calculate drawdownimport pandas as pd
    data["cumulative_P&L"] = data["P&L"].cumsum()
    data["previous_peak"] = data["cumulative_P&L"].cummax()
    data["drawdown"] = data["cumulative_P&L"] - data["previous_peak"]
    
    drawdown_periods = []
    
    Year_day = {
        "ExitTime":data["ExitTime"],
        "EntryPrice":data["EntryPrice"],
        "ExitPrice":data["ExitPrice"],
        "P&L":data["P&L"],
        "Day":data["day_of_week"]
    }
    year_kuch = pd.DataFrame(Year_day)
    current_drawdown = None
    for i in range(len(data)):
        if current_drawdown is None:
            if data["drawdown"][i] < 0:
                current_drawdown = {
                    "Start Date": data["ExitTime"][i],
                    "Max Date": data["ExitTime"][i],
                    "End Date": None,
                    "Drawdown": float("inf"),
                }
        else:
            if data["drawdown"][i] >= 0:
                current_drawdown["End Date"] = data["ExitTime"][i - 1]
                if current_drawdown["Start Date"] != current_drawdown["End Date"] and current_drawdown["Drawdown"] != float("inf"):
                    drawdown_periods.append(current_drawdown)
                    current_drawdown = None
            else:
                if data["drawdown"][i] < current_drawdown["Drawdown"]:
                    current_drawdown["Drawdown"] = data["drawdown"][i]
                    current_drawdown["Max Date"] = data["ExitTime"][i]
    # st.write(current_drawdown)
    if (
        current_drawdown is not None
        and current_drawdown["Start Date"] != current_drawdown["End Date"]
        and current_drawdown["Drawdown"] != float("inf")
    ):
        current_drawdown["End Date"] = data["ExitTime"][len(data) - 1]
        drawdown_periods.append(current_drawdown)
    
    drawdown_df = pd.DataFrame(drawdown_periods)
    
    drawdown_graph = px.bar(drawdown_df, y="Drawdown", title="Drawdown")
    return year_kuch,drawdown_graph,drawdown_df