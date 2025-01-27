
# make picture
# make picture function
# make UI outline - eith buttons and the works
# use function to put picture in UI
# make it so that UI changes based on inputs

from Functions import *
import tkinter as tk
from PIL import Image, ImageTk
from events import *
import subprocess
import ast



# Notice, This is Using YFINANCE data whic may be unreliable
# ALSO data maybe not be going far enough back
# so, you need to use flat files!

symbollist = ['tsla', 'aapl', 'msft', 'spy', 'AUDUSD=X', 'X', 'bno', 'BTC', 'f', 'fxb', 'xom', 'nflx']

graphnamelist = ['Tesla Stock', 'Apple Stock', 'Microsoft Stock', 'S&P500 Index', 'AUS Dollar vs US Dollar',
                  'X', 'Brent Crude Oil Futures', 'Bitcoin Futures', 'Ford Stock', 'GPB vs US Dollar', 
                  'Exonn Mobil Stock', 'Netflix Stock']


window = 3
bits = False
legend = False

with open('datelist.txt', 'r') as f:
    content = f.read()
    dates = ast.literal_eval(content)

for i in range(0, 12, 1):
    symbol = symbollist[i]
    title = graphnamelist[i]
    makePlot(symbol, window, dates, title_= title, bits_= True)

subprocess.run(['python', 'GUI.py'])

