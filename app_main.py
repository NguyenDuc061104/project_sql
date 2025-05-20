import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from app_finance import finance_layout 
from app_asm import asm_layout
from app_bckd import bckd_layout
from app_rpt_area import baocao_tonghop_layout
from app_rpt_asm import baocao_xh_layout
from app_flowchart import flowchart_layout
from app_business import business_layout


# Config server
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Multi-page Dashboard"
server = app.server

# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.Div(
                [
                    dbc.NavbarBrand(
                        "Trung Tâm Tài Chính Báo Cáo Dữ liệu",
                        className="fw-bold text-white",
                        style={"fontSize": "30px"}
                    ),
                ],
                style={
                    "position": "absolute",
                    "left": "50%",
                    "transform": "translateX(-50%)",
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                }
            ),
            dbc.Nav(
                [
                    dbc.DropdownMenu(
                        label="📑 Đề tài",
                        children=[
                            dbc.DropdownMenuItem("Yêu cầu", href="/yeucau"),
                            # dbc.DropdownMenuItem("Nghiệp vụ", href="/nghiepvu"),
                        ],
                        nav=True,
                        in_navbar=True,
                        className="me-3",
                        style={"fontSize": "18px"}
                    ),
                    dbc.DropdownMenu(
                        label="📑 Báo cáo",
                        children=[
                            dbc.DropdownMenuItem("Tổng hợp khu vực", href="/tonghop"),
                            dbc.DropdownMenuItem("Xếp hạng nhân sự khu vực", href="/xephang"),
                        ],
                        nav=True,
                        in_navbar=True,
                        className="me-3",
                        style={"fontSize": "18px"}
                    ),
                    dbc.DropdownMenu(
                        label="📈 Bảng biểu đồ",
                        children=[
                            dbc.DropdownMenuItem("Báo cáo tổng quan", href="/baocaokinhdoanh"),
                            dbc.DropdownMenuItem("Chi phí lũy kế năm", href="/finance"),
                            dbc.DropdownMenuItem("Đánh giá ASM", href="/asm"),
                        ],
                        nav=True,
                        in_navbar=True,
                        style={"fontSize": "18px"}
                    ),
                ],
                className="ms-auto",
                navbar=True
            ),
        ],
        fluid=True,
        className="position-relative"
    ),
    color="primary",
    dark=True,
    className="mb-3 shadow-sm"
)

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', className="p-4")
])

# Logic hiển thị trang
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/yeucau':
        return flowchart_layout()
    elif pathname == '/xephang':
        return baocao_xh_layout()
    elif pathname == '/baocaokinhdoanh':
        return bckd_layout
    elif pathname == '/finance':
        return finance_layout
    elif pathname == '/asm':
        return asm_layout
    elif pathname in ["/", "/tonghop"]:
        return baocao_tonghop_layout()
    # elif pathname == '/nghiepvu':
    #     return business_layout()
    else:
        return html.Div("Không tìm thấy trang.", className="text-center mt-5")

# Chạy app
if __name__ == '__main__':
    app.run_server(debug=True)
