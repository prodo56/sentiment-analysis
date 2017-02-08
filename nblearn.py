import re
import json
import sys
from math import log as log
review = {}
stopwords=[".",",","?","&","/","%","\"","-"]

#text = sys.argv[1]
#labels = sys.argv[2]
text = "train-text.txt"
labels = "train-labels.txt"
with open(text) as f:
    for line in f.readlines():
        for stopword in stopwords:
            if stopword in line:
                line = line.replace(stopword," ")
                line = line.replace("'","")
        linetokens = line.rstrip().lstrip().split()
        #print linetokens
        reviewId = linetokens[0]
        tokens = []
        for token in linetokens[1:]:
            token = token.lower()
            match = re.search('(?P<word>[a-zA-Z0-9-]*[!$ ]*)(?P<brackets>[)(]*)', token)
            if match and match.group("brackets"):
                token = match.group("word")
            match = re.search(
                '(?P<word>[a-zA-z0-9-]+)(?P<leftbrackets>[()])|(?P<rightbrackets>[()])(?P<word1>[a-zA-Z0-9]+)', token)
            if match and (match.group("rightbrackets") or match.group("leftbrackets")) and (
                match.group("word") or match.group("word1")):
                token = token.replace(")", "").replace("(", "")
            match = re.search('(?P<word>[a-zA-Z0-9-]*)(?P<spaces>[ ]*)(?P<exclaimation>[!]*)', token)
            if match and match.group("exclaimation"):
                if match.group("exclaimation") not in tokens:
                    tokens.append(match.group("exclaimation"))
                token = match.group("word")
            match = re.search('(?P<word>[a-zA-Z0-9-]*)(?P<space>[ ]*)(?P<smiley>[:=]+[)]*)', token)
            if match and match.group("smiley"):
                if match.group("smiley") not in tokens:
                    tokens.append(match.group("smiley"))
                token = match.group("word")
            tokens.append(token)
        review[reviewId] = tokens

reviewLabels = {}
with open(labels) as f:
    for line in f.readlines():
        linetokens = line.rstrip().lstrip().split()
        #print linetokens
        reviewId = linetokens[0]
        reviewlabel = [token.lower() for token in linetokens[1:]]
        reviewLabels[reviewId]=reviewlabel

#print review
print len(review)
#print reviewLabels
print len(reviewLabels)

tokens = {}
tokenPositiveFake = {}
tokenPositive= {}
tokenPositiveTrue = {}
tokenNegFake = {}
tokenNegtrue={}
tokenNeg={}
tokenFake={}
tokenTrue={}
for reviewId in review.keys():
    if 'truthful' in reviewLabels[reviewId] and 'negative' in reviewLabels[reviewId]:
        for token in review[reviewId]:
            if token in tokenNegtrue.keys():
                tokenNegtrue[token] = tokenNegtrue[token] + 1
            elif token != "":
                tokenNegtrue[token] = 1
            if token in tokenTrue.keys():
                tokenTrue[token] = tokenTrue[token] + 1
            elif token != "":
                tokenTrue[token] = 1
            if token in tokenNeg.keys():
                tokenNeg[token] = tokenNeg[token] + 1
            elif token != "":
                tokenNeg[token] = 1
            if token in tokens.keys():
                tokens[token] = tokens[token] + 1
            elif token != "":
                tokens[token] = 1
    elif 'truthful' in reviewLabels[reviewId] and 'positive' in reviewLabels[reviewId]:
        for token in review[reviewId]:
            if token in tokenTrue.keys():
                tokenTrue[token] = tokenTrue[token] + 1
            elif token != "":
                tokenTrue[token] = 1
            if token in tokenPositive.keys():
                tokenPositive[token] = tokenPositive[token] + 1
            elif token != "":
                tokenPositive[token] = 1
            if token in tokenPositiveTrue.keys():
                tokenPositiveTrue[token] = tokenPositiveTrue[token] + 1
            elif token != "":
                tokenPositiveTrue[token] = 1
            if token in tokens.keys():
                tokens[token] = tokens[token] + 1
            elif token != "":
                tokens[token] = 1
    elif 'deceptive' in reviewLabels[reviewId] and 'positive' in reviewLabels[reviewId]:
        for token in review[reviewId]:
            if token in tokenPositive.keys():
                tokenPositive[token] = tokenPositive[token] + 1
            elif token != "":
                tokenPositive[token] = 1
            if token in tokenFake.keys():
                tokenFake[token] = tokenFake[token] + 1
            elif token != "":
                tokenFake[token] = 1
            if token in tokenPositiveFake.keys():
                tokenPositiveFake[token] = tokenPositiveFake[token] + 1
            elif token != "":
                tokenPositiveFake[token] = 1
            if token in tokens.keys():
                tokens[token] = tokens[token] + 1
            elif token != "":
                tokens[token] = 1
    else:
        for token in review[reviewId]:
            if token in tokenFake.keys():
                tokenFake[token] = tokenFake[token] + 1
            elif token != "":
                tokenFake[token] = 1
            if token in tokenNeg.keys():
                tokenNeg[token] = tokenNeg[token] + 1
            elif token != "":
                tokenNeg[token] = 1
            if token in tokenNegFake.keys():
                tokenNegFake[token] = tokenNegFake[token] + 1
            elif token != "":
                tokenNegFake[token] = 1
            if token in tokens.keys():
                tokens[token] = tokens[token] + 1
            elif token != "":
                tokens[token] = 1

