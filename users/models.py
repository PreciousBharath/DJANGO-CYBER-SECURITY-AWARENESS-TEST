from django.db import models


# Create your models here.
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'


class TokenCountModel(models.Model):
    loginid = models.CharField(unique=True, max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'TokenCountTable'


class BlockChainTransactionModel(models.Model):
    c_index = models.CharField(max_length=100)
    c_timestamp = models.CharField(max_length=100)
    c_sender = models.CharField(max_length=100)
    c_recipient = models.CharField(max_length=100)
    c_vote = models.CharField(max_length=100)
    c_proof = models.CharField(max_length=100)
    c_previous_hash = models.CharField(max_length=100)
    p_index = models.CharField(max_length=100)
    p_timestamp = models.CharField(max_length=100)
    p_sender = models.CharField(max_length=100)
    p_recipient = models.CharField(max_length=100)
    p_vote = models.CharField(max_length=100)
    p_proof = models.CharField(max_length=100)
    p_previous_hash = models.CharField(max_length=100)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "BlockChainTransactiontable"