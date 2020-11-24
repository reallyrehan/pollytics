import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
import time
import os
import requests
import json
import pandas as pd
from datetime import datetime
import re
from IPython.core.display import display, HTML
import dash_bootstrap_components as dbc
import plotly.express as px
import calendar
import plotly.graph_objects as go

def calNormalize(t_val):
    return 0-((50-t_val)*2)/100

# Reading All DataFrames
# df_global = pd.read_pickle('one_df.pickle')
# df_global.reset_index(inplace=True)

print("Loading Aggregated One Dataframe from Firebase")
test_message = requests.get('https://data-management-ac8c8.firebaseio.com/one_aggregated.json')
df_global = pd.DataFrame(json.loads(test_message.json()))
df_global["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in df_global["_date"]]



list_of_months = pd.Series([i.strftime("%B") for i in df_global["_date"]]).unique()
list_of_months= {i+1: '{}'.format(list_of_months[i]) for i in range(0,9)}

#print(df_global.columns)

print("Loading Aggregated Twitter Dataframe from Firebase")

test_message = requests.get('https://data-management-ac8c8.firebaseio.com/twitter_aggregated.json')
test_dict = test_message.json()

# with open("twitter_aggregated.json","r") as f_r:
#     test_dict = json.load(f_r)
biden_df = pd.DataFrame(json.loads(test_dict["biden"]))
trump_df = pd.DataFrame(json.loads(test_dict["trump"]))
biden_df["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in biden_df["_date"]]
trump_df["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in trump_df["_date"]]

print("Loading Aggregated Reddit Dataframe from Firebase")

test_message = requests.get('https://data-management-ac8c8.firebaseio.com/aggregated.json')
test_dict = test_message.json()
# with open("aggragated.json","r") as f_r:
#     test_dict = json.load(f_r)
topic = pd.DataFrame(json.loads(test_dict["topic"]))
total = pd.DataFrame(json.loads(test_dict["total"]))
link = pd.DataFrame(json.loads(test_dict["link"]))
created = pd.DataFrame(json.loads(test_dict["created"]))
subreddit = pd.DataFrame(json.loads(test_dict["subreddit"]))

topic["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in topic["date"]]
topic["month"]=pd.DatetimeIndex(topic['_date']).month
topic["week"]=pd.DatetimeIndex(topic['_date']).week

total["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in total["date"]]
link["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in link["date"]]
link["month"]=pd.DatetimeIndex(link['_date']).month
link["week"]=pd.DatetimeIndex(link['_date']).week
created["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in created["date"]]
created["month"]=pd.DatetimeIndex(created['_date']).month
created["week"]=pd.DatetimeIndex(created['_date']).week
subreddit["_date"] = [datetime.utcfromtimestamp(u/1000).date() for u in subreddit["date"]]
subreddit["month"]=pd.DatetimeIndex(subreddit['_date']).month
subreddit["week"]=pd.DatetimeIndex(subreddit['_date']).week


poll_data = pd.read_csv('president_polls.csv')
poll_data["weighted_pct"]=poll_data["sample_size"]*poll_data["pct"]
poll_date = pd.DataFrame(poll_data.groupby(['answer','start_date'])["weighted_pct"].sum()/poll_data.groupby(['answer','start_date'])["sample_size"].sum())
poll_date.reset_index(inplace=True)
poll_date["_date"]=[datetime.strptime(x, '%m/%d/%y').date() for x in  poll_date["start_date"]]
poll_date.rename(columns={'answer': 'user',0:"pct"},inplace=True)
poll_date = poll_date[(poll_date["user"].isin(["Trump","Biden"])) & (poll_date["_date"]>=datetime.strptime("01/01/20", '%m/%d/%y').date())]
poll_date["user"]=["poll_trump" if y == "Trump" else "poll_biden" for y in poll_date["user"]]
poll_date["mean"]=[calNormalize(m) for m in poll_date["pct"]]



color_dict = {'trump':'red','reddit_trump':'orange','poll_trump':'goldenrod','biden':'blue','poll_biden':'darkblue','reddit_biden':'skyblue'}



server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')

app = dash.Dash('app', server=server,external_stylesheets=[dbc.themes.LUX])

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'




def getPieGraph():
    colors = ['blue','red']
    fig = go.Figure(data=[go.Pie(labels=['biden','trump'],
                                values=[2799,10263])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                    marker=dict(colors=colors))
    return fig

app.layout = html.Div([
    dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink("About Us", href="#about-us"))
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="Pollytics",
    brand_href="#",
    color="primary",
    dark=True,
),
    html.Div([
        html.Div([
            html.H1('What does Reddit think about Biden and Trump?')],className="row d-flex justify-content-center mt-4 mb-4"),
        html.Div([
            html.H2('Sentiment Score Vs Polls')],className="row d-flex justify-content-center mt-4 mb-4"),


        ## TEST
        html.Div([
            html.Div([
                html.H5("Biden",className="ml-auto mr-auto text-info")
            ],className="col-6 d-flex"),
            html.Div([
                html.H5("Trump",className="ml-auto mr-auto text-danger")
            ],className="col-6 d-flex"),
        ],className = "row "),

        html.Div([
            html.Div([
                dbc.Checklist(
                    id = 'graph1-checklist-1',
                    options=[
                        
                        {'label': 'Twitter', 'value': 'biden'},
                        {'label': 'Reddit', 'value': 'reddit_biden'},
                        {'label': 'Polls', 'value': 'poll_biden'}
                    
                    ],
                    labelClassName ="ml-4 mr-4",
                    value=['reddit_biden'],
                    className="d-flex ml-auto mr-auto")
            ],className="col-6 d-flex"),
            html.Div([
                dbc.Checklist(
                    id = 'graph1-checklist-2',
                    options=[
                        
                        {'label': 'Twitter', 'value': 'trump'},
                        {'label': 'Reddit', 'value': 'reddit_trump'},
                        {'label': 'Polls', 'value': 'poll_trump'},
                    ],
                    labelClassName ="ml-4 mr-4",
                    value=['reddit_trump'],
                    className="d-flex ml-auto mr-auto")
            ],className="col-6 d-flex"),
  
            
        ],className = "row  justify-content-around"),
        ##
        
        dcc.Graph(id='graph1'),
        html.Div([
            html.H5('Choose A Moving Average Value')
        ],className = "row justify-content-around"),
        
        dcc.Slider(
                id = 'graph1-slider',
                min=1,
                max=31,
                marks={i: '{}'.format(i) for i in range(1,30,3)},
                value=3,
                className="mt-2 mb-4"
            )
    ],className = "container"),
     
    html.Div([
        html.Div([
            #dcc.Graph(id="graph3")
           html.H2("Overall Stats",className="ml-auto mr-auto")
        ],className="row d-flex"),
        html.Div([
            html.Div([
                dcc.Graph(id="graph3")
            ],className="col-6"),
            html.Div([
                dcc.Graph(figure=getPieGraph())
                #html.Iframe(src=app.get_asset_url("tableau2.html"),height=300,width="100%",className="mt-4 mb-2")

            ],className="col-6")
            
        ],className="row  justify-content-around"),
       
        html.Div([
            # html.Div([
            #     html.H1("Hello")
            # ],className="col-6"),
            # html.Div([
            #     html.H1("Hello")
            # ],className="col-6")
        ],id="yearstats",className="row ")

    ],className="container"),

    html.Div([
        html.Iframe(
        src = app.get_asset_url("tableau3.html"),height=800,width="100%",className="mt-2 mb-2 ml-auto mr-auto"
        )
    ],className="container d-flex mt-4"),
    html.Hr(className="mt-4"),

    html.Div([
        html.Div([
            html.H1('Month Analysis')
        ],className = "row justify-content-around mt-4"),
        html.Div([
            #dcc.Graph(id="graph3")
           html.H3("Score Per Month",className="ml-auto mr-auto")
        ],className="row d-flex"),
        html.Div([
            #dcc.Graph(id="graph3")
           html.Iframe(src=app.get_asset_url("tableau1.html"),height=550,width="100%",className="mt-4 mb-2")
        ],className="row  justify-content-around mt-4"),
        html.Div([
            html.H5('Choose A Month')
        ],className = "row mt-2 justify-content-around"),
        
        dcc.Slider(
            id = 'graph2-slider',
            min=1,
            max=10,
            marks=list_of_months,
            value=1,
            className="mt-2 mb-4"
        ),
        
        html.Div(id="favorites",className="row "),
        html.Div([

        ],id="monthstats",className="row ")

    ],className="container"),

    html.Hr(className = "mb-4 mt-4"),
    html.Div([
        html.Div([
            html.H1('Topics Per Month')],className="row d-flex justify-content-center mt-4 mb-2"),
    ],className = "container"),


        html.Div([

        html.Div([
            html.Div([
                dbc.RadioItems(
                    id = 'graph2-checklist',
                    options=[
                        {'label': 'Biden', 'value': 'biden'},
                        {'label': 'Trump', 'value': 'trump'}
                        
                    ],
                    labelCheckedClassName="ml-4 mr-4",
                    value='trump',
                    className="d-flex ml-auto mr-auto")
            ],className = "col-12 d-flex")

            
        ],className = "row mt-4"),
        html.Div(id='graph2'),

    ],className = "container"),

    html.Div([
        html.Div([
            html.Div([
                dbc.RadioItems(
                    id = 'graph4-radio',
                    options=[
                        {'label': 'Count', 'value': 'count'},
                        {'label': 'Sentiment Score', 'value': 'mean'},
                        {'label': 'Positive %', 'value': 'pos'},
                        {'label': 'Neutral %', 'value': 'neu'},
                        {'label': 'Negative %', 'value': 'neg'}
                        
                    ],
                    labelCheckedClassName="ml-4 mr-4",
                    value='mean',
                    className="d-flex ml-auto mr-auto")
            ],className = "col-12 d-flex")

            
        ],className = "row"),
        
        dcc.Graph(id="graph4"),
 
    ],className="container"),


    html.Div([
        html.Div(id="redditstats",className="row "),
    ],className="container"),
    html.Hr(),

    html.Div([
        html.Div([
            html.H1("About Us",id="about-us",className= "ml-auto mr-auto")
        ],className = "row mb-4 mt-4 d-flex"),
        html.Div([
            html.Div([
                dbc.Card([
                    html.Img(src=app.get_asset_url("re.jpg"),className="img-fluid rounded-circle mt-4 mb-4 mr-4 ml-4"),
                    html.H1("Rehan Ahmed",className="card-title  mt-4 mb-2  mr-auto ml-auto"),
                    dbc.Button("Pakistan",color="primary",className = "mb-2 mr-4 ml-4"),
                    html.P("A technology geek who wants to make sense of the world of ones and zeroes. Passionate about all things data, I am currently pursuing my Masters in Applied Data Science from USC on a Fulbright Scholarship.",className="card-text  mb-4 mr-4 ml-4")
                    
                ])
                
            ],className = "col-4"),
            html.Div([
                dbc.Card([
                    html.Img(src=app.get_asset_url("sa2.jpg"),className="img-fluid rounded-circle mt-4 mb-4 mr-4 ml-4"),
                    html.H1("Saurabh Jain",className="card-title  mt-4 mb-2  mr-auto ml-auto"),
                    dbc.Button("India",color="primary",className = "mb-2 mr-4 ml-4"),
                    html.P("A proud Mechanical Engineer who is excited to merge Data Science with hardware engineering, currently pursuing a Masters in Applied Data Science at USC. Looking forward to his time in SoCal and meeting new people!",className="card-text  mb-4 mr-4 ml-4")
                    
                
                    
                ])
                
            ],className = "col-4"),
            html.Div([
                dbc.Card([
                    html.Img(src=app.get_asset_url("da3.jpg"),className="img-fluid rounded-circle mt-4 mb-4 mr-4 ml-4"),
                    html.H1("Danielle Sim",className="card-title  mt-4 mb-2 mr-auto ml-auto"),
                    dbc.Button("United States",color="primary",className = "mb-2 mr-4 ml-4"),
                    html.P("Currently pursuing a Masters degree in Data Science, with a high interest in Cyber Security. Extensive background and work experience in statistics/biostatistics, with skills in R/RStudio, SAS, SQL, and Python.",className="card-text  mb-4 mr-4 ml-4")
                    
                
                    
                ])
                
            ],className = "col-4"),
           

        ],className="row mb-4"),
    ],className="container mt-4")


])
#,"height":"800","width":"100%"


@app.callback(Output('graph4', 'figure'),
              [Input('graph2-checklist','value'),Input('graph2-slider','value'),Input('graph4-radio','value')])
def make_graph4(selected_user,selected_slider,selected_radio):


    global topic,color_dict

    df = topic.copy()

    df = df[(df["month"]==selected_slider) & (df["user"]==selected_user)]
    print(df.head(5))


    temp_df = df.groupby(["graph_topic","week"])["count","mean","pos","neu","neg"].sum()
    temp_df.reset_index(inplace=True)
    if selected_radio in ["pos","neg","neu"]:
        temp_df[selected_radio] = (temp_df[selected_radio]/temp_df["count"])*100

    #df = df[df["graph_topic"]==1]
    #df["mean"]=df["mean"].rolling(7).mean()

    #print(df.keys())
    #print(df.head(10))
    fig = px.line(temp_df, x="week", y=selected_radio, color="graph_topic",color_discrete_map=color_dict,
         labels = dict(week = "Weeks of "+calendar.month_name[selected_slider],user="",mean="Sentiment Score",count="Count",pos="Positive Tweet %",neg="Negative Tweet %",neu="Neutral Tweet %"),line_shape='linear')

    return fig



@app.callback(Output('favorites', 'children'),
              [Input('graph2-slider','value')])
def getFavorites(selected_slider):

    fig0=html.H2(calendar.month_name[selected_slider],className="d-flex mt-1 mb-4 justify-content-center col-12")
    fig1=getCard(selected_slider,"biden",True)
    fig2=getCard(selected_slider,"biden",False)
    fig3=getCard(selected_slider,"trump",True)
    fig4=getCard(selected_slider,"trump",False)

    return fig0,fig1,fig2,fig3,fig4

def getCard(selected_month,user,fav):
    global biden_df,trump_df
    emoji=""
    if fav:
        card_title = "Most 💗"
        #emoji="💗"
        to_find = "favorites"
    else:
        card_title = "Most 🔁"
        #emoji="🔁"
        to_find = "retweets"

    if user=="biden":
        card_class = "bg-info"
        df = biden_df[biden_df.month==selected_month]
        #id_text = "tweet id"
        #url_txt = "https://twitter.com/JoeBiden/status/"

    else:
        card_class = "bg-danger"
        df = trump_df[trump_df.month==selected_month]
        #id_text = "id"
        #url_txt = "https://twitter.com/realDonaldTrump/status/"

    temp_df = df[df[to_find]==max(df[to_find])]

    txt= temp_df["text"]
    if temp_df[to_find].iloc[0]/1000<1000:
        btn_txt = emoji+str(round(temp_df[to_find].iloc[0]/1000,2))+"K"
    else:
        btn_txt = emoji+str(round(temp_df[to_find].iloc[0]/1000000,2))+"M"
    
    #url_txt = url_txt+str(temp_df[id_text].iloc[0])
    #print(url_txt)

    fig1= html.Div([
        dbc.Card(
            [
                dbc.CardBody(
                    [   
                        html.H4(card_title, className="card-title"),
                        dbc.Button(btn_txt, color="primary",className="mb-2"),
                        #html.P(txt, className="card-text"),
                        html.P(txt,className="card-text")
                        
                        
                    ]
                ),
            ],
            style={"width": "18rem"},className="mr-auto ml-auto "+card_class
        ),
        
    ],className="col-3 d-flex")
    return fig1
@app.callback(Output('monthstats', 'children'),
              [Input('graph2-slider','value')])
def getMonthStats(selected_slider):

    fig1=getYearCard(selected_slider,"biden",1,selected_slider)
    fig2=getYearCard(selected_slider,"biden",2,selected_slider)
    fig3=getYearCard(selected_slider,"biden",3,selected_slider)
    fig4=getYearCard(selected_slider,"trump",1,selected_slider)
    fig5=getYearCard(selected_slider,"trump",2,selected_slider)
    fig6=getYearCard(selected_slider,"trump",3,selected_slider)

    return fig1,fig2,fig3,fig4,fig5,fig6



@app.callback(Output('yearstats', 'children'),
              [Input('graph2-slider','value')])
def getYear(selected_slider):

    fig1=getYearCard(selected_slider,"biden",1,0)
    fig2=getYearCard(selected_slider,"biden",2,0)
    fig3=getYearCard(selected_slider,"biden",3,0)
    fig4=getYearCard(selected_slider,"trump",1,0)
    fig5=getYearCard(selected_slider,"trump",2,0)
    fig6=getYearCard(selected_slider,"trump",3,0)

    return fig1,fig2,fig3,fig4,fig5,fig6

def getYearCard(selected_month,user,mode,mode_month):
    global biden_df,trump_df



    if user=="biden":
        card_class = "bg-info"
        df = biden_df
    else:
        card_class = "bg-danger"
        df = trump_df

    if mode_month>0:
        df = df[df["month"]==mode_month]

    if mode == 1:
        c = len(df)
        card_title = "Total 🐦"
    elif mode == 2:
        c= df['retweets'].mean()
        card_title = "AVG 🔁"
    elif mode ==3:
        c = df['favorites'].mean()
        card_title = "AVG 💗"

    if c<1000:
        txt=str(c)
    elif (c/1000)<1000:
        c = round(c/1000,2)
        txt = str(c)+"K"
    else:
        c = round(c/1000000,2)
        txt = str(c)+"M"

    
    fig1= html.Div([
        dbc.Card(
            [
                dbc.CardBody(
                    [   
                        html.H4(card_title, className="card-title"),
                        #html.P(temp_df["text"], className="card-text"),
                        # html.Div([
                        #     html.Div([
                        #         html.P("Total Tweets",className="card-text"),
                        #         dbc.Button(txt3, color="primary"),
                        #     ],className="col-4"),
                        #     html.Div([
                        #         html.P("Average Retweets",className="card-text"),
                        #         dbc.Button(txt2, color="primary")
                        #     ],className="col-4"),
                        #     html.Div([
                        #         html.P("Average Favorites",className="card-text"),
                        #         dbc.Button(txt, color="primary")
                        #     ],className="col-2")
                        # ],className="row")

                        dbc.Button(txt, color="primary")
                        
                       
                    ]
                ),
            ],
            style={"width": "18rem"},className="ml-auto mr-auto "+card_class
        ),
        
    ],className="col-2 d-flex mt-4")
    return fig1

@app.callback(Output('graph2', 'children'),
              [Input('graph2-checklist', 'value'),Input('graph2-slider','value')])
def make_graph2(selected_value,selected_slider):
    graph_html = selected_value+str(selected_slider)+'.html'

    if selected_value=="trump":
        txt_class ="text-danger"
    else:
        txt_class = "text-info"

    fig0 = html.Div([
        html.H1(selected_value,className="mt-4 ml-auto mr-auto "+txt_class)
    ],className = "row d-flex")
    


    #print(graph_html)
    fig = html.Iframe(
        src = app.get_asset_url(graph_html),height=800,width="100%",className="mt-4 mb-2"
    )

    # fig = html.Iframe(
    #     src = app.get_asset_url("test.html"),height=800,width="100%",className="mt-4 mb-2"
    # )
    return fig0,fig



@app.callback(Output('graph1', 'figure'),
              [Input('graph1-checklist-1', 'value'),Input('graph1-checklist-2', 'value'),Input('graph1-slider','value')])
def make_graph1(selected_value_1,selected_value_2,selected_slider):
    #print(selected_slider)

    selected_value = selected_value_1.copy()
    selected_value.extend(selected_value_2)

    # print("==")
    # print(selected_value_1)
    # print(selected_value_2)
    # print("==")
    global df_global,total,color_dict
    #df =  df_global[df_global["user"]==selected_dropdown_value]
    #fig = px.histogram(df, x="pos")
    df =  df_global.copy()

    #del df["moving_avg"]
    temp_df=total.copy()
    temp_df["user"]=["reddit_trump" if y == "trump" else "reddit_biden" for y in total["user"]]
    temp_df = df.append(temp_df)


    temp_df_2 = poll_date.copy()
    temp_df = temp_df.append(temp_df_2)

    temp_df.sort_values(["user","_date"],inplace=True)

    temp_list = []
    for u in temp_df["user"].unique():
        temp_list.extend(temp_df[temp_df["user"]==u]["mean"].rolling(selected_slider).mean())
    temp_df["moving_avg"]=temp_list
    
   

    df = temp_df.copy()
    #df["moving_avg"]=group_df[group_df["user"]=="biden"]["mean"].rolling(selected_slider).mean().append(group_df[group_df["user"]=="trump"]["mean"].rolling(selected_slider).mean())
    #df.reset_index(inplace=True)
    fig = ""

    #print(selected_value)
    df = df[df['user'].isin(selected_value)]

    if len(df)==0:
        return ""




    fig = px.line(df, x="_date", y="moving_avg", color="user",color_discrete_map=color_dict,
    labels = dict(_date = "Date",moving_avg="Moving Average - "+str(selected_slider),user=""),line_shape='linear')
    

    return fig

    

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    global df_global
    df = df_global[df_global["user"]==selected_dropdown_value]
    


    return {
        'data': [{
            'x': df.index,
            'y': df["mean"],
           
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }


@app.callback(Output('graph3', 'figure'),
              [Input('graph1-checklist-1', 'value')])
def make_graph3(selected_dropdown_value):

    global df_global,colors
    one_df = df_global.copy()
    #one_df['month']=pd.DatetimeIndex(one_df.index).month
    trump_agg = one_df[one_df["user"]=="trump"].sum()
    biden_agg = one_df[one_df["user"]=="biden"].sum()


    # figure={
    #     'data': [
    #         {'x': ["Positive", "Neutral", "Negative"], 'y': [round((trump_agg["pos"]/trump_agg["count"])*100), round((trump_agg["neu"]/trump_agg["count"])*100), round((trump_agg["neg"]/trump_agg["count"])*100)], 'type': 'bar', 'name': "Trump"},
    #         {'x': ["Positive", "Neutral", "Negative"], 'y': [round((biden_agg["pos"]/biden_agg["count"])*100), round((biden_agg["neu"]/biden_agg["count"])*100), round((biden_agg["neg"]/biden_agg["count"])*100)], 'type': 'bar', 'name': "Biden"},
    #     ]
    # }
    
    months = ['Positive',"Neutral","Negative"]
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=[round((biden_agg["pos"]/biden_agg["count"])*100), round((biden_agg["neu"]/biden_agg["count"])*100), round((biden_agg["neg"]/biden_agg["count"])*100)],
        name='Biden',
        marker_color='blue'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=[round((trump_agg["pos"]/trump_agg["count"])*100), round((trump_agg["neu"]/trump_agg["count"])*100), round((trump_agg["neg"]/trump_agg["count"])*100)],
        name='Trump',
        marker_color='red'
    ))
    return fig
   
    
@app.callback(Output('redditstats', 'children'),
              [Input('graph2-checklist','value'),Input('graph2-slider','value')])
def getRedditStats(selected_user,selected_slider):
    global link,subreddit

    df = link[(link["month"]==selected_slider) & (link["user"]==selected_user)]
    temp_df=pd.DataFrame(df.groupby(["title","url"])["doc_count"].sum())
    temp_df = temp_df.sort_values(["doc_count"],ascending=False).head(4)
    temp_df.reset_index(inplace=True)

    fig0 = html.Div([
        html.H1("Most Shared Links for "+calendar.month_name[selected_slider],className="mt-4 ml-auto mr-auto ")
    ],className = "col-12 d-flex")

    fig1=getRedditCard(temp_df.iloc[0],selected_user)
    fig2=getRedditCard(temp_df.iloc[1],selected_user)
    fig3=getRedditCard(temp_df.iloc[2],selected_user)
    fig4=getRedditCard(temp_df.iloc[3],selected_user)
    #fig5=getRedditCard(temp_df.iloc[4],selected_user)


    df = subreddit[(subreddit["month"]==selected_slider) & (subreddit["user"]==selected_user)]
    temp_df=pd.DataFrame(df.groupby(["key"])["doc_count"].sum())
    temp_df = temp_df.sort_values(["doc_count"],ascending=False).head(4)
    temp_df.reset_index(inplace=True)

    fig6=getSubreddits(temp_df.iloc[0],selected_user)
    fig7=getSubreddits(temp_df.iloc[1],selected_user)
    fig8=getSubreddits(temp_df.iloc[2],selected_user)
    fig9=getSubreddits(temp_df.iloc[3],selected_user)

    fig5 = html.Div([
        html.H1("Most Popular Subreddits for "+calendar.month_name[selected_slider],className="mt-4 ml-auto mr-auto ")
    ],className = "col-12 d-flex")


    return fig0,fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9

def getRedditCard(temp_row,user):
    #global link



    if user=="biden":
        card_class = "info"
       
    else:
        card_class = "danger"

    
    c= temp_row["doc_count"]
    card_title = temp_row["title"]
    card_url = temp_row["url"]

    if c<1000:
        txt=str(c)
    elif (c/1000)<1000:
        c = round(c/1000,2)
        txt = str(c)+"K"
    else:
        c = round(c/1000000,2)
        txt = str(c)+"M"

    
    fig1= html.Div([
        dbc.Card(
            [
                dbc.CardBody(
                    [   
                        
                        #html.A("Open Link",href=card_url,className="mr-4"),
                        dbc.Button(txt, color=card_class+" btn-block mb-4"),
                        html.A(card_title, href=card_url,className="card-title")
                        
                       
                    ]
                ),
            ],
            style={"width": "18rem"},className="ml-auto mr-auto "
        ),
        
    ],className="col-3 d-flex mt-4")
    return fig1


def getSubreddits(temp_row,user):
    


    if user=="biden":
        card_class = "info"
       
    else:
        card_class = "danger"

    
    c= temp_row["doc_count"]
    card_title = temp_row["key"]
    #card_url = temp_row["url"]

    if c<1000:
        txt=str(c)
    elif (c/1000)<1000:
        c = round(c/1000,2)
        txt = str(c)+"K"
    else:
        c = round(c/1000000,2)
        txt = str(c)+"M"

    
    fig1= html.Div([
        dbc.Card(
            [
                dbc.CardBody(
                    [   
                        dbc.Button(card_title, color="primary btn-block"),
                        #html.A("Open Link",href=card_url,className="mr-4"),
                        dbc.Button(txt, color=card_class+" btn-block"),
                        #html.P(card_title, className="card-title")
                        
                       
                    ]
                ),
            ],
            style={"width": "18rem"},className="ml-auto mr-auto "
        ),
        
    ],className="col-3 d-flex mt-4")
    return fig1


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=80)