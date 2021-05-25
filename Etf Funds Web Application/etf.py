import streamlit as st
import plotly.express as px
from tiingo import TiingoClient
import pandas as pd
import sys
from streamlit import cli as stcli

config = {'session':True, 'api_key':'7de537e033ab0eb82d4dc8cab2fc0c39d1393acf'}
client = TiingoClient(config)

etf_name = {'VT':'Total World Stock ETF', 'VGK':'FTSE Europe ETF', 
            'VWO':'FTSE Emerging Markets ETF', 'QQQ':'Invesco QQQ Trust'}
ticker_list = ['VT', 'VGK', 'VWO', 'QQQ']

ticker_history = client.get_dataframe(ticker_list,
                                      frequency='monthly',
                                      metric_name='adjClose',
                                      startDate='2019-01-01',
                                      endDate='2021-12-31')

ticker_history.reset_index(inplace=True)
ticker_history.rename(columns={'index':'Date'}, inplace=True)
ticker_history.rename(columns = etf_name, inplace=True)

ticker_history['Date'] = pd.to_datetime(ticker_history['Date'])
ticker_history['Year'] = ticker_history['Date'].dt.year

for col in ticker_history[['Total World Stock ETF','FTSE Europe ETF',
                           'FTSE Emerging Markets ETF','Invesco QQQ Trust']]:
    ticker_history[f"{col} return pct"] = ticker_history[col].pct_change()*100

ticker_history.to_csv('Etf_dataset.csv', index=False)

def main():

	st.set_page_config(page_title='ETF Monthly Return')
	st.header('ETF Monthly Return Since 2019')
	st.subheader('Presented as Precentage')

	dataset = pd.read_csv('Etf_dataset.csv')

	year_select = st.slider('Year:', min_value= min(dataset['Year']), 
		max_value= max(dataset['Year']), value=(min(dataset['Year']), max(dataset['Year'])))

	mask = dataset['Year'].between(*year_select) 
	dataset = dataset[mask]


	line_chart = px.line(dataset, x="Date", y=["Total World Stock ETF return pct", "FTSE Europe ETF return pct",
	                      "FTSE Emerging Markets ETF return pct", "Invesco QQQ Trust return pct"],
	                     labels={'value':'Precentage', 'Date':'Time Span','variable':'ETF'}, width=1200, height=700)
	st.plotly_chart(line_chart)

	st.dataframe(dataset)

if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())