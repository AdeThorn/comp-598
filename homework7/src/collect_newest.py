import json
import requests
import requests.auth
import os
import argparse
import os.path as osp
import sensitive #file with sensitive values such as passwords

CLIENT_ID= sensitive.CID
SECRET_KEY= sensitive.SKEY
SCRIPT_DIR = os.path.dirname(__file__)
user = sensitive.user
pw =  sensitive.pw


def setUp():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data ={ 'grant_type': 'password', 'username':user, 'password': pw }


    headers = {'User-Agent': f'MyAPI/0.01 by {user}'}

    #request for auth token
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data , headers=headers)

    TOKEN = response.json()['access_token']

    headers['Authorization'] = f'bearer {TOKEN}'

    response=requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    return headers


'''gets list of 100 newest posts from sub reddit'''
def get_new_posts(sub_name, headers):
    response = requests.get(f'https://oauth.reddit.com{sub_name}/new',headers=headers, params={'limit':'100'})
    res_dict = response.json()

    #return 100 newest posts from subreddit sub_name

    return res_dict['data']['children']



'''output posts to file'''
def output_posts(out_file,sub,headers):
    dir_name,file_name = osp.split(out_file)

    if dir_name != '':
        try:
            os.makedirs(dir_name)
        except OSError as error:
           pass        

    with open(out_file,'w') as f:
        #iterate over posts in subreddit
        for post in get_new_posts(sub,headers):
            json.dump(post,f)
            f.write('\n')




def main():
    headers = setUp()

    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output_file')
    parser.add_argument('-s','--subreddit')

    args = parser.parse_args()

    
    #output posts
    output_posts(args.output_file,args.subreddit,headers)
    
    #if not os.path.exists(args.output_file):
     #   os.makedirs(cache_dir)




if __name__=='__main__':
    main()
