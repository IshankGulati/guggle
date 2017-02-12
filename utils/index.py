import string


class IndexDocument(object):
    """Stores the inverted indexed document.
    """
    def __init__(self, _id, context):
        self._id = _id
        self.context = context

    def _preprocess(self):
        self.context = self.context.lower()
        self.context = self.context.translate(None, string.punctuation)

    def _create_inverted_index(self):
        self.inv_index_ = {}
        tokens = self.context.split(' ')
        for token in tokens:
            if token in self.inv_index_:
                self.inv_index_[token]['doc_freq'] += 1
            else:
                self.inv_index_[token] = {}
                self.inv_index_[token]['doc_freq'] = 1
                self.inv_index_[token]['doc_id'] = self._id

    def execute(self):
        """Create inverted index.
        """
        self._preprocess()
        self._create_inverted_index()
        return self
