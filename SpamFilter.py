# -*- coding: utf-8 -*-

#AZ.FD
#A simple Bayesian spam filtering implementation
#base.txt => Used as base data to precalculate some probabilities. each row represent an email.
#from column 1 to 45 =>the amount of times a word appears in the email
#column 46 total amount of words in the email
#column 47 indicates if the email is considered spam on not
#e1.txt => each row represent an email, each column represent the existant of a certain word in that email
#salida.txt => Stores the results

#Store the amount of times a word appears in a spam/notSpam email
cantPalSpam = []
cantPal = []

#Probability of a word being in a spam/notSpam email. P(wi|S)
wProbSpam = []
wProbNoSpam = []

#total Amount of words in a spam/notSpam email 
totalWordsSpam = []
totalWordsNoSpam = []

#store the probability of each given email from being spam
isSpam = []

#Total amount of emails from base.txt
nMails = 0.0

#Amount of spam emails
nSpam = 0

#Represent the probability of N words being in a spam email. 
probCount = 1 #P(W|S), W=w1,w2,w3...wn, S=spam
probNoCount = 1 #P(W|H) H=not spam

#Initialize the arrays
for i in range(0,45):
	cantPal.append(0.0)
	cantPalSpam.append(0.00)
	wProbSpam.append(0.0)
	totalWordsSpam.append(0.00)
	wProbNoSpam.append(0.0)
	totalWordsNoSpam.append(0.0)

# Open base.txt
fo = open('base.txt','r')

#Read the first line from the file to skip the header
line = fo.readline()

#Proceed to read the remain lines from base.txt
for line in fo:

	line = line.split(' ') #Isolate every value from a line [frec_pal,total_words,is_spam]

	nMails+= 1 #email counter	

	#Every word is represented by a number that is stored in the array 'line'.
	#This number indicates amount of times a word appears in the emails
	#The loop will check if a word is part of the email and if that email is considered spam
	#In case that the word exists and the email is spam/notSpam, we summarize the amount of times the word appears and insert them into cantPalSpam[i]/cantPal[i]
	if( int(line[46])==1 ):

		nSpam+= 1 #email Spam counter

		for i in xrange(0,45):
			cantPalSpam[i]+= int(line[i])
			wProbSpam[i]+= int(line[i])
			totalWordsSpam[i]+= int(line[45])
	
	else:
		for i in xrange(0,45):
			cantPal[i]+= int(line[i])
			wProbNoSpam[i]+= int(line[i]) 
			totalWordsNoSpam[i]+= int(line[45])

#Close the file since we dont retrieve data anymore
fo.close()

#Calculate the word probability of being spam given the total amount of words
for i in xrange(0,45):
	wProbSpam[i] = cantPalSpam[i] / totalWordsSpam[i]
	wProbNoSpam[i] = cantPal[i] / totalWordsNoSpam[i]

#Calculate the email probability of being spam. P(S)
spamMail = float(nSpam / nMails)


# Open entrada.txt for read only
fo = open('e1.txt','r')

for line in fo:	

	line = line.split(' ')

	probCount = 1
	probNoCount = 1

	#verify if a word exist in a certain email
	for i in xrange(0,45):
		if( int(line[i])==1 ):
			probCount *= wProbSpam[i]
			probNoCount*= wProbNoSpam[i]

	#Bayesian spam filtering formula
	isSpam.append( ( (probCount)*(spamMail) ) / ( (probCount)*(spamMail) + (probNoCount)*(1 - spamMail) ) )

fo.close

#Store the results in the file "salida.txt". The results will be set to a four decimals precision 0.0000
fo = open('salida.txt','wb')

n = len(isSpam)

for i in xrange(0,n):
	fo.write(str(round(isSpam[i],4)))
	fo.write("\n")

fo.close
