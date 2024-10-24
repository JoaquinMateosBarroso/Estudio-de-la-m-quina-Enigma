import random

random.seed(0)

def verticalizeText(text: str):
    '''Include a \\n before each letter of the text'''
    return "".join(["\n" + char for char in text])

def randomPermutation(text: str):
    '''Return a random permutation of the text'''
    return "".join(random.sample(text, len(text)))