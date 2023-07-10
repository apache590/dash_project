import dash
from dash import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbs
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as poi

poi.renderers.default = 'browser'

dict_conv={
    'Глава': lambda x: str(x),
    'Код вида расходов': lambda x: str(x)
    }

df = pd.read_excel('date_2023_year.xlsx', converters=dict_conv)

app = dash.Dash(__name__, external_stylesheets=[dbs.themes.BOOTSTRAP])

fig_pie = px.pie(data_frame=df, values='Доведено ЛБО', names='Код вида расходов', title='Распределение ЛБО по видам расходов',)

def create_hisogram(x_value:str, y1_value:str,
                    y2_value:str, y3_value:str,
                    title_text:str, xaxis_title_text:str,
                    yaxis_title_text:str):
    fig_histograms = go.Figure()
    fig_histograms.add_trace(go.Histogram(
        x=df[x_value],
        y=df[y1_value],
        name=y1_value,
        histfunc = 'sum',
        marker_color='#EB89B5',
        opacity=0.75,
    ))

    fig_histograms.add_trace(go.Histogram(
        x=df[x_value],
        y=df[y2_value],
        name=y2_value,
        histfunc = 'sum',
        marker_color='#330C73',
        opacity=0.75
    ))

    fig_histograms.add_trace(go.Histogram(
        x=df[x_value],
        y=df[y3_value],
        name=y3_value,
        histfunc = 'sum',
        marker_color='#FF1493',
        opacity=0.75
    ))

    fig_histograms.update_layout(
        title_text=title_text,
        xaxis_title_text=xaxis_title_text,
        yaxis_title_text=yaxis_title_text
    )
    return fig_histograms

app.layout = html.Div([
    dbs.Row(html.H1('Отчёт по исполнению Федерального бюджета по расходам УФК по Пермскому краю')),
    dbs.Row([
        dbs.Col([
            dcc.Graph(figure=fig_pie)
        ],
        width={'size':6}
        ),
        dbs.Col([
            dcc.Graph(figure=create_hisogram('Код вида расходов', 'Доведено ЛБО', 'Принято БО: всего',
                                             'Исполнено ДО', 'Распределение по видам расходов', 'Виды расходов', 'Сумма'))
        ],
        width={'size':6}
        )
    ],
    justify='start'
),
    dbs.Row([
        dbs.Col([
            dcc.Graph(figure=create_hisogram('Код НП', 'Доведено ЛБО', 'Принято БО: всего',
                                             'Исполнено ДО', 'Распределение по национальным проектам', 'Национальный проект', 'Сумма'))
        ],
        width={'size':6}
        ),
        dbs.Col([
            dcc.Graph(figure=create_hisogram('Глава', 'Доведено ЛБО', 'Принято БО: всего',
                                             'Исполнено ДО', 'Распределение по главам', 'Глава', 'Сумма'))
        ],
        width={'size':6}
        )
    ],
    justify='start'
)
    ],
style={'text-align':'left',
         'margin-left':'20px'}
)

if __name__ == '__main__':
    app.run_server(debug=True)