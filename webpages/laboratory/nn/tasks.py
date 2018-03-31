from celery import task
from .models import NN
from keras.models import model_from_json, Model
import numpy as np
from django.core.files.uploadedfile import UploadedFile
@task
def train(nn_id):
    nn = NN.objects.get(id=nn_id)
    json_string = nn.model_json.read()
    samples = np.load(nn.samples.file)
    (X_train, y_train), (X_test, y_test) = samples
    model = model_from_json(json_string)
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    i = 0
    epochs = nn.epochs
    max_learning_progress = epochs * X_train.shape[0]
    while i<epochs:

        k = 0
        while k < X_train.shape[0]:
            model.train_on_batch(np.expand_dims(X_train[k], axis=0), np.expand_dims(y_train[k], axis=0))
            #model.train_on_batch(X_train[k], y_train[k])

            if k%100==0:
                nn.progress = ((k*epochs) / max_learning_progress) * 100
                nn.save()

            k += 1
        i += 1

    nn.progress = 100
    nn.save()
    print('Complete')