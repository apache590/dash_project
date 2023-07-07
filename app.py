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

df = pd.read_excel('date_2023_year.xlsx')
df['Код вида расходов'] = df['Код вида расходов'].astype(str)

app = dash.Dash(__name__, external_stylesheets=[dbs.themes.BOOTSTRAP])

fig_pie = px.pie(data_frame=df, values='Доведено ЛБО', names='Код вида расходов', title='Распределение ЛБО по видам расходов')

fig_histograms_types_of_expenses = go.Figure()
fig_histograms_types_of_expenses.add_trace(go.Histogram(
    x=df['Код вида расходов'],
    y=df['Доведено ЛБО'],
    #  xbins=dict(
    #     start=100.0,
    #     end=900.0,
    #     size=50.0),
    name='Доведено ЛБО',
    histfunc = 'sum',
    marker_color='#EB89B5',
    opacity=0.75,
))

fig_histograms_types_of_expenses.add_trace(go.Histogram(
    x=df['Код вида расходов'],
    y=df['Принято БО: всего'],
    name='Принято БО: всего',
    histfunc = 'sum',
    # xbins=dict(
    #     start=100.0,
    #     end=900.0,
    #     size=50.0),
    marker_color='#330C73',
    opacity=0.75
))

fig_histograms_types_of_expenses.add_trace(go.Histogram(
    x=df['Код вида расходов'],
    y=df['Исполнено ДО'],
    name='Исполнено ДО',
    histfunc = 'sum',
    #  xbins=dict(
    #     start=100.0,
    #     end=900.0,
    #     size=50.0),
    marker_color='#FF1493',
    opacity=0.75
))

fig_histograms_types_of_expenses.update_layout(
    title_text='Виды расходов',
    xaxis_title_text='Вид расходов',
    yaxis_title_text='Сумма'
    # bargap=0.2,
    # bargroupgap=0.1
)

fig_histograms_national_project = go.Figure()
fig_histograms_national_project.add_trace(go.Histogram(
    x=df['Код НП'],
    y=df['Доведено ЛБО'],
    name='Доведено ЛБО',
    histfunc='sum',
    marker_color='#EB89B5',
    opacity=0.75
))

fig_histograms_national_project.add_trace(go.Histogram(
    x=df['Код НП'],
    y=df['Принято БО: всего'],
    name='Принято БО: всего',
    histfunc='sum',
    marker_color='#330C73',
    opacity=0.75
))

fig_histograms_national_project.add_trace(go.Histogram(
    x=df['Код НП'],
    y=df['Исполнено ДО'],
    name='Исполнено ДО',
    histfunc='sum',
    marker_color='#FF1493',
    opacity=0.75
))

fig_histograms_national_project.update_layout(
    title_text='Национальные проекты',
    xaxis_title_text='Код национального проекта',
    yaxis_title_text='Сумма'
)
app.layout = html.Div([
    dbs.Row(html.H1('Отчёт по исполнению Федерального бюджета по расходам УФК по Пермскому краю')),
    dbs.Row([
        dbs.Col([
            # html.Div('Виды расходов'),
            dcc.Graph(figure=fig_pie)
        ],
        width={'size':4}
        ),
        dbs.Col([
            # html.Div('Уровень принятых БО к ЛБО'),
            dcc.Graph(figure=fig_histograms_types_of_expenses)
        ],
        width={'size':4}
        ),
        dbs.Col([
            dcc.Graph(figure=fig_histograms_national_project)
        ], width={'size':4}
        )
    ],
    justify='start'
)
],style={'text-align':'left',
         'margin-left':'20px'}
         )

if __name__ == '__main__':
    app.run_server(debug=True)