# This is a sample Python script.
from os import listdir
from os.path import join, isdir, isfile
import math
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from collections import Counter

def filesinDir(dir_path):
    try:
        files_in_dir = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    except:
        "something wrong with the directory, put in the full path"
    finally:
        return files_in_dir


def count_term(terms, book):
    # init dic
    term_ct = {}
    for term in terms:
        term_ct[term] = 0
    # count each term
    for word in book:
        for term in terms:
            if word == term or word[:-1]==term :
                term_ct[term] = term_ct[term] + 1
                break

    return term_ct


def TF(bookfile,terms):
    #split query into terms



    #append the book.txt into book for 1 time read
    book = []
    with open(bookfile,'r')as file:
        for line in file:
            for word in line.split():
                book.append(word)

    #count words in book
    book_len= len(book)
    ct_terms=count_term(terms,book)

    #create the TF final dic
    TF={}
    for key, value in ct_terms.items():
       TF[key]=value/book_len

    return TF

#IDF
def IDF(files,terms,TF_dic):
    num_of_docs= len(files)
    ct_terms={}
    for term in terms:
        ct_terms[term]=0
    for k in TF_dic:
        for key,value in TF_dic[k].items():
            if value>0:
                ct_terms[key]=ct_terms[key]+1
    for key , value in ct_terms.items():
        ct_terms[key]=math.log(num_of_docs/value)
    return ct_terms







class TF_IDF:
    def __init__(self,bookLib,files,query):
        self.bookLib = bookLib#".\\books\\"
        self.files = files#filesinDir('.\\books\\')
        self.query = query#"big mountains sorrow"
        self.terms_score={}
        self.sorted_terms_score={}
        self.TF_dic={}
        self.terms=""
        self.idf_dic={}


    def  tf_idf_scoring(self):
        self.terms = self.query.split()
        self.create_tf_dic()
        self.idf_dic = IDF(self.files, self.terms, self.TF_dic)
        self.score_items()
        self.sort_values()

    def worker(self):
        self.terms = self.query.split()
        self.create_tf_dic()

    def leader(self,TF_dics:list):

        for d in TF_dics:
            for k, v in d.items():  # d.items() in Python 3+
                self.TF_dic.setdefault(k, []).append(v)

        self.idf_dic = self.LEADER_IDF(self.files, self.TF_dic)
        self.score_items()
        self.sort_values()

    def LEADER_IDF(self,files, TF_dic):
        num_of_docs = len(self.TF_dic.items())
        ct_terms = {}
        self.terms=self.query.split()

        terms=self.terms
        for term in terms:
            ct_terms[term] = 0
        for k in TF_dic.keys():
            for key, value in TF_dic[k][0].items():
                if value > 0:
                    ct_terms[key] = ct_terms[key] + 1
        for key, value in ct_terms.items():
            if value>0:
                ct_terms[key] = math.log(num_of_docs / value)
        return ct_terms

    def create_tf_dic(self):
        for f in self.files:
            file_name = self.bookLib + f
            self.TF_dic[f] = TF(file_name, self.terms)
    def pracentage_score(self):
        sum_list=sum(self.terms_score.values())
        if sum_list == 0:
            return "smth went wrong"

        for key in self.terms_score.keys():
            self.terms_score[key]=100*self.terms_score[key]/sum_list



    def score_items(self):
        for doc in self.files:
            self.terms_score[doc]=0
            for key in self.TF_dic[doc]:
                self.terms_score[doc]=self.terms_score[doc]+self.TF_dic[doc][key]*self.idf_dic[key]

    def score_items_LEADER(self):
        for doc in self.TF_dic.keys():
            self.terms_score[doc] = 0
            for key in self.TF_dic[doc][0]:
                self.terms_score[doc] = self.terms_score[doc] + self.TF_dic[doc][0][key] * self.idf_dic[key]

    def sort_values(self):
        self.sorted_terms_score=sorted(self.terms_score.items(),key=lambda x: x[1], reverse=True)



# Press the green button in the gutter to run the script.

   # print(ct_terms)
  #  print(TF_dic)
# #final doc score
# def score_items(files,TF_dic,ct_terms):
#     terms_score={}
#     for doc in files:
#         terms_score[doc]=0
#         for key in TF_dic[doc]:
#             terms_score[doc]=terms_score[doc]+TF_dic[doc][key]*ct_terms[key]
#
#     sorted_terms_score=sorted(terms_score,key=lambda x: x[1], reverse=False)
#     return sorted_terms_score, terms_scoreSee PyCharm help at https://www.jetbrains.com/help/pycharm/
