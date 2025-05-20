# app.py ───────────────────────────────────────────────────────────
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# ═════════════════ CONSTANTS ═════════════════
CHART_H = 280  # Chiều cao chuẩn cho tất cả biểu đồ (px)
COMMON_LAYOUT = dict(
    template="plotly_white",
    margin=dict(l=20, r=20, t=20, b=20),
    autosize=True  # Cho phép Plotly tự co giãn theo container
)

# ═════════════════ INIT APP ═════════════════
external_stylesheets = [
    dbc.themes.FLATLY,
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap",
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# ═════════════════ LOAD DATA ═════════════════
file1 = "fact_rpt_loss_area_202203210922.xlsx"
df = pd.read_excel(file1)

df["month_key"] = pd.to_datetime(df["month_key"], format="%Y%m")
START_DATE, END_DATE = "2023-01-01", "2023-05-31"
df = df[(df["month_key"] >= START_DATE) & (df["month_key"] <= END_DATE)]

# ═════════════════ SUB‑TABLES ═════════════════
df_profit = df[df["information"] == "A. Lợi nhuận trước thuế(E+F+G)"]
df_income = df[df["information"] == "E. Tổng thu nhập hoạt động(B+C+D)"]
df_margin = df[df["information"] == "K. Margin(%)"]
df_cir = df[df["information"] == "I. CIR(%)"]
df_action = df[df["information"] == "D. Chi phí thuần hoạt động khác(D1+D2+D3)"]
df_kdv = df[df["information"] == "C. Chi phí thuần KDV(C1+C2)"]
df_duphong = df[df["information"] == "G. Chi phí dự phòng"]

# ═════════════════ REGION MAPPING ═════════════════
area_mapping = {
    "db_song_hong": "Đồng Bằng Sông Hồng",
    "dong_nam_bo": "Đông Nam Bộ",
    "tay_nam_bo": "Tây Nam Bộ",
    "dong_bac_bo": "Đông Bắc Bộ",
    "tay_bac_bo": "Tây Bắc Bộ",
    "bac_trung_bo": "Bắc Trung Bộ",
    "nam_trung_bo": "Nam Trung Bộ",
}
area_color_map = {
    "Tây Bắc Bộ": "#4C3BCF",
    "Đông Bắc Bộ": "#295AB7",
    "Đồng Bằng Sông Hồng": "#14FEC6",
    "Đông Nam Bộ": "#FEEB82",
    "Nam Trung Bộ": "#4B70F5",
    "Bắc Trung Bộ": "#0D74B1",
    "Tây Nam Bộ": "#3DC2EC",
}

region_keys = list(area_mapping.keys())
BRAND_COLOR = "#1E88E5"

# ═════════════════ UI HELPERS ═════════════════

def chart_card(component, title):
    return dbc.Card(
        [
            dbc.CardHeader(
                title.upper(),
                className="fw-bold text-center text-white",
                style={"backgroundColor": BRAND_COLOR, "textTransform": "uppercase"},
            ),
            dbc.CardBody(component, style={"padding": 0}),
        ],
        className="shadow-sm h-100",
        style={"border": f"2px solid {BRAND_COLOR}", "borderRadius": "10px"},
    )


def create_card(title, value, color, delta=None):
    delta_txt, d_color = "N/A", "#333"
    if isinstance(delta, (int, float)):
        arrow = "▲" if delta > 0 else "▼"
        delta_txt = f"{arrow} {abs(delta):.2f} tỷ so với tháng trước"
        d_color = "green" if delta > 0 else "red"
    
    # display_val = abs(value) if isinstance(value, (int, float)) else value
    return dbc.Card(
        [
            html.H6(title, className="text-center mt-1"),
            html.H4(f"{value:.2f} tỷ" if value else "N/A", className="text-center fw-bold", style={"color": color}),
            html.P(delta_txt, className="text-center mb-0", style={"color": d_color, "fontSize": "12px"}),
        ],
        style={"border": f"2px solid {BRAND_COLOR}", "borderRadius": "10px", "padding": "12px"},
    )

# ═════════════════ KPI CALCULATION ═════════════════

def kpi_value(info_code, month, region):
    df_sub = df[df["information"] == info_code]
    if region == "all":
        return df_sub[df_sub["month_key"] == month][region_keys].astype(float).sum(axis=1).iloc[0] / 1e9
    return float(df_sub.loc[df_sub["month_key"] == month, region].iloc[0]) / 1e9


def total_cost(month, region):
    def _sum(df_part):
        return df_part[df_part["month_key"] == month][region_keys].astype(float).sum(axis=1).iloc[0]

    if region == "all":
        total = _sum(df_action) + _sum(df_kdv) + _sum(df_duphong)
        return total / 1e9
    return (
        float(df_action.loc[df_action["month_key"] == month, region].iloc[0])
        + float(df_kdv.loc[df_kdv["month_key"] == month, region].iloc[0])
        + float(df_duphong.loc[df_duphong["month_key"] == month, region].iloc[0])
    ) / 1e9


def get_val(df_sub, month, region):
    if region == "all":
        return df_sub[df_sub["month_key"] == month][region_keys].astype(float).sum(axis=1).iloc[0]
    return float(df_sub.loc[df_sub["month_key"] == month, region].iloc[0])

# ═════════════════ CHART: COST & CIR ═════════════════

def generate_cost_cir_chart(df_month):
    area_mapping_br = {
        key: val.replace(" ", "<br>") for key, val in area_mapping.items()
    }

    # Danh sách cột khu vực
    columns_to_melt = [col for col in df_month.columns if col not in ["id", "head", "month_key", "information"]]

    # Lọc và melt
    df_fee = df_month[df_month["information"] == "F. Tổng chi phí hoạt động(F1+F2+F3)"]
    df_cir = df_month[df_month["information"] == "I. CIR(%)"]

    df_fee_melted = df_fee.melt(id_vars=["month_key", "information"], value_vars=columns_to_melt, var_name="region", value_name="Chi phí")
    df_cir_melted = df_cir.melt(id_vars=["month_key", "information"], value_vars=columns_to_melt, var_name="region", value_name="CIR")

    df_combined = pd.merge(df_fee_melted, df_cir_melted, on="region")

    # Chuẩn hóa số liệu
    df_combined["Chi phí"] = pd.to_numeric(df_combined["Chi phí"], errors="coerce").abs() / 1e9
    df_combined["CIR"] = pd.to_numeric(df_combined["CIR"], errors="coerce").abs()
    if df_combined["CIR"].max() > 1:
        df_combined["CIR"] /= 100

    x_labels = [area_mapping_br.get(r, r) for r in df_combined["region"]]

    # Biểu đồ
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=x_labels, y=df_combined["Chi phí"], name="Chi phí hoạt động", marker_color="#00bfae", yaxis="y1")
    )
    fig.add_trace(
        go.Scatter(x=x_labels, y=df_combined["CIR"], name="CIR (%)", mode="lines+markers", line=dict(width=3, color="darkblue"), yaxis="y2")
    )

    fig.update_layout(
        yaxis=dict(title="Chi phí", tickformat=",.0f", ticksuffix=" tỷ"),
        yaxis2=dict(title="CIR", overlaying="y", side="right", tickformat=".0%"),
        **COMMON_LAYOUT,
    )

    return fig

