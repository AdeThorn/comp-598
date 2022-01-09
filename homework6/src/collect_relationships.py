import bs4
import os
import os.path as osp
import argparse
from bs4 import BeautifulSoup 
import requests
import json
import hashlib

BASE_URL ="https://www.whosdatedwho.com/dating/"

'''returns dict from json file'''
def json_to_dict(in_file):
    with open(in_file,'r') as f:
        dict_to_return = json.load(f)
    
    return dict_to_return

'''hash function'''
def hash_fun(name):
    return hashlib.sha1(name.encode("UTF-8")).hexdigest()

'''checks if cache exissts'''
def cache_exists(name,cache_dir):
    hash_name = hash_fun(name)
    if osp.exists(osp.join(cache_dir,hash_name)):
        return True
    return False

'''saves beautifulsoup page to cache'''
def make_cache(name,cache_dir):
    hash_name = hash_fun(name)
    
    page=requests.get(BASE_URL+name)
    soup = BeautifulSoup(page.content,'html.parser') 
    with open(osp.join(cache_dir,hash_name),'w') as f:
        f.write(str(soup))

'''return soup from cache'''
def return_cache(name,cache_dir):
    hash_name = hash_fun(name)
    
    with open(osp.join(cache_dir,hash_name),'r') as f:
        return f.read()


'''return list of people person has been in relationship with'''
def list_relations(person,cache_dir):
    
    soup = BeautifulSoup(return_cache(person,cache_dir),'html.parser')

    #page = requests.get(BASE_URL+person)
    #soup = BeautifulSoup(page.content,'html.parser')

    box = soup.find_all('div',class_='clearfix')[0]
     
    #in clearfix div get all p tags before about section
    
    #get name of target person
    name = box.find('h1',class_='ff-name')
    name = name.contents[0].string
    name = ' '.join(name.split())
    
    #about section header
    about_header = box.find("h4",class_='ff-auto-about')


    #list of people target person has beein in relationship with 
    relations= [a.string for a in about_header.find_all_previous("a")]
    relations=set(relations)
    if None in relations:
        relations.remove(None)
    bad_words=['lists', 'trending','popular', 'view relationship']
    
    lower_case_name = ''.join(person.lower().split('-'))

    for n in relations:
        if n.lower() == name.lower():
            bad_words.append(n)

    #remove words in list that aren't relationships
    for word in bad_words:
        if word in relations:
            relations.remove(word)

    return list(relations)

    

'''output target people and their relationships to output file'''
def output(out_file,names,cache_dir):
    
    output_dict={}
    for name in names:
        output_dict[name]=list_relations(name,cache_dir)
    with open(out_file, 'w' ) as f:
        f.write(json.dumps(output_dict,indent=3))
        

    
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--config_file')
    parser.add_argument('-o','--output_file')

    args = parser.parse_args()
    config_dict=json_to_dict(args.config_file)
    cache_dir = config_dict["cache_dir"]
    
    #if cache dir doesn't exist make it
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    target_people = config_dict["target_people"]
    
    #check if cache for each person exists , if not make one
    for person in target_people:
        if not cache_exists(person,cache_dir):
            make_cache(person,cache_dir)
            
    #output target people and their relationships to output file 
    output(args.output_file,target_people,cache_dir)
if __name__ == "__main__":
    main()
