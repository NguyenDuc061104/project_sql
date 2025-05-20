# ─────────────────────────── app.py ────────────────────────────────────────────
from dash import Dash, html, dcc, dash_table, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

# 1 ── APP & GIAO DIỆN ─────────────────────────────────────────────────────────
external_stylesheets = [
    dbc.themes.MINTY,
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap"
]
app    = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server    # cần cho deploy Heroku/Vercel …

# 2 ── DỮ LIỆU ─────────────────────────────────────────────────────────────────
file2       = "fact_rpt_rank_202203210922.xlsx"
df_rank     = pd.read_excel(file2)
list_months = [202301, 202302, 202303, 202304, 202305]
df_rank     = df_rank[df_rank["month_key"].isin(list_months)]

# 3 ── MÀU KHU VỰC ─────────────────────────────────────────────────────────────
area_color_map = {
    "Tây Bắc Bộ":          "#4C3BCF",
    "Đông Bắc Bộ":         "#295AB7",
    "Đồng Bằng Sông Hồng": "#14FEC6",
    "Đông Nam Bộ":         "#FEEB82",
    "Nam Trung Bộ":        "#4B70F5",
    "Bắc Trung Bộ":        "#0D74B1",
    "Tây Nam Bộ":          "#3DC2EC",
}

# 4 ── TIỆN ÍCH CARD ───────────────────────────────────────────────────────────
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
            dbc.CardBody(component, style={"padding": 0})
        ],
        className="shadow-sm h-100",
        style={
            "border": "2px solid #1E88E5",
            "borderRadius": "10px"
        }
    )


# 5 ── COMPONENT RIÊNG LẺ ──────────────────────────────────────────────────────
dropdown_card = dbc.Card(
    dbc.CardBody([
        html.Label("Chọn tháng:", className="fw-bold"),
        dcc.Dropdown(
            id="month-dropdown",
            options=[
                {"label": f"Tháng {str(m)[4:]}/{str(m)[:4]}", "value": m}
                for m in list_months
            ],
            value=list_months[0],
            clearable=False
        )
    ]),
    className="shadow-sm",
    style={
        "border": "2px solid #1E88E5",
        "borderRadius": "10px"
    }
)

comment_card = dbc.Card(
    [
        # Tiêu đề
        dbc.CardHeader(
            "NHẬN XÉT",
            className="fw-bold text-center text-white",
            style={
                "backgroundColor": "#1E88E5",
                "textTransform": "uppercase"
            },
        ),

        # Nội dung
        dbc.CardBody(
            dbc.Alert(
                id="comment-section",
                color = "light",
                className="mb-0 border",        # thêm border nếu muốn khung
                style={"fontSize": "18px"}      # cỡ chữ
            )
        ),
    ],
    className="shadow-sm",
)

table_card = dbc.Card(
    dbc.CardBody(
        dash_table.DataTable(
            id="top10-table",
            data=[], columns=[],
            style_table={"overflowX": "auto"},
            style_header={
                "backgroundColor": "#0d6efd", "color": "white",
                "fontWeight": "bold", "fontSize": "17px"
            },
            style_cell={
                "textAlign": "center", "fontSize": "15px",
                "fontFamily": "Poppins, sans-serif"
            }
        )
    ),
    className="shadow-sm h-100",
    style={
        "border": "2px solid #1E88E5",
        "borderRadius": "10px"
    }
)

# 6 ── BỐ CỤC ──────────────────────────────────────────────────────────────────
asm_layout = dbc.Container([
    html.H2(
        "BÁO CÁO ĐÁNH GIÁ ASM",
        className="text-center my-4 fw-bold",
    ),

    dbc.Row([
        # ---- CỘT TRÁI (Dropdown + Nhận xét) ----------------------------------
        dbc.Col(
            [dropdown_card, comment_card],
            md=3,
            className="gy-4 mb-4"
        ),

        # ---- CỘT PHẢI (Chart + Table) ----------------------------------------
        dbc.Col(
            [
                dbc.Row([
                    dbc.Col(
                        chart_card(dcc.Graph(id="ranking-chart"),
                                   "Xếp hạng nhân sự"),
                        md=6, className="mb-4"
                    ),
                    dbc.Col(
                        chart_card(dcc.Graph(id="asm-area-pie"),
                                   "Tổng ASM theo khu vực"),
                        md=6, className="mb-4"
                    )
                ], className="gy-4"),

                dbc.Row([
                    dbc.Col(
                        chart_card(dcc.Graph(id="top10-area-stacked"),
                                   "Số ASM trong Top 10 – theo khu vực"),
                        md=6, className="mb-4"
                    ),
                    dbc.Col(
                        table_card,
                        md=6, className="mb-4"
                    )
                ], className="gy-4")
            ],
            md=9
        )
    ], className="gy-4")
], fluid=True, style={"fontFamily": "Poppins, sans-serif"})

