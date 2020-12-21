import re
from gensim.summarization import keywords
import collections
import heapq
import gensim.downloader as gdl
import ssl
import nltk
import pymysql
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy import spatial
import numpy as np
 
ssl._create_default_https_context = ssl._create_unverified_context
 
class Parser:
 def __init__(self, input_text = "", most_similar = 3):
 
   self.input_text = input_text
   self.most_similar = most_similar
   self.currency_dict = {'AUD': 0.76,
               'CAD': 0.79,
               'CHF': 1.13,
               'DKK': 0.16,
               'EUR': 1.23,
               'GBP': 1.36,
               'HKD': 0.13,
               'JPY': 0.0097,
               'MXN': 0.05,
               'NOK': 0.12,
               'NZD': 0.72,
               'SEK': 0.12,
               'SGD': 0.75,
               'USD': 1.0}
   self.categories =['Publishing', 'Film & Video','Music','Food','Design','Games','Fashion','Theater','Comics','Crafts','Art','Photography','Technology','Dance','Journalism']
   self.glove = self.create_glove("glove.6B.100d.txt")
   self.top_keywords = self.get_keywords()
   print("Top keywords:", self.top_keywords)
   #self.token_dict, self.costs_dict, self.success_dict = self.get_dictionary()
   self.max_category = self.find_category()
   self.total_count, self.total_successes, self.avg_cost = self.parse_query()
 
 
 def parse_query(self):
   # create connection
   connection = pymysql.connect(host='localhost',
                               user='root',
                               password='ferhat437',
                               db='mydatabase')
 
   # Create cursor
   my_cursor = connection.cursor()
 
   # define the category
   main_category = self.max_category
 
   # query for finding all categories and storing them in a list
 
   sqlquery = "SELECT DISTINCT main_category from projects"
 
   my_cursor.execute(sqlquery)
   result = my_cursor.fetchall()
 
   maincategory_lst = []
 
   for i in result:
       maincategory_lst.append(i[0])
 
   # query to find count of projects of main category
   sqlquery = "SELECT COUNT(id) from projects WHERE main_category = '{}'".format(main_category)
   my_cursor.execute(sqlquery)
   count = my_cursor.fetchall()
 
   total_count = count[0][0]
 
   # query to find count of successful projects of main category
   sqlquery = "SELECT COUNT(id) from projects WHERE main_category = '{}' AND (state = 'successful' OR state = 'live')".format(main_category)
   my_cursor.execute(sqlquery)
   success_count = my_cursor.fetchall()
 
   total_successes = success_count[0][0]
 
 
   # query to find avg goal amount of main category
   sqlquery = "SELECT AVG(usd_goal_real) from projects WHERE main_category = '{}'".format(main_category)
   my_cursor.execute(sqlquery)
   result = my_cursor.fetchall()
 
   avg = result[0][0]
 
   # Close the connection
   connection.close()
   return total_count, total_successes, avg
  
 def get_values(self):
   return round(self.avg_cost, 2), round(self.total_successes / self.total_count, 3), self.max_category
 
 def create_glove(self, gloveFile):
   with open(gloveFile, encoding="utf8" ) as f:
       content = f.readlines()
   model = {}
   for line in content:
       splitLine = line.split()
       word = splitLine[0]
       embedding = np.array([float(val) for val in splitLine[1:]])
       model[word] = embedding
   return model
 
 def get_keywords(self):
   print(self.input_text)
   text_keywords = keywords(self.input_text, words = 5, scores = True, split = True, lemmatize = True)
   keywords_f = []
   for t in text_keywords:
     words = t[0].split(" ")
     for word in words:
       keywords_f.append((word, t[1]))
   return keywords_f
 
 def get_similarity(self, project, token_list, k=1):
   print("project:", project)
   print(token_list)
   maximum_heap = []
   for category in token_list:
       total_sim = 0
       for token in category:
           for data in project:
               token_vec = self.glove[token.lower()]
               data_vec = self.glove[data[0]]
               similarity = 1 - spatial.distance.cosine(data_vec, token_vec)
               similarity *= data[1]
               total_sim += similarity
       total_sim /= len(category)
       if len(project) > 0:
         total_sim /= len(project)
       maximum_heap.append((-total_sim, category))
      
   heapq.heapify(maximum_heap)
          
   top_k = maximum_heap[:k]
  
   return [(-score, token) for score, token in top_k]
 
 def find_category(self):
   y_tokens = [self.clean_sentence(c) for c in self.categories]
   topic_cat = self.get_similarity(self.top_keywords, y_tokens)[0]
   print("max category in topic form:", topic_cat)
   for i in range(len(y_tokens)):
       if topic_cat[1][0] == y_tokens[i][0]:
           max_cat = self.categories[i]
           return max_cat
 
 def clean_sentence(self, s):
   #makes sentence readable for similarity analysis
   s = s.replace(r'-', ' ')
   s = s.split(" ")
   s = [re.sub(r'[^\w\s]', '', char) for char in s]
   s = [x for x in s if x != '']
   return s
 
 
# dummy = Parser("garden house")
# print(dummy.top_keywords)
# print(dummy.get_values())

