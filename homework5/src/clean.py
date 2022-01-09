import json
import argparse
from datetime import datetime
import pytz


'''
Remove posts with no title or title_text field
'''
def remove_post_title(post_list):
    return [post for post in post_list if "title" in post or "title_text" in post]

#rename title_text key to title
def rename_title_text(post_list):

    for i in range(len(post_list)):
        if "title_text" in post_list[i]:
            post_list[i]["title"]=post_list[i].pop("title_text")

    return post_list

def read_in_json(input_file):
    
    posts=[]

    #read json objects and append to posts list
    with open(input_file,"r") as in_file:
        for line in in_file:
            try:
                posts.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                #if invalid dictionary skip
                continue
    return posts

#standardize iso date times to utc timezone

def standardize_iso(posts):
    
    bad_posts=[]

    for i in range(len(posts)):
        if 'createdAt' in posts[i]:
            
            if type(posts[i]["createdAt"]) !=str or len(posts[i]["createdAt"])<3:
                bad_posts.append(posts[i])
                continue
            else:
                #if no colon in time add colon
                if posts[i]["createdAt"][-3] != ":":
                    posts[i]["createdAt"] = posts[i]["createdAt"][:-2] + ":" + posts[i]["createdAt"] [-2:] 
            #standardize to utc
            try:
                date_obj = datetime.fromisoformat( posts[i]['createdAt'])
                date_obj= date_obj.astimezone(pytz.utc)

                #str(date_obj) looks like 2020-10-19 02:56:51+00:00 but T is needed between date and time
                updated_date = str(date_obj).split()
                updated_date.insert(1,"T")
                updated_date= "".join(updated_date)
                posts[i]['createdAt'] = updated_date
            except ValueError:
                #if date doesn't pass ISO datetime standard
                bad_posts.append(posts[i])
    
    for bad_post in bad_posts:
        posts.remove(bad_post)

    return posts

#removes posts where author fiel is empty null or NA
def remove_author(posts):
    
    bad_posts=[]# posts to remove
    
    for i in range(len(posts)):
        if "author" in posts[i]:
            if posts[i]["author"] =="" or posts[i]["author"] == "N/A" or posts[i]["author"] == "null" or posts[i]["author"] == None:
                bad_posts.append(posts[i])

    for bad_post in bad_posts:
        posts.remove(bad_post)

    return posts

'''
make total_count value in each post an int
'''
def count_to_int(posts):
    
    bad_posts = [] #posts to remove

    for i in range(len(posts)):
        if "total_count" in posts[i]:
            if type(posts[i]["total_count"])!=int and type(posts[i]["total_count"])!=str and type(posts[i]["total_count"])!=float:
                bad_posts.append(posts[i]) 
                continue
            else:
                try:
                    posts[i]["total_count"]= int(float(posts[i]["total_count"]))
                except ValueError:
                    bad_posts.append(posts[i]) 
    
    for bad_post in bad_posts:
        posts.remove(bad_post)
    
    return posts


def ensure_valid_tags(posts):
    

    for i in range(len(posts)):
        if "tags" in posts[i]:
            new_tags=[]
            for tag in posts[i]['tags']:

                if " " in tag:
                    new_tags.extend(tag.split())
                else:    
                    new_tags.append(tag)

            posts[i]['tags'] = new_tags
    return posts

'''output'''
def output_json(output_file,posts):
    
    with open(output_file,'w') as out_file:
        for post in posts:
            json.dump(post,out_file)
            out_file.write('\n')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_file')
    parser.add_argument('-o','--output_file')

    args = parser.parse_args()
    posts= read_in_json(args.input_file)
    
    
    #remove posts with no title or title_text fields
    posts=remove_post_title(posts)
    
    
    #Rename title_text key in every post to title
    posts= rename_title_text(posts)
    
    #standardize createdAt date times to UTC timezone
    posts = standardize_iso(posts)
    
    #Rrmove posts with invalid value for author
    posts = remove_author(posts)

    #remove posts with invalid value for total_count if total_count is valid convert to int
    posts = count_to_int(posts)
    
    
    posts=ensure_valid_tags(posts)

    output_json(args.output_file,posts)

if __name__ == "__main__":
    main()
