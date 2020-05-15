from django.db import models

# Create your models here.

class dailyData(models.Model):
	stateName = models.CharField(max_length=50)
	confirmedCases = models.CharField(max_length=50)
	curedCases = models.CharField(max_length=50)
	deathCases = models.CharField(max_length=50)
	when = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.stateName+str(self.when)


class Counter(models.Model):
	count1 =  models.IntegerField()
	when = models.DateTimeField(auto_now=True)



class TestCounter(models.Model):

	tests =  models.IntegerField()
	when = models.DateTimeField(auto_now=True)

