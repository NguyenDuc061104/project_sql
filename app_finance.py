from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# ═════════════════ INIT APP ═════════════════
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ═════════════════ LOAD DATA ═════════════════
file_path = "fact_rpt_loss_area_202203210922.xlsx"          # <-- đường dẫn file excel
df = pd.read_excel(file_path)
df["month_key"] = pd.to_datetime(df["month_key"], format="%Y%m")
df = df[(df["month_key"] >= "2023-01-01") & (df["month_key"] <= "2023-05-31")]

# ═════════════════ SUB-TABLES ═════════════════
df_cir      = df[df["information"] == "I. CIR(%)"]
df_margin   = df[df["information"] == "K. Margin(%)"]
df_perf     = df[df["information"] == "M. Hiệu suất BQ/ Nhân sự"]
df_profit   = df[df["information"] == "A. Lợi nhuận trước thuế(E+F+G)"]
df_income   = df[df["information"] == "B. Tổng thu nhập từ hoạt động thẻ(B1+B2+B3+B4+B5)"]
df_action   = df[df["information"] == "D. Chi phí thuần hoạt động khác(D1+D2+D3)"]
df_thuankdv = df[df["information"] == "C. Chi phí thuần KDV(C1+C2)"]
df_duphong  = df[df["information"] == "G. Chi phí dự phòng"]
df_staff = df[df["information"] == "F1. CP nhân viên"]
df_manage = df[df["information"] == "F2. CP quản lý"]
df_asset = df[df["information"] == "F3. CP tài sản"]

region_names = {
    "tay_nam_bo":  "Tây Nam Bộ",
    "tay_bac_bo":  "Tây Bắc Bộ",
    "nam_trung_bo":"Nam Trung Bộ",
    "dong_nam_bo": "Đông Nam Bộ",
    "dong_bac_bo": "Đông Bắc Bộ",
    "db_song_hong":"Đồng bằng Sông Hồng",
    "bac_trung_bo":"Bắc Trung Bộ"
}
region_keys = list(region_names.keys())


def chart_card(component, title):
    """Card bao biểu đồ + tiêu đề (tiêu đề căn giữa, CHỮ IN HOA, nền xanh)."""
    return dbc.Card(
        [
            dbc.CardHeader(
                title.upper(),                       # ép thành CHỮ HOA
                className="fw text-center text-white",
                style={
                    "backgroundColor": "#1E88E5",    # nền xanh đậm
                    "textTransform": "uppercase"     # (phòng khi bạn quên .upper())
                }
            ),
            dbc.CardBody(component, style={"padding": 10})
        ],
        className="shadow-sm h-100",
        style={
            "border": "2px solid #1E88E5",
            "borderRadius": "10px"
        }
    )

# ═════════════════ HELPERS ═════════════════
def wrap_label(text: str) -> str:
    """Mỗi từ xuống 1 dòng để nhãn hẹp, không chồng lấn."""
    return "<br>".join(text.split())

def get_chart_data(df_type: pd.DataFrame, month: pd.Timestamp) -> dict:
    return {
        k: abs(df_type[df_type["month_key"] == month][k].iloc[0])
        if not df_type[df_type["month_key"] == month][k].empty else 0
        for k in region_keys
    }

def chart_trend(region_selected: str):
    fig = go.Figure()
    months = df_income["month_key"].dt.strftime("%Y/%m").unique()
    show_regions = region_keys if region_selected in (None, "all") else [region_selected]
    for r in show_regions:
        y = [df_income[df_income["month_key"].dt.strftime("%Y/%m") == m][r].iloc[0] / 1e9
             if not df_income[df_income["month_key"].dt.strftime("%Y/%m") == m][r].empty else 0
             for m in months]
        fig.add_trace(go.Scatter(x=months, y=y, mode="lines+markers", name=region_names[r]))
    
    fig.update_layout(
        colorway=["#4C3BCF", "#295AB7", "#14FEC6", "#FEEB82",
                  "#4B70F5", "#0D74B1", "#3DC2EC"],
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(
            ticksuffix=" tỷ",
            tickformat=",.0f",
        ),
    )
    return fig

