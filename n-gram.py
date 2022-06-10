from operator import indexOf
from typing import OrderedDict

from numpy import matrix

import random


def load_words(filename):
    word_list = []
    with open(filename) as data:
        for line in data:
            word_list.append(line[:-1]) #remueve \n

    return word_list

def add_decorator(words,decorator,n):
    decorated_list = []
    decorator_string = ""
    
    for i in range(n):
        decorator_string = decorator_string + decorator #agrega la cantidad de decoradores que se quieren al inicio o final
 
    for word in words:
        decorated_word = decorator_string + word.lower() + decorator_string #agrega los decoradores al inicio y final del string
        decorated_list.append(decorated_word) #agrega a la lista
    return decorated_list #retorna la lista

def get_sequences(words, n):
    sequences = []
    for word in words:
        for i in range(len(word)-n):
            sequences.append(word[i:i+n])

    sequences = list(OrderedDict.fromkeys(sequences))
    sequences.sort()
    for sequence in sequences:
        if len(sequence) < n:
            sequences.remove(sequence)
    return sequences

def calculate_transitions(words, sequences): 
    size = len(sequences)
    transition_matrix = [[0 for x in range(size)] for y in range(size)] 
    sequence_size = len(sequences[0]) 
    frequency_matrix = [0 for x in range(size)]
    
    for word in words: #get each word 
        for i in range (len(word)-sequence_size):
            transition_matrix[sequences.index(word[i:i+sequence_size])][sequences.index(word[i+1:i+sequence_size+1])] +=  1
            frequency_matrix[sequences.index(word[i:i+sequence_size])] += 1

    for i in range(size):
        for j in range(size):
            transition_matrix[i][j] = transition_matrix[i][j]/frequency_matrix[i]

    return transition_matrix

def create_model(words, ngrams):
    decorated_words = add_decorator(words,"$", ngrams)
    sequences = get_sequences(decorated_words, ngrams)
    transitions = calculate_transitions(decorated_words,sequences)
    return (transitions, sequences)

def generate_word(model,seed):
    r = random.Random()
    r.seed(seed)
    sequence = model[1]
    transition_matrix = model[0]
    current_sequence = sequence[0]
    generated_word = "" + current_sequence
    sequence_size = len(current_sequence)
    while(current_sequence != sequence[0] or len(generated_word) == sequence_size):
        value = r.random()
        counter = 0
        while(True):
            if value > transition_matrix[sequence.index(current_sequence)][counter]:
                value -= transition_matrix[sequence.index(current_sequence)][counter]
                counter += 1
            else:
                current_sequence = sequence[counter] 
                generated_word = generated_word + current_sequence[-1]
                break

    generated_word = generated_word[sequence_size:-sequence_size].capitalize() #curates the word
    return generated_word

def get_probability(model, word):
    e = None


words = load_words("pokemon.csv")

modelo = create_model(words, 3) 

print(generate_word(modelo,21))