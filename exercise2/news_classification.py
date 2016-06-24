# -*- coding: utf-8 -*-

import time
import random
import nltk
import io
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier, classify
import os
import random
from collections import Counter


def main():
	
	start = time.time()

	###### Loading and cleaning the data ######
	path = 'bbc/'

	business_news = building_data('business', path)
	entertainment_news = building_data('entertainment', path)
	politics_news = building_data('politics', path)
	sport_news = building_data('sport', path)
	tech_news = building_data('tech', path)

	all_news = [(news, 'business') for news in business_news]
	all_news += [(news, 'entertainment') for news in entertainment_news]
	all_news += [(news, 'politics') for news in politics_news]
	all_news += [(news, 'sport') for news in sport_news]
	all_news += [(news, 'tech') for news in tech_news]

	random.shuffle(all_news) # to mix the different categories

	###### Extracting the features ######
	# 2 different manners of featuring
	all_features_1 = [(get_features(news, 'bow'), label) for (news, label) in all_news] # with the frequency of occurence
	all_features_2 = [(get_features(news, ''), label) for (news, label) in all_news] # with the presence/absence

	###### Training the classifier ######
	training_set_1, testing_set_1, classifier_1 = training(all_features_1, 'NaiveBayes', 0.70)
	training_set_2, testing_set_2, classifier_2 = training(all_features_2, 'NaiveBayes', 0.70)
	
	###### Evaluating the method #####	
	print("Classifier accuracy percent:",(classify.accuracy(classifier_1, testing_set_1))*100)
	print("Classifier accuracy percent:",(classify.accuracy(classifier_2, testing_set_2))*100)
	
	end = time.time()
	elapsed = end - start
	print "Time taken: ", elapsed, "seconds."


def building_data(category, path):
	data = []
	
	file_list = os.listdir(path+category)

	for i in file_list:
		file = io.open(path + category + "/" + i, 'r', encoding = 'utf-8') # important to specify the encoding
		sentence_news = file.read()
		line_news = nltk.word_tokenize(sentence_news) # to separate the words and punctuations
			
		line_news_normalized = []
		for line in line_news:
			if not line in stopwords.words('english') : # to remove words like "the", "of" that do not have much content
				line_news_normalized.append(WordNetLemmatizer().lemmatize(line.lower())) # to put all words in lowercase and to make identic singular and plural, is and are... 		
		data.append(line_news_normalized)
	file.close()
	return(data)
	
def get_features(text, setting):
	if setting=='bow':
		return {word: count for word, count in Counter(text).items()}
	else:
		return {word: True for word in text}	

def training(features, method, proportion_training):
	training_set = features[:int(proportion_training*len(features))] # we take 2/3 for training and 1/3 for testing
	testing_set = features[int(proportion_training*len(features)):]
				
	if method == 'NaiveBayes':
		classifier = NaiveBayesClassifier.train(training_set)
				
	return training_set, testing_set, classifier


if __name__ == "__main__":	
	main() # Call main function	

