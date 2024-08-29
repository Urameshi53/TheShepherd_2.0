from functools import partial
import sys
import os
from sklearn.feature_extraction.text import CountVectorizer 
import scipy as sp 
import nltk.stem 
import sklearn.datasets

from discussions.models import Discussion
from repository.models import File 

from googlesearch import search
searches = search("Google", num_results=100)

english_stemmer = nltk.stem.SnowballStemmer('english')

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyser = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyser(doc))

vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english')

posts = [discussion.content for discussion in Discussion.objects.all()]
discussions = Discussion.objects.all()

X_train = vectorizer.fit_transform(posts)
num_samples, num_features = X_train.shape
#print(vectorizer.get_feature_names_out())
#posts = [open(os.path.join(DIR, f)).read() for f in os.listdir(DIR)]

#print(vectorizer.get_feature_names_out())


def dist_raw(v1, v2):
    v1_normalized = v1/sp.linalg.norm(v1.toarray())
    v2_normalized = v2/sp.linalg.norm(v2.toarray())
    delta = v1_normalized-v2_normalized            
    return sp.linalg.norm(delta.toarray())

#print('Best post is %i with dist=%.2f'%(best_i, best_dist))

class Search():
    def get_result(new_post):
        #new_post = "tech"
        new_post_vec = vectorizer.transform([new_post])
        
        res = []
        res2 = []
        l = []
        best_dist = 100 
        best_post = ''
        for i in range(num_samples):
            post = posts[i]

            if post==new_post:
                continue 
            post_vec = X_train.getrow(i) 
            d = dist_raw(post_vec, new_post_vec)
            #print("=== Post %i with dist=%.2f: %s"%(i, d, post))
            
            if d<best_dist:
                res.append(post)
                best_dist = d 
                best_i = i 
                best_post = post
            else:
                res2.append(post)

        #print(len(res))
        for i in discussions:
            for j in res:
                if i.content == j:
                    l.append(i)
            for k in res2:
                if i.content == k:
                    l.append(i)
                    
                
        return l[::-1]
    
#s = Search()
#s.get_result()