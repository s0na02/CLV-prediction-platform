import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter
from pandas_profiling import ProfileReport
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import *
from lifetimes.utils import *
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.plotting import plot_probability_alive_matrix
from lifetimes.plotting import plot_frequency_recency_matrix
from lifetimes.plotting import plot_period_transactions
from lifetimes.utils import calibration_and_holdout_data
import squarify
# TODO: from wordcloud import WordCloud

from dash import Dash, html, dcc
from dash.dependencies import Input, Output

data = pd.read_excel("Dataset.xlsx")

data['InvoiceDate'].agg(['min', 'max'])

fd = data.drop_duplicates()


# TODO:
# text = " ".join(review for review in data.Country.astype(str))
# x, y = np.ogrid[:300, :00]
# #mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
# #mask = 560 * mask.astype(int)
# wc = WordCloud(background_color="white", repeat=True, width=1600, height=800,  colormap='Dark2',)
# wc.generate(text)
# plt.axis("off")

# total purchase category plot
fd = fd[['Customer ID','Description','InvoiceDate','Invoice','Quantity','Price', 'Country']]
fd = fd[(fd['Quantity']>0)]
fd['TotalPurchase'] = fd['Quantity'] * fd['Price']

df_plot_bar = fd.groupby('Description').agg({'TotalPurchase':'sum'}).sort_values(by = 'TotalPurchase', ascending=False).reset_index().head(5)
df_plot_bar['Percent'] = round((df_plot_bar['TotalPurchase'] / df_plot_bar['TotalPurchase'].sum()) * 100,2)
fir_plotbar = px.bar(df_plot_bar, y='Percent', x='Description', title='Top selling products', 
text='Percent', color='Percent')
fir_plotbar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
fir_plotbar.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(1, 0, 0, 0)',
})
fir_plotbar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',showlegend=False)

#  
df_plot = fd.groupby(['Country','Description','Price','Quantity']).agg({'TotalPurchase': 'sum'},{'Quantity':'sum'}).reset_index()
fig_miricle = px.scatter(df_plot[:25000], x="Price", y="Quantity", color = 'Country', 
        size='TotalPurchase',  size_max=20, log_y= True, log_x= True, title= "PURCHASE TREND ACROSS COUNTRIES")
fig_miricle.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(1, 0, 0, 0)',
})

#
time_serious_invoice = go.Figure([go.Scatter(x=fd['InvoiceDate'], y=fd['Quantity'])])

#
new = summary_data_from_transaction_data(fd, 'Customer ID', 'InvoiceDate', monetary_value_col='TotalPurchase', observation_period_end='2011-12-9')
new['percent'] = round((new['frequency'] / new['frequency'].sum()) * 100,2)
frequency_barchart = px.bar(new, y=new['percent'], x=new['frequency'], title='Frequency BarChart', color='percent')


app = Dash(
    __name__,
    # TODO: implement styles
	external_stylesheets = [],
    suppress_callback_exceptions=True
)

server=app.server

app.layout = html.Div([
    html.Div([
		html.Div([
			html.H1('CLV Project')
		], id = 'title')
	]),
	html.Div([
		dcc.Tabs(id='tabs', value='tab-1', children=[
			dcc.Tab(label='CLV', value='clv-tab'),
			dcc.Tab(label='DATA DESCRIPTION', value='data-description-tab'),
			dcc.Tab(label='MODEL VISUALS', value='model-visuals-tab'),
    	]),
        html.Div(id='tab-content')
	]),
], className="container")

def render_stats():
    container_styles = {
        'display': 'flex',
        'flexWrap': 'wrap',
        'width': '100%',
    }

    item_styles = {
        'width': 'calc(50% - 128px)',
        'margin': '64px',
    }

    html.Div([
        html.Div([
            html.Span(children="Total Customers"),
            # TODO: show actual number
            html.Span(children="10")
        ], style=item_styles),
        html.Div([
            html.Span(children="Total Purchases"),
            # TODO: show actual number
            html.Span(children="10")
        ], style=item_styles),
    ], className='stats-container', style=container_styles)

def render_clv_graphs():
    container_styles = {
        'display': 'flex',
        'flexWrap': 'wrap',
        'width': '100%',
    }

    graphs = html.Div([
        html.Div([
            # dcc.Graph(figure=)
        ], style={}),
        html.Div([
            html.Div([
                # dcc.Graph(figure=)
            ]),
            html.Div([
                html.Div([
                    # dcc.Graph(figure=)
                ]),
                html.Div([
                    # dcc.Graph(figure=)
                ])
            ]),
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
        }),
    ], style=container_styles)

    return graphs

def render_data_description_graphs():
    container_styles = {
        'display': 'flex',
        'flexWrap': 'wrap',
        'width': '100%',
    }

    item_styles = {
        'width': 'calc(50% - 128px)',
        'margin': '64px',
    }

    graphs = html.Div([
        html.Div([
            dcc.Graph(figure=fir_plotbar),
        ], style=item_styles),
        html.Div([
            dcc.Graph(figure=fig_miricle),
        ], style=item_styles),
        html.Div([
            dcc.Graph(figure=time_serious_invoice),
        ], style=item_styles),
        html.Div([
            dcc.Graph(figure=frequency_barchart),
        ], style=item_styles),
    ], style=container_styles)

    return graphs

@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'clv-tab':
        return html.Div([
            render_clv_graphs()
        ], id='data-description-tab')

    if tab == 'data-description-tab':
        return html.Div([
            render_data_description_graphs()
        ], id='data-description-tab')


if __name__=='__main__':
	app.run_server(debug=True)
