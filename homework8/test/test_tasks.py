import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

src_dir = os.path.join(parentdir, 'src')
sys.path.append(src_dir)

import compute_pony_lang
import compile_word_counts

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        
        #read csv into pd dataframe
        df=compile_word_counts.csv_to_df(self.mock_dialog)

        #replace punctuation in speechacts with space
        df=compile_word_counts.replace_punct(df)
        

        #remove stop words from speech acts
        df = compile_word_counts.remove_stop(df)


        #get word count for each pony (all words must appear at least 5 times over all speech acts)
        pony_wc= compile_word_counts.get_totals(df)
        #pony_wc = compile_word_counts.words_more5(pony_wc)
        
        #read in word_counts.true.json
        with open(self.true_word_counts,'r') as f:
            true_wc = json.load(f)
        self.assertEqual(true_wc,pony_wc)

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        
        pony_wc = compute_pony_lang.json_to_dict(self.true_word_counts)
        

        pony_tfidf = compute_pony_lang.get_tfidf_list(pony_wc)

        dict_to_print = compute_pony_lang.dict_to_output(2,pony_tfidf)
        
        #read in tf_idfs.true.json
        with open(self.true_tf_idfs,'r') as f:
            true_tfidf = json.load(f)
        self.assertEqual(true_tfidf,dict_to_print)



    
if __name__ == '__main__':
    unittest.main()
