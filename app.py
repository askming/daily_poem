# https://www.gushiwen.cn/
# from ssl import PEM_FOOTER
import requests, os
# from os.path import join, dirname, abspath
# from dotenv import load_dotenv
from dash import Dash, dcc, html, Input, Output
from pyunsplash import PyUnsplash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output

# dotenv_path = join(dirname(abspath("app.py")), '../.env')
# load_dotenv(dotenv_path)
UNSPLASH_ACCESS_KEY = os.environ["UNSPLASH_ACCESS_KEY"]
X_User_Token = os.environ["X_User_Token"]

header = {"X-User-Token": X_User_Token}
pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    style = {'width': '50%', 'margin': '0 auto'}, 
    children=[
        html.H1("Chinese Poem of the Day", style={'textAlign': 'center', 'font-family': 'REEJI-Xiaodou-PoemGBT-Flash', 'text-shadow': '2px 2px #d7dbe0'}),
        html.H2(id="poem_title", style={'textAlign': 'center', 'font-family':'FangSong'}),
        html.P(id="poem_dynasty_author", style={'textAlign': 'center', 'font-family':'FangSong'}),
        html.H4(id="poem_content", style={'textAlign': 'center', 'font-family':'FangSong'}),
        html.Img(id='image', height='50%', width = '60%', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'border-radius': "15px"}),
        html.P(id="poem_translate", style={'font-family':'LXGW WenKai'}),
        html.Div(
            [html.Button('再来一首', id = "shuffle", n_clicks=0, style={'border-radius': '8px', 'font-family':'LXGW WenKai'})], style={'textAlign': 'center'}),
        dcc.Store(id = "poem")
])
# Define callback to update poem
@app.callback(
    Output('poem', 'data'),
    Input("shuffle", "n_clicks")
)
def get_a_poem(n_clicks):
    poem = requests.get("https://v2.jinrishici.com/sentence", headers = header)
    poem_data = poem.json()['data']
    return poem_data

@app.callback(
    Output('poem_title', 'children'),
    Input('poem', 'data')
)
def update_poem_title(poem):
    return poem['origin']['title']

@app.callback(
    Output('poem_dynasty_author', 'children'),
    Input('poem', 'data')
)
def update_poem_author(poem):
    return f"{poem['origin']['author']} [{poem['origin']['dynasty']}]"

@app.callback(
    Output('poem_content', 'children'),
    Input('poem', 'data')
)
def update_poem_content(poem):
    out = []
    for p in poem['origin']['content']:
        out.append(p)
        out.append(html.Br())
    return out

@app.callback(
    Output('poem_translate', 'children'),
    Input('poem', 'data')
)
def update_poem_translate(poem):
    return poem['origin']['translate']


@app.callback(
    Output('image', 'src'),
    Input("poem", "data")
)
def get_a_photo(poem):
    # if poem['matchTags'][0]:
    photo_kw = poem['origin']['title']
    photos = pu.search(type_='photos', page=1, per_page=1, query=photo_kw)
    for photo in photos.entries:
        # print(photo.link_html)
        return photo.link_download

# Run app and display result inline in the notebook
if __name__ == '__main__':
    app.server.run(debug = True)