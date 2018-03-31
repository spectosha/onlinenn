from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension
# Create your models here.

class NN(models.Model):

	name = models.CharField(max_length=120)
	epochs = models.IntegerField(default=1)
	loosing = models.FloatField(null=True)
	progress = models.FloatField(null=True)
	date = models.TimeField(null=True)
	remain = models.TimeField(null=True)
	model_json = models.FileField(null=True, upload_to='media/models',)
	samples = models.FileField(null=True, upload_to='media/samples', validators=[validate_file_extension])
	weights = models.FileField(null=True, upload_to='media/weights',)
	complite = models.BooleanField(default=False)
	id_user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % (self.name)

	class Meta:
		db_table = 'NN'
		verbose_name = 'Neural network'
		verbose_name_plural = 'Neural networks'
