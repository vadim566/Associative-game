import TF_IDF


if __name__ == '__main__':
    sub_folder=['a\\','b\\','c\\']
    bookLib = ".\\books\\"
    #files = TF_IDF.filesinDir(".\\books\\")
    query='bell'
    test_query=[]

    test_dics=[]

    #leader
    leader_test=TF_IDF.TF_IDF(bookLib=bookLib,files=TF_IDF.filesinDir(str(bookLib)),query=query)

    for i in range(3):
        test_query.append(TF_IDF.TF_IDF(bookLib=str(bookLib)+str(sub_folder[i]), files=TF_IDF.filesinDir(str(bookLib)+str(sub_folder[i])),query=query))
        test_query[i].worker()
        test_dics.append(test_query[i].TF_dic)


    leader_test.leader(test_dics)
    leader_test.score_items_LEADER()
    leader_test.pracentage_score()
    leader_test.sort_values()
    print(leader_test.sorted_terms_score)


#    test_query = TF_IDF.TF_IDF(bookLib, files, query)
#   test_query.tf_idf_scoring()
#
#     print(test_query.terms_score)
#     print(test_query.sorted_terms_score)
#     test_query.pracentage_score()
#     test_query.sort_values()
#     print(test_query.TF_dic)
#
#
#     print(test_query.terms_score)
#     print(test_query.sorted_terms_score)
