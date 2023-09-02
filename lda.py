import re
import gensim
from gensim import corpora, models
from konlpy.tag import Mecab

class TopicAnalyzer:
    def __init__(self):
        self.mecab = Mecab()
        self.stop_words = ['것', '의', '에', '에서', '을', '를', '이', '가', '에게', '한테', '와', '과', '과 같은', '은', '는', '라는', '들의', '조차', '따위의', '도', '만', '까지', '부터', '까지만', '마저', '조차', '든지', '나', '니', '다가', '든지', '이라도', '이나', '이든지', '이라고', '이며', '이든가', '이라며', '이든가', '이야말로', '이어서', '인가', '일지라도', '일까', '지말고', '지마', '처럼', '커녕', '한테', '하고', '하면서', '하면서도', '해서', '해도']

    def analyze_text(self, documents):
        texts = []
        for doc in documents:
            nouns = self.mecab.nouns(doc)
            for noun in nouns:
                raw = noun.lower()
                tokens = re.findall(r'\w+', raw)
                stopped_tokens = [t for t in tokens if not t in self.stop_words]
                texts.append(stopped_tokens)

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)

        lda_model = gensim.models.ldamodel.LdaModel(corpus=tfidf[corpus], id2word=dictionary, num_topics=1, passes=10)

        topics = lda_model.print_topics(num_words=4)
        result = []
        for topic_num, topic in topics:
            words = [re.sub(r'[^a-zA-Z가-힣0-9\s]', '', word.split("*")[1]).strip() for word in topic.split("+") if word.split("*")[1].strip() != ""]
            result.append(', '.join(words))

        return result
