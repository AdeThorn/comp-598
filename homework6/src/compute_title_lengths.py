import json
import sys

'''Print average title length'''
def main():
    out_file = sys.argv[1]
    lines=[]
    sum_len=0 #sum of lengths of all titles

    with open(out_file,'r') as f:
        for line in f:
            post=json.loads(line)
            
            sum_len+= len(post['data']['title'])
    avg = sum_len/1000
    print(avg)




if __name__=="__main__":
    main()
