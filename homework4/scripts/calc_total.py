import json
import sys
import os
import os.path as osp
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import column
from bokeh.models import CustomJS, Dropdown


#load zipcode dictionary from output.json



def main():
    

    #load zipcode dictionary from output.json

    script_dir = osp.dirname(__file__)
    with open(osp.join(script_dir,"..","data","zip_codes.json"),"r") as codes_file:
        zip_codes = json.load(codes_file)

    #calc avgs
    sums=[0,0,0,0,0,0,0,0,0,0,0,0]
    averages=[0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range(12):
        for code in zip_codes:
            sums[i]+=zip_codes[code][str(i+1)]
    
    for i in range(12):
        averages[i]=sums[i]/len(zip_codes)

    with open(osp.join(script_dir, '..', 'data','total.json'), 'w') as out_file:
        json.dump({"total":averages}, out_file, indent=2)

if __name__ == "__main__":
    main()
