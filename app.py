import dash
from dash import html
import dash_bootstrap_components as dbc
from layout import create_layout
# from callbacks import register_callbacks

# Khởi tạo Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Gán layout
app.layout = create_layout()

# Đăng ký callback
# register_callbacks(app)

# Thêm server để Gunicorn có thể chạy
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
