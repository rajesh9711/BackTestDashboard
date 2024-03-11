import streamlit as st
def streak(data):
    
       # Calculate the streaks
    data["is_win"] = data["P&L"] > 0
    data["is_loss"] = data["P&L"] < 0
    # Calculate the streak ID for winning and losing streaks
    data["win_streak_id"] = (data["is_win"] != data["is_win"].shift()).cumsum()
    data["loss_streak_id"] = (data["is_loss"] != data["is_loss"].shift()).cumsum()
    win_streaks = (
        data[data["is_win"]]
        .groupby("win_streak_id")
        .agg(
            Days=("ExitTime", "count"),
            Start=("ExitTime", "first"),
            End=("ExitTime", "last"),
            Profit=("P&L", "sum"),
        )
        .nlargest(5, "Profit")
        .reset_index(drop=True)
    )
    win_streaks = win_streaks[["Days", "Start", "End", "Profit"]]
    # Calculate the streak details for losing streaks
    loss_streaks = (
        data[data["is_loss"]]
        .groupby("loss_streak_id")
        .agg(
            Days=("ExitTime", "count"),
            Start=("ExitTime", "first"),
            End=("ExitTime", "last"),
            Loss=("P&L", "sum"),
        )
        .nsmallest(5, "Loss")
        .reset_index(drop=True)
    )
    loss_streaks = loss_streaks[["Days", "Start", "End", "Loss"]]
    return win_streaks,loss_streaks