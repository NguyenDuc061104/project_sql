from dash import html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# -----------------------------------------------------------------------------
# DATA PREPARATION
# -----------------------------------------------------------------------------

def _load_business_df(path: str) -> pd.DataFrame:
    """Load Excel and fix cases where the real headers are stored in first row."""
    df = pd.read_excel(path, header=0)
    candidate_header = df.iloc[1].astype(str).str.lower()
    expected = {"index", "name", "description", "calculation"}
    if expected.issubset(set(candidate_header)):
        df.columns = df.iloc[1]
        df = df[1:].reset_index(drop=True)
    return df


df_business = _load_business_df("description.xlsx")

# ------------------------------------------------------------------
# CONSTANTS & STYLES
# ------------------------------------------------------------------
PRIMARY_COLOR   = "#0d6efd"
BORDER_COLOR    = "#1f2d3d"
BORDER_WIDTH    = "2px"

STYLE_TABLE = {
    "overflowY": "auto",
    "maxHeight": "85vh",
    "height": "80vh",
    "width": "100%",
    "borderCollapse": "collapse",
    # ép bảng dùng fixed layout để cột ko tự phình to
    "tableLayout": "fixed",
}

STYLE_CELL = {
    "textAlign": "left",
    "whiteSpace": "normal",   # quan trọng để xuống dòng
    "height": "auto",         # tự giãn theo text
    "padding": "8px 10px",
    "fontFamily": "Roboto, Arial, sans-serif",
    "fontSize": "14px",
    # viền 4 cạnh
    "border": f"{BORDER_WIDTH} solid {BORDER_COLOR}",
}

STYLE_HEADER = {
    "backgroundColor": "#0056b3",
    "color": "white",
    "fontWeight": "700",
    "fontSize": "18px",
    "textAlign": "center",
    "border": f"{BORDER_WIDTH} solid {BORDER_COLOR}",
}

# Quy định kích thước cụ thể cho từng cột
STYLE_CELL_COND = [
    {                       # Index hẹp
        "if": {"column_id": "Index"},
        "minWidth": "60px",
        "width":    "60px",
        "maxWidth": "60px",
    },
    {                       # Name vừa phải
        "if": {"column_id": "Name"},
        "minWidth": "180px",
        "width":    "180px",
        "maxWidth": "180px",
    },
    {                       # Description thu gọn, xuống dòng
        "if": {"column_id": "Description"},
        "minWidth": "350px",
        "width":    "100%",      # chiếm phần còn lại
        "maxWidth": "100%",
    },
    {                       # Calculation (nếu có)
        "if": {"column_id": "Calculation"},
        "minWidth": "200px",
        "width":    "220px",
        "maxWidth": "220px",
    },
]

# ------------------------------------------------------------------
# LAYOUT FUNCTION
# ------------------------------------------------------------------
def business_layout():
    header_block = dbc.Row(
        dbc.Col(
            html.H2("📄 Mô Tả Nghiệp Vụ",
                    className="fw-bold text-center",
                    style={"color": PRIMARY_COLOR}),
            width=12,
        ),
        className="my-3",
    )

    table_component = dash_table.DataTable(
        id="data-table-business",
        columns=[{"name": col, "id": col} for col in df_business.columns],
        data=df_business.to_dict("records"),
        page_action="none",
        fixed_rows={"headers": True},
        style_table=STYLE_TABLE,
        style_cell=STYLE_CELL,
        style_cell_conditional=STYLE_CELL_COND,
        style_header=STYLE_HEADER,
        style_as_list_view=True,
    )

    card = dbc.Card(
        dbc.CardBody(table_component, className="p-0"),
        className="shadow-sm border-0 w-100",
    )

    return dbc.Container([header_block, card], fluid=True, className="py-2")
