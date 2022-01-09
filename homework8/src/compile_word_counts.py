import pandas as pd
import json
import argparse
import os
import os.path as osp

SCRIPT_DIR = os.path.dirname(__file__)
STOP_FILE = osp.join(SCRIPT_DIR,'..','data','stopwords.txt')

#load in stop words
with open(STOP_FILE,'r') as f:
    STOP_WORDS = f.readlines()[6:]

#remove '\n' in stop words
STOP_WORDS= [word.rstrip('\n') for word in STOP_WORDS]

def csv_to_df(input_csv):
    df = pd.read_csv(input_csv)

    #keep only valid speech acts in df
    names =["twilight sparkle", "applejack", "rarity","pinkie pie", "rainbow dash", "fluttershy"]

    valid_df = df[df['pony'].apply(lambda x: x.lower() ).isin(names)]

    #convert speeches to lower case
    #valid_df['dialog'] = valid_df['dialog'].apply(lambda x:x.lower())
    
    return valid_df



'''replace punctuation in a string with a space'''
def replc(x):
    for punct in ['(', ')', '[', ']', ',', '-', '.', '?', '!', ':', ';', '#', '&']:
        x=x.replace(punct, ' ')
    return x

'''replace punctuation with space'''
def replace_punct(df): 
    
    df['dialog'] = df['dialog'].apply(replc)

    return df


'''remove stop words from string'''
def pre_remove_stops(x): 

    x_words=x.split()
    x_words=[w.lower() for w in x_words]
    for word in STOP_WORDS:
        if word.lower() in x_words:
            x_words.remove(word.lower())

    return ' '.join(x_words)
  

'''remove stop words'''
def remove_stop(df):
    
    df['dialog'] = df['dialog'].apply(pre_remove_stops)
    return df


'''counts number of occurences of each word in a speech act'''
def count_words_speech(act):
    word_count={}

    for word in act.split():
        
        #Ignore non alphabetic words
        if not word.isalpha():
            continue

        if word.lower() not in word_count:
            word_count[word.lower()]=1
        else:
            word_count[word.lower()]+=1

    return word_count     


'''get counts of all words'''
def get_totals(df):

    pony_wc = {n:{} for n in ["twilight sparkle", "applejack", "rarity",
                              "pinkie pie", "rainbow dash", "fluttershy"]}

    for pony,act in zip(df['pony'],df['dialog']):
        
        #get num appearences of each word in act
        word_counts = count_words_speech(act)
        
        #all words in word_counts are lowercase
        
        #update pony_wc with count values of words in act
        for word in word_counts:
            if word not in pony_wc[pony.lower()]:
                pony_wc[pony.lower()][word] = word_counts[word]
            else:
                pony_wc[pony.lower()][word] += word_counts[word]
    return pony_wc


        


'''keeps words that appear more than 5 times across all valid speech acts'''
def words_more5(pony_wc):
    
    sus_words = {}
    for pony in pony_wc:
        for word in pony_wc[pony]:
            if pony_wc[pony][word] < 5:
                if word not in sus_words:
                    sus_words[word] = pony_wc[pony][word]
                else:
                    sus_words[word] += pony_wc[pony][word]

    #remove words from pony_wc if appear less than 5 times
    for word in sus_words:
        if sus_words[word] < 5:
            for pony in pony_wc:
                if word in pony_wc[pony]:
                    pony_wc[pony].pop(word)
    return pony_wc



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
    parser.add_argument('-o','--output_file')
    parser.add_argument('-d','--input_csv')

    args = parser.parse_args()
    
    #read csv into pd dataframe
    df=csv_to_df(args.input_csv)
    
    
    #replace punctuation in speechacts with space
    df=replace_punct(df)
    

    #remove stop words from speech acts
    df = remove_stop(df)
    
    #print(df['dialog'].head())

    #get word count for each pony (all words must appear at least 5 times over all speech acts)
    pony_wc= get_totals(df)
    pony_wc = words_more5(pony_wc)

    #output to json file
    to_json(args.output_file,pony_wc) 
 
if __name__=='__main__':
    main()
