from django.core.files.base import ContentFile

from numpy.lib import format as format_np
from .encoding import encoding
from celery import task
from .models import NN
from keras.models import model_from_json, Model
import numpy as np
import root
import os
from django.core.files.uploadedfile import UploadedFile
from keras.datasets import cifar10
from keras.datasets import mnist

@task
def train(username, nn_id):
    try:
        nn = NN.objects.get(id=nn_id)
        nn.complite = False
        nn.loosing = 100
        nn.save(update_fields=['complite', 'loosing'])
        samples = np.load(nn.samples.file)
        [[X_train, y_train], [X_test, y_test]] = samples
        json_string = nn.model_json
        (model, epochs) = encoding.create_model(json_string)

        i = 0
        dataset_c = X_train.shape[0]

        max_learning_progress = epochs * dataset_c
        # =============
        # EPOCHS
        # =============
        while i<epochs:
            # =============
            # SAVE MODEL
            # =============
            json = model.to_json()
            nn.model.delete()
            nn.model.save(nn.name, ContentFile(json), True)
            nn.save(update_fields=['model'])
            # =============
            # SAVE WEIGHTS
            # =============
            nn.save_weights(model.get_weights(), nn)
            '''
            HOW TO USE NUMPY IN KERAS
            name_npy = root.get_root() + '/media/weights/' + str(username) + '/weights_' + nn.name + '_' + str(nn.id) + '.npy'
            ww = np.load(name_npy)
            model.set_weights(ww)
            '''

            # =============
            # DATASET SIZE
            # =============
            k = 0
            while k < dataset_c:
                if NN.objects.get(id=nn_id).complite==True:
                    nn.progress = 100
                    nn.save(update_fields=['progress'])
                    print("Stop")
                    return

                data = np.expand_dims(X_train[k], axis=0)
                predict = np.expand_dims(y_train[k], axis=0)
                a = model.train_on_batch(data, predict)

                # =============
                # UPDATE PROGRESSBAR AND REMAIN
                # =============
                nn.progress = round(((k*epochs) / max_learning_progress) * 100, 2)
                nn.save(update_fields=['progress'])

                if k%100==0:
                    print("test")
                    dataset_l = int(X_test.shape[0]/10)
                    loos = 0
                    for x in range(dataset_l):
                        da = np.expand_dims(X_test[x], axis=0)
                        pr = np.expand_dims(y_test[x], axis=0)
                        p = model.predict_on_batch(da)
                        if np.argmax(p) != np.argmax(pr):
                            loos += 1
                    print(round(loos/dataset_l*100, 2))
                    nn.loosing = round(loos/dataset_l*100, 2)
                    nn.save(update_fields=['loosing'])

                k += 1

            i += 1

        nn.progress = 100
        nn.complite = True
        nn.save(update_fields=['complite','progress'])
        print('Complete')
    except Exception as e:
        print(e)
        nn.progress = 100
        nn.complite = True
        nn.save(update_fields=['complite', 'progress'])
        return

