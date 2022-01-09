import os
import os.path as osp
import json
import argparse
import math

def json_to_dict(in_file):
    
    with open(in_file,'r') as f:
        data=json.load(f)
    return data

def tf(w,pony,pony_wc):
    return pony_wc[pony][w]

def idf(w,pony_wc):

    #get number of ponies that use word w
    num_used = 0
    
    for pony in pony_wc:
        if w in pony_wc[pony]:
            num_used+=1
    
    return math.log(6/num_used)


def tf_idf(w,pony,pony_wc):
    return tf(w,pony,pony_wc) * idf(w,pony_wc)

def get_tfidf_list(pony_wc):
    
    pony_tfidf = {n:[] for n in ["twilight sparkle", "applejack", "rarity",
                              "pinkie pie", "rainbow dash", "fluttershy"]}
    
    #pony_tfidf is dictionary with keys pony name and vaues are tuple of word and its tfidf score
    for pony in pony_wc:
        for word in pony_wc[pony]:
            pony_tfidf[pony].append((word,tf_idf(word,pony,pony_wc)))
    
    #sort lists in pony_tfidf in descendinng order
    for pony in pony_tfidf:
        pony_tfidf[pony].sort(key=lambda x:x[1] , reverse=True)

    return pony_tfidf

def dict_to_output(num_words,pony_tfidf):
    dict_to_print = {}
    for pony in pony_tfidf:
        dict_to_print[pony]= [x[0] for x in pony_tfidf[pony][0:num_words]]
    
    return dict_to_print

def print_output(d):
    json_obj = json.dumps(d,indent=3)
    print(json_obj)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--pony_counts')
    parser.add_argument('-n','--num_words',type=int)

    args = parser.parse_args()

    pony_wc = json_to_dict(args.pony_counts)
    num_words = args.num_words

    pony_tfidf = get_tfidf_list(pony_wc)
    
    dict_to_print = dict_to_output(num_words,pony_tfidf)

    print_output(dict_to_print)


if __name__=="__main__":
    main()
