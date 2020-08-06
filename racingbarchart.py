
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import datetime
from IPython.display import HTML

df = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')


a = list(df.columns.values)
dates = a[-30:]

count = 0
dff = (df.sort_values(by=dates[count], ascending=False)
       .head(10))
dff

fig, ax = plt.subplots(figsize=(15, 10))
dff = dff[::-1]  # flip the order of items in data frame
ax.barh(dff['Country/Region'], dff[dates[count]])

colors = dict(zip(
    ['US', 'Brazil', 'Russia', 'United Kingdom', 'India', 'Spain',
     'Italy', 'Germany', 'France', 'Peru', 'China', 'Turkey',
     'Belgium', 'Switzerland', 'Iran', 'Mexico', 'Chile', 'South Africa', 'Colombia'],
    ['#00429d', '#b41648',  '#4771b2', '#5d8abd', '#e4576b', '#8abccf',
     '#a5d5d8', '#c5eddf', '#ffdec7', '#ffbcaf', '#ff9895', '#f4777f',
     '#73a2c6', '#cf3759', '#2e59a8', '#93003a', '#73003a', '#d3003a', '#0fa29d']  # colors are from https://gka.github.io/palettes/
))
group_lk = df.set_index('Country/Region').to_dict()

fig, ax = plt.subplots(figsize=(15, 10))


def draw_barchart(date):
    dff = df.sort_values(by=date, ascending=True).tail(10)
    ax.clear()
    ax.barh(dff['Country/Region'], dff[date], color=[colors[x]
                                                     for x in dff['Country/Region']])
    dx = dff[date].max() / 200

    for i, (value, country) in enumerate(zip(dff[date], dff['Country/Region'])):
        ax.text(value-dx, i,     country,           size=10,
                weight=600, ha='right', va='bottom')
        ax.text(value+dx, i,     f'{value:,.0f}',
                size=14, ha='left',  va='center')

    # polish styles
    current_date = datetime.datetime.strptime(date, "%m/%d/%y")
    new_current_date = current_date.strftime("%d %B %Y")
    #print (new_current_date)

    ax.text(1, 0.4, new_current_date, transform=ax.transAxes,
            color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Cases (thousands)',
            transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.12, 'Coronavirus (COVID-19) cases recorded for the last 30 days',
            transform=ax.transAxes, size=24, weight=600, ha='left')
    ax.text(1, 0, 'by @farhan; credit @pratapvardhan', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)


draw_barchart('6/14/20')

"""Animation"""

fig, ax = plt.subplots(figsize=(15, 10))
animator = animation.FuncAnimation(
    fig, draw_barchart, frames=dates, interval=600)
HTML(animator.to_jshtml())

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='farhan'), bitrate=1800)

animator.save('lines.mp4', writer=writer)
