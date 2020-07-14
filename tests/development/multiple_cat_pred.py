import lightwood
import pandas as pd

from lightwood import Predictor
from lightwood.encoders.text import ShortTextEncoder
from lightwood.encoders.tags import TagsEncoder

lightwood.config.config.CONFIG.USE_CUDA = True

df = pd.read_csv("../../../datasets/mpst/mpst_full_data.csv")

df = df[['title', 'tags', 'split']]
df = df.sample(1000)
df.tags = df.tags.apply(lambda x: x.split(', '))

df_train = df[df.split == 'train'].copy()
df_test = df[df.split == 'test'].copy()
df_train = df_train.drop(['split'], axis=1)
df_test = df_test.drop(['split'], axis=1)

config = {'input_features': [
        {'name': 'title',
         'type': 'text',
         'encoder_class': ShortTextEncoder,
         'encoder_attrs': {'_combine': 'concat'}},
    ],
    'output_features': [
        {'name': 'tags', 'type': 'tags', 'encoder_class': TagsEncoder}
    ],
}
predictor = Predictor(config)


def iter_function(epoch, error, test_error, test_error_gradient, test_accuracy):
    print(
        'epoch: {iter}, error: {error}, test_error: {test_error}, test_error_gradient: {test_error_gradient}, test_accuracy: {test_accuracy}'.format(
            iter=epoch, error=error, test_error=test_error, test_error_gradient=test_error_gradient,
            accuracy=predictor.train_accuracy, test_accuracy=test_accuracy))

predictor.learn(from_data=df_train,
                callback_on_iter=iter_function,
                eval_every_x_epochs=4,
                stop_training_after_seconds=1)

# Why does it try to encode the missing column tags?
predictions = predictor.predict(when_data=df_test.drop(['tags'], axis=1))

print(predictions)
