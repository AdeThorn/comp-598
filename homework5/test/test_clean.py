import unittest
from pathlib import Path
import os, sys
import json


parentdir = Path(__file__).parents[1]
current_dir = os.path.dirname(__file__)
sys.path.append(parentdir)

src_dir = os.path.join(parentdir, 'src')
sys.path.append(src_dir)

import clean

class CleanTest(unittest.TestCase):
    
    def load_dict(self,input_file):
        #read json objects and append to posts list
        with open(input_file,"r") as in_file:
            line= in_file.readline()
            try:
                return json.loads(line)
            except json.decoder.JSONDecodeError:
                #if invalid dictionary return None
                return None



    def setUp(self):
        # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.
       
        self.fix_1 = clean.read_in_json(os.path.join(current_dir, 'fixtures','test_1.json'))
        self.fix_2 = clean.read_in_json(os.path.join(current_dir, 'fixtures','test_2.json'))
        self.fix_3 = clean.read_in_json(os.path.join(current_dir, 'fixtures','test_3.json'))
        self.fix_4 = clean.read_in_json(os.path.join(current_dir, 'fixtures','test_4.json'))
        self.fix_5 = clean.read_in_json(os.path.join(current_dir, 'fixtures','test_5.json'))
        self.fix_6 = clean.read_in_json(os.path.join(current_dir, 'fixtures','test_6.json'))
    
    #fix 1 test
    def test_post_with_no_title_removed(self):
        self.assertEqual(clean.remove_post_title(self.fix_1),[] )
    
    #fix 2 test
    def test_created_date(self):
        self.assertEqual(clean.standardize_iso(self.fix_2),[])

    #fix3 test
    def test_invalid_JSON_dict_not_loaded_in(self):
        self.assertEqual(self.fix_3,[] )
    
    #fix 4 test
    def test_post_with_NA_author_removed(self):
        self.assertEqual(clean.remove_author(self.fix_4),[] )

    #def test_post_with_null_author_removed(self):
      #  self.assertEqual(clean.remove_author([{"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "null", "total_count": "12"}] ),[] )

    #def test_post_with_empty_author_removed(self):
     #   self.assertEqual(clean.remove_author([{"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "", "total_count": "12"}] ),[] )

    #def test_post_with_None_author_removed(self):
   #     self.assertEqual(clean.remove_author([{"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": None , "total_count": "12"}] ),[] )


    #fix5 test
    def test_post_with_invalid_total_count_removed(self):
        self.assertEqual(clean.count_to_int(self.fix_5),[] )
    
    #def test_post_with_str_count_cast_to_int(self):
     #   post = clean.count_to_int( [ {"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "druths", "total_count": "12"} ])
    #    self.assertEqual(post, [ {"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "druths", "total_count": 12} ])

    
   # def test_post_with_float_count_cast_to_int(self):
      #  post = clean.count_to_int( [ {"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "druths", "total_count": 22.9} ])
     #   self.assertEqual(post, [ {"title": "First title", "createdAt": "2020-10-19T02:56:51+0000", "text": "Some post content", "author": "druths", "total_count": 22} ])

    
    #fix6 test
    def test_tags_split_properly(self):
        
        #count words in tags
        wc = 0
        for word in self.fix_6[0]["tags"]:
            wc += len(word.split())
                                                
        
        updated_post = clean.ensure_valid_tags(self.fix_6)

        self.assertEqual(len(updated_post[0]["tags"]), wc )


if __name__ == '__main__':
    unittest.main()
