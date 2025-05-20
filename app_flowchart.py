from dash import html
import dash_bootstrap_components as dbc

def flowchart_layout():
    return dbc.Container([
        html.H3("Yêu cầu doanh nghiệp", className="text-center mb-4"),

        html.H5("🎯 MỤC TIÊU"),
        html.P("Ban điều hành (BOD) muốn biết được hiệu quả kinh doanh của doanh nghiệp (công ty tài chính) và các khu vực mạng lưới trên toàn quốc cũng như đánh giá năng lực của các nhân sự (ASM)."),

        html.H5("📥 INPUT"),
        html.Ul([
            html.Li("File `fact_kpi_month_raw_data`: nguồn sao kê dữ liệu thẻ theo khách hàng tại thời điểm cuối mỗi tháng."),
            html.Li("File `fact_txn_month_raw_data`: nguồn dữ liệu các khoản phát sinh được hạch toán vào sổ cái kế toán (General Ledger)."),
            html.Li("File `kpi_asm_data`: nguồn số liệu về doanh số kinh doanh theo từng tháng của các ASM (Area Sales Manager)."),
        ]),

        html.H5("📤 OUTPUT"),
        html.Ul([
            html.Li("Báo cáo tổng hợp (báo cáo chính): ghi nhận tình hình kinh doanh của các khu vực mạng lưới trên toàn quốc."),
            html.Li("Báo cáo xếp hạng (báo cáo chính): đánh giá nhân sự (ASM) theo các chỉ số tài chính và các chỉ số kinh doanh."),
            html.Li("Báo cáo kinh doanh: thống kê, phân tích tình hình kinh doanh của các khu vực mạng lưới trên toàn quốc."),
            html.Li("Chi phí lũy kế năm: thống kê, phân tích tình hình các nguồn chi phí, phân bổ chi phí các khu vực mạng lưới trên toàn quốc và đưa ra đánh giá về mức độ hiệu quả."),
            html.Li("Đánh giá ASM: thống kê, phân tích và đánh giá mức độ hiệu quả của các nhân sự (ASM) theo các chỉ số tài chính và các chỉ số kinh doanh."),
        ]),

        html.H5("📊 FLOWCHART"),
        html.Img(src='/assets/flowchart.png', style={"width": "100%", "border": "1px solid #ccc", "borderRadius": "8px"}),

    ], fluid=True)
