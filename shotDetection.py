# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 15:33:20 2017

@author: Matt
"""

import numpy as np
import csv
import pandas as pd

def sigmoid(t):
    return 1/(1 + np.exp(-t))

def checkSize(w, X, y):
	# w and y are column vector, shape [N, 1] not [N,]
	# X is a matrix where rows are data sample
	assert X.shape[0] == y.shape[0]
	assert X.shape[1] == w.shape[0]
	assert len(y.shape) == 2
	assert len(w.shape) == 2
	assert w.shape[1] == 1
	assert y.shape[1] == 1

def compactNotation(X):
	return np.hstack([np.ones([X.shape[0], 1]), X])

"""
Read data from path (either)
return X in compact notation (has one appended)
return Y in with shape [n,1] and starts from 0 instead of 1
"""
def readData(path):
    print("reading data from "+path)
    reader = csv.reader(open(path, "r"), delimiter=",")
    d = list(reader)
    
    # import data and reshape appropriately
    data = np.array(d).astype("float")
    X = data[:,0:-1] #I think there are 784 cols, with the last one being the label
    y = data[:,-1]-1
    y.shape = (len(y),1)
    
    # pad data with ones for more compact gradient computation
    o = np.ones((np.shape(X)[0],1))
    X = np.concatenate((o,X),axis = 1)

    print("done reading in the data")
    return X,y

def softmaxGrad(w, X, y):
    checkSize(w, X, y)
    return -np.matmul(X.T, np.multiply(sigmoid(-y*np.matmul(X, w)), y))
    
#     return grad ### RETURN GRADIENt
"""
Calculate accuracy using matrix operations!
"""
def accuracy(OVA, X, y):
#    pred = np.matmul(X, w) > 0
#    pred = pred.astype(int) 
#    pred = 2*pred - 1 # convert to either 1 or -1
#    return np.sum(np.multiply(pred, y) < 0)
    try:
        
        prediction = np.dot(X,OVA) #n by 2,
        #with each row an observation and each column the score for the class
        
        prediction=prediction.astype(int)
        
        digit_prediction=np.argmax(prediction, axis=1) #
        (p,l)=y.shape
        matches_per_row = y.reshape((p,))-digit_prediction==0
        num_matches = sum(matches_per_row) #double check this
        
        accuracy=  1/p * (num_matches)
    except Exception as e:
        print(e)
        accuracy="Something messed up"
    
    return accuracy
    

def gradientDescent(grad, w0, *args, **kwargs):
	max_iter = 5000 #mess around with this
	alpha = 0.001
	eps = 10^(-5)

	w = w0
	iter = 0
	while True:
		gradient = grad(w, *args)
		w = w - alpha * gradient

		if iter > max_iter or np.linalg.norm(gradient) < eps:
			break

		if iter  % 1000 == 1:
			print("Iter %d " % iter)

		iter += 1

	return w

"""
generate label Yout, 
where Y == value then Yout would be 1
otherwise Yout would be -1
"""
def oneVersusAll(Y, value): #done good to go!
    Y_bool = Y == value
    Yout=2*Y_bool - 1
    return Yout


def main():
    trainX, trainY = readData('This will be a path with training data')
    # training individual classifier
    Nfeature = trainX.shape[1]
    Nclass = 2 #there are 2 different classes
    OVA = np.zeros((Nfeature, Nclass)) #each column is a vector of weights
    for i in range(Nclass):
        print("Training for class " + str(i))
        w0 = np.random.rand(Nfeature, 1)
        OVA[:, i:i+1] = gradientDescent(softmaxGrad, w0, trainX, oneVersusAll(trainY, i))
        
    df=pd.DataFrame(OVA)
    df.to_csv("weights.csv")
    print("Accuracy for training set is: ", accuracy(OVA, trainX, trainY))
    
#    testX, testY = readData('MNIST_data/MNIST_test_data.csv')
#    print("Accuracy for test set is: ", accuracy(OVA, testX, testY))

main()
