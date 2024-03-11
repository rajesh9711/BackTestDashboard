import streamlit as st
import pandas as pd
import numpy as np
import base64
import requests
import requests
import re
from PIL import Image
import io
import os
import datetime
import matplotlib.pyplot as plt
import july
from july.utils import date_range
from pyecharts import options as opts
from pyecharts.charts import Calendar

from streamlit_option_menu import option_menu
from src.main import load_data
from src.main import color_negative_red
from src.main import format_int_with_commas
from src.main import formats
from src.controller.streak import streak
from src.controller.drawDown import drawnDown
from src.controller.stats import stats
from src.controller.summary import summary
from src.controller.charts import charts
from src.controller.dataTable import dataTable
from src.controller.display import display

# Configure default Streamlit theme
st.set_page_config(
    page_title="Multyfi Backtester",
    page_icon="image.png",
    layout="wide",
)

Menu = ["Charts", "Streaks",  "Stats", 'Summary','Drawdown','Data Table']
selected_menu = option_menu(None, [Menu[0], Menu[1],  Menu[2], Menu[3],Menu[4],Menu[5]], 
    icons=['bar-chart-fill', 'graph-up', "list-task", 'gear','file-bar-graph','file-spreadsheet-fill','table'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#7072E9", "font-size": "25px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2EB2B6"},
    }
)

data_t = []
# Function to save uploaded data to a CSV file
def save_uploaded_data(file, filename):
    file_path = os.path.join("uploaded_data", filename)
    with open(file_path, "wb") as f:
        f.write(file.getvalue())

# Create directory for uploaded data if it doesn't exist
os.makedirs("uploaded_data", exist_ok=True)

url = (
    "https://drive.google.com/file/d/1-ABYp-BzXjjZTmkMGzjJz7jV1MHIfHH-/view?usp=sharing"
)
# Extract the file ID from the URL
file_id_match = re.match(r"^https://drive.google.com/file/d/([^/]+)/.*$", url)
if file_id_match:
    file_id = file_id_match.group(1)
else:
    raise ValueError("Invalid Google Drive file URL")

# Construct the file download URL

download_url = f"https://drive.google.com/uc?id={file_id}"

# Make a request to the file download URL
response = requests.get(download_url)

if response.status_code == 200:
    # Read the file data
    image_data = response.content

    # Open the image using PIL
    pil_image = Image.open(io.BytesIO(image_data))

    # Convert RGBA image to RGB
    if pil_image.mode == "RGBA":
        pil_image = pil_image.convert("RGB")

    # Convert the image to a base64-encoded string
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")  # Change the format as per your image type
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    st.sidebar.image(pil_image,width=260)
    # st.sidebar.image('image.png',width=100)
    # st.sidebar.write('Multyfi backtesting')
else:
    print("Failed to download the file")


link = (
    "https://drive.google.com/file/d/1Ts8yaB_MQdYNzzWTwEgJ4Qfi0OKrGj5Q/view?usp=sharing"
)
text = "User guide"
samplef = "https://docs.google.com/spreadsheets/d/11V8m6LhMwjxNrL_9vadOtdBYk-TPnh4Oe2mJqnXmOfY/edit?usp=sharing"
textf = "Sample File"
col_first,col_second = st.sidebar.columns(2)
with col_first:
    st.button(f"[{text}]({link})",type="secondary")
with col_second:
    st.button(f"[{textf}]({samplef})",type="secondary")

header = ["ExitTime","EntryPrice","ExitPrice","Pnl","PositionStatus","Quantity","Symbol"]
head = ["ExitPrice","ExitTime","fhjfhjf", "Entrydgrice","ExitPrice","Pnl","PositionStatus","hjbfh","Quantity","Symbol"]

csv_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
if csv_file is not None:
    d = pd.read_csv(csv_file,nrows=0)
    head = d.columns.tolist()
    all_present = all(item in head for item in header)
    if not all_present:
        st.warning("Please Check File Structural")
        

# Multiselect widget to select previous files
uploaded_files = os.listdir("uploaded_data")
selected_filename = st.sidebar.selectbox("Select previous file:", uploaded_files)
data = []
# Display data corresponding to the selected file
if csv_file is not None:
    # Save uploaded data to a CSV file
    save_uploaded_data(csv_file, csv_file.name)
    selected_filename = csv_file.name

if selected_filename:
    selected_df = load_data(selected_filename)
    if selected_df is not None:
        st.write("Data for", selected_filename)
        data = selected_df
    else:
        st.error("Data not found for selected file.")

