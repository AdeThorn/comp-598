import json
import sys
import os
import os.path as osp
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import column
from bokeh.models import CustomJS, Dropdown



        
#load zipcode dictionary from output.json

script_dir = osp.dirname(__file__)
        
with open(osp.join(script_dir,"..","data","zip_codes.json"),"r") as codes_file:
    zip_codes = json.load(codes_file)

with open(osp.join(script_dir,"..","data","total.json"),"r") as total_file:
    total = json.load(total_file)

#create menus for dropdowns
menu=[str(code) for code in zip_codes ]

x = [1, 2, 3, 4, 5,6,7,8,9,10,11,12]

y_total = total["total"]

# create a new plot with a title and axis labels
p = figure(title="Graph of average response time vs month", x_axis_label='month (1-12)', y_axis_label='average response time (hours)',x_range=(0, 12), toolbar_location=None)

# add 2s line renderers to the plot
line_1 = p.line(x, y=[], legend_label="zip code 1", line_color="blue", line_width=2)
line_2 =p.line(x, y=[], legend_label="zip code 2", line_color="red", line_width=2)
line_3=p.line(x, y_total, legend_label="average of all zip codes", line_color="green", line_width=2)
ds1 = line_1.data_source
ds2 = line_2.data_source

def callback1(event):
    ds1.data['y'] = list(zip_codes[event.item].values())


def callback2(event):
    ds2.data['y'] = list(zip_codes[event.item].values())



dropdown1= Dropdown(label="choose zipcode 1", button_type="warning", menu=menu)
dropdown2= Dropdown(label="choose zipcode 2", button_type="warning", menu=menu)

# show the results
dropdown1.on_click(callback1)
dropdown2.on_click(callback2)
curdoc().add_root(column(dropdown1,dropdown2,p))