# ═════════════════ COMMENT PLACEHOLDER ═════════════════

def comment_chart(month, region):
    label = "các khu vực" if region == "all" else area_mapping[region]

    return html.Div([
        # 1) Tăng trưởng chung 5 tháng
        html.P([
            f"Lợi nhuận trước thuế trong 5 tháng đầu năm tại {label} tăng trưởng ấn tượng ",
            html.B("~50%"),
            ". Tổng thu nhập hoạt động (doanh thu) cũng ghi nhận mức tăng đều đặn ",
            html.B("~60%"),
            " trong cùng kỳ, phản ánh động lực tăng trưởng bền vững."
        ]),

        # 2) Cơ cấu lợi nhuận theo vùng
        html.P([
            "Tây Nam Bộ chiếm khoảng ",
            html.B("2/3"),
            " tổng lợi nhuận; kế đến là Đồng bằng Sông Hồng (",
            html.B("~25%"),
            "). Các vùng còn lại lép vế: mỗi khu vực khác đóng góp dưới ",
            html.B("20%"),
            "."
        ]),

        # 3) Hiệu quả vận hành
        html.P(
            "CIR trung bình và Margin của hầu hết khu vực vẫn ở mức tốt, "
            "cho thấy khả năng kinh doanh ổn định – ngoại trừ CIR khu vực Đông Nam Bộ vẫn chưa tạo ra giá trị tương xứng."
        ),

        html.Hr(style={"margin": "10px 0"}),
    ])


# ═════════════════ LAYOUT ═════════════════

