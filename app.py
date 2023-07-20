import dash
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Group, Scheme, Sign
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbs
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# import plotly.io as poi

# poi.renderers.default = 'browser'

# конвертируем тип данных
dict_conv={
    'Глава': lambda x: str(x),
    'Код вида расходов': lambda x: str(x)
    }

df = pd.read_excel("current_year's_data.xlsx", converters=dict_conv)

tb1 = df[['Код вида расходов', 'ЛБО на текущий финансовый год', 'БО на текущий финансовый год', 'Исполнение (сумма)']]
tb1 = tb1.fillna(0)

tb1.loc[:, ['ЛБО на текущий финансовый год', 'БО на текущий финансовый год', 'Исполнение (сумма)']] /= 1000000

# CREATE PIVOT TABLE
tb1_pivot = pd.pivot_table(
    tb1,
    values=['ЛБО на текущий финансовый год', 'БО на текущий финансовый год', 'Исполнение (сумма)'],
    index='Код вида расходов',
    margins=False,
    aggfunc='sum'
)

tb1_pivot['% ЛБО'] = tb1_pivot['ЛБО на текущий финансовый год']/tb1_pivot['ЛБО на текущий финансовый год'].sum()
tb1_pivot['% БО от ЛБО'] = tb1_pivot['БО на текущий финансовый год']/tb1_pivot['ЛБО на текущий финансовый год']
tb1_pivot['% ДО от ЛБО'] = tb1_pivot['Исполнение (сумма)']/tb1_pivot['ЛБО на текущий финансовый год']
tb1_pivot['% ДО от БО'] = tb1_pivot['Исполнение (сумма)']/tb1_pivot['БО на текущий финансовый год']
tb1_pivot.reset_index(inplace=True) # переводим индекс в название столбца
tb1_pivot = tb1_pivot.round(2)

app = dash.Dash(__name__, external_stylesheets=[dbs.themes.BOOTSTRAP])

CHARTS_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family='Century Gothic'),
        legend=dict(orientation='h',
                    x=-0.03,
                    y=1.1),
        xaxis=dict(autotypenumbers='strict')
    )
)

fig_pie = px.pie(data_frame=df, values='ЛБО на текущий финансовый год',
                 names='Код вида расходов',
                 title='Распределение ЛБО по видам расходов',
                 hole=0.5)

# FUNCTION FROM CREATE HISTOGRAM
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
        marker_color='#EB89B0',
        opacity=0.70,
    ))

    fig_histograms.add_trace(go.Histogram(
        x=df[x_value],
        y=df[y2_value],
        name=y2_value,
        histfunc = 'sum',
        marker_color='#325C73',
        opacity=0.70
    ))

    fig_histograms.add_trace(go.Histogram(
        x=df[x_value],
        y=df[y3_value],
        name=y3_value,
        histfunc = 'sum',
        marker_color='#FF1493',
        opacity=0.70
    ))

    fig_histograms.update_layout(
        title_text=title_text,
        xaxis_title_text=xaxis_title_text,
        yaxis_title_text=yaxis_title_text,
        template=CHARTS_TEMPLATE
    )
    return fig_histograms

# MURKUP ELEMENTS
information_cards = dbs.Row(
    [
        dbs.Col(
            dbs.Card(
                [
                    html.H2('ЛБО на текущий финансовый год',
                            style={'margin-top':'10px'}),
                    html.H2(f"{tb1_pivot['ЛБО на текущий финансовый год'].sum()} млрд.руб")
                ],
                color="#767986", inverse=True
            )
        ),
        dbs.Col(
            dbs.Card(
                [
                    html.H2('Принято БО',
                             style={'margin-top':'10px'}),
                    html.H2(f"{tb1_pivot['БО на текущий финансовый год'].sum()} млрд.руб")
                ],
                color="#767986", inverse=True
            )
        ),
        dbs.Col(
            dbs.Card(
                [
                    html.H2('Исполнение (сумма)',
                            style={'margin-top':'10px'}),
                    html.H2(f"{tb1_pivot['Исполнение (сумма)'].sum()} млрд.руб")
                ],
                color="#767986", inverse=True
            )
        )
    ],
    style={'margin-top':'10px',
          'text-align':'center',
          'margin-left':'5px',
          'margin-right':'5px',
          'font-family':'PTF55F-webfont'}
)

# CREATE TABLE
table_view = DataTable(
    data=tb1_pivot.to_dict('records'),
    columns=[
        dict(id='Код вида расходов', name='Код вида расходов'),
        dict(id='ЛБО на текущий финансовый год', name='ЛБО на текущий финансовый год', type='numeric', format=Format(precision=2, scheme=Scheme.fixed, group=True, group_delimiter=' ')),
        dict(id='% ЛБО', name='Доля ЛБО', type='numeric', format=Format(precision=2, scheme=Scheme.percentage)),
        dict(id='БО на текущий финансовый год', name='Принято БО', type='numeric', format=Format(precision=2, scheme=Scheme.fixed, group=True, group_delimiter=' ')),
        dict(id='% БО от ЛБО', name='% БО от ЛБО', type='numeric', format=Format(precision=2, scheme=Scheme.percentage)),
        dict(id='Исполнение (сумма)', name='Исполнение (сумма)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed, group=True, group_delimiter=' ')),
        dict(id='% ДО от ЛБО', name='% ДО от ЛБО', type='numeric', format=Format(precision=2, scheme=Scheme.percentage)),
        dict(id='% ДО от БО', name='% ДО от БО', type='numeric', format=Format(precision=2, scheme=Scheme.percentage))
    ],
    style_data={
        'color': 'black',
        'backgroundColor': 'white',
        'font-family':'Century Gothic'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold',
        'font-family':'Century Gothic',
        'whiteSpace': 'normal',
        'height': 'auto'
    },
    style_cell={
        'textAlign':'center',
        'font-size':'30px'
    }
)
# LAYOUT
app.layout = html.Div([
    # HEADER
    html.Div([
        html.Img(src=app.get_asset_url('images/emblem.png'),
                 style={'width':'70px',
                        'margin-left':'20px'}
                        ),
        html.H1('Отчёт по исполнению Федерального бюджета по расходам УФК по Пермскому краю',
                style={'display':'inline-block',
                       'margin-left':'10px'}
                       )
    ], className='app-header'),
    # BODY
    html.Div([
        html.Div(
            information_cards
        ),
        dbs.Row([
            dbs.Col([
                dcc.Graph(figure=fig_pie)],
            width={'size':4}
            ),
            dbs.Col([
                dcc.Graph(figure=create_hisogram('Код НП', 'ЛБО на текущий финансовый год', 'БО на текущий финансовый год',
                                                'Исполнение (сумма)', 'Распределение по национальным проектам',
                                                'Национальный проект', 'Сумма'))],
            width={'size':4}),
            dbs.Col([
                dcc.Graph(figure=create_hisogram('Код вида расходов', 'ЛБО на текущий финансовый год', 'БО на текущий финансовый год',
                                                'Исполнение (сумма)', 'Распределение по видам расходов', 'Виды расходов', 'Сумма'))],
            width={'size':4})
        ],
            className='row g-0',
            style={'justify':'start',
                   'margin-top':'10px'}
        )
    ]),
    html.Div(
        dbs.Row(html.Table(table_view),
                style={'margin-left':'10px',
                       'margin-right':'10px'}
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)