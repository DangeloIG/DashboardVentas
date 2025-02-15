# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, dash_table, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import sqlite3
import io
import xlsxwriter
from dash.dependencies import Input, Output
from reportlab.pdfgen import canvas

# ✅ Función para obtener datos desde SQLite
def obtener_datos():
    conn = sqlite3.connect("database/data.db")
    df = pd.read_sql_query("SELECT * FROM ventas", conn)
    conn.close()
    return df if not df.empty else pd.DataFrame(columns=["categoria", "valor", "fecha"])

# ✅ Inicializar la aplicación Dash con Bootstrap y CSS personalizado
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], assets_folder="assets")
app.title = "Dashboard de Ventas"

# ✅ Obtener datos iniciales
df = obtener_datos()
categorias = df["categoria"].unique().tolist() if not df.empty else ["N/A"]

# ✅ Diseño del dashboard
app.layout = dbc.Container([
    html.H1("📊 Dashboard de Ventas 🚀", className="animated-title"),

    dbc.Row([
        dbc.Col([
            html.Label("Selecciona una categoría", className="dropdown-label"),
            dcc.Dropdown(
                id="categoria-dropdown",
                options=[{"label": cat, "value": cat} for cat in categorias],
                value=categorias[0],
                clearable=False,
                className="custom-dropdown"
            )
        ], width=4)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dbc.Button("📥 Descargar Excel", id="download-excel", color="success", className="btn-custom"), width=3),
        dbc.Col(dbc.Button("📥 Descargar PDF", id="download-pdf", color="danger", className="btn-custom"), width=3),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="grafico-barras", className="dash-graph")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="grafico-lineas", className="dash-graph")), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="grafico-pie", className="dash-graph")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="grafico-dispersion", className="dash-graph")), width=6),
    ]),

    dash_table.DataTable(
        id="table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_header={"fontWeight": "bold", "backgroundColor": "#333333", "color": "white"},
        style_cell={"textAlign": "center", "backgroundColor": "#222222", "color": "white"},
    ),

    dcc.Download(id="download-excel-file"),
    dcc.Download(id="download-pdf-file"),
], fluid=True)

# ✅ Callback para actualizar gráficos dinámicamente
@app.callback(
    [Output("grafico-barras", "figure"),
     Output("grafico-lineas", "figure"),
     Output("grafico-pie", "figure"),
     Output("grafico-dispersion", "figure")],
    [Input("categoria-dropdown", "value")]
)
def actualizar_graficos(categoria):
    df_filtrado = df[df["categoria"] == categoria] if not df.empty else df

    fig_barras = px.bar(df_filtrado, x="fecha", y="valor", title="📊 Ventas por Fecha", color="valor")
    fig_lineas = px.line(df_filtrado, x="fecha", y="valor", title="📈 Tendencia de Ventas", markers=True)
    fig_pie = px.pie(df, names="categoria", values="valor", title="📌 Distribución de Ventas por Categoría", hole=0.3)
    fig_dispersion = px.scatter(df, x="fecha", y="valor", title="📍 Relación Fecha-Ventas", color="valor", size="valor")

    return fig_barras, fig_lineas, fig_pie, fig_dispersion

# ✅ Callback para descargar Excel
@app.callback(
    Output("download-excel-file", "data"),
    Input("download-excel", "n_clicks"),
    prevent_initial_call=True
)
def descargar_excel(n_clicks):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Ventas")
    output.seek(0)
    return dcc.send_bytes(output.read(), filename="Ventas.xlsx")

# ✅ Callback para descargar PDF
@app.callback(
    Output("download-pdf-file", "data"),
    Input("download-pdf", "n_clicks"),
    prevent_initial_call=True
)
def descargar_pdf(n_clicks):
    output = io.BytesIO()
    pdf = canvas.Canvas(output)
    pdf.drawString(100, 750, "Reporte de Ventas")
    
    y = 730
    for index, row in df.iterrows():
        pdf.drawString(100, y, f"{row['categoria']} - {row['valor']} - {row['fecha']}")
        y -= 20
    
    pdf.save()
    output.seek(0)
    return dcc.send_bytes(output.read(), filename="Ventas.pdf")

# ✅ Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)