bckd_layout = dbc.Container(
    fluid=True,
    style={"backgroundColor": "#f4f6f8", "padding": "20px"},
    children=[
        dbc.Row(
            dbc.Col(
                html.H2(
                    "BÁO CÁO DOANH THU TOÀN HÀNG",
                    className="text-center",
                    style={"fontFamily": "Poppins", "color": "#2a3f5f", "marginBottom": "10px"},
                )
            )
        ),
        dbc.Row(
            [
                # LEFT ─────────────────────────────────────────────────
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Chọn Tháng:", className="fw-bold mb-1"),
                                    dcc.Dropdown(
                                        id="month-dd",
                                        options=[{"label": f"Tháng {i}/2023", "value": f"2023-{i:02d}-01"} for i in range(1, 6)],
                                        value="2023-05-01",
                                        clearable=False,
                                        style={"fontSize": "14px"},
                                    ),
                                    html.Br(),
                                    html.Label("Chọn Khu vực:", className="fw-bold mb-1"),
                                    dcc.Dropdown(
                                        id="region-dd",
                                        options=[{"label": "Tất cả khu vực", "value": "all"}] + [{"label": v, "value": k} for k, v in area_mapping.items()],
                                        value="all",
                                        clearable=False,
                                        style={"fontSize": "14px"},
                                    ),
                                ]
                            ),
                            style={"border": f"2px solid {BRAND_COLOR}", "borderRadius": "10px"},
                            className="mb-3",
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "NHẬN XÉT",
                                    className="fw-bold text-center text-white",
                                    style={"backgroundColor": BRAND_COLOR, "textTransform": "uppercase"},
                                ),
                                dbc.CardBody(html.Div(id="comment-chart")),
                            ],
                            style={"border": f"2px solid {BRAND_COLOR}", "borderRadius": "10px", "height": "auto"},
                        ),
                    ],
                    width=3,
                    style={"minWidth": "0"},
                ),
                # RIGHT ────────────────────────────────────────────────
                dbc.Col(
                    [
                        dbc.Row(id="kpi-row", className="mb-2"),
                        # Row 1: LN+Margin & Cost‑CIR
                        dbc.Row(
                            [
                                dbc.Col(
                                    chart_card(
                                        dcc.Graph(id="combo-chart", style={"height": f"{CHART_H}px", "width": "100%"}, config={"displayModeBar": False, "responsive": True}),
                                        "Lợi nhuận trước thuế và Margin(%) theo khu vực",
                                    ),
                                    md=6,
                                ),
                                dbc.Col(
                                    chart_card(
                                        dcc.Graph(id="cost-cir-chart", style={"height": f"{CHART_H}px", "width": "100%"}, config={"displayModeBar": False, "responsive": True}),
                                        "TỔNG CHI PHÍ HOẠT ĐỘNG & CIR",
                                    ),
                                    md=6,
                                ),
                            ],
                            className="mb-2",
                        ),
                        # Row 2: Growth & Pie
                        dbc.Row(
                            [
                                dbc.Col(
                                    chart_card(
                                        dcc.Graph(id="growth-chart", style={"height": f"{CHART_H}px", "width": "100%"}, config={"displayModeBar": False, "responsive": True}),
                                        "Tốc độ tăng trưởng",
                                    ),
                                    md=8,
                                ),
                                dbc.Col(
                                    chart_card(
                                        dcc.Graph(id="pie-profit", style={"height": f"{CHART_H}px", "width": "100%"}, config={"displayModeBar": False, "responsive": True}),
                                        "Tỉ trọng lợi nhuận trước thuế",
                                    ),
                                    md=4,
                                ),
                            ]
                        ),
                    ],
                    width=9,
                ),
            ]
        ),
    ],
)

app.layout = bckd_layout

# ═════════════════ CALLBACK ═════════════════

