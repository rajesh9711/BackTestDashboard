table_maker = """
    <style>
        table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            min-width: 400px;
            border-radius: 5px 5px 0 0;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.25);
        }

        table thead tr {
            background-color: #d7dbdb;
            color: #ffffff;
            text-align: middle;
            font-weight: bold;
            font-size: 20px;
        }

        table th,
        table td {
            padding: 12px 15px;
        }

        table tbody tr {
            border-bottom: 1px solid #dddddd;
            font-size: 15px;
            font-weight: bold;
        }

        table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }

        table tbody tr:last-of-type {
            border-bottom: 2px solid #009879;
        }

        table tbody tr.active-row {
            font-weight: bold;
            color: #009879;
        }
        table thead tr{
            color:white;
        }
        table thead tr{
            color: #ffffff;
        }

    </style>
"""

# Apply CSS styling to the tables
table_style = """
    <style>
    table {
        color: [#6D73E5];
        font-family: Arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        border: 5px solid #780415;
        border-radius: 5px;
    }

    table th {
        background-color: #BDBDBD;
        text-align: left;
        padding: 8px;
        color: black;
        font-size: 20px;
        font-weight: 900;
    }

    table td {
        padding: 8px;
    }

    table tr:nth-child(even) {
        background-color: #f9f9f9;
        color:black
    }
    </style>
"""
table_style += """
    <style>
    table, table td {
        font-weight: bold;
    }
    </style>
"""