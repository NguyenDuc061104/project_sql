from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table
from db import get_Data
def create_layout():
        df = get_Data()
        return html.Div([
        html.H1("Bảng Area Code", style={"textAlign": "center"}),

        dash_table.DataTable(
            id='area_code_table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,  # Hiển thị 10 dòng trên mỗi trang
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={
                'backgroundColor': 'lightblue',
                'fontWeight': 'bold'
            }
    )
])



# Thiết kế phần layout của ứng dụng
# def create_layout():
#     return html.Div([
#         # Navigation Bar
#         dbc.NavbarSimple(
#             children=[
#                 dbc.NavItem(dbc.NavLink("Báo cáo tổng hợp", href="/")),
#                 dbc.NavItem(dbc.NavLink("Báo cáo xếp hạng", href="/xh"))
#             ],
#             brand=html.Div("Báo cáo tài chính", style={
#             "fontSize": "28px", 
#             "fontWeight": "bold", 
#             "textAlign": "center",
#              "width": "100%"
#             }),
#     brand_href="/",
#     color="primary",
#     dark=True
#         ),
        
#         # dcc.Location giúp theo dõi URL và điều hướng nội dung
#         dcc.Location(id='url', refresh=False),
        
#         # Nội dung thay đổi theo URL
#         html.Div(id='page-content')
#     ])

# Trang Báo cáo Tổng hợp

# def baocao_tonghop_layout():
#     return html.Div([
#         html.H1("Báo cáo tổng hợp", className="text-center mt-4"),
#         dbc.Row([
#             dbc.Col([
#                 html.Label("Chọn Tháng - Báo cáo Tổng hợp"),
#                 dcc.Dropdown(
#                     id="month-dropdown-baocao",
#                     options=[{"label": f"Tháng {m} - 2023", "value": m} for m in range(1, 6)],
#                     value=1,  # Mặc định là tháng 1
#                     clearable=False
#                 ),
#             ], width=3),
#         ], className="mb-4"),

#         dash_table.DataTable(
#             id='data-table-baocao',
#             columns=[],
#             data=[],
#             style_table={'overflowX': 'auto', 'maxHeight': '500px', 'overflowY': 'auto'},
#             style_cell={'textAlign': 'center', 'padding': '10px'},
#             style_header={'backgroundColor': 'deepskyblue ', 'fontWeight': 'bold'},
#             style_data_conditional=[
#     {
#         'if': {'filter_query': '{Thông tin} = "Lợi nhuận trước thuế"'},
#         'backgroundColor': 'lightgreen',
#         'color': 'black',
#         'fontWeight': 'bold'
#     },
#     {
#         'if': {'filter_query': '{Thông tin} = "Tổng thu nhập từ hoạt động thẻ"'},
#         'backgroundColor': 'powderblue',
#         'color': 'black',
#         'fontWeight': 'bold'
#     },
#     {
#         'if': {'filter_query': '{Thông tin} = "Chi phí thuần KDV"'},
#         'backgroundColor': 'powderblue',
#         'color': 'black',
#         'fontWeight': 'bold'
#     },
#     {
#         'if': {'filter_query': '{Thông tin} = "Chi phí thuần hoạt động khác"'},
#         'backgroundColor': 'powderblue',
#         'color': 'black',
#         'fontWeight': 'bold'
#     },
#     {
#         'if': {'filter_query': '{Thông tin} = "Tổng thu nhập hoạt động"'},
#         'backgroundColor': 'powderblue',
#         'color': 'black',
#         'fontWeight': 'bold'
#     },
#     {
#         'if': {'filter_query': '{Thông tin} = "Tổng chi phí hoạt động"'},
#         'backgroundColor': 'powderblue',
#         'color': 'black',
#         'fontWeight': 'bold'
#     },
#     {
#         'if': {'filter_query': '{Thông tin} = "Chi phí dự phòng"'},
#         'backgroundColor': 'powderblue',
#         'color': 'black',
#         'fontWeight': 'bold'
#     }, 
#     {
#         'if': {'filter_query': '{Thông tin} = "Số lượng nhân sự ( Sale Manager )"'},
#         'backgroundColor': 'yellow',
#         'color': 'black',
#         'fontWeight': 'bold'
#     }
# ]

#         ),
#     ])


# # Trang Báo cáo XH
# def baocao_xh_layout():
#     return html.Div([
#         html.H1("Báo cáo xếp hạng", className="text-center mt-4"),
#         dbc.Row([
#             dbc.Col([
#                 html.Label("Chọn Tháng - Báo cáo XH"),
#                 dcc.Dropdown(
#                     id="month-dropdown-xh",
#                     options=[{"label": f"Tháng {m} - 2023", "value": m} for m in range(1, 6)],
#                     value=1,  # Mặc định là tháng 1
#                     clearable=False
#                 ),
#             ], width=3),
#         ], className="mb-4"),

#         dash_table.DataTable(id='data-table-xh', columns=[], data=[],
#                              style_table={'overflowX': 'auto', 'maxHeight': '500px', 'overflowY': 'auto'},
#                              style_cell={'textAlign': 'center', 'padding': '10px'},
#                              style_header={'backgroundColor': 'deepskyblue', 'fontWeight': 'bold'}),
#     ])