def chart_profit_income(month: str, region_selected: str):
    staff = get_chart_data(df_staff, pd.to_datetime(month))
    manage = get_chart_data(df_manage, pd.to_datetime(month))
    asset = get_chart_data(df_asset, pd.to_datetime(month))
    sel = region_keys if region_selected in (None, "all") else [region_selected]
    labels = [wrap_label(region_names[r]) for r in sel]

    fig = go.Figure([
        go.Bar(x=labels, y=[staff[r] / 1e9 for r in sel], name="Chi phí nhân viên", marker_color="#0D74B1"),
        go.Bar(x=labels, y=[manage[r] / 1e9 for r in sel], name="Chi phí quản lý", marker_color="#295AB7"),
        go.Bar(x=labels, y=[asset[r] / 1e9 for r in sel], name="Chi phí tài sản", marker_color="#3DC2EC")
    ])
    fig.update_layout(
        barmode="group",
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=30),
        xaxis=dict(tickangle=0, automargin=True, tickfont=dict(size=11)),
        yaxis=dict(
            tickformat=".0f",
            ticksuffix=" tỷ",
            automargin=True
        )
    )
    return fig


# ═════════════════ COMMENT BOX ═════════════════
def generate_comment(_, __):
    return html.Div(
        [
            html.P([
                "    Chi phí hoạt động trong 5 tháng đầu này tăng ",
                html.B("~50%"),
                " mỗi tháng"
            ]),
            html.P([
                "    Tây Nam Bộ là khu vực có xu hướng thu nhập tốt nhất, trong khi Bắc Trung Bộ có xu hướng thu nhập thấp nhất."
            ]),
            html.P([
                "    Chi phí dự phòng là khoản chi chủ đạo: luôn > ",
                html.B("2/3"),
                " tổng chi. Chi phí thuần KDV dao động (≈ ",
                html.B("15 – 30 %"),
                ") và Bắc Trung Bộ là ngoại lệ – tỷ trọng KDV cao nhất, hoạt động kinh doanh dịch vụ (KDV) ở vùng này cần được xem kỹ về hiệu quả."
            ]),
            html.Hr(),
        ],
        style={"overflowY": "auto"}
    )


# ═════════════════ LAYOUT HELPERS ═════════════════
CHART_HEIGHT = "42vh"

def card(component, dashed=False, grow=False):
    style = {
        "border": f"2px {'dashed' if dashed else 'solid'} #1E88E5",
        "borderRadius": "10px",
        "height": CHART_HEIGHT if not grow else "100%",
        "padding": "8px"
    }
    class_name = "mb-3"
    if grow:
        class_name += " flex-fill d-flex"
    return dbc.Card(dbc.CardBody(component, style={"height": "100%"}),
                    className=class_name, style=style)

# ═════════════════ SIDEBAR ═════════════════
sidebar_controls = dbc.Card(
    dbc.CardBody([
        html.Label("Chọn tháng:", className="fw-bold mb-1"),
        dcc.Dropdown(id="month-dropdown",
                     options=[{"label": f"Tháng {i}/2023", "value": f"2023-0{i}-01"} for i in range(1, 6)],
                     value="2023-05-01", clearable=False),
        html.Br(),
        html.Label("Chọn khu vực:", className="fw-bold mb-1"),
        dcc.Dropdown(id="region-dropdown",
                     options=[{"label": "Tất cả khu vực", "value": "all"}] +
                             [{"label": v, "value": k} for k, v in region_names.items()],
                     value="all", clearable=False),
    ]),
    className="mb-3",
    style={"border": "2px solid #1E88E5", "borderRadius": "10px"}
)
# Card "Nhận xét" trong thanh bên
sidebar_comment = chart_card(
    html.Div(
        id="comment-box",
        style={
            "height": "100%",          # cho phép card dãn chiều cao
            "overflowY": "auto"        # cuộn khi nội dung dài
        }
    ),
    "Nhận xét"
)


sidebar = dbc.Col(
    [sidebar_controls, sidebar_comment],
    md=3, xs=12,
    className="d-flex flex-column h-100 pe-2"  # Padding phải để tách với main panel
)

