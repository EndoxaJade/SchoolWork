import tensorflow as tf
import numpy as np
import tflearn
import nltk
import json
nltk.download('punkt')

# Import learn file
with open('learndata.json') as file:
    data = json.load(file)
    
# Tokenize the text
words = []
for dialogue in data:
    for sentence in dialogue['dialogue']:
        sentence_words = nltk.word_tokenize(sentence)
        words.extend(sentence_words)
# Remove punctuation
words = [word for word in words if word.isalnum()]
# Text convert to lowercase
words = [word.lower() for word in words]

# Creating a dictionary
word_freq = nltk.FreqDist(words)
common_words = word_freq.most_common(1000)
word_list = [word[0] for word in common_words]
word_dict = {word: index for index, word in enumerate(word_list)}
training_data = []
for dialogue in data:
    for i in range(len(dialogue['dialogue']) - 1):
        input_sentence = dialogue['dialogue'][i]
        output_sentence = dialogue['dialogue'][i+1]
        input_words = nltk.word_tokenize(input_sentence)
        output_words = nltk.word_tokenize(output_sentence)
        input_words = [word for word in input_words if word.isalnum()]
        output_words = [word for word in output_words if word.isalnum()]
        input_vector = [0] * len(word_list)
        for word in input_words:
            if word in word_dict:
                index = word_dict[word]
                input_vector[index] = 1
        output_vector = [0] * len(word_list)
        for word in output_words:
            if word in word_dict:
                index = word_dict[word]
                output_vector[index] = 1
        training_data.append([input_vector, output_vector])
        
# Building the model
net = tflearn.input_data(shape = [None, len(word_list)])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(word_list), activation ='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net)
    
# Training the model
model.fit([data[0] for data in training_data], [data[1] for data in training_data], n_epoch = 1000, batch_size = 8, show_metric = True)
    
    # Questioning function
def get_response(question):
    question_words = nltk.word_tokenize(question)
    question_words = [word for word in question_words if word.isalnul()]
    question_vector = [0] * len(word_list)
    for word in question_words:
        if word in word_dict:
            index = word_dict[word]
            question_vector[index] = 1
    prediction = model.predict([question_vector])[0]
    response_vector = np.zeros(len(word_list))
    response_vector[np.argmax(prediction)] = 1
    response_words = []
    for index, value in enumerate(response_vector):
        if value == 1:
            response_words.append(word_list[index])
    response = ' '.join(response_words)
    return response

while True:
    question = input("You: ")
    response = get_response(question)
    print("AI: " + response)