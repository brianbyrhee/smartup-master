import numpy as np
import pandas as pd
import re
from gensim.summarization import keywords
import collections
import csv

#we need to calculate success rate, how much it will take to succeed and 

class Parser:
  def __init__(self, data, input_text = "", most_similar = 3):
    self.input = input_text

    self.dataset = data
    self.most_similar = most_similar
    self.combined_data = self.combine_data()

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
    print("categories:", categories)
    print("main categories:", main_categories)
    return categories, main_categories
    

  def parser(self):
    #parse words to find top 5 most representative words of the input text
    pass

  def find_category(self):
    #perform glove and/or word2vec on the keys to find the most relevant keywords
    pass

  def similarity_score(self):
    pass

  def get_ksimilar(self):
    #heapify similarity score and data, and then heappop top k elements
    pass
    
test = Parser(['ks-projects-201612.csv', 'ks-projects-201801.csv'])
#print(test.get_categories())

text_en = (
    'I want to design a mystical magical healing tarot deck that will assist others in knowing themselves more deeply and help sharpen their intuition')

print(keywords(text_en,words = 3,scores = True, split = True, lemmatize = True))