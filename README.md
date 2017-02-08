# sentiment analysis of hotel reviews
nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data

The learning program will be invoked in the following way:
> python nblearn.py /path/to/text/file /path/to/label/file

The classification program will be invoked in the following way:
> python nbclassify.py /path/to/text/file

The argument is the test data file, which has the same format as the training text file. The program will read the parameters of a naive Bayes model from the file nbmodel.txt, classify each entry in the test data, and write the results to a text file called nboutput.txt in the same format as the label file from the training data.
