import glob
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score
from sklearn.svm import SVC
# from sklearn import LogisticRegression as lr
import re
import os
import numpy as np

start = time.time()

my_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(my_path, "stopWords\\stopWords.txt")

stop_words_file = open(path, 'r')
stop_words = []
for line in stop_words_file.readlines():
	new_split = line.split("\n")
	stop_words.append(new_split[0])


# data_path = "../../ML CSVs/*.CSV"

# all_files = pd.DataFrame()
# for filename in glob.glob(data_path):
# 	current_file = pd.read_csv(filename)
# 	all_files = pd.concat([all_files, current_file])


# Label (0 = Bug, 1 = Feature Request, 2 = Not 1 or 0)
labeled_data_path_1 = os.path.join(my_path, 'SSL1.xlsx')

all_files = pd.read_excel(labeled_data_path_1)

#all_files = pd.concat([labeled_contents_1], axis=0, sort=False)

all_files.reset_index(inplace = True, drop = True)

# all_title_and_body = []
# for title, body in zip(all_files['title'], all_files['body']):
# 	split_title = re.split('\W+', title)
# 	split_body = re.split('\W+', body)
# 	if 'b' in split_title:
# 		split_title.remove('b')
# 	if 'b' in split_body:
# 		split_body.remove('b')
# 	if 'n' in split_title:
# 		split_title.remove('n')
# 	if 'n' in split_body:
# 		split_body.remove('n')
# 	if 'r' in split_title:
# 		split_title.remove('r')
# 	if 'r' in split_body:
# 		split_body.remove('r')
# 	if '' in split_title:
# 		split_title.remove('')
# 	if '' in split_body:
# 		split_body.remove('')
# 	all_title_and_body.append([split_title, split_body])

# all_issues = []
# for issue in all_title_and_body:
# 	current_issue = []
# 	for item in issue[0]:
# 		if item in stop_words:
# 			continue
# 		else:
# 			current_issue.append(item)
# 	for item in issue[1]:
# 		if item in stop_words:
# 			continue
# 		else:
# 			current_issue.append(item)
# 	all_issues.append(current_issue)

# print(all_issues)

all_title_and_body = []
for title, body in zip(all_files['title'], all_files['body']):
	all_title_and_body.append(str(title) + " " + str(body))


# create the transform
vectorizer = CountVectorizer(stop_words='english', min_df=10, max_df=160)

# tokenize and build vocab
vectorizer.fit(all_title_and_body)

# summarize
# print(vectorizer.vocabulary_)

# encode document
vector = vectorizer.transform(all_title_and_body)

# summarize encoded vector
X = vector.toarray()

y = all_files['label']

X_train, X_test, y_train, y_test = train_test_split( X, y )

classifier = OneVsRestClassifier(SVC(class_weight='balanced')).fit(X_train, y_train)

parameters = {
    "estimator__C": [0.1, 1, 10, 100, 1000],
    "estimator__kernel": ["linear","poly","rbf"],
    "estimator__degree":[0, 1, 2, 3, 4, 5, 6],
	"estimator__gamma":[0.1, 1, 10, 100],
}

model_tuning = GridSearchCV(classifier, param_grid=parameters, verbose=2)

model_tuning.fit(X_train, y_train)

predictions = model_tuning.predict(X_test)

print(predictions)

accuracy_scores = accuracy_score(y_test, predictions)

print("Accuracy: " + str(accuracy_scores))

end = time.time()

print("Run Time: " + str(end-start))