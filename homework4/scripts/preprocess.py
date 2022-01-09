import pandas as pd
import sys, os
import os.path as osp
from datetime import datetime
import json

#calculate response time(hours) given start date and enddate
def calc_response_time(row):
    start_date=row[1]
    end_date=row[2]
    #date format 10/12/2021 02:07:06 AM
    
    #convert dates to datetime objects
    #date in mm/dd/yyyy format
    start_date = datetime.strptime(start_date, "%m/%d/%Y %I:%M:%S %p")
    end_date = datetime.strptime(end_date, "%m/%d/%Y %I:%M:%S %p")

    diff = end_date - start_date
    hour_diff = diff.total_seconds() / 3600

    #hour_diff=diff.total_seconds() // 3600 (this gives quotient)

    return hour_diff

#get month number from input date
def get_month(row,i):
    date_given = datetime.strptime(row[1], "%m/%d/%Y %I:%M:%S %p")
    return date_given.month == i


def main():
    script_dir = osp.dirname(__file__)
    trimmed_csv = osp.join(script_dir,'..','data','trimmed_nyc_311_limit.csv')
    
    #read trimmed csv into dataframe
    df = pd.read_csv(trimmed_csv,header=None)
 
    
    #delete rows with missing zipcodes (na in data frame)
    #zipcode in 9th column

    df = df[df[8].notna()] #drop rows with missing zipcodes (removes ~ 50k rows)
    

    #drop rows with no end date (end date in column 3) removes ~100k rows
    df = df[df[2].notna()]
    
    
    #drop rows with closed date before create date (removes ~150k rows)
    df = df[ df[1] < df[2] ]

    #print(f"after dropping invalid dates {len(df.index)}" )
    
    #make dataframe with only columns (start date, end date, zip code)
    df = df.filter(items = [1,2,8], axis=1)
    

    #dictionary of key: unique zipcodes value: ( dictionary with key: month number, value: list of response times)
    zip_codes= {code:{1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0} for code in df[8]}
    


    #populate zip_codes
    
    for code in zip_codes:
        code_df = df[df[8]==code] # dataframe with incidents at zip code code
        df = df[df[8] != code] #drop zipcode=code rows from df to make next iteration faster

        for month in range(1,13):
            month_df = code_df [ code_df.apply(get_month, axis=1, args=[month])]  #dataframe with incidents started in month i
            
            #append average response times
            resp_times=month_df.apply(calc_response_time, axis=1).values.tolist()
            
            if len(resp_times)==0:
                continue #else would get div by 0 error
            zip_codes[code][month]=  sum(resp_times)/len(resp_times)
            
    #change zip_codes to ints instead of float
    zip_codes={int(k):v for (k,v) in zip_codes.items()}

    # output zip_codes to json file
    with open(osp.join(script_dir, '..', 'data','zip_codes.json'), 'w') as out_file:
        json.dump(zip_codes, out_file, indent=2)

if __name__=="__main__":
    main()
