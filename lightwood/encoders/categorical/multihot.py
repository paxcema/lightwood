import torch
from lightwood.encoders import BaseEncoder
from sklearn.preprocessing import MultiLabelBinarizer


class MultihotEncoder(BaseEncoder):
    def __init__(self, is_target=False):
        super().__init__(is_target)
        self.max_words_per_sent = None
        self.binarizer = MultiLabelBinarizer()

    def combine_vectors(self, vectors):
        category_counts = torch.sum(vectors, axis=0)
        return category_counts

    def prepare_encoder(self, column_data, max_dimensions=100):
        self.binarizer.fit(column_data)
        self._prepared = True

    def encode(self, column_data):
        data_array = self.binarizer.transform(column_data)
        return self._pytorch_wrapper(data_array)

    def decode(self, vectors):
        words_tuples = self.binarizer.inverse_transform(vectors)
        return [list(w) for w in words_tuples]
