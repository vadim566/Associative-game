import TF_IDF


if __name__ == '__main__':
    bookLib=".\\books\\a\\"
    files=TF_IDF.filesinDir('.\\books\\a\\')
    #file_name=".\\books\\bulldog.txt"
    query="bell"

    test_query=TF_IDF.TF_IDF(bookLib,files,query)
    test_query.tf_idf_scoring()

    print(test_query.terms_score)
    print(test_query.sorted_terms_score)
    test_query.pracentage_score()
    test_query.sort_values()
    print(test_query.TF_dic)



    print(test_query.terms_score)
    print(test_query.sorted_terms_score)