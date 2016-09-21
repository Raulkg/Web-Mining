import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk import *
from nltk.corpus import stopwords
import re
import urllib
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
    
def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

# page-1 
html1 = urllib.urlopen('http://www.briansolis.com/2015/01/25-disruptive-technology-trends-2015-2016/')
soup1 = BeautifulSoup(html1, "lxml")
data1 = soup1.findAll(text=True)         
result1 = filter(visible, data1)

# page-2
html2 = urllib.urlopen('https://www.jimcarroll.com/2014/12/trend-report-the-future-of-autonomous-vehicle-technology/#.V985adGVs8q')
soup2 = BeautifulSoup(html2, "lxml")
data2 = soup2.findAll(text=True)
result2 = filter(visible, data2)

# page-3 
html3 = urllib.urlopen('http://www.infoworld.com/article/3007057/cloud-computing/9-enterprise-tech-trends-for-2016-and-beyond.html')
soup3 = BeautifulSoup(html3, "lxml")
data3 = soup3.findAll(text=True)
result3 = filter(visible, data3)

# extracting meaningful sentences and words
text1 = []
for i in result1:
	if len(i) > 10:
		text1.append(i)
text2 = []
for i in result2:
	if len(i) > 10:
		text2.append(i)
text3 = []
for i in result3:
	if len(i) > 10:
		text3.append(i)

# removing punctuation and numbers
punct = set(string.punctuation)
num = ["1","2","3","4","5","6","7","8","9","0"]
stop = stopwords.words('english')
porter = PorterStemmer()

meaningful_text1 = []
nouns_text1 = []
for i in range(len(text1)):
	text1[i] = text1[i].lower()
	text1[i] = "".join(x for x in text1[i] if x not in punct)	
	text1[i] = "".join(x for x in text1[i] if x not in num)	
	sentence = sent_tokenize(text1[i])
	for j in range(len(sentence)):
		tokens = word_tokenize(text1[i])
		tokens_filtered = [x for x in tokens if x not in stop]
		# Parts of speech first
		pos_tagging = nltk.pos_tag(tokens_filtered)
		for word,tag in pos_tagging:
			meaningful_text1.append(word)
			if tag == 'NN':
				nouns_text1.append(word)

meaningful_text2 = []
nouns_text2 = []
for i in range(len(text2)):
	text2[i] = text2[i].lower()
	text2[i] = "".join(x for x in text2[i] if x not in punct)	
	text2[i] = "".join(x for x in text2[i] if x not in num)	
	sentence = sent_tokenize(text2[i])
	for j in range(len(sentence)):
		tokens = word_tokenize(text2[i])
		tokens_filtered = [x for x in tokens if x not in stop]
		# Parts of speech first
		pos_tagging = nltk.pos_tag(tokens_filtered)
		for word,tag in pos_tagging:
			meaningful_text2.append(word)
			if tag == 'NN':
				nouns_text2.append(word)

meaningful_text3 = []
nouns_text3 = []
for i in range(len(text3)):
	text3[i] = text3[i].lower()
	text3[i] = "".join(x for x in text3[i] if x not in punct)	
	text3[i] = "".join(x for x in text3[i] if x not in num)	
	sentence = sent_tokenize(text3[i])
	for j in range(len(sentence)):
		tokens = word_tokenize(text3[i])
		tokens_filtered = [x for x in tokens if x not in stop]
		# Parts of speech first
		pos_tagging = nltk.pos_tag(tokens_filtered)
		for word,tag in pos_tagging:
			meaningful_text3.append(word)
			if tag == 'NN':
				nouns_text3.append(word)


# Part 1 -- commanalities netween these pages
common = list(set(meaningful_text1).intersection(meaningful_text2).intersection(meaningful_text3))
print "====== PART 1 ======"
for i in common:
	print i

# Part 2 -- print pages similar to the 3 pages
# using cosine similarity to validate if any given test page has similar content to the given 3 pages
html4 = urllib.urlopen('http://stackoverflow.com/questions/8270092/python-remove-all-whitespace-in-a-string')	# enter test URL
soup4 = BeautifulSoup(html4, "lxml")
data4 = soup4.findAll(text=True)
result4 = filter(visible, data4)

text4 = []
for i in result4:
	if len(i) > 10:
		text4.append(i)

meaningful_text4 = []
nouns_text4 = []
for i in range(len(text4)):
	text4[i] = text4[i].lower()
	text4[i] = "".join(x for x in text4[i] if x not in punct)	
	text4[i] = "".join(x for x in text4[i] if x not in num)	
	sentence = sent_tokenize(text4[i])
	for j in range(len(sentence)):
		tokens = word_tokenize(text4[i])
		tokens_filtered = [x for x in tokens if x not in stop]
		# Parts of speech first
		pos_tagging = nltk.pos_tag(tokens_filtered)
		for word,tag in pos_tagging:
			meaningful_text4.append(word)
			if tag == 'NN':
				nouns_text4.append(word)

pattern = re.compile(r'\s+')
text1 = re.sub(pattern, ' ', ' '.join(text1))
text2 = re.sub(pattern, ' ', ' '.join(text2))
text3 = re.sub(pattern, ' ', ' '.join(text3))
text4 = re.sub(pattern, ' ', ' '.join(text4))
print text4

documents = [text1, text2, text3, text4]

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(documents)
similarities = cosine_similarity(tfidf_matrix[3:4], tfidf_matrix)	# similarity of 4th document with all other documents
print similarities
similarities = similarities.tolist()

# let us assume that if test page is more than 70% similar to every individual page, then it will be listed as similar
flag = 0
for i in similarities[0]:
	if i < 0.7:
		flag = flag + 1

print "====== PART 2 ======"
if flag==0:
	print "test page is similar to the three pages given"
else:
	print "test page is not similar to the three pages given"			
	
	
# part 3 -- finding similar pages, assuming test page has an average similarity of 70% to the given 3 pages
print "====== PART 3 ======"
if numpy.mean(similarities[0:3]) >= 0.7:
	print "test page is similar to the three pages given"
else:
	print "test page is not similar to the three pages given"
 




