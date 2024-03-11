import streamlit as st
def dataTable(data,format_int_with_commas,color_negative_red):
    # Apply color formatting to the entire DataFrame
    
    selected_headers = [
        "ExitTime",
        "EntryPrice",
        "ExitPrice",
        "P&L",
        "PositionStatus",
        "Quantity",
        "Symbol",
    ]

    # Subset the data with selected headers
    subset_data = data[selected_headers]
    styled_data_table = (
        subset_data.applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
        .applymap(lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x)
        .reset_index(drop=True)
        .apply(lambda x: x.apply(format_int_with_commas) if x.name == "P&L" else x)
        .style.applymap(color_negative_red, subset=["P&L"])
    )

    # Calculate the total P&L for each month and year
    monthly_PnL_unstyled = data.groupby(["year", "month_name"])["P&L"].sum().unstack()
    monthly_PnL_unstyled["Net P&L"] = monthly_PnL_unstyled.sum(axis=1)
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
        "Net P&L",
    ]
    monthly_PnL = (
        monthly_PnL_unstyled.reindex(month_order, axis=1)
        .fillna(0)
        .applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else x)
        .applymap(lambda x: x.rstrip("0").rstrip(".") if isinstance(x, str) else x)
        .applymap(format_int_with_commas)
        .style.applymap(color_negative_red)
    )
    return monthly_PnL,styled_data_table