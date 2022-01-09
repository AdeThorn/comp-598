import pandas as pd
import json
import random
import argparse
import os
import os.path as osp
'''returns list of of list'''
def json_to_list(in_file):

    #take keys name of post, title of post
    with open(in_file,'r') as f:
        dict_list=[json.loads(line) for line in f]
    
    updated_dict_list=[]
    for d in dict_list:
        updated_dict_list.append([d["data"]["name"],d["data"]["title"]])
    #format : [ [name_post1,title_post1, ], [name_post2,title_post2, ] ]
    return updated_dict_list

def list_to_df(lst):
    df = pd.DataFrame(lst,columns =['Name','title'])
    df['coding']=""
    return df

'''random samples from list without replacement'''
def rand_samps(lst,num_samps):
    rand_lst=[]
    if num_samps >=100:
        return lst
    else: 
        nums_seen=set()
        while len(rand_lst) < num_samps:
            rand_num = random.randint(0,99)
            if rand_num not in nums_seen:
                nums_seen.add(rand_num)
                rand_lst.append(lst[rand_num])
    return rand_lst

    
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--out_file')
    parser.add_argument('json_file')
    parser.add_argument('num_posts_to_output',type=int)

    args = parser.parse_args()

    #convert json objects(reddit posts) to list of posts
    lst=json_to_list(args.json_file)

    #get num_posts_to_output random posts from lst
    lst= rand_samps(lst,args.num_posts_to_output)
    
    #convert list to pandas df
    df=list_to_df(lst)
    
    #make folder if not exist
    dir_name,file_name = osp.split(args.out_file)

    if dir_name != '':
        try:
            os.makedirs(dir_name)
        except OSError as error:
           pass


    #convert df to tab separated file
    df.to_csv(args.out_file, sep = '\t', index=False)
    


if __name__=="__main__":
    main()