if selected_filename is not None:
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    (
        but_summary,
        but_stats,
        but_charts,
        but_streaks,
        but_drawdown,
        but_datatable,
    ) = st.columns(6)
    cost_col, capital_col,year_col,day_col = st.columns(4)

    df = data
    important_columns = [ "ExitTime","Symbol","EntryPrice","ExitPrice","PositionStatus","Quantity",]
    data = df.drop(columns=[col for col in df.columns if col not in important_columns])

    data = data.sort_values("ExitTime")
    # setting the cost
    with cost_col:
        cost = st.number_input("Insert the Cost")
   
    data["ExitPrice"] = pd.to_numeric(data["ExitPrice"], errors="coerce")
    data["EntryPrice"] = pd.to_numeric(data["EntryPrice"], errors="coerce")
    
    # Define a function to apply the calculations based on positionstatus
    def calculate_prices(row):
        if row["PositionStatus"] == -1:
            row["EntryPrice"] = row["EntryPrice"] * (1 - (cost / 100))
            row["ExitPrice"] = row["ExitPrice"] * (1 + (cost / 100))
        elif row["PositionStatus"] == 1:
            row["EntryPrice"] = row["EntryPrice"] * (1 + (cost / 100))
            row["ExitPrice"] = row["ExitPrice"] * (1 - (cost / 100))
        return row

    # Apply the calculations to the DataFrame
    data = data.apply(calculate_prices, axis=1)

    data["P&L"] = (
        (data["EntryPrice"] - data["ExitPrice"])
        * data["Quantity"]
        * data["PositionStatus"]
        * -1
    )

    for fmt in formats:
        converted_dates = pd.to_datetime(data["ExitTime"], format=fmt, errors="coerce")
        if pd.isnull(converted_dates).any() == False:
            break

    data["ExitTime"] = converted_dates
    
    data = data.dropna()
    data["year"] = data["ExitTime"].dt.year

    data["year"] = (
        data["year"]
        .apply(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
        .apply(lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x)
    )
    data["month_name"] = data["ExitTime"].dt.month_name()
    data = data.sort_values("ExitTime")

    # Extract month and year from the date
    data["month_year"] = data["ExitTime"].dt.to_period("M")
    data["day_of_week"] = data["ExitTime"].dt.day_name()
    options1, options2 = st.columns(2)
    with year_col:
        options_year = st.multiselect(
            "Years", data["year"].unique(), key="years_multiselect"
        )
    with day_col:
        options_days = st.multiselect("Days", day_order, key="days_multiselect")
    if options_year != []:
        data = data[data["ExitTime"].dt.year.isin(options_year)].reset_index(drop=True)
    if options_days != []:
        data = data[data["ExitTime"].dt.day_name().isin(options_days)].reset_index(drop=True)
    # st.write(data)
    grouped_df = data.groupby(['year', 'day_of_week']).agg({'P&L': 'sum'}).reset_index()
    pivot_table = grouped_df.pivot_table(index='day_of_week', columns='year', values='P&L', aggfunc='sum')
    years = data['year'].unique()
    ## Create data
    dates = date_range("2020-01-01", "2020-12-31")
    datac = np.random.randint(-10000, 10000, len(dates))

    ## Create a figure with a single axes
    fig, ax = plt.subplots()

    ## Tell july to make a plot in a specific axes
    july.month_plot(dates, data['P&L'], month=2, date_label=True, ax=ax, colorbar=True)
    ## Tell streamlit to display the figure
    

    data['ExitTime'] = pd.to_datetime(data['ExitTime'])
    selected_year = st.selectbox('Select Year',years)
    if selected_year is not None:

        data_year = data[data['ExitTime'].dt.year == selected_year]
        total_pnl_by_date = data_year.groupby([data_year['ExitTime'].dt.date, 'day_of_week', 'month_name'])['P&L'].sum().reset_index()
        data_ttt = total_pnl_by_date[['ExitTime','P&L']].values.tolist()
        maxpnl = total_pnl_by_date['P&L'].max()
        minpnl= total_pnl_by_date['P&L'].min()
        pnl_calender = (
            Calendar()
            .add('',data_ttt,calendar_opts=opts.CalendarOpts(range_=selected_year))
            .set_global_opts(
                title_opts=opts.TitleOpts(title='Pnl Calender',subtitle='in USD'),
                legend_opts=opts.LegendOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(
                    max_= maxpnl,
                    min_=minpnl,
                    orient='horizontal',
                    is_piecewise=False,
                    
                )
            )
        )
        pnl_calender.render_notebook()
        

    # ===============STREAKS============
    win_streaks,loss_streaks = streak(data)

    # ===============DRAWDOWN===========

    year_kuch,drawdown_graph,drawdown_df = drawnDown(data)
    
    # ===============Stats==============

    monthly_PnL,daywise_breakup,Ratios,statistics,Stats2,minimum_PnL,monthly_trades_overview,capital,year_Daywise,month_Daywise = stats(data,day_order,capital_col)

    # ===============but_summary========

    total_PnL,bar_fig_quarterly,area_fig,quarterly_PnL_percent,quarterly_PnL = summary(data,capital)

    # ===============but_charts==========

    bar_fig_monthly,bar_fig_trades,monthly_trades,weekly_fig,daily_fig,area_fig = charts(data)

    # ==============DATA TABLE===========

    monthly_PnL,styled_data_table = dataTable(data,format_int_with_commas,color_negative_red)

    # ====================================================running the code===============================================================================================           
    if selected_menu == "Charts":
        x = 3
    if selected_menu == "Streaks":
        x = 4
    if selected_menu == "Stats":
        x = 2
    if selected_menu == "Summary":
        x = 1
    if selected_menu == "Data Table":
        x = 6
    if selected_menu == "Drawdown":
        x = 5
    # st.table(data)
    display(x,area_fig,bar_fig_monthly,weekly_fig,daily_fig,bar_fig_trades,win_streaks,loss_streaks,styled_data_table,monthly_PnL,statistics,Stats2,Ratios,daywise_breakup,monthly_trades_overview,minimum_PnL,pivot_table,quarterly_PnL,quarterly_PnL_percent,bar_fig_quarterly,drawdown_graph,drawdown_df,year_Daywise,month_Daywise)

