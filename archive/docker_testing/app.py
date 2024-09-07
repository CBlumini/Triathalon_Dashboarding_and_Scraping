# app.py
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Hello Dash"),
        dcc.Markdown(
            """
            This is a simple Dash app running inside a Docker container.
            """
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
