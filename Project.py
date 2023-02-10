# first task:  Understand what each field means.
# The Reuters-21578 collection is distributed in 22 files. Each of the first 21 files contain 1000 documents
# while the last document contains 578 documents.
# A document type declaration line appears at the top of each of the 22 files. <!DOCTYPE lewis SYSTEM "lewis.dtd">
# In the beginning of each article is an "open tag" <REUTERS TOPICS,LEWISSPLIT,CGISPLIT,OLDID,NEWID>,
# The potential values for these attributes are as follows:
# 1.TOPICS :
# a.YES: shows that there was at least one element in the TOPICS fields in the original data. b.NO: the opposite of yes.
# c.BYPASS: shows that the story was marked with the string BYPASS in the original data.
# 2. LEWISSPLIT
# a. TRAINING: indicates that it was utilized in the training set or b. NOT-USED
# 3. CGISPLIT
# a.TRAINING-SET: indicating the document was in the training set  b.PUBLISHED-TESTSET: the document was in the test set
# 4.OLDID: The story's identification (ID) number in the Reuters-22173 collection.
# 5.NEWID: The story's identification number (ID) in the Reuters-21578, Distribution 1.0 collection.
# A "close tag" is used to end each article: </REUTERS>
# The date and time of the document start with <DATE> and finish with </DATE>.
# the same for all tags begin with <tag> and end with </tag>
# <MKNOTE>, </MKNOTE> corrections made to the original Reuters corpus.
# <TOPICS>, </TOPICS> includes a list of the document's TOPICS categories, if any are present,they will all be separated
# by the tags <D> and </D>.
# <PLACES>, </PLACES> Same as <TOPICS> but for PLACES categories.
# <PEOPLE>, </PEOPLE>  Same as <TOPICS> but for PEOPLE categories.
# <ORGS>, </ORGS> Same as <TOPICS> but for ORGS categories.
# <EXCHANGES>, </EXCHANGES> Same as <TOPICS> but for EXCHANGES categories.
# <COMPANIES>, </COMPANIES> Since there are no COMPANIES categories specified in the collection, these tags will always
# be next to one other.
# <TEXT>, </TEXT>, The potential values for <TEXT> tag has the following attributes:
# a. Type
# NORM : meaning the story's text has a typical structure. In this situation, the TEXT tag is simply shown as <TEXT>.
# BRIEF :  when the story is a short
# UNPROC : when the format of the story is unusual
# b. <AUTHOR>, </AUTHOR>: Author of the story
# c. <DATELINE>, </DATELINE> : The location of the narrative, as well as the period of the year
# d. <TITLE>, </TITLE>: Title of the story
# e. <BODY>, </BODY>: The main text of the story.
##
# second task: split the single file into files, each containing a single news item.
with open("reuters.txt", "r") as f:  # Open the file in read mode
    text = f.read()  # Read data from given text file
    rep_text = text.replace('"', "").replace("=", "").replace(">", "").replace("NEWID", "répartir NEWID  ")  # i
    # replace some punctuations by nothing and replace every occurrence NEWID by répartir NEWID
    before, sep, after = rep_text.partition("répartir")  # searches for a specified string "répartir"I chose that
    # words in frensh because I know  not appear in any place in the corpus
    text_pr = after  # and  take just what after répartire = NEWID
    split_text = text_pr.split("répartir")  # specify répartir like a  separator for split the text
    for i in split_text:  # iterating over a sequence for each element in contents
        name = i.split("\n")  # split the split_text any time there is a new line character
        form_name = name[0]  # put in form_name just list of NEWID references
        with open(f"{form_name}.txt", mode="a+", encoding="utf-8") as f:  # call a with operator and every
            # time there is NEWID it's going to take all the data comes after
            f.write(i)  # and write it in individual text files
##
# third task: find 100 stop words in the collection,and Compare your stop words to the list given in as part of the data.
from nltk.corpus import stopwords
sl = []
slr = []
reuters = open('reuters.txt', 'r')  # Open the file reuters in read mode
stopwords = list(set(stopwords.words('english')))  # import stop words the library nltk
for line in stopwords:  # Loop through each line of the file stopwords
    split_t = line.split()  # Split the lines into words
    for terms in split_t:  # Loop through each term of the split lines
        sl.append(terms)  # add terms to a given list
number = 0  # reinitialize the variable number
for line in reuters:  # Loop through each line of the file reuters
    split_tx = line.split()  # Split the lines into words
    for terms in split_tx:  # Loop through each term of the split lines
        if terms in sl:  # Loop through each term in reuters and compare it with stopwords if exist
            number += 1  # increment number with 1
            if number < 101:  # if number < 100
                slr.append(terms)
