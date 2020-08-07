#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 17:41:55 2020

@author: Alex
"""

##Importing libaries
import os
import plotly.graph_objs as go #Offline plotting
import chart_studio.plotly as py #Online plotting
import plotly.io as pio
import pandas as pd
import datetime
import calendar
# import modin.pandas as pd #This utilises all CPU cores, rather than Pandas default one core 
pio.renderers.default = "browser"
pio.templates


##Adding plot.ly credentials
import chart_studio
chart_studio.tools.set_credentials_file(username='alexhewson',
                                  api_key='3EEPd2mvBSQd1vGCq14s')

##Set working directory
os.chdir("/Users/Alex/Prison Reform Trust/Policy and Comms Team - Documents/Python/Weekly prison population")


##Setting templates
prt_template = go.layout.Template(
    layout=go.Layout(title_font=dict(
            family="Helvetica Neue, Arial", 
            size=17),

font_color = '#54565B',
font_family = "Helvetica Neue, Arial",
font_size = 12,
paper_bgcolor = "#FBFAF7",
plot_bgcolor = "#FBFAF7",
colorway = ("#A01D28", "#499CC9", "#F9A237", "#6FBA3A"))
)

##Reading in data
df = pd.read_csv("HDC.csv",
                 usecols=["date", "hdc_pop"],
                 index_col=["date"],
                 parse_dates = ['date'])

df['year'] = df.index.year
df['week'] = df.index.week
df['month'] = df.index.month

df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])

weeks = 52/12.0
months = [datetime.date(2020, m, 1).strftime('%b') for m in range(1, 13)]


##Plotting

fig = go.Figure()

for year in df['year']['2017':'2020'].unique():
  df_year = df[df['year'] == year]
  
  fig.add_trace(go.Scatter(x=df_year['week'], y=df_year['hdc_pop'],
                    mode='lines',
                    connectgaps = True,
                    hovertext =df['month'],
                    hovertemplate = 
                    '<b>%{hovertext}</b><br>'+
                    '%{y:,.0f}',
                    name=str(year)))


##Edit the layout

fig.update_layout(title="<b>HDC population in England and Wales</b>",
                  yaxis_title='Number of people on HDC',
                  yaxis_tickformat=',.0f',
                  xaxis_showgrid=False,
                  xaxis_tickmode = 'array',
                  xaxis_tickvals=[(2*k-1)*weeks/2 for k in range(1,13)],
                  xaxis_ticktext=months,
                  xaxis_ticks="inside",
                  xaxis_tickcolor='#54565B',
                  template=prt_template,                   
                  showlegend=False,
                  hovermode='x',
                  modebar_activecolor="#A12833",
                  width=655,
                  height=500,
                  annotations=[
                      go.layout.Annotation(
                          x=-0.08,
                          y=-0.19,
                          showarrow=False,
                          text="<b>Source: Ministry of Justice Prison Population Bulletin\n</b>",
                          font_size=12,
                          xref="paper",
                          yref="paper"
                          )
                      ],
                  )


'''Still in development. Range selector is no longer working following switch of
x-values to weeks of the year'''

# fig.update_xaxes(hoverformat = '%d %b %Y',
#                  tickformatstops = [
#                          dict(dtickrange=[None, "M0.5"], value="%e %b"),
#                          dict(dtickrange=["M0.5", "M11"], value="%b %Y"),
#                          dict(dtickrange=["M11", None], value="%Y")
#                          ],
#                   rangeselector=dict(
#                           x=-0.06,
#                           y=0.91,
#                           buttons=list([
#                                   dict(count=3,
#                                       label="3m",
#                                       step="month",
#                                       stepmode="backward"),
#                                  dict(count=6,
#                                       label="6m",
#                                       step="month",
#                                       stepmode="backward"),
#                                  dict(count=1,
#                                       label="1y",
#                                       step="year",
#                                       stepmode="backward"),
#                                  dict(step="all")])
#                                  )
#                   )


fig.update_yaxes(range=[0, 3500], nticks=10)


'''
This section outputs the final chart, with static; interactive offline; and interactive online versions.
'''

##Plot static image
fig.write_image("images/HDC_population.png", width=655, height=500)

##Plot file offline
# fig.show(config={'displayModeBar': False})

##Plot file online with PRT logo

##PRT logo
fig.layout.images =[dict(
                source="https://i.ibb.co/jhfYbyc/PRTlogo-RGB.png",
                xref="paper", yref="paper",
                x=0.04, y=1.25,
                sizex=0.15, sizey=0.15,
                xanchor="right", yanchor="top"
                )]

py.plot(fig, filename = 'HDC population E&W', auto_open=True)