import numpy as np
import pandas as pd
import re
from gensim.summarization import keywords
import collections
import csv
import heapq
import fasttext

#we need to calculate success rate, how much it will take to succeed and 

class Parser:
  def __init__(self, data, input_text = "", most_similar = 3):
    self.input = input_text
    self.dataset = data
    self.most_similar = most_similar
    self.input_text = input_text

    self.combined_data = self.combine_data()
    self.category_dict, self.mcategory_dict = self.get_categories()
    self.top_keywords = self.get_keywords()
    self.top_ksimilar = self.get_ksimilar()
    #print(self.find_keywords())
    print(len(self.combined_data))
    print(self.combined_data[:10])
    #print(self.top_ksimilar())
    print(self.clean_sentence("Support Solar Roasted Coffee & Green Energy!  SolarCoffee.co"))

  def open_data(self, data_csv):
    #returns the data in a 2d list
    data_list = []
    with open(data_csv, 'r', encoding="utf8", errors='ignore') as file:
      reader = csv.reader(file)
      for row in reader:
        row = row[:12]
        if row[0] != 'ID':
          data_list.append(row)
      return data_list
    
  def combine_data(self):
    #combined multiple data into one datastream
    combined_data = []
    for data in self.dataset:
        combined_data.append(self.open_data(data))
    combined_data = [item for sublist in combined_data for item in sublist]
    return combined_data
  
  def get_categories(self):
    categories = collections.Counter([x[2] for x in self.combined_data])
    categories = {key: val for key, val in categories.items() if val > 5}
    main_categories = collections.Counter([y[3] for y in self.combined_data])
    main_categories = {key: val for key, val in main_categories.items() if val > 5}
    #print("categories:", categories)
    #print("main categories:", main_categories)
  
    return categories, main_categories

  def get_keywords(self):
    text_keywords = keywords(self.input_text, words = 3, scores = True, split = True, lemmatize = True)
    keywords_f = []
    for t in text_keywords:
      words = t[0].split(" ")
      for word in words:
        keywords_f.append((word, t[1]))
    return keywords_f

  def get_top_category(self, keywords, category_keys):
    #returns the data under category associated with average highest similarity score
    heap = []
    for key in category_keys:
      score_sum = 0
      for word in keywords:
        score_sum += self.similarity_score(key, word)
      heap.append([score_sum, key])
    heapq.heapify(heap)
    category = heap[0]
    category_data = [category]
    ## ^ should return all data associated with specific category
    return category_data

  def similarity_score(self, word1, word2):
    #returns the similarity between two words
    return 0

  def similarity_sentence(self, s1, s2):
    #returns similarity between 2 sentences
    return 0

  def clean_sentence(self, s):
    #makes sentence readable for similarity analysis
    s = s.replace(r'-', ' ')
    s = s.split(" ")
    s = [re.sub(r'[^\w\s]', '', char) for char in s]
    s = [x for x in s if x != '']
    return s

  def get_ksimilar(self):
    # we need to find similarity score between category data and 
    # heapify similarity score and data, and then get top k elements
    category_keys = self.category_dict.keys()
    category_data = self.get_top_category(self.top_keywords, category_keys)
    #with the data and top keywords, we need to return the top k similar projects
    project_names = [w[1] for w in category_data]
    scores = [self.similarity_sentence(self.top_keywords, x) for x in project_names]
    heap = [(scores[i], category_data[i]) for i in range(len(category_data))]
    heapq.heapify(heap)
    #return heap[0:self.most_similar][1]    
    return 0

text_en = (
    'I want to design a mystical magical tarot deck that will assist others in knowing themselves more deeply and help sharpen their intuition')

test = Parser(['ks-projects-201612.csv', 'ks-projects-201801.csv'], text_en)
#print(test.get_categories())