print tokens
print len(tokens)

#word count for each class
NpositveFake = 0
NpositveTruthful = 0
NnegativeFake = 0
NnegativeTruthful = 0
Npositive = 0
Nnegative = 0
Nfake = 0
Ntruthful = 0
n = len(review)

for reviewId in review.keys():
    l = len(review[reviewId])
    if 'truthful' in reviewLabels[reviewId] and 'negative' in reviewLabels[reviewId]:
        NnegativeTruthful = NnegativeTruthful + l
        Ntruthful = Ntruthful + l
        Nnegative = Nnegative + l
    elif 'truthful' in reviewLabels[reviewId] and 'positive' in reviewLabels[reviewId]:
        Ntruthful = Ntruthful + l
        Npositive = Npositive + l
        NpositveTruthful = NpositveTruthful + l
    elif 'deceptive' in reviewLabels[reviewId] and 'positive' in reviewLabels[reviewId]:
        Npositive = Npositive + l
        Nfake = Nfake + l
        NpositveFake = NpositveFake + l
    else:
        Nfake = Nfake + l
        Nnegative = Nnegative + l
        NnegativeFake = NnegativeFake + l

'''
for label in reviewLabels.values():
    if 'truthful' in label and 'negative' in label:
        NnegativeTruthful = NnegativeTruthful + 1
        Ntruthful = Ntruthful + 1
        Nnegative = Nnegative + 1
    elif 'truthful' in label and 'positive' in label:
        NpositveTruthful = NpositveTruthful + 1
        Npositive = Npositive + 1
        Ntruthful = Ntruthful + 1
    elif 'deceptive' in label and 'positive' in label:
        NpositveFake = NpositveFake + 1
        Npositive = Npositive + 1
        Nfake = Nfake + 1
    else:
        NnegativeFake = NnegativeFake + 1
        Nnegative = Nnegative + 1
        Nfake = Nfake + 1

Add1Smoothing = {}
for token in tokens.keys():
    Add1Smoothing[token] = tokens[token] + 1
'''
vocabulary = list(set(tokens.keys()))
vocabLength = len(vocabulary)

print vocabulary
print vocabLength
print NnegativeTruthful, NpositveTruthful, NnegativeFake, NpositveFake, Nnegative, Npositive, Ntruthful, Nfake

#types of features
#positive fake
#positive true
#negative fake
#nrgative true


#calculate probabilities
#tokenProbabilityTwolabels = {}
tokenProbabilityPosTrue = {}
tokenProbabilityNegTrue = {}
tokenProbabilityPosFake = {}
tokenProbabilityNegFake = {}
tokenProbabilityNeg = {}
tokenProbabilityPos = {}
tokenProbabilityTrue = {}
tokenProbabilityFake = {}
probabilityPos = float(log(Npositive) - log(n))
probabilityNeg = float(log(Nnegative) - log(n))
probabilityFake = float(log(Nfake) - log(n))
probabilityTrue = float(log(Ntruthful) - log(n))
probabilityPosFake = float(log(NpositveFake) - log(n))
probabilityPosTrue = float(log(NpositveTruthful) - log(n))
probabilityNegFake = float(log(NnegativeFake) - log(n))
probabilityNegTrue = float(log(NnegativeTruthful) - log(n))


for token in tokens.keys():
    # negative fake
    if token in tokenNegFake.keys():
        tokenProbabilityNegFake[token] = float(log(tokenNegFake[token] + 1)-log(NnegativeFake+vocabLength))
    else:
        tokenProbabilityNegFake[token] = float(log(1)-log(NnegativeFake+vocabLength))

    # negative true
    if token in tokenNegtrue.keys():
        tokenProbabilityNegTrue[token] = float(log(tokenNegtrue[token] + 1)-log(NnegativeTruthful+vocabLength))
    else:
        tokenProbabilityNegTrue[token] = float(log(1) - log(NnegativeTruthful + vocabLength))

    # positive fake
    if token in tokenPositiveFake.keys():
        tokenProbabilityPosFake[token] = float(log(tokenPositiveFake[token] + 1)-log(NpositveFake + vocabLength))
    else:
        tokenProbabilityPosFake[token] = float(log(1) - log(NpositveFake + vocabLength))

    # positive true
    if token in tokenPositiveTrue.keys():
        tokenProbabilityPosTrue[token] = float(log(tokenPositiveTrue[token] + 1)-log(NpositveTruthful + vocabLength))
    else:
        tokenProbabilityPosTrue[token] = float(log(1) - log(NpositveTruthful + vocabLength))

    # negative
    if token in tokenNeg.keys():
        tokenProbabilityNeg[token] = float(log(tokenNeg[token] + 1)-log(Nnegative + vocabLength))
    else:
        tokenProbabilityNeg[token] = float(log(1) - log(Nnegative + vocabLength))

    #positive
    if token in tokenPositive.keys():
        tokenProbabilityPos[token] = float(log(tokenPositive[token] + 1)-log(Npositive + vocabLength))
    else:
        tokenProbabilityPos[token] = float(log(1) - log(Npositive + vocabLength))

    # fake
    if token in tokenFake.keys():
        tokenProbabilityFake[token] = float(log(tokenFake[token] + 1)-log(Nfake+vocabLength))
    else:
        tokenProbabilityFake[token] = float(log(1) - log(Nfake + vocabLength))

    # true
    if token in tokenTrue.keys():
        tokenProbabilityTrue[token] = float(log(tokenTrue[token] + 1)-log(Ntruthful + vocabLength))
    else:
        tokenProbabilityTrue[token] = float(log(1) - log(Ntruthful + vocabLength))

print tokenProbabilityPosTrue, tokenProbabilityPosFake, tokenProbabilityPos
print tokenProbabilityNegTrue, tokenProbabilityNegFake, tokenProbabilityNeg
print tokenProbabilityTrue, tokenProbabilityFake

jsonFile = {}
jsonFile["tokenProbabilityPosTrue"] = tokenProbabilityPosTrue
jsonFile["tokenProbabilityPosFake"] = tokenProbabilityPosFake
jsonFile["tokenProbabilityPos"] = tokenProbabilityPos
jsonFile["tokenProbabilityNegTrue"] = tokenProbabilityNegTrue
jsonFile["tokenProbabilityNegFake"] = tokenProbabilityNegFake
jsonFile["tokenProbabilityNeg"] = tokenProbabilityNeg
jsonFile["tokenProbabilityTrue"] = tokenProbabilityTrue
jsonFile["tokenProbabilityFake"] = tokenProbabilityFake
jsonFile["probabilityPos"] = probabilityPos
jsonFile["probabilityNeg"] = probabilityNeg
jsonFile["probabilityFake"] = probabilityFake
jsonFile["probabilityTrue"] = probabilityTrue
jsonFile["probabilityPosFake"] = probabilityPosFake
jsonFile["probabilityPosTrue"] = probabilityPosTrue
jsonFile["probabilityNegFake"] = probabilityNegFake
jsonFile["probabilityNegTrue"] = probabilityNegTrue

#save the model
outputFile ="nbmodel.txt"
with open(outputFile, "w") as f:
    json.dump(jsonFile,f,ensure_ascii=True,encoding='utf-8')