# 7 ── COMMENT DICT ────────────────────────────────────────────────────────────
comments = {
    202301: "Ở tháng 1/2023, nhân viên có kết quả kinh doanh tốt nhất là Hoàng Văn Nam của khu vực Đồng Bằng Sông Hồng. Tổng quan, trong top 10 saler tốt nhất đều thuộc 3 khu vực Bắc Trung Bộ, Nam Trung Bộ, và Đồng Bằng Sông Hồng",
    202302: "Ở tháng 2/2023, nhân viên có kết quả kinh doanh tốt nhất là Hoàng Văn Nam của khu vực Đồng Bằng Sông Hông. Điểm tài chính của khu vực Đông Nam Bộ cao nhất với 26 điểm và thấp nhất là Nam Trung Bộ",
    202303: "Ở tháng 3/2023, nhân viên có kết quả kinh doanh tốt nhất là Hoàng Văn Nam của khu vực Đồng Bằng Sông Hồng, nhờ vào điểm tài chính thấp phân bổ theo khu vực của nhân viên đó, và lần đầu tiên Tây Bắc Bộ có nhân viên nằm trong top 10 saler tốt nhất",
    202304: "Ở tháng 4/2023, nhân viên có kết quả kinh doanh tốt nhất là Hoàng Thị Hà của khu vực Nam Trung Bộ. 3 khu vực Bắc Trung Bộ, Nam Trung Bộ, và Đồng Bằng Sông Hồng chiếm tất cả trong vị trí top 10 saler tốt nhất",
    202305: "Ở tháng 5/2023, nhân viên có kết quả kinh doanh tốt nhất là Hoàng Thị Hà của khu vực Nam Trung Bộ.  Chỉ có 1 saler của Bắc Trung Bộ nằm trong top 10, còn lại đều thuộc về Nam Trung Bộ và Đồng Bằng Sông Hồng"
}

# 8 ── CALLBACKS ───────────────────────────────────────────────────────────────
@callback(
    Output("ranking-chart", "figure"),
    Output("asm-area-pie", "figure"),
    Output("comment-section", "children"),
    Input("month-dropdown", "value")
)
def update_charts(month_key):
    df = df_rank[df_rank["month_key"] == month_key]

    # Bar ---------------------------------------------------------------------
    top12 = df.sort_values("tong_diem").head(12)
    bar = go.Figure(go.Bar(
        y=top12["email"],
        x=top12["tong_diem"],
        orientation="h",
        marker=dict(
            color=top12["area_name"].map(area_color_map).fillna("#bdbdbd"),
            line=dict(color="white", width=1)
        ),
        text=top12["tong_diem"],
        textposition="auto",
        customdata=top12[["area_name"]],
        hovertemplate="<b>Email:</b> %{y}<br><b>Khu vực:</b> %{customdata[0]}"
                      "<br><b>Tổng điểm:</b> %{x}<extra></extra>"
    ))
    bar.update_layout(
        template="plotly_white", height=320,
        margin=dict(t=50, l=140, r=15, b=10)
    )
    bar.update_yaxes(autorange="reversed")

    # Pie ---------------------------------------------------------------------
    pie_df = df.groupby("area_name")["email"].nunique().reset_index(name="SoASM")
    pie = go.Figure(go.Pie(
        labels=pie_df["area_name"],
        values=pie_df["SoASM"],
        marker=dict(
            colors=pie_df["area_name"].map(area_color_map).fillna("#bdbdbd"),
            line=dict(color="white", width=2)
        ),
        textinfo="percent",
        textposition="inside",
        hovertemplate="<b>Khu vực:</b> %{label}<br>Số ASM: %{value}<extra></extra>"
    ))
    pie.update_layout(
        template="plotly_white", height=320,
        margin=dict(t=50, l=15, r=15, b=10),
        showlegend=True
    )

    return bar, pie, comments.get(month_key, "Chưa có nhận xét")

# -----------------------------------------------------------------------------        
@callback(
    Output("top10-table", "data"),
    Output("top10-table", "columns"),
    Output("top10-table", "style_data_conditional"),
    Input("month-dropdown", "value")
)
def update_table(month_key):
    df_m  = df_rank[df_rank["month_key"] == month_key]
    top10 = df_m.sort_values("rank_final").head(10)[[
        "email", "rank_final", "rank_ltn_avg", "rank_psdn_avg",
        "rank_approval_rate_avg", "rank_ptkd"
    ]]
    top10.columns = [
        "Email", "XH Tổng", "XH Dư nợ", "XH Phát sinh",
        "XH % hồ sơ duyệt", "XH % nợ xấu"
    ]
    summary = pd.DataFrame(top10.iloc[:, 1:].sum()).T
    summary.insert(0, "Email", "Tổng cộng")
    df_show = pd.concat([top10, summary], ignore_index=True)

    return (
        df_show.to_dict("records"),
        [{"name": c, "id": c} for c in df_show.columns],
        [{
            "if": {"row_index": len(df_show) - 1},
            "backgroundColor": "#f2f2f2",
            "fontWeight": "bold"
        }]
    )

# -----------------------------------------------------------------------------        
@callback(
    Output("top10-area-stacked", "figure"),
    Input("month-dropdown", "value")
)
def update_stacked(month_key):
    df_m  = df_rank[df_rank["month_key"] == month_key]
    top10 = df_m.sort_values("rank_final").head(10)
    counts = top10["area_name"].value_counts().reset_index()
    counts.columns = ["area_name", "SoASM"]
    counts["color"] = counts["area_name"].map(area_color_map).fillna("#bdbdbd")

    fig = go.Figure(go.Bar(
        x=counts["area_name"],
        y=counts["SoASM"],
        marker=dict(color=counts["color"]),
        text=counts["SoASM"],
        textposition="auto",
        hovertemplate="<b>Khu vực:</b> %{x}<br>Số ASM Top10: %{y}<extra></extra>"
    ))
    fig.update_layout(
        template="plotly_white", height=350,
        # title="📊 ASM Top 10 – theo khu vực",
        title_x=0.5,
        xaxis_title="Khu vực",
        yaxis_title="Số ASM"
    )
    return fig

