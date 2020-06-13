#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 09:19:32 2019

@author: Natalie
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import functions as f
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from ast import literal_eval
from geopy import distance
from sklearn.metrics.pairwise import cosine_similarity
#import doc_map.html
import folium

# instantiating the class
r = f.Recommendation('vectorized', 'response', 'zipsdf', 'gender', 'new_patient', 'need_ins', 'langs', 'specs', 'ins_s', '_id', 'zipcode', 'rec_input', 'n')
all_options =  f.all_plans
yesno = ['Yes', 'No']
languages = f.languages
specialties = f.specialties
genders = ['Female', 'Male', 'I do not have a preference']
rec_df = f.response
df = f.vectorized
zipsdf = f.zipsdf
for_model = df.iloc[:, 3:]

# def rec_input(gender, new_patient, need_ins, langs, specs, plan):
#     tests = for_model
#     testdict = tests.to_dict()
#     series_template = {x:0 for x in testdict} 
        
#     if gender == genders[0]:
#         series_template['Gender'] = 1
#     elif gender == genders[1]:
#         series_template['Gender'] = 0
#     elif gender == genders[2]:
#         series_template['Gender'] = 0.5
            
#     if new_patient == yesno[0]:
#         series_template['New_Patients'] = 1
            
#     series_template['num_lang'] = len(langs)
        
#     if need_ins == yesno[0]:
#         series_template['insurance'] = 1
            
#     for spec in specs: 
#         series_template['{}'.format(spec)] = 1
        
#     if plan == 'na':
#         pass
#     else:
#         series_template['{}'.format(plan)] = 1
            
#     for lang in langs: 
#         series_template['{}'.format(lang)] = 1
            
#     return pd.DataFrame(series_template, index=[0])


print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# adding callbacks to things that don't exist yet --> we need to suppress callback exceptions
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='session', storage_type = 'local')
#    html.Div(id='intermediate-value', style={'display': 'none'})
])


index_page = html.Div([
        
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
        
    html.H1('Welcome to Recommind!', 
            style = {'color': '#008080', 'fontSize': 25, 'font-weight': 'bold'}),
    dcc.Link(html.Button('Get Started'), href='/form', id = 'start'),
    html.Br()
], style = {'textAlign': 'center', 'vertical-align': 'middle'})

page_1_layout = html.Div([
        
    
    html.H1('Welcome to Recommind!', 
            style = {'color': '#008080', 'fontSize': 25, 'text-align': 'center', 'font-weight': 'bold'}),
            
    html.H1('Please fill out the following questionnaire:', 
            style = {'color': '#008080', 'fontSize': 20, 'text-align': 'center', 'font-style': 'italic'}),
    
    dcc.Markdown('''
                 **Do you need insurance coverage?**
                 '''),
    dcc.RadioItems(id = 'need_ins', 
                   options = [{'label': i, 'value': i} for i in yesno],
                   labelStyle={'display': 'inline-block'}),

    html.Hr(),
    dcc.Markdown('''
                 **Please select your insurance provider if applicable. Otherwise, select 'na':**
                 '''),
    dcc.Dropdown(
        id='providers-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Aetna'),

    html.Hr(),
    dcc.Markdown('''
                 **If you have selected an insurance provider, please select your insurance plan.
                 If you have selected 'na' for your insurance provider, select 'na' for the plan as well:**
                 '''),
    dcc.Dropdown(
            id='plans-dropdown'),
    html.Div(id='intermediate-value', style={'display': 'none'}),

    html.Hr(),
    dcc.Markdown('''
                 **Are you a new patient?**
                 '''),
    dcc.RadioItems(
            id = 'new_patient',
            options = [{'label': i, 'value': i} for i in yesno],
            labelStyle={'display': 'inline-block'}),
              
    html.Hr(),
    dcc.Markdown('''
                 **Which language(s) do you speak?**
                 '''),
    dcc.Dropdown(
            id = 'langs',
            options = [{'label': i, 'value': i} for i in languages],
            multi=True),
    
    html.Hr(),
    dcc.Markdown('''
                 **Do you have a gender preference for your practitioner?**
                 '''),
    dcc.RadioItems(
            id = 'gender', 
            options= [{'label': i, 'value':i} for i in genders],
            labelStyle={'display': 'inline-block'}),
            
    html.Hr(),
    dcc.Markdown('''
                 **Which specialty/specialties do you need?**
                 '''),
    dcc.Dropdown(
            id = 'specs', 
            options = [{'label': i, 'value': i} for i in specialties],
            multi=True),
            
    html.Hr(),
    dcc.Markdown('''
                 **Input your zipcode below:**
                 '''),
            
    dcc.Input(
            id='zipcode', 
            placeholder = 'eg. 10004',
            maxLength = 5),
    
    html.Hr(),
    html.Div(id='page-1-content'),
    html.Br(),
    html.Div([
    html.Div([dcc.Link(html.Button('Submit'), href='/results', id = 'submit-button')], 
              style = {'display': 'inline-block', 'align': 'left'}),
    
    html.Div([dcc.Link(html.Button('Go back to home'), href='/')], 
              style = {'display': 'inline-block', 'align': 'left'})
    ], style = {'textAlign': 'center'})
])
    
