import pandas as pd
import json
import argparse
import os
import os.path as osp

'''computes 101 most frequent characters'''
def compute_101(df):
    
    chars_101 = set()

    # dict of number of times every pony speaks key: pony name value: number of speech acts
    occurences_dict = df['pony'].value_counts().to_dict() 

    #list of tuple (char name, num speech acts)
    list_chars = list(occurences_dict.items())
    
    #sort list in descending order by num speech acts
    list_chars.sort(key=lambda x: x[1], reverse=True)
    
    ig_names =["others", "ponies", "and","all"]
    
    skip= False
    for tup in list_chars:
        
        if len(chars_101)>=101:
            break
        
        #ignore char if name in ig_names is a substring of char name
        for name in ig_names:
            if name in tup[0]:
                skip=True

        if skip:
            skip=False
            continue

        chars_101.add(tup[0])
    
    return chars_101


def build_network(df,chars_101):
    
    #initialize network of dictionary with keys: name of character value: empty dictionary
    net = {n:{} for n in chars_101}
    

    #iterate through df and update network
    lst = list(zip(df["title"], df["pony"]))

    i=0 #keep track of iteration

    while i < len(lst)-1:
        pony1=lst[i][1]
        pony2=lst[i+1][1]
        
        pony_same = pony1==pony2
        same_ep = lst[i][0] == lst[i+1][0] #bool for if ponies speeches in same episode

        if pony_same:
            i+=1
            continue

        if not same_ep:
            i+=1
            continue

        if is_valid(pony1,chars_101) and is_valid(pony2,chars_101):

            #add connection or update connection
            if pony2 not in net[pony1]:
                net[pony1][pony2]=1
                net[pony2][pony1]=1
            else:
                net[pony1][pony2]+=1
                net[pony2][pony1]+=1
            
            i+=1

        elif not is_valid(pony2,chars_101):
            #skip to pony after pony2
            i+=2
        
        elif not is_valid(pony1,chars_101):
            i+=1

    return net

def is_valid(pony,chars_101): 
    if pony in chars_101:
        return True

    return False

def to_json(out_file,in_dict):
    dir_name,file_name = osp.split(out_file)

    if dir_name != '':
        try:
            os.makedirs(dir_name)
        except OSError as error:
           pass

    with open(out_file,'w') as f:
            json.dump(in_dict,f,indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--csv')
    parser.add_argument('-o','--out_json')

    args = parser.parse_args()

    #convert csv file to pd df
    df = pd.read_csv(args.csv)
    #put names in lower case
    df['pony'] = df['pony'].apply(lambda x: x.lower())

    chars_101 = compute_101(df)
    net = build_network(df,chars_101)
    
    #output network to json file
    to_json(args.out_json,net)

if __name__=="__main__":
    main()
