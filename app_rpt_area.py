from dash import html, dcc, Input, Output, callback
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash import dash_table
from decimal import Decimal

# Load initial data
file1 = 'fact_rpt_loss_area_202203210922.xlsx'
df_loss_area = pd.read_excel(file1)
df_kd = df_loss_area.copy()
df_kd['month_key'] = pd.to_datetime(df_kd['month_key'], format='%Y%m')

# Number formatting function
def format_number(value):
    try:
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return ""
        if isinstance(value, Decimal):
            value = float(value)
        if isinstance(value, (int, float, np.int64, np.float64, np.float32)):
            if abs(value) >= 100_000:
                return "{:,.0f}".format(value / 1_000_000)
            return "{:,.2f}".format(value)
        if isinstance(value, str):
            try:
                num_value = float(value.replace(',', ''))
                if abs(num_value) >= 100_000:
                    return "{:,.0f}".format(num_value / 1_000_000)
                return "{:,.2f}".format(num_value)
            except ValueError:
                return value
        return str(value)
    except Exception:
        return str(value)

# Format table data
def format_table_data(data):
    if isinstance(data, list):
        for row in data:
            for key in row:
                row[key] = format_number(row[key])
    return data

# Data processing function
def update_dashboard_baocao(month):
    if not month:
        return [], []

    df = df_kd.copy()
    if df.empty:
        return [], []

    selected_month = pd.to_datetime(f"2023-{month:02d}-01")
    df = df[df['month_key'] == selected_month]

    column_mapping = {
        "information": "Chỉ tiêu",
        "head": "Head",
        "dong_bac_bo": "Đông Bắc Bộ",
        "tay_bac_bo": "Tây Bắc Bộ",
        "db_song_hong": "Đồng Bằng Sông Hồng",
        "bac_trung_bo": "Bắc Trung Bộ",
        "nam_trung_bo": "Nam Trung Bộ",
        "tay_nam_bo": "Tây Nam Bộ",
        "dong_nam_bo": "Đông Nam Bộ",
    }

    df.drop(columns=["id", "month_key"], errors="ignore", inplace=True)
    df.rename(columns=column_mapping, inplace=True)

    # XÓA nội dung trong ngoặc ở cột "Chỉ tiêu", trừ dòng "H. Số lượng nhân sự ( Sale Manager )"
    df["Chỉ tiêu"] = df["Chỉ tiêu"].apply(
        lambda x: x if "Số lượng nhân sự" in x else pd.Series(x).str.replace(r"\(.*\)", "", regex=True).str.strip()[0]
    )

    # Thụt lề chỉ tiêu con (B1–B5, C1–C2, D1–D3, F1–F3)
    indent_prefixes = ["B1", "B2", "B3", "B4", "B5",
                       "C1", "C2",
                       "D1", "D2", "D3",
                       "F1", "F2", "F3"]
    
    df["Chỉ tiêu"] = df["Chỉ tiêu"].apply(
        lambda x: " " + x if any(x.strip().startswith(prefix) for prefix in indent_prefixes) else x
    )

    formatted_data = format_table_data(df.to_dict('records'))
    columns = [{"name": i, "id": i} for i in df.columns]

    return formatted_data, columns

# Layout definition
def baocao_tonghop_layout():
    return html.Div([
        html.H2("BÁO CÁO KẾT QUẢ HOẠT ĐỘNG THẺ THEO KHU VỰC", className="text-center mt-3 mb-1", style={
            "fontWeight": "bold", "color": "#003366"
        }),

        html.P("Đơn vị tính: triệu đồng", className="text-center mb-3", style={
            "fontStyle": "italic", "color": "#666", "fontSize": "14px"
        }),

        dbc.Row([
            dbc.Col([
                html.Label("Chọn tháng:", style={"fontWeight": "bold", "fontSize": "15px"}),
                dcc.Dropdown(
                    id="month-dropdown-baocao",
                    options=[{"label": f"Tháng {m} - 2023", "value": m} for m in range(1, 6)],
                    value=1,
                    clearable=False,
                    style={
                        "fontSize": "13px",
                        "height": "32px",
                        "lineHeight": "14px",
                        "padding": "0px 8px"
                    },
                )
            ], width=4, className="offset-md-4")
        ], className="mb-3"),

        html.Div([
            dash_table.DataTable(
                id='data-table-baocao',
                columns=[],
                data=[],
                style_table={
                    'overflowX': 'auto',
                    'maxHeight': '72vh',
                    'overflowY': 'auto',
                    'marginBottom': '0px'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '8px',
                    'fontFamily': 'Arial',
                    'fontSize': '15px',
                    'whiteSpace': 'normal'
                },
                style_header={
                    'textAlign': 'center',
                    'backgroundColor': '#0074D9',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'fontSize': '18px'
                },
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Chỉ tiêu} = "A. Lợi nhuận trước thuế"'},
                        'backgroundColor': '#C8E6C9',
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'filter_query': '{Chỉ tiêu} contains "Tổng thu nhập"'},
                        'backgroundColor': '#D0E0F0',
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'filter_query': '{Chỉ tiêu} contains "Chi phí"'},
                        'backgroundColor': '#F5E1A4',
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'filter_query': '{Chỉ tiêu} = "H. Số lượng nhân sự ( Sale Manager )"'},
                        'backgroundColor': '#FFF176',
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    # CHỈ thụt lề cột "Chỉ tiêu" cho các chỉ tiêu phụ
                    *[
                        {
                            'if': {
                                'column_id': 'Chỉ tiêu',
                                'filter_query': f'{{Chỉ tiêu}} contains "{prefix}"'
                            },
                            'paddingLeft': '20px'
                        } for prefix in ["B1", "B2", "B3", "B4", "B5",
                                         "C1", "C2",
                                         "D1", "D2", "D3",
                                         "F1", "F2", "F3"]
                    ]
                ]
            )
        ], className="px-3", style={"marginBottom": "0px", "paddingBottom": "0px"})
    ], style={"paddingBottom": "0px", "marginBottom": "0px"})

# Callback definition
@callback(
    [Output("data-table-baocao", "data"),
     Output("data-table-baocao", "columns")],
    [Input("month-dropdown-baocao", "value")]
)
def update_table(month):
    data, columns = update_dashboard_baocao(month)
    return data, columns 