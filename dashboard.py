from inspect import trace
import dash
from matplotlib.pyplot import legend, xlabel
import pandas as pd
import plotly.express as px
from dash import dcc, Output, Input
from dash import html
import os
import glob

app = dash.Dash(__name__)
# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df1 = pd.read_csv('ex1.csv')
df2 = pd.read_csv('ex2.csv')
df3 = pd.read_csv('ex3.csv')
#print(df1)
#df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y%m%d %H:%M:%S.%f')
#line_fig = px.line(df, x='DateTime', y=['DATA 1', 'DATA 2', 'DATA 3', 'DATA 4'])

#print(df1['song'])

#XAY DUNG KHUNG UI
#THONG KE BAI HAT
app.layout = html.Div(children=[
    html.H1("TRENDING SONGS"),
    html.H2("Statistics of total views of songs:"),
    html.B('Filter from top: '),
    dcc.Input(id="start-range", type="number", value=1, min = 1),
    html.B(' to top: '),
    dcc.Input(id="end-range", type="number", value=30),
    dcc.Graph(
        id='cntsong-graph'
   ),

   html.H2("Trending songs in June 2022:"),
    html.B('June, from: '),
    dcc.Input(id="day-start-range-song", type="number", value=1, min = 1),
    html.B(' to: '),
    dcc.Input(id="day-end-range-song", type="number", value=30),
    html.B(' , 2022'),
    dcc.Graph(
        id='trending-song-graph'
   ),

   html.Br(),
    html.H1("ACTIVE USERS"),
    html.H2("Statistics of total visits of User-Ids:"),
    html.B('Filter from top: '),
    dcc.Input(id="start-range-user", type="number", value=1, min = 1),
    html.B(' to top: '),
    dcc.Input(id="end-range-user", type="number", value=10),
    dcc.Graph(
        id='cntuser-graph'
    ),

    html.H2("Active Users of the month in June 2022:"),
    html.B('June, from: '),
    dcc.Input(id="day-start-range-user", type="number", value=1, min = 1),
    html.B(' to: '),
    dcc.Input(id="day-end-range-user", type="number", value=30),
    html.B(' , 2022'),
    dcc.Graph(
        id='active-user-graph'
   ),
    
    html.Br(),
    html.H1("POTENTIAL CITIES"),
    html.H2("Statistics of total visits in cities:"),
    html.B('Filter from top: '),
    dcc.Input(id="start-range-city", type="number", value=1, min = 1),
    html.B(' to top: '),
    dcc.Input(id="end-range-city", type="number", value=10),
    dcc.Graph(
        id='cntcity-graph'
    ),

    html.H2("Top Active Cities in June 2022:"),
    html.B('June, from: '),
    dcc.Input(id="day-start-range-city", type="number", value=1, min = 1),
    html.B(' to: '),
    dcc.Input(id="day-end-range-city", type="number", value=30),
    html.B(' , 2022'),
    dcc.Graph(
        id='active-city-graph'
   )
])
@app.callback(
    Output("cntsong-graph", 'figure'),
    Input("start-range", "value"),
    Input("end-range", "value")
)
def update_song_graph(start_top, end_top):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "start-range":
        start_top = None if end_top is None else start_top-1
    else :
        end_top = None if start_top is None else end_top
    return {
        'data': [
            {'x': df1['song'][start_top-1:end_top], 'y': df1['count'], 'type': 'bar', 'name': 'SF'}
        ]
    }

#THONG KE NGUOI DUNG
@app.callback(
    Output("cntuser-graph", 'figure'),
    Input("start-range-user", "value"),
    Input("end-range-user", "value")
)
def update_user_graph(start_top, end_top):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "start-range-user":
        start_top = None if end_top is None else start_top-1
    else :
        end_top = None if start_top is None else end_top
    return {
        'data': [
            {'x': df2['userId'][start_top-1:end_top], 'y': df1['count'], 'type': 'bar', 'name': 'SF'}
        ]
    }

#THONG KE THANH PHO
@app.callback(
    Output("cntcity-graph", 'figure'),
    Input("start-range-city", "value"),
    Input("end-range-city", "value")
)
def update_city_graph(start_top, end_top):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "start-range-city":
        start_top = None if end_top is None else start_top-1
    else :
        end_top = None if start_top is None else end_top
    return {
        'data': [
            {'x': df3['city'][start_top-1:end_top], 'y': df1['count'], 'type': 'bar', 'name': 'SF'}
        ]
    }


