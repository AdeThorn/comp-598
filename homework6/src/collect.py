import json
import requests
import requests.auth
import os
import sensitive # sesnsitive values from local file

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
    response = requests.get(f'https://oauth.reddit.com/r/{sub_name}/new',headers=headers, params={'limit':'100'})
    res_dict = response.json()

    #return 100 newest posts from subreddit sub_name

    return res_dict['data']['children']



'''output posts to file'''
def output_posts(out_file,subs,headers):
    
    with open(out_file,'w') as f:
        #iterate over subreddits
        for sub in subs:
            #iterate over posts in subreddit
            for post in get_new_posts(sub,headers):
                json.dump(post,f)
                f.write('\n')




def main():
    headers = setUp()
    pop_subs = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
    pop_subs_by_posts = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends','unpopularopinion']
    
    #output posts
    output_posts(os.path.join(SCRIPT_DIR,'..','sample1.json'),pop_subs,headers)
    output_posts(os.path.join(SCRIPT_DIR,'..','sample2.json'),pop_subs_by_posts,headers)




if __name__=='__main__':
    main()