@callback(
    Output("kpi-row", "children"),
    Output("combo-chart", "figure"),
    Output("cost-cir-chart", "figure"),
    Output("growth-chart", "figure"),
    Output("pie-profit", "figure"),
    Output("comment-chart", "children"),
    Input("month-dd", "value"),
    Input("region-dd", "value"),
)
def update_all(month, region):
    month_dt = pd.to_datetime(month)
    prev_dt = month_dt - pd.offsets.MonthBegin(1)

    # KPIs───────────────────────────────────────────────────────────
    ln = kpi_value("A. Lợi nhuận trước thuế(E+F+G)", month_dt, region)
    inc = kpi_value("E. Tổng thu nhập hoạt động(B+C+D)", month_dt, region)
    cost = abs(total_cost(month_dt, region))
    prov = abs(kpi_value("G. Chi phí dự phòng", month_dt, region))

    ln_prev = inc_prev = cost_prev = prov_prev = None
    if prev_dt >= pd.to_datetime(START_DATE):
        ln_prev = kpi_value("A. Lợi nhuận trước thuế(E+F+G)", prev_dt, region)
        inc_prev = kpi_value("E. Tổng thu nhập hoạt động(B+C+D)", prev_dt, region)
        cost_prev = abs(total_cost(prev_dt, region))
        prov_prev = abs(kpi_value("G. Chi phí dự phòng", prev_dt, region))

    kpi_cards = dbc.Row(
        [
            dbc.Col(create_card("Lợi nhuận trước thuế", ln, "#009688", (ln - ln_prev) if ln_prev is not None else None), md=3),
            dbc.Col(create_card("Tổng thu nhập hoạt động", inc, "#009688", (inc - inc_prev) if inc_prev is not None else None), md=3),
            dbc.Col(create_card("Tổng chi phí hoạt động", cost, "#009688", (cost - cost_prev) if cost_prev is not None else None), md=3),
            dbc.Col(create_card("Chi phí dự phòng", prov, "#009688", (prov - prov_prev) if prov_prev is not None else None), md=3),
        ]
    )

    # Combo chart───────────────────────────────────────────────────
    x_keys = [k for k in df_profit.columns[3:] if k != "head"]
    labels = [area_mapping[k] for k in x_keys]

    row_p = df_profit[df_profit["month_key"] == month_dt]
    row_m = df_margin[df_margin["month_key"] == month_dt]
    ln_vals = (row_p[x_keys].astype(float).values[0] / 1e9 if not row_p.empty else [0] * len(x_keys))
    mar_vals = (row_m[x_keys].astype(float).values[0] if not row_m.empty else [0] * len(x_keys))

    fig_combo = go.Figure()
    fig_combo.add_trace(go.Bar(x=labels, y=ln_vals, name="Lợi nhuận trước thuế", marker_color="#FEEB82", yaxis="y1"))
    fig_combo.add_trace(go.Scatter(x=labels, y=mar_vals, name="Margin %", mode="lines+markers", line=dict(width=3, color="#295AB7"), yaxis="y2"))
    fig_combo.update_layout(
    xaxis=dict(tickvals=labels,
               ticktext=[l.replace(" ", "<br>") for l in labels]),
    yaxis=dict(title="Lợi nhuận", ticksuffix=" tỷ", tickformat=",.0f"),
    yaxis2=dict(title="Margin", ticksuffix=" %",overlaying="y", side="right"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="center",   x=0.5),
    **COMMON_LAYOUT,
)

    # Cost‑CIR chart───────────────────────────────────────────────
    fig_cost_cir = generate_cost_cir_chart(df[df["month_key"] == month_dt])

    # Growth chart─────────────────────────────────────────────────
    months_dt = pd.date_range("2023-01-01", month_dt, freq="MS")
    m_labels = [m.strftime("%Y/%m") for m in months_dt]
    ln_t = [kpi_value("A. Lợi nhuận trước thuế(E+F+G)", m, region) for m in months_dt]
    inc_t = [kpi_value("E. Tổng thu nhập hoạt động(B+C+D)", m, region) for m in months_dt]

    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(x=m_labels, y=ln_t, mode="lines+markers", name="Lợi nhuận trước thuế", line=dict(width=3)))
    fig_growth.add_trace(go.Scatter(x=m_labels, y=inc_t, mode="lines+markers", name="Tổng thu nhập hoạt động", line=dict(width=3, color="#FEEB82")))
    fig_growth.update_layout(legend=dict(orientation="h", x=0, y=1.08), yaxis=dict(ticksuffix=" tỷ"), **COMMON_LAYOUT)

    # Pie chart────────────────────────────────────────────────────
    fig_pie = go.Figure(go.Pie(labels=labels, values=ln_vals, marker=dict(colors=[area_color_map.get(l) for l in labels]), textinfo="percent", textposition="outside"))
    fig_pie.update_layout(**COMMON_LAYOUT)

    # Comment──────────────────────────────────────────────────────
    fig_comment = comment_chart(month_dt, region)

    return kpi_cards, fig_combo, fig_cost_cir, fig_growth, fig_pie, fig_comment
