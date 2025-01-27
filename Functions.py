from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import datetime, timedelta
from tkinter import filedialog


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return "Error: " + str(e)

def upload_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        return file_path.split("/")[-1]  # Returns just the filename
    return None


# Function to write list exactly as it appears
def list_to_file(lst, filename):
    # Convert list to string representation exactly as it appears in Python
    string_content = str(lst)
    
    # Write to file
    with open(filename, 'w') as f:
        f.write(string_content)


def get_earliest_date(date_list, date_format="%Y-%m-%d"):
    return min(date_list, key=lambda date: datetime.strptime(date, date_format))

def get_latest_date(date_list, date_format="%Y-%m-%d"):
    return max(date_list, key=lambda date: datetime.strptime(date, date_format))

def get_most_recent_date(ticker):
    try:
        # Download the last available day's data
        data = yf.download(ticker, period="1d", interval="1d", progress=False)
        if not data.empty:
            # Get the most recent date from the index
            most_recent_date = data.index[0].strftime("%Y-%m-%d")
            return most_recent_date
        else:
            return "No data available for this ticker."
    except Exception as e:
        return f"An error occurred: {e}"


# Further enhancing the function to make the graph even more visible
def makePlot(symbol_, window_, dates_, title_, bits_=False, legend_=False):

    symbol = symbol_
    window = window_
    bits = bits_
    legend = legend_
    election_dates = dates_ # dates should be brought in as a list EX: ['2025-01-03','2016-11-08','2012-11-06','2008-11-04','2007-11-04']
    title = title_

    earliest_date = get_earliest_date(election_dates)
    recent_date = get_most_recent_date(symbol)

    # Download S&P 500 data with a wider range to account for weekends/holidays
    ticker = yf.download(symbol, start=earliest_date, end=recent_date)

    def get_event_window(data, event_date, window):
        event_date = pd.to_datetime(event_date)
    
        # Find the actual trading day on or after the event date
        while event_date not in data.index:
            event_date += pd.Timedelta(days=1)
    
        # Get window_size trading days before and after
        event_loc = data.index.get_loc(event_date)
        start_loc = max(0, event_loc - window)
        end_loc = min(len(data.index), event_loc + (int(window * 3)) + 1)
    
        window_data = data.iloc[start_loc:end_loc]['Adj Close']
    
        # Calculate percentage change from event day
        event_price = window_data.iloc[window_data.index.get_loc(event_date)]
        window_data = (window_data / event_price - 1) * 100
    
        # Create relative index (-7 to +7)
        relative_days = range(-len(window_data[:event_date].values) + 1, len(window_data[event_date:].values))
        window_data.index = relative_days
    
        return window_data

    # Get data for all elections
    all_events = pd.DataFrame()
    for date in election_dates:
        try:
            event_data = get_event_window(ticker, date, window=window)
            all_events = pd.concat([all_events, event_data], axis=1)
        except Exception as e:
            print("Could not process date: " + date + ", Error: " + str(e))

    # Calculate average across all events
    average_movement = all_events.mean(axis=1)

    # Create the plot
    plt.figure(figsize=(6, 4))  # Further increased figure size for better visibility
    
    # Calculate average and standard deviation (add this line)
    std_dev = all_events.std(axis=1)

    # Calculate average and standard deviation (add this line)
    std_dev = all_events.std(axis=1)

    # In the plotting section, add these two lines before plotting the average line:
    plt.fill_between(average_movement.index, 
                    average_movement - 2*std_dev, 
                    average_movement + 2*std_dev, 
                    color='red', alpha=0.1, 
                    label='2σ Band')
    
    plt.fill_between(average_movement.index, 
                    average_movement - std_dev, 
                    average_movement + std_dev, 
                    color='red', alpha=0.1, 
                    label='1σ Band')

    # Plot average line (even thicker and grey)
    plt.plot(average_movement.index, average_movement.values, 
            linewidth=2, color='grey', label='Average', zorder=5, alpha=0.9)

    # Add only the most recent election line (2020)
    most_recent_date = election_dates[0]  # '2020-11-03'
    event_data = get_event_window(ticker, most_recent_date, window=window)
    plt.plot(event_data.index, event_data.values, 
            linewidth=4, color='#6495ED', label='Current Occurrence', zorder=6)

    plt.axvline(x=0, color='gray', linestyle='-', alpha=0.6, linewidth=2, label='Event Day')
    plt.axhline(y=0, color='gray', linestyle='-', alpha=0.6, linewidth=2)

    # Add labels and title with even larger, bold fonts
    plt.title(title, fontsize=15, pad=7, fontfamily='monospace')

    # Increase tick label sizes
    plt.tick_params(axis='both', which='major', labelsize=15)

    # Add percentage signs to y-axis ticks
    plt.gca().yaxis.set_major_formatter(PercentFormatter(decimals=0))

    # Add legend with larger font
    if legend:
        plt.legend(title='', fontsize=16)

    # Tight layout for better spacing
    plt.tight_layout()

    # Save the plot
    plt.savefig(symbol + '_event_analysis.png')
    #plt.show()

    print("Event Analysis for '" + symbol + "' complete with window of " + str(window))

# Done further enhancing the function
