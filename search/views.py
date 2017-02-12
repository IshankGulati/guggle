import math
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from django.views import View
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import HttpResponseServerError
from django.http.response import JsonResponse
from django.conf import settings

from utils.index import IndexDocument


MONGO_DB = settings.MONGO_DB
DOCUMENT_COLL = MONGO_DB.documents
INDEX_COLL = MONGO_DB.index


class IndexView(View):
    """Used to index the documents.
    """
    def post(self, request, *args, **kwargs):
        _id = request.POST.get('id', None)
        title = request.POST.get('title', None)
        data = request.POST.get('data', None)

        if _id is None or title is None or data is None:
            return HttpResponseBadRequest

        query = {'_id': _id}
        update = {
            'title': title,
            'data': data
            }
        # insert raw document in mongodb
        try:
            DOCUMENT_COLL.update(query, update, True)
        except PyMongoError:
            return HttpResponseServerError
        context = "{0} {1}".format(title, data)
        doc = IndexDocument(_id, context)
        doc.execute()
        bulk = INDEX_COLL.initialize_unordered_bulk_op()
        for term, data in doc.inv_index_.iteritems():
            query = {'term': term}
            update = {
                '$inc': {'doc_freq': data['doc_freq'], 'num_docs': 1},
                '$push': {'doc_meta': {
                    'doc_ids': data['doc_id'],
                    'term_freq': data['doc_freq']
                    }}
                }
            bulk.find(query).upsert().update_one(update)
        try:
            bulk.execute()
        except PyMongoError:
            return HttpResponseServerError
        return HttpResponse(status=200)


class SearchView(View):
    """Used to search on indexed documents.
    """
    def get(self, request, *args, **kwargs):

        def score(doc):
            "calculate score of document"
            tf = []
            idf = []
            tf_idf = []
            for token in tokens:
                tf.append(math.sqrt(tf_dict.get(doc.get('_id'), {}).get(token,
                                                                        0)))
                idf.append(1 + (math.log(total_docs / float(1 + token_dict.get(
                    token, {}).get('doc_freq', 0)))))

            tf_idf = [x*y for x, y in zip(tf, idf)]
            doc['score'] = sum(tf_idf)
            return doc

        q = request.GET.get('q', 0)
        tokens = q.split(' ')
        docs_dict = {}
        token_dict = {}
        tf_dict = {}
        try:
            total_docs = DOCUMENT_COLL.find().count()
        except PyMongoError:
            total_docs = 0
        for token in tokens:
            try:
                token_index = INDEX_COLL.find_one({'term': token})
            except PyMongoError:
                token_index = {}
            token_dict[token] = token_index
            ids = []
            for meta in token_index.get('doc_meta', {}):
                ids.append(meta.get('doc_ids'))
                if meta.get('doc_ids') not in tf_dict:
                    tf_dict[meta.get('doc_ids')] = {}
                tf_dict[meta.get('doc_ids')][token] = meta.get('term_freq')
            try:
                docs = DOCUMENT_COLL.find({'_id': {'$in': ids}})
            except PyMongoError:
                docs = []
            for doc in docs:
                docs_dict[doc.get('_id')] = doc
        if len(docs) is not 0:
            docs = sorted([score(doc) for doc in docs_dict.values()],
                          key=lambda k: k['score'], reverse=True)
        return JsonResponse(docs, safe=False)

