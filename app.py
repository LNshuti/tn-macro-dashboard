import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import gradio as gr
from PIL import Image
import io

def fetch_and_plot(company_name, indicator_type):
    # Map company names to tickers
    companies = {
        'HCA Healthcare': 'HCA',
        'FedEx': 'FDX',
        'AutoZone': 'AZO',
        'Dollar General': 'DG',
        'Tractor Supply Company': 'TSCO',
        'Mid-America Apartment Communities': 'MAA',
        'International Paper': 'IP',
        'Eastman Chemical': 'EMN',
        'Unum Group': 'UNM',
        'First Horizon Corporation': 'FHN',
        'Acadia Healthcare': 'ACHC',
        'Delek US Holdings': 'DK',
        'Community Health Systems': 'CYH'
    }

    # Get the ticker from the company name
    ticker = companies[company_name]

    # Get the current date minus one day
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Fetch Historical Data
    data = yf.download(ticker, start='2000-01-01', end=end_date)

    # Initialize the plot
    plt.figure(figsize=(10, 7))

    # Plot Various Technical Indicators based on the selected type
    if indicator_type == "SMA and EMA":
        sma = data['Close'].rolling(window=50).mean()
        ema = data['Close'].ewm(span=50, adjust=False).mean()
        plt.plot(data['Close'], label='Close')
        plt.plot(sma, label='50-day SMA')
        plt.plot(ema, label='50-day EMA')
        plt.title(f'{company_name} ({ticker}) Moving Averages')
        plt.legend()

    elif indicator_type == "RSI":
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        plt.plot(rsi, label='RSI')
        plt.axhline(70, linestyle='--', alpha=0.5, color='red')
        plt.axhline(30, linestyle='--', alpha=0.5, color='green')
        plt.title(f'{company_name} ({ticker}) Relative Strength Index')
        plt.legend()

    elif indicator_type == "MACD":
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        plt.plot(macd, label='MACD')
        plt.plot(signal, label='Signal Line')
        plt.bar(data.index, macd - signal, label='MACD Histogram', use_line_collection=True)
        plt.title(f'{company_name} ({ticker}) Moving Average Convergence Divergence')
        plt.legend()

    elif indicator_type == "Bollinger Bands":
        sma = data['Close'].rolling(window=20).mean()
        std = data['Close'].rolling(window=20).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        plt.plot(data['Close'], label='Close')
        plt.plot(sma, label='20-day SMA')
        plt.plot(upper_band, label='Upper Bollinger Band')
        plt.plot(lower_band, label='Lower Bollinger Band')
        plt.title(f'{company_name} ({ticker}) Bollinger Bands')
        plt.legend()

    # Convert plot to a PIL Image object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image = Image.open(buf)

    return image

# Define the company and indicator options
company_choices = [
    'HCA Healthcare',
    'FedEx',
    'AutoZone',
    'Dollar General',
    'Tractor Supply Company',
    'Mid-America Apartment Communities',
    'International Paper',
    'Eastman Chemical',
    'Unum Group',
    'First Horizon Corporation',
    'Acadia Healthcare',
    'Delek US Holdings',
    'Community Health Systems'
]

indicators = ["SMA and EMA", "RSI", "MACD", "Bollinger Bands"]

with gr.Blocks() as app:
    with gr.Tab("Technical Indicators"):
        with gr.Column():
            dropdown_company = gr.Dropdown(choices=company_choices, label="Select a Company")
            dropdown_indicator = gr.Dropdown(choices=indicators, label="Select Indicator Type")
            plot_button = gr.Button("Plot")
            image_display = gr.Image()

    plot_button.click(
        fetch_and_plot,
        inputs=[dropdown_company, dropdown_indicator],
        outputs=image_display
    )

app.launch()