print("100 stop words in the collection : ")
print(slr)
with open("stopwords.txt", "r") as f:
    stopwords_text = f.read()
stopwords_list = stopwords_text.split() # Split the stopwords string into a list of stop words
list = []
overlap = 0
for word in slr:
    if word in stopwords_list and word in slr: # Count the number of stop words that appear in both lists
        overlap += 1
        list.append(word)
print("Overlap between the two lists:", overlap)
print("the words are : \n " , list)
##
# fourth task: construct the inverted index of the collection
import re
import nltk
from nltk.tokenize import word_tokenize

with open("reuters.txt", "r") as f:
    f1 = f.read()
corpus = re.compile('<BODY>(.*?)</BODY>', re.DOTALL).findall(f1)  # define just the body of the corpus
for document in corpus:
    word_token = word_tokenize(document)  # tokenize the documents
inverted_index = {}
for i, doc in enumerate(corpus):  # enumerate each document to produce doc id
    for term in doc.split():  # for each term in document
        if term in inverted_index:  # if that term is in the inverted index already
            inverted_index[term].add(f"doc{i}")  # add doc id to term
        else:
            inverted_index[term] = {f"doc{i}"}  # create new doc id for the next set
for element, id in inverted_index.items():
    print(f"{element}:{(id)}")

##
# fifth task: processes AND queries.
def process_query(query1, query2, text):
    documents = text.split(
        "</BODY>")  # Split the text into a list of documents, using the <BODY> and </BODY> tags as delimiters
    matching_documents = []  # Initialize an empty list to store the matching documents
    for document in documents:  # loop over the documents
        id_start_index = document.find("NEWID")  # Get the ID of the document by searching for NEWID
        if id_start_index == -1:  # If the NEWID  is not found, skip this document
            continue
        id_start_index += len("NEWID=")  # start index by the length of "NEWID="
        id_start_index = document.find("\"", id_start_index)  # find the index of the first quotation mark
        id_end_index = document.find("\"", id_start_index + 1)  # find the index of the second quotation mark
        document_id = document[id_start_index + 1:id_end_index]  # extract the ID from between the quotation marks
        if query1 in document and query2 in document:  # Check if the document contains  the query
            matching_documents.append((document_id, document))  # If it does, add the document ID and the document to
            # the list of matching documents
    return matching_documents  # Return the list of matching documents


with open("reuters.txt") as f:
    text = f.read()  # read the text from the reuters
query1 = "Bahia"  # define the first query
query2 = "levels"  # define the second query
matching_documents = process_query(query1, query2, text)  # call the process_query function
for document_id, document in matching_documents:  # use the matching_documents variable to access the list of matching
    # documents.
    print("the matching documents ID using AND queries are ID:", document_id)  # print out the ID

##
# sixth task: find the most similar document to a query using cosine similarity.
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def find_most_similar(query, text):
    documents = text.split("</BODY>")  # Split the text into a list of documents, using the <BODY> and </BODY> tags
    document_ids = []
    for document in documents:
        id_start_index = document.find("NEWID")
        if id_start_index == -1:  # If the NEWID attribute is not found, skip this document
            continue
        id_start_index += len("NEWID=")
        id_start_index = document.find("\"", id_start_index)
        id_end_index = document.find("\"", id_start_index + 1)
        document_id = document[id_start_index + 1:id_end_index]
        document_ids.append(document_id)
    documents_clean = [document.replace("NEWID=", "") for document in documents]  # Create a list of the documents
    # without the NEWID
    vectorizer = CountVectorizer()  # Convert the documents and query into vectors using a CountVectorizer
    query_vector = vectorizer.fit_transform([query]).toarray()
    document_vectors = vectorizer.transform(documents_clean)
    similarities = []  # Initialize a list to store the similarities between the query and each document
    for document_vector in document_vectors:  # Loop over the document vectors and calculate the cosine similarity
        # between each one and the query vector
        similarity = cosine_similarity(query_vector, document_vector)[0][0]
        similarities.append(similarity)
    most_similar_index = np.argmax(similarities)  # Find the index of the most similar document
    return document_ids[most_similar_index]  # Return the ID of the most similar document


with open("reuters.txt") as f:
    text = f.read()
query = "Comissaria "  # define the query
most_similar_id = find_most_similar(query, text)
print("the most similar documents to the query using cosine similarity are \n  the documents ID:", most_similar_id)
