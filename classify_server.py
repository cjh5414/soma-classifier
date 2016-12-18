
# coding: utf-8

# In[ ]:




# In[ ]:

from sklearn.externals import joblib


# In[ ]:

clf = joblib.load('classify.model')
cate_dict = joblib.load('cate_dict.dat')
vectorizer = joblib.load('vectorizer.dat')


# In[ ]:

joblib.dump(clf,'n_classify.model')


# In[ ]:

joblib.dump(cate_dict,'n_cate_dict.dat')
joblib.dump(vectorizer,'n_vectorizer.dat')


# In[ ]:

cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))


# In[ ]:

pred = clf.predict(vectorizer.transform(['[신한카드5%할인][서우한복] 아동한복 여자아동 금나래 (분홍)']))[0]
print cate_id_name_dict[pred]


# In[ ]:

from bottle import route, run, template,request,get, post

import time
from threading import  Condition
from konlpy.tag import Twitter
twitter = Twitter()

_CONDITION = Condition()
@route('/classify')
def classify():
    img = request.GET.get('img','')
    name = request.GET.get('name', '')
    
    # 형태소
    nl_list = twitter.morphs(name.decode('utf-8'))


    def removeWord(word_list):
        i=0
        while i < len(word_list) :
            word = word_list[i]
            if (u"대행" in word
                or u"환불" in word
                or u"최저" in word
                or u"해외" in word
                or u"구매" in word
                or u"즉시" in word
                or u"할인" in word
                or u"쿠폰" in word
                #or u"포함" in word
                #or u"직구" in word
                #or u"정품" in word
                #or u"대리점" in word
                or u"수입" in word
                #or u"서비스" in word
                or u"최저가" in word
                or u"전문" in word
                #or u"국산" in word
                or u"빠른" in word
                or u"배송" in word
                or u"판매" in word
                or u"형" in word
                or u"무료" in word
                or u"친절" in word):
                    word_list.remove(word)
                    i -= 1
            i += 1
            return word_list
    
    nl_list = removeWord(nl_list)    


    def filtSpecialCh(filt_str):
        filt_str = filt_str.replace("(", "")
        filt_str = filt_str.replace(")", "")
        filt_str = filt_str.replace("]", "")
        filt_str = filt_str.replace("[", "")
        filt_str = filt_str.replace("}", "")
        filt_str = filt_str.replace("{", "")
        filt_str = filt_str.replace(":", "")
        filt_str = filt_str.replace("-", "")
        filt_str = filt_str.replace("~", "")
        filt_str = filt_str.replace("/", "")
        filt_str = filt_str.replace("+", "")
        filt_str = filt_str.replace(".", "")
        filt_str = filt_str.replace(u"▶", "")
        filt_str = filt_str.replace(u"◀", "")
        filt_str = filt_str.replace(u"★", "")
        filt_str = filt_str.replace(u"♥", "")
        filt_str = filt_str.replace("!", "")
        filt_str = filt_str.replace("^", "")
        filt_str = filt_str.replace("%", "")
        filt_str = filt_str.replace(u"━", "")
        return filt_str
           
    nl_str = " " + " ".join(nl_list)
    
    nl_str = filtSpecialCh(nl_str)
    
    
    """
    # n-gram 
    import re
    p = re.compile('[^ ㄱ-ㅣ가-힣]+')
    re_str = p.sub('',name + nl_str) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
    re_result = re_str.split(" ")
    """
    
    bi_name = ""
    tri_name = ""

    
    re_result = filtSpecialCh(name).split(" ")
    
    for word in re_result:
        word_list = list(word.decode('utf-8'))
        bi_result = zip(word_list, word_list[1:])
        for i in range(0, len(bi_result)):
            bi_name += " " + "".join(bi_result[i])
        tri_result = zip(*[word_list[i:] for i in range(3)])
        for i in range(0, len(tri_result)):
            tri_name += " " + "".join(tri_result[i])

    print name.decode('utf-8') + nl_str + bi_name + tri_name
    pred = clf.predict(vectorizer.transform([name.decode('utf-8') + nl_str + bi_name + tri_name]))[0]
    return {'cate':cate_id_name_dict[pred]}

run(host='0.0.0.0', port=8887)


#  * 추후 여기 docker 에서 뭔가 python package 설치할게 있으면 
#  * /opt/conda/bin/pip2 install bottle 이런식으로 설치 가능

# In[ ]:




# In[ ]:



