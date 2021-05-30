import pandas as pd
import numpy as np
import py_stringsimjoin as ssj
import py_stringmatching as sm
import py_entitymatching as em

def preprocess_title(title):
	title = title.lower()
	title = title.replace(',', ' ')
	title = title.replace("'", '')    
	title = title.replace('&', 'and')
	title = title.replace('?', '')
	title = title.encode('utf-8', 'ignore')
	return title.strip()


hn_itviec = pd.read_json('hanoi_itviec.json')
hn_vnwork = pd.read_json('hanoi_vietnamwork.json')


print(hn_itviec.head(5))
print(hn_vnwork.head(5))

hn_itviec['id'] = range(hn_itviec.shape[0])
hn_vnwork['id'] = range(hn_vnwork.shape[0])

hn_itviec['mixture'] = hn_itviec['title'] + ' ' + hn_itviec['company']
hn_vnwork['mixture'] = hn_vnwork['title'] + ' ' + hn_vnwork['company']

hn_itviec.to_csv('data_3005/hn_itviec.csv')
hn_vnwork.to_csv('data_3005/hn_vnwork.csv')

C = ssj.overlap_coefficient_join(hn_itviec, hn_vnwork, 'id', 'id', 'mixture', 'mixture', sm.WhitespaceTokenizer(), 
								 l_out_attrs=['title', 'company', 'salary'],
								 r_out_attrs=['title', 'company', 'maxSalary'],
								 threshold=0.6)
print(C.head(5))
print(C.shape)
print(C.loc[0])

em.set_key(hn_itviec, 'id')   # specifying the key column in the kaggle dataset
em.set_key(hn_vnwork, 'id')     # specifying the key column in the imdb dataset
em.set_key(C, '_id')            # specifying the key in the candidate set
em.set_ltable(C, hn_itviec)   # specifying the left table 
em.set_rtable(C, hn_vnwork)     # specifying the right table
em.set_fk_rtable(C, 'r_id')     # specifying the column that matches the key in the right table 
em.set_fk_ltable(C, 'l_id')     # specifying the column that matches the key in the left table 

#C.to_csv('./data_3005/sampled.csv', encoding='utf-8')
labeled = em.read_csv_metadata('data_3005/labeled.csv', ltable=hn_itviec, rtable=hn_vnwork,
							   fk_ltable='l_id', fk_rtable='r_id', key='_id')

labeled.head()
labeled['l_title'] = labeled['l_title'].map(preprocess_title)
labeled['r_title'] = labeled['r_title'].map(preprocess_title)
labeled['l_company'] = labeled['l_company'].map(preprocess_title)
labeled['r_company'] = labeled['r_company'].map(preprocess_title)
# hn_itviec = em.read_csv_metadata('data_3005/hn_itviec.csv', key='id')
# hn_vnwork = em.read_csv_metadata('data_3005/hn_vnwork.csv', key='id')

split = em.split_train_test(labeled, train_proportion=0.6, random_state=0)
train_data = split['train']
test_data = split['test']

dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NaiveBayes')

attr_corres = em.get_attr_corres(hn_itviec, hn_vnwork)
# attr_corres['corres'] = [('title', 'title'),
# 						('company', 'company')]

l_attr_types = em.get_attr_types(hn_itviec)
r_attr_types = em.get_attr_types(hn_vnwork)

tok = em.get_tokenizers_for_matching()
sim = em.get_sim_funs_for_matching()

F = em.get_features(hn_itviec, hn_vnwork, l_attr_types, r_attr_types, attr_corres, tok, sim)

train_features = em.extract_feature_vecs(train_data, feature_table=F, attrs_after='label', show_progress=False) 
train_features = em.impute_table(train_features,  exclude_attrs=['_id', 'l_id', 'r_id', 'label'], strategy='mean', missing_val = np.nan)

result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=train_features, 
						   exclude_attrs=['_id', 'l_id', 'r_id', 'label'], k=5,
						   target_attr='label', metric_to_select_matcher='f1', random_state=0)
result['cv_stats']

best_model = result['selected_matcher']
best_model.fit(table=train_features, exclude_attrs=['_id', 'l_id', 'r_id', 'label'], target_attr='label')

test_features = em.extract_feature_vecs(test_data, feature_table=F, attrs_after='label', show_progress=False)
test_features = em.impute_table(test_features, exclude_attrs=['_id', 'l_id', 'r_id', 'label'], strategy='mean', missing_val = np.nan)

# Predict on the test data
predictions = best_model.predict(table=test_features, exclude_attrs=['_id', 'l_id', 'r_id', 'label'], 
								 append=True, target_attr='predicted', inplace=False)

# Evaluate the predictions
eval_result = em.eval_matches(predictions, 'label', 'predicted')
em.print_eval_summary(eval_result)

candset_features = em.extract_feature_vecs(C, feature_table=F, show_progress=True)
candset_features = em.impute_table(candset_features, exclude_attrs=['_id', 'l_id', 'r_id'], strategy='mean', missing_val = np.nan)
predictions = best_model.predict(table=candset_features, exclude_attrs=['_id', 'l_id', 'r_id'],
								 append=True, target_attr='predicted', inplace=False)
matches = predictions[predictions.predicted == 1]

from py_entitymatching.catalog import catalog_manager as cm
matches = matches[['_id', 'l_id', 'r_id', 'predicted']]
matches.reset_index(drop=True, inplace=True)
cm.set_candset_properties(matches, '_id', 'l_id', 'r_id', hn_itviec, hn_vnwork)
matches = em.add_output_attributes(matches, l_output_attrs=['title', 'salary', 'company', 'address'],
								   r_output_attrs=['title', 'maxSalary', 'company', 'address'],
								   l_output_prefix='l_', r_output_prefix='r_',
								   delete_from_catalog=False)
matches.drop('predicted', axis=1, inplace=True)
matches.head()
matches.to_csv('data_3005/matches.csv')