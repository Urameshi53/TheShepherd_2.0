#import regex 
import re

from discussions.models import Discussion

from googlesearch import search

searches = search("Google", num_results=100)

def match_words(words, string):
    return regex.search(r'\b\L<words>\b', string, words=words)

class Search(object):
    def __init__(self):
        self.discussions = Discussion.objects.all()
        self.discussions_list = [discussion.content for discussion in self.discussions]
        self.query = 'hello world'
        self.discussions_dictionary = {}
        self.results = []

    def find(self, query):
        self.query = query
        for i in self.discussions_list:
            q = self.query.split()
            for j in q:
                x = re.findall(j, i)
                if x:
                    if not i in self.discussions_dictionary:
                        self.discussions_dictionary[i] = 1
                    else:
                        self.discussions_dictionary[i] += 1
                        print(i)
            else:
                print(i,'is not a match for', j)
        #print(d.sort(reverse=True))
        l = sorted(self.discussions_dictionary, reverse=True)

        for discussion in self.discussions:
            for i in l:
                if discussion.content == i:
                    self.results.append(discussion)

        return self.results
        #print(l)

    def find_s(self, query):
        searches = search(query, num_results=100)
        return searches

#find(query, text)