# MAIN PANEL
main_panel = dbc.Col(
    [
        dbc.Row([
            dbc.Col(
                chart_card(dcc.Graph(id="trend-chart", style={"height": "100%"}), "Xu hướng thu nhập"),
                md=6, xs=12
            ),
            dbc.Col(
                chart_card(dcc.Graph(id="profit-income-chart", style={"height": "100%"}), "Phân bổ chi phí hoạt động"),
                md=6, xs=12
            ),
        ], className="gx-2"),
        dbc.Row([
            dbc.Col(
                chart_card(dcc.Graph(id="cost-distribution-chart", style={"height": "100%"}), "Tỷ trọng chi phí theo khu vực"),
                md=6, xs=12
            ),
            dbc.Col(
                chart_card(dcc.Graph(id="cost-distribution-stacked100", style={"height": "100%"}), "Phân bổ các loại chi phí"),
                md=6, xs=12
            ),
        ], className="gx-2")
    ],
    md=9, xs=12,
    className="ps-2"  # Padding trái để tách khỏi sidebar
)


finance_layout = dbc.Container(
    [
        html.H2("BÁO CÁO THEO DÕI CHI PHÍ TOÀN HÀNG", className="text-center my-3 fw-bold"),
        dbc.Row([sidebar, main_panel], className="g-0")
    ],
    fluid=True, style={"maxWidth": "1600px"}
)

# ═════════════════ CALLBACKS ═════════════════
@callback(
    Output("trend-chart", "figure"),
    Output("profit-income-chart", "figure"),
    Output("comment-box", "children"),
    Input("month-dropdown", "value"),
    Input("region-dropdown", "value")
)
def update_main(month, region):
    return chart_trend(region), chart_profit_income(month, region), generate_comment(month, region)

# ---- Pie chart chi phí ----
@callback(Output("cost-distribution-chart", "figure"), Input("month-dropdown", "value"))
def cost_pie(month):
    m = pd.to_datetime(month)
    act = get_chart_data(df_action, m)
    kdv = get_chart_data(df_thuankdv, m)
    dp  = get_chart_data(df_duphong,  m)
    total = {r: act[r] + kdv[r] + dp[r] for r in region_keys}

    fig = go.Figure(go.Pie(
        labels=[region_names[r] for r in region_keys],
        values=[total[r] for r in region_keys],
        marker=dict(
        colors=[  # danh sách màu cho mỗi slice
            "#4C3BCF", "#295AB7", "#14FEC6", "#FEEB82",
            "#4B70F5", "#0D74B1", "#3DC2EC"
        ],
        line=dict(color="white", width=2)
        ),
        textinfo="percent",
        textposition="inside",             # <<< luôn trong lát cắt
        insidetextorientation="horizontal",
        textfont_size=12
    ))
    fig.update_layout(template="plotly_white",
                      margin=dict(l=20, r=20, t=40, b=20))
    return fig

# ---- Stacked 100 % ----
@callback(Output("cost-distribution-stacked100", "figure"), Input("month-dropdown", "value"))
def cost_pct(month):
    m = pd.to_datetime(month)
    act, kdv, dp = (get_chart_data(df_action, m),
                    get_chart_data(df_thuankdv, m),
                    get_chart_data(df_duphong, m))
    df_plot = pd.DataFrame({
        "area": [wrap_label(region_names[r]) for r in region_keys],
        "act":  [act[r] for r in region_keys],
        "kdv":  [kdv[r] for r in region_keys],
        "dp":   [dp[r]  for r in region_keys],
    })
    tot = df_plot[["act", "kdv", "dp"]].sum(axis=1)
    df_pct = df_plot.copy()
    df_pct[["act", "kdv", "dp"]] = df_plot[["act", "kdv", "dp"]].div(tot, axis=0) * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_pct["area"], y=df_pct["act"], name="Chi phí thuần HĐ khác",marker_color="#295AB7"))
    fig.add_trace(go.Bar(x=df_pct["area"], y=df_pct["kdv"], name="Chi phí thuần KDV",marker_color="#0D74B1"))
    fig.add_trace(go.Bar(x=df_pct["area"], y=df_pct["dp"], name="Chi phí dự phòng", marker_color="#3DC2EC"))
    fig.update_layout(
        barmode="stack",
        template="plotly_white",
        margin=dict(l=20, r=10, t=40, b=30),
        yaxis=dict(range=[0, 100],tickformat=".0f",
            ticksuffix=" tỷ",
            automargin=True),
        xaxis=dict(tickangle=0, automargin=True, tickfont=dict(size=11))
    )
    return fig