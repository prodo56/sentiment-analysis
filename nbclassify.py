import json
import sys
import re
from math import log as log


jsonFile = "nbmodel.txt"

with open(jsonFile) as f:
    model = json.load(f)

print model
tokenProbabilityPosTrue = model["tokenProbabilityPosTrue"]
tokenProbabilityPosFake = model["tokenProbabilityPosFake"]
tokenProbabilityPos = model["tokenProbabilityPos"]
tokenProbabilityNegTrue = model["tokenProbabilityNegTrue"]
tokenProbabilityNegFake = model["tokenProbabilityNegFake"]
tokenProbabilityNeg = model["tokenProbabilityNeg"]
tokenProbabilityTrue = model["tokenProbabilityTrue"]
tokenProbabilityFake = model["tokenProbabilityFake"]
probabilityPos = model["probabilityPos"]
probabilityNeg = model["probabilityNeg"]
probabilityFake = model["probabilityFake"]
probabilityTrue = model["probabilityTrue"]
probabilityPosFake = model["probabilityPosFake"]
probabilityPosTrue = model["probabilityPosTrue"]
probabilityNegFake = model["probabilityNegFake"]
probabilityNegTrue = model["probabilityNegTrue"]

review = {}
stopwords=[".",",","?","&","/","%","\"","-"]
testFile = sys.argv[1]
#testFile = "test.txt"
with open(testFile) as f:
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


#write classifier for P(positiveFake|review)
#write classifier for P(positiveTrue|review)
#write classifier for P(negativeFake|review)
#write classifier for P(negativeTrue|review)
classification = {}
for reviewId in review.keys():
    probSumPositiveFake = probabilityPosFake
    probSumPositiveTrue = probabilityPosTrue
    probSumNegFake = probabilityNegFake
    probSumNegTrue = probabilityNegTrue
    for token in review[reviewId]:
        if token in tokenProbabilityPosTrue.keys():
            probSumPositiveTrue = probSumPositiveTrue + tokenProbabilityPosTrue[token]
        if token in tokenProbabilityPosFake.keys():
            probSumPositiveFake = probSumPositiveFake + tokenProbabilityPosFake[token]
        if token in tokenProbabilityNegTrue.keys():
            probSumNegTrue = probSumNegTrue + tokenProbabilityNegTrue[token]
        if token in tokenProbabilityNegFake.keys():
            probSumNegFake = probSumNegFake + tokenProbabilityNegFake[token]
    # compare log(P)
    maxValue = max(probSumPositiveFake,probSumPositiveTrue,probSumNegFake,probSumNegTrue)
    if maxValue == probSumNegTrue:
        classification[reviewId] = "truthful negative"
    elif maxValue == probSumNegFake:
        classification[reviewId] = "deceptive negative"
    elif maxValue == probSumPositiveFake:
        classification[reviewId] = "deceptive positive"
    else:
        classification[reviewId] = "truthful positive"

#output results
print classification
resultFile = "nboutput.txt"
with open(resultFile, "w") as file:
    for key, value in classification.items():
        file.write("%s %s\n" % (key, value))











