import re
from gensim.summarization import keywords
import collections
import csv
import heapq
import gensim.downloader as gdl
import ssl
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from scipy import spatial
import gensim.downloader as gdl

ssl._create_default_https_context = ssl._create_unverified_context

class Parser:
  def __init__(self, data, input_text = "", most_similar = 3):
    self.input_text = input_text
    self.dataset = data
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
    self.glove = gdl.load("glove-wiki-gigaword-100")
    self.combined_data = self.combine_data()
    self.category_dict, self.mcategory_dict = self.get_categories()
    self.top_keywords = self.get_keywords()
    self.token_dict, self.costs_dict, self.success_dict = self.get_dictionary()
    print("token dict:", self.token_dict)
    print(self.top_keywords)
    self.max_category = self.find_category()
    print(self.max_category, self.return_values())


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
    print(self.input_text)
    text_keywords = keywords(self.input_text, words = 5, scores = True, split = True, lemmatize = True)
    keywords_f = []
    for t in text_keywords:
      words = t[0].split(" ")
      for word in words:
        keywords_f.append((word, t[1]))
    return keywords_f

  def get_dictionary(self):
    stop_words = set(stopwords.words('english'))  

    x = [d[1] for d in self.combined_data[1:]]
    y = [d[3] for d in self.combined_data[1:]]
    success = [d[9] for d in self.combined_data[1:]]
    cost = [d[6] for d in self.combined_data[1:]]
    currency = [d[4] for d in self.combined_data[1:]]

    token_dictionary = collections.defaultdict(list)
    costs = collections.defaultdict(int)
    success_rate = collections.defaultdict(int)

    for index in range(len(x)):
        title = x[index]
        cleaned = self.clean_sentence(title)
        cleaned_str = ""
        if not cleaned:
            continue
        for word in cleaned:
            cleaned_str += word + " "
        word_tokens = word_tokenize(cleaned_str)  

        filtered_sentence = [w for w in word_tokens if not w in stop_words]  

        filtered_sentence = []  

        for w in word_tokens:  
            if w not in stop_words:  
                filtered_sentence.append(w)  
        
        x_token = []
        print("glove:", self.glove)
        if len(filtered_sentence) >= 3:
            for token in filtered_sentence:
                if len(x_token) == 3:
                    break
                if token in self.glove:
                    x_token.append(token)
        print("x_token:", x_token)
        if x_token:
            topic = y[index]
            did_succeed = success[index]
            if did_succeed == 'live' or did_succeed == 'successful':
                success_rate[topic] += 1
                costs[topic] += float(cost[index]) * self.currency_dict[currency[index]]
            token_dictionary[topic].append(x_token)
        return token_dictionary, costs, success_rate

  def get_similarity(self, project, token_list, k=1):
    maximum_heap = []
    for category in token_list:
        total_sim = 0
        for token in category:
            for data in project:
                token_vec = self.glove[token]
                data_vec = self.glove[data[0]]
                similarity = 1 - spatial.distance.cosine(data_vec, token_vec)
                similarity *= data[1]
                total_sim += similarity
        total_sim /= len(project) * len(category)
        maximum_heap.append((-total_sim, category))
        
    heapq.heapify(maximum_heap)
            
    top_k = maximum_heap[:k]
    
    return [(-score, token) for score, token in top_k]

  def find_category(self):
    categories = list(self.token_dict.keys())
    y_tokens = [self.clean_sentence(c) for c in categories]
    print(self.top_keywords, y_tokens)
    topic_cat = self.get_similarity(self.top_keywords, y_tokens)
    for i in range(len(y_tokens)):
        if topic_cat[1][0] == y_tokens[i][0]:
            max_cat = categories[i]
            return max_cat

  def return_values(self):
    max_cost = self.costs_dict[self.max_category]
    max_length = len(self.token_dict[self.max_category])
    max_success = self.success_dict[self.max_category]
    print(max_cost, max_length, max_success)
    avg_cost = max_cost / max_length
    avg_success = max_success / max_length
    return avg_cost, avg_success

  def clean_sentence(self, s):
    #makes sentence readable for similarity analysis
    s = s.replace(r'-', ' ')
    s = s.split(" ")
    s = [re.sub(r'[^\w\s]', ' ', char) for char in s]
    s = [x for x in s if x != '']
    return s


text_en = (
    'STUDIO IN THE SKY - A Documentary Feature Film (Canceled)')

test = Parser(['ks-projects-201612.csv', 'ks-projects-201801.csv'], text_en)
#print(test.get_categories())
