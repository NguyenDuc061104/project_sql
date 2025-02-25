from dash.dependencies import Input, Output
from dash import dcc, html
from db import get_data_from_postgres
from layout import baocao_tonghop_layout, baocao_xh_layout

def register_callbacks(app):
    # Callback cập nhật nội dung trang khi URL thay đổi
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/xh':
            return baocao_xh_layout()
        else:
            return baocao_tonghop_layout()

    # Callback cập nhật dữ liệu cho bảng `baocao_tonghop`
    @app.callback(
        [Output("data-table-baocao", "data"),
         Output("data-table-baocao", "columns")],
        [Input("month-dropdown-baocao", "value")]
    )
    def update_dashboard_baocao(month):
        df = get_data_from_postgres(month, "baocao_tonghop")

        if df.empty:
            return [], []
        
        column_mapping = {
        "information": "Thông tin",
        "head": "Head",
        "dong_bac_bo": "Đông Bắc Bộ",
        "tay_bac_bo": "Tây Bắc Bộ",
        "db_song_hong": "Đồng Bằng Sông Hồng",
        "bac_trung_bo": "Bắc Trung Bộ",
        "nam_trung_bo": "Nam Trung Bộ",
        "tay_nam_bo": "Tây Nam Bộ",
        "dong_nam_bo": "Đông Nam Bộ",
    }
        if "id" in df.columns:
            df.drop(columns=["id"], inplace=True)


        df.rename(columns=column_mapping, inplace=True)

        columns = [{"name": column_mapping.get(i, i), "id": i} for i in df.columns]
        data = df.to_dict('records')

        return data, columns

    # Callback cập nhật dữ liệu cho bảng `fact_report_xh`
    @app.callback(
        [Output("data-table-xh", "data"),
         Output("data-table-xh", "columns")],
        [Input("month-dropdown-xh", "value")]
    )
    def update_dashboard_xh(month):
        df = get_data_from_postgres(month, "fact_report_xh")

        if df.empty:
            return [], []

        column_mapping = {
        "area_code": "Mã khu vực",
        "area_name": "Khu vực",
        "email": "Email",
        "tong_diem": "Tổng điểm",
        "rank_final": "Rank final",
        "ltn_avg": "Loan to new trung bình",
        "rank_ltn_avg": "Rank Loan to new trung bình",
        "psdn_avg": "Phát sinh dư nợ trung bình",
        "rank_psdn_avg": "Rank phát sinh dư nợ trung bình",
        "approval_rate_avg": "Approval rate trung bình",
        "rank_approval_rate_avg": "Rank Approval rate trung bình",
        "npl_truoc_wo_luy_ke": "Npl trước writeoff lũy kế",
        "rank_npl_truoc_wo_luy_ke": "Rank npl trước writeoff lũy kế",
        "diem_quy_mo": "Điểm quy mô",
        "rank_ptkd": "Rank ptkd",
        "cir": "Cir",
        "rank_cir": "Rank cir",
        "margin": "Margin",
        "rank_margin": "Rank margin",
        "hs_von": "Hiệu số vốn",
        "rank_hs_von": "Rank hiệu số vốn",
        "hsbq_nhan_su": "Hiệu số bình quân nhân sự",
        "rank_hsbq_nhan_su": "Rank hiệu số bình quân nhân sự",
        "diem_fin": "Điểm tài chính",
        "rank_fin": "Rank tài chính"        
    }
        if "month_key" in df.columns:
            df.drop(columns=["month_key"], inplace=True)


        df.rename(columns=column_mapping, inplace=True)

        columns = [{"name": column_mapping.get(i, i), "id": i} for i in df.columns]
        data = df.to_dict('records')

        return data, columns