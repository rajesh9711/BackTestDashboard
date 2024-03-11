import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sn 
import matplotlib.pyplot as plt 
from src.controller.table import table_maker
from src.main import format_int_with_commas
from src.main import color_negative_red

def display(x,area_fig,bar_fig_monthly,weekly_fig,daily_fig,bar_fig_trades,win_streaks,loss_streaks,styled_data_table,monthly_PnL,statistics,Stats2,Ratios,daywise_breakup,monthly_trades_overview,minimum_PnL,pivot_table,quarterly_PnL,quarterly_PnL_percent,bar_fig_quarterly,drawdown_graph,drawdown_df,year_Daywise,month_Daywise):
    if x == 3:
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
    if x == 4:
        col1, col2 = st.columns(2)
        with col1:
            st.write("Top 5 Maximum Winning Streaks (Moneywise):")
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                win_streaks.applymap(
                    lambda x: f"{x:.2f}" if isinstance(x, float) else x
                )
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
                .style.applymap(lambda x: "color: #77dd77")
            )
            st.write("Top 5 Maximum Losing Streaks (Moneywise):")
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                loss_streaks.applymap(
                    lambda x: f"{x:.2f}" if isinstance(x, float) else x
                )
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
                .style.applymap(lambda x: "color: #ff6961")
            )
            st.markdown(table_maker,unsafe_allow_html=True)
        with col2:
            st.write("Top 5 Longest Winning Streaks (Timewise):")
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                win_streaks.nlargest(5, "Days")
                .reset_index(drop=True)
                .applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
                .style.applymap(lambda x: "color: #77dd77")
            )
            st.write("Top 5 Longest Losing Streaks (Timewise):")
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                loss_streaks.nlargest(5, "Days")
                .reset_index(drop=True)
                .applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
                .style.applymap(lambda x: "color: #ff6961")
            )
    if x == 6:
        st.markdown(table_maker, unsafe_allow_html=True)
        st.table(styled_data_table)
    if x == 2:
        st.header("Monthly Breakup")
        # Display the monthly P&L breakup
        st.table(monthly_PnL)

        st.divider()
        s1, s2, s3 = st.columns(3)
        with s1:
            # Display the table with custom styling
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                pd.DataFrame.from_dict(
                    statistics, orient="index", columns=["Value"]
                )
                .applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
            )
        with s2:
            # Display the table with custom styling
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                pd.DataFrame.from_dict(Stats2, orient="index", columns=["Value"])
                .applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
            )
        with s3:
            # Display the table with custom styling
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                pd.DataFrame.from_dict(Ratios, orient="index", columns=["Value"])
                .applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
            )
        st.divider()
        st.header("Day- Wise Breakup")
        # Display the day=wise breakup as a table
        st.markdown(table_maker, unsafe_allow_html=True)
        st.table(
            daywise_breakup.applymap(
                lambda x: f"{x:.2f}" if isinstance(x, float) else x
            )
            .applymap(
                lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
            )
            .applymap(format_int_with_commas)
            .style.applymap(color_negative_red)
        )
        st.divider()
        st.markdown(table_maker, unsafe_allow_html=True)
        st.subheader("Monthly Win Rate")
        st.table(
            monthly_trades_overview.applymap(
                lambda x: f"{x:.2f}" if isinstance(x, float) else x
            )
            .applymap(
                lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
            )
            .applymap(format_int_with_commas)
            .applymap(lambda x: f"{x}%")
            .style.applymap(color_negative_red)
        )
        st.divider()
        st.subheader("Minimum P&L")
        st.markdown(table_maker, unsafe_allow_html=True)
        st.table(
            minimum_PnL.applymap(
                lambda x: f"{x:.2f}" if isinstance(x, float) else x
            )
            .applymap(
                lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
            )
            .applymap(format_int_with_commas)
            .style.applymap(color_negative_red)
        )
        st.subheader("Year-daywise Pnl")
        st.table(year_Daywise.style.applymap(color_negative_red))
        st.subheader("Monthly-Daywise Pnl")
        st.table(month_Daywise.style.applymap(color_negative_red))


    if x == 1:
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("Quarterly P&L Breakup (Absolute Values)")
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                quarterly_PnL.applymap(
                    lambda x: f"{x:.2f}" if isinstance(x, float) else x
                )
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
                .style.applymap(color_negative_red)
            )
            st.subheader("Quarterly P&L Breakup (Percentages)")
            st.markdown(table_maker, unsafe_allow_html=True)
            st.table(
                quarterly_PnL_percent.applymap(
                    lambda x: f"{x:.2f}" if isinstance(x, float) else x
                )
                .applymap(
                    lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
                )
                .applymap(format_int_with_commas)
                .applymap(lambda x: f"{x}%")
                .style.applymap(color_negative_red)
            )
            st.divider()
        with col2:
            st.plotly_chart(area_fig)
            st.divider()
        with col2:
            st.header("Quarterly Bar Chart")
            st.plotly_chart(bar_fig_quarterly)
        st.subheader("Year-Daywise Pnl:")
        st.markdown(table_maker, unsafe_allow_html=True)
        pivot = pivot_table.T
        st.table(
            pivot.applymap(
               lambda x: f"{x:.2f}" if isinstance(x, float) else x
           )
           .applymap(
               lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
           )
           .applymap(format_int_with_commas)
           .style.applymap(lambda x: "color: #77dd77")
        )
    if x == 5:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.plotly_chart(drawdown_graph)
        st.markdown(table_maker, unsafe_allow_html=True)
        st.table(
            drawdown_df.sort_values(by="Drawdown")
            .reset_index(drop=True)
            .applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
            .applymap(
                lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x
            )
            .applymap(format_int_with_commas)
            .style.applymap(lambda x: "color: #ff6961", subset=["Drawdown"])
        )
