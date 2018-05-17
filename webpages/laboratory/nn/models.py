from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension
import numpy as np
import os
import root
import onlinenn.settings as settings
from django.core.files.base import ContentFile

# Create your models here.

class NN(models.Model):

	def user_directory_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'samples/user_{0}/{1}'.format(instance.id_user, filename)

	def samples_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'samples/user_{0}/samples_{1}.npy'.format(instance.id_user, filename)

	def model_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'models/user_{0}/model_{1}.json'.format(instance.id_user, filename)

	def weights_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'weights/user_{0}/weights_{1}.npy'.format(instance.id_user, filename)

	name = models.CharField(max_length=120,default="Noname")
	epochs = models.IntegerField(default=1)
	loosing = models.FloatField(null=True)
	progress = models.FloatField(null=True)
	date = models.TimeField(null=True)
	remain = models.TimeField(null=True)
	model_json = models.TextField(null=True)
	samples = models.FileField(null=True, upload_to=samples_path, validators=[validate_file_extension])
	weights = models.FileField(null=True, upload_to=weights_path,)
	model = models.FileField(null=True, upload_to=model_path,)
	complite = models.BooleanField(default=False)
	id_user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % (self.name)

	def save_weights(self, weights, nn):
		name_npy = settings.MEDIA_ROOT + '/temp/' + str(nn.id_user) + '_' + nn.name + ".npy"
		weights = np.array(weights)
		np.save(name_npy, weights)
		fil = open(name_npy, 'rb')
		string = fil.read()
		fil.close()
		os.remove(name_npy)
		nn.weights.delete()
		nn.weights.save(nn.name, ContentFile(string), True)
		nn.save(update_fields=['weights'])

	class Meta:
		db_table = 'NN'
		verbose_name = 'Neural network'
		verbose_name_plural = 'Neural networks'
