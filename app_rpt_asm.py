from dash import dcc, html, dash_table, Input, Output, callback
import pandas as pd
import numpy as np
from decimal import Decimal
import dash_bootstrap_components as dbc

# Load data
file2 = 'fact_rpt_rank_202203210922.xlsx'
try:
    df_rank = pd.read_excel(file2)
except FileNotFoundError:
    df_rank = pd.DataFrame()

def format_number(value):
    try:
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return ""
        if isinstance(value, Decimal):
            value = float(value)
        if isinstance(value, (int, float, np.int64, np.float64, np.float32)):
            if abs(value) >= 1_000_000:
                return "{:,.2f}".format(value / 1_000_000)
            return "{:,.0f}".format(value)
        if isinstance(value, str):
            try:
                num_value = float(value.replace(',', ''))
                if abs(num_value) >= 1_000_000:
                    return "{:,.2f}".format(num_value / 1_000_000)
                return "{:,.2f}".format(num_value)
            except ValueError:
                return value
        return str(value)
    except Exception:
        return str(value)

def format_table_data(data):
    if isinstance(data, list):
        return [{key: format_number(value) for key, value in row.items()} for row in data]
    return data

def baocao_xh_layout():
    return html.Div([
        html.H2("📊 BÁO CÁO XẾP HẠNG NHÂN SỰ TOÀN QUỐC", className="text-center mt-4 mb-2", style={
            "fontWeight": "bold", "color": "#003366"
        }),

        html.Div("Theo dữ liệu tổng hợp các chỉ số KPI năm 2023", className="text-center mb-4", style={
            "fontStyle": "italic", "color": "#666", "fontSize": "14px"
        }),

        dbc.Row([
            dbc.Col([
                html.Label("Chọn tháng:", style={"fontWeight": "bold", "fontSize": "15px"}),
                dcc.Dropdown(
                    id="month-dropdown-xh",
                    options=[{"label": f"Tháng {m} - 2023", "value": 202300 + m} for m in range(1, 6)],
                    value=202305,
                    clearable=False,
                    style={"fontSize": "14px"}
                )
            ], md=4),

            dbc.Col([
                html.Label("Chọn khu vực:", style={"fontWeight": "bold", "fontSize": "15px"}),
                dcc.Dropdown(
                    id="area-dropdown-xh",
                    options=[],
                    multi=True,
                    placeholder="Tất cả khu vực...",
                    style={"fontSize": "14px"}
                )
            ], md=6),
        ], className="mb-3 justify-content-center"),

        html.Div([
            dash_table.DataTable(
                id='data-table-xh',
                columns=[],
                data=[],
                style_table={
                    'overflowX': 'auto',
                    'maxHeight': '70vh', 
                    'overflowY': 'auto',
                    'marginBottom': '0px'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '8px',
                    'fontFamily': 'Arial',
                    'fontSize': '15px',
                    'whiteSpace': 'nonspace',
                    'minWidth': '120px'
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
                        'if': {
                            'column_id': 'Xếp hạng tổng',
                            'filter_query': '{Xếp hạng tổng} <= 5'
                        },
                        'backgroundColor': '#C8E6C9',
                        'color': 'black',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'column_id': 'Xếp hạng tổng',
                            'filter_query': '{Xếp hạng tổng} >= 70'
                        },
                        'backgroundColor': '#FFCDD2',
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                ]
            )
        ], className="px-3", style={"marginBottom": "0px", "paddingBottom": "0px"})
    ], style={"paddingBottom": "0px", "marginBottom": "0px"})


@callback(
    Output("data-table-xh", "data"),
    Output("data-table-xh", "columns"),
    Output("area-dropdown-xh", "options"),
    Input("month-dropdown-xh", "value"),
    Input("area-dropdown-xh", "value")
)
def update_dashboard_xh(month_key, selected_areas):
    if df_rank.empty:
        return [], [], []

    df = df_rank[df_rank['month_key'] == month_key].copy()
    df.drop(columns=['month_key'], inplace=True, errors='ignore')

    column_mapping = {
        "area_code": "Mã khu vực",
        "ltn_avg": "Loan to new trung bình",
        "psdn_avg": "Phát sinh dư nợ trung bình",
        "area_name": "Khu vực",
        "email": "Email",
        "tong_diem": "Tổng điểm",
        "rank_final": "Xếp hạng tổng",
        "rank_ltn_avg": "Xếp hạng Dư nợ cho vay",
        "rank_psdn_avg": "Xếp hạng Phát sinh dư nợ",
        "rank_approval_rate_avg": "Xếp hạng Tỷ lệ hồ sơ được duyệt",
        "rank_ptkd": "Xếp hạng Tỷ lệ nợ xấu",
        "rank_cir": "Xếp hạng CIR",
        "rank_margin": "Xếp hạng Margin",
        "rank_fin": "Xếp hạng Điểm tài chính",
        "rank_hsbq_nhan_su": "Xếp hạng Hiệu suất/NS",
        "approval_rate_avg": "Trung bình tỷ lệ hồ sơ được duyệt",
        "npl_truoc_wo_luy_ke":"Nợ xấu tích lũy trước khi xóa sổ",
        "rank_npl_truoc_wo_luy_ke":"Xếp hạng nợ xấu tích lũy trước khi xóa sổ",
        "diem_quy_mo": "Điểm quy mô",
        "diem_fin": "Điểm tài chính",
        "Xếp hạng Hiệu suất/NS": "Xếp hạng Hiệu số/nhân sự",
        "cir": "Cir",
        "margin": "Margin",
        "hs_von": "Hiệu số vốn",
        "rank_hs_von": "Xếp hạng hiệu số vốn",
        "hsbq_nhan_su": "Hiệu số bình quân/nhân sự",

    }

    df.rename(columns=column_mapping, inplace=True)
    if selected_areas:
        df = df[df["Khu vực"].isin(selected_areas)]

    area_options = [{"label": area, "value": area} for area in sorted(df["Khu vực"].unique())]
    data = format_table_data(df.to_dict('records'))
    columns = [{"name": col, "id": col} for col in df.columns]

    return data, columns, area_options
