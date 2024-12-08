import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib as mpl
import json
import os
from datetime import datetime


def get_dates_boundaries(diagram_data):
    min_date = diagram_data[0]['groups'][0]['date-begin']
    max_date = diagram_data[0]['groups'][0]['date-end']
    for item in diagram_data[1:]:
        for group in item['groups']:
            min_date = min(min_date, group['date-begin'])
            max_date = max(max_date, group['date-end'])
    return (min_date, max_date)

def get_rows_boundaries(diagram_data):
    min_row = diagram_data[0]['row']
    max_row = diagram_data[0]['row']
    for item in diagram_data[1:]:
        min_row = min(min_row, item['row'])
        max_row = max(max_row, item['row'])
    return (min_row, max_row)

def get_list_of_groups(diagram_data):
    groups = []
    for item in diagram_data:
        for group in item['groups']:
            if group['name'] not in groups:
                groups.append(group['name'])
    return groups

def load_json(filename):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, filename), 'r') as file:
        json_file = json.load(file)
    return json_file


TEXT_PADDING = 10
EDGESIZE = 2
ROW_HEIGHT_INCH = 3
ROW_PADDING = .5
COLORS = ['r', 'g']

diagram_data = load_json('test-file.json')['chronological_sankey_data']
(min_row, max_row) = get_rows_boundaries(diagram_data)
(min_date, max_date) = get_dates_boundaries(diagram_data)

list_of_groups = get_list_of_groups(diagram_data)

with mpl.rc_context({
    'xtick.minor.size': 2,
    'xtick.major.size': 12}):

    fig, ax = plt.subplots(figsize=(12, (max_row - min_row)*ROW_HEIGHT_INCH))

    for item in diagram_data:
        row = item['row']
        for i, group in enumerate(item['groups']):
            start = mdates.date2num(datetime.fromisoformat(group['date-begin']))
            end = mdates.date2num(datetime.fromisoformat(group['date-end']))
            color = COLORS[list_of_groups.index(group['name'])]

            if i > 0:
                ax.add_patch(plt.Rectangle((start, -row), prev_end-start, 1, fc='k', alpha=.5))

            ax.add_patch(plt.Rectangle((start, -row), end-start, 1, fc=color))
            if i == 0:
                ax.text(start + TEXT_PADDING, -row+.5, item['name'], verticalalignment='center_baseline', fontsize=15)

            prev_end = end
    
    for parent in diagram_data:
        number_of_childs = len(parent['childs'])
        for i, child_name in enumerate(parent['childs']):
            for child in diagram_data:
                if child['name'] == child_name:
                    row_begin_path = 1-parent['row']-i/number_of_childs
                    row_end_path = 1-child['row']

                    row_begin_height = 1/number_of_childs
                    row_end_height = 1

                    date_begin = parent['groups'][-1]['date-end']
                    date_end = child['groups'][0]['date-begin']

                    date_begin_path = mdates.date2num(datetime.fromisoformat(date_begin))
                    date_end_path = mdates.date2num(datetime.fromisoformat(date_end))

                    path_data = [
                        (mpath.Path.MOVETO, (date_begin_path, row_begin_path)),
                        (mpath.Path.CURVE4, ((date_begin_path + date_end_path)/2, row_begin_path)),
                        (mpath.Path.CURVE4, ((date_begin_path + date_end_path)/2, row_end_path)),
                        (mpath.Path.CURVE4, (date_end_path, row_end_path)),
                        (mpath.Path.LINETO, (date_end_path, row_end_path-row_end_height)),
                        (mpath.Path.CURVE4, ((date_begin_path + date_end_path)/2, row_end_path-row_end_height)),
                        (mpath.Path.CURVE4, ((date_begin_path + date_end_path)/2, row_begin_path-row_begin_height)),
                        (mpath.Path.CURVE4, (date_begin_path, row_begin_path-row_begin_height)),
                        (mpath.Path.CLOSEPOLY, (date_begin_path, row_begin_path))
                        ]

                    codes, verts = zip(*path_data)
                    patch = mpatches.PathPatch(mpath.Path(verts, codes), facecolor='k', alpha=.5)
                    ax.add_patch(patch)

    ax.set_xlim([mdates.date2num(datetime.fromisoformat(min_date)),
                mdates.date2num(datetime.fromisoformat(max_date))])

    ax.set_ylim([-max_row-ROW_PADDING,
                1-min_row+ROW_PADDING])

    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.get_yaxis().set_visible(False)

    ax.spines.left.set_visible(False)
    ax.spines.right.set_visible(False)

    ax.grid(True)

    plt.show()
