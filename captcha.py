from PIL import Image
from math import fabs
import numpy as np
import os
from sklearn.neural_network import MLPClassifier

def TotallyShit(im):
	x,y=im.size
	mmltilist=list()
	for i in range(x):
		for j in range(y):
			if im.getpixel((i,j))<200:
				mmltilist.append(1)
			else:
				mmltilist.append(0)
	return mmltilist

def clf():
	clf=MLPClassifier()
	mmltilist=list()
	X=list()
	for i in range(0,12):
		for j in os.listdir("douplings/douplings-{}".format(i)):
			mmltilist.append(TotallyShit(Image.open("douplings/douplings-{0}/{1}".format(i,j)).convert("L")))
			X.append(i)
	clf.fit(mmltilist,X)
	return clf