#BIEU DO TRENDING

#Xu huong bai hat
dfs = pd.DataFrame({'song':[]})
for path in sorted(glob.glob(os.path.join('ex1', "*")), key=lambda a : int(a[-2:])):
    for filename in glob.glob(os.path.join(path, "*.csv")):
        with open(filename, 'r', encoding='utf-8') as file:
            tmp = pd.read_csv(file)
            tmp.rename(columns={'count': str(os.path.split(path)[1])}, inplace = True)
            dfs = pd.merge(dfs, tmp, on='song', how='right')
tmp = pd.read_csv('ex1.csv')
dfs = pd.merge(dfs, tmp, on='song', how='right')
dfs = dfs.rename(columns = {'count':'Total'})
dfs.sort_values('Total', axis=0, ascending=False)
dfs = dfs[:5]
@app.callback(
    Output("trending-song-graph", 'figure'),
    Input("day-start-range-song", "value"),
    Input("day-end-range-song", "value")
)
def update_trending_song(day_start, day_end):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "day-start-range-song":
        day_start = None if day_end is None else day_start-1
    else :
        day_end = None if day_start is None else day_end
    return px.line(
        dfs[:5].drop(['song', 'Total'], axis=1).T[day_start-1:day_end+1],
        labels={
                     "index": "Day (June 2022)",
                     "value": "Views",
                     "variable": "Song: ",
                 },
        category_orders={"Song": dfs[:5].song}
    )

#Nguuoi Dung active torng thang
dfu = pd.DataFrame({'userId':[]})
for path in sorted(glob.glob(os.path.join('ex2', "*")), key=lambda a : int(a[-2:])):
    for filename in glob.glob(os.path.join(path, "*.csv")):
        with open(filename, 'r', encoding='utf-8') as file:
            tmp = pd.read_csv(file)
            tmp.rename(columns={'count': str(os.path.split(path)[1])}, inplace = True)
            dfu = pd.merge(dfu, tmp, on='userId', how='right')
tmp = pd.read_csv('ex2.csv')
dfu = pd.merge(dfu, tmp, on='userId', how='right')
dfu = dfu.rename(columns = {'count':'Total'})
dfu.sort_values('Total', axis=0, ascending=False)
dfu = dfu[:5]
@app.callback(
    Output("active-user-graph", 'figure'),
    Input("day-start-range-user", "value"),
    Input("day-end-range-user", "value")
)
def update_active_user(day_start, day_end):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "day-start-range-user":
        day_start = None if day_end is None else day_start-1
    else :
        day_end = None if day_start is None else day_end
    return px.line(
        dfu[:5].drop(['userId', 'Total'], axis=1).T[day_start-1:day_end+1],
        labels={
                     "index": "Day (June 2022)",
                     "value": "Visits",
                     "variable": "UserId: ",
                 },
        category_orders={"userId": dfu[:5].userId}
    )

#Thanh pho truy cap nhieu torng thang
dfc = pd.DataFrame({'city':[]})
for path in sorted(glob.glob(os.path.join('ex3', "*")), key=lambda a : int(a[-2:])):
    for filename in glob.glob(os.path.join(path, "*.csv")):
        with open(filename, 'r', encoding='utf-8') as file:
            tmp = pd.read_csv(file)
            tmp.rename(columns={'count': str(os.path.split(path)[1])}, inplace = True)
            dfc = pd.merge(dfc, tmp, on='city', how='right')
tmp = pd.read_csv('ex3.csv')
dfc = pd.merge(dfc, tmp, on='city', how='right')
dfc = dfc.rename(columns = {'count':'Total'})
dfc.sort_values('Total', axis=0, ascending=False)
dfc = dfc[:5]
@app.callback(
    Output("active-city-graph", 'figure'),
    Input("day-start-range-city", "value"),
    Input("day-end-range-city", "value")
)
def update_active_city(day_start, day_end):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "day-start-range-city":
        day_start = None if day_end is None else day_start-1
    else :
        day_end = None if day_start is None else day_end
    return px.line(
        dfc[:5].drop(['city', 'Total'], axis=1).T[day_start-1:day_end+1],
        labels={
                     "index": "Day (June 2022)",
                     "value": "Actives",
                     "variable": "City: ",
                 },
        category_orders={"city": dfc[:5].city}
    )


if __name__ == '__main__':
   app.run_server(debug=True)