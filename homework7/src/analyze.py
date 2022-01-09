import argparse
import os 
import os.path as osp
import json
import pandas as pd


def tsv_col_to_list(in_file):
    df=pd.read_csv(in_file, sep='\t')
    lst = df['coding'].tolist()
    return lst


def count_vals(in_list):
    out_dict={"course-related":0,"food_related":0,"residence-related":0,"other":0}
    
    for val in in_list:
        if val =="c":
            out_dict["course-related"]+=1

        elif val =="f":
            out_dict["food_related"]+=1

        elif val =="r":
            out_dict["residence-related"]+=1

        elif val =="o":
            out_dict["other"]+=1

    return out_dict



def output_screen(out_dict):
    json_s = json.dumps(out_dict)
    print(json_s)

def output_json(out_dict,out_file):
    
    #make folder if not exist
    dir_name,file_name = osp.split(out_file)

    if dir_name != '':
        try:
            os.makedirs(dir_name)
        except OSError as error:
           pass
    
    #output to json file
    with open(out_file,'w') as f:
        json.dump(out_dict,f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--out_file')
    parser.add_argument('-i','--coded_file')


    args = parser.parse_args()
    
    lst = tsv_col_to_list(args.coded_file)
    
    #if -o argument not specified output json obj to stdout
    if args.out_file:
        output_json(count_vals(lst),args.out_file)
    else:
        output_screen(count_vals(lst))



if __name__=="__main__":
    main()