page_2_layout = html.Div([
    html.H1('See Results Below', 
            style = {'color': '#008080', 'fontSize': 25, 'text-align': 'center', 'font-weight': 'bold'}),
#    dcc.RadioItems(
#        id='page-2-radios',
#        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
#        value='Orange'
#    ),
    html.Div([html.P(id='page-2-content')], style={'display': 'inline-block'}),
    
    
             
    html.Div([
    html.Div([
    dcc.Link(html.Button('Go back to form'), href='/form', style = {'display': 'inline-block', 'align' : 'right'})],
             style = {'display': 'inline-block', 'align': 'left'}),
    html.Div([
    dcc.Link(html.Button('Go back to home'), href='/')
    ], style = {'display': 'inline-block', 'align': 'left'})
    ], style = {'textAlign': 'center'})

])
    
    
@app.callback(
    Output('plans-dropdown', 'options'),
    [Input('providers-dropdown', 'value')])

def set_plans_options(selected_plan):
    return [{'label': i, 'value': i} for i in all_options[selected_plan]]

@app.callback(
    Output('intermediate-value', 'children'),
    [Input('plans-dropdown', 'value')])
def set_cities_value(value):
    return value

@app.callback(Output('session', 'data'),
              [Input('need_ins', 'value'),
               Input('intermediate-value', 'children'),
               Input('gender', 'value'),
               Input('new_patient', 'value'),
               Input('langs', 'value'),
               Input('specs', 'value'),
               Input('zipcode', 'value')
               ],
              [State('session', 'data')])
def on_click1(ins, plans, gender, new_pat, langs, specs, zipcode, data):
    data = []
    if ins is None:
        raise PreventUpdate
    data.append(ins)
    
    if plans is None:
        raise PreventUpdate
    data.append(plans)
    
    if gender is None:
        raise PreventUpdate
    data.append(gender)
    
    if new_pat is None:
        raise PreventUpdate
    data.append(new_pat)
    
    if langs is None: 
        raise PreventUpdate
    data.append(langs)
    
    if specs is None:
        raise PreventUpdate
    data.append(specs)
    
    if zipcode is None:
        raise PreventUpdate
    data.append(zipcode)
        
    return data


@app.callback(Output('page-2-content', 'children'),
              [Input('session', 'data')])
#               State('session', 'data')])
def page_2_ins(data):
    n = 5
    gender = data[2]
    new_pat = data[3]
    need_ins = data[0]
    plans = data[1]
    langs = data[4]
    specs = data[5]
    zipcode = data[6]
    test = r.rec_input(gender, new_pat, need_ins, langs, specs, plans)
    recs = r.cos_sim(df, test, n, zipcode)
    spaced = []
    for i in range(len(recs)):
        spaced.append(f"{i+1}" + ".")
        spaced.append(html.Br())
        for j in range(len(recs[i])):
            spaced.append(f"{recs[i][j]}")
            spaced.append(html.Br())
        spaced.append(html.Hr())
        
    return spaced

    


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/form':
        return page_1_layout
    elif pathname == '/results':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
    
