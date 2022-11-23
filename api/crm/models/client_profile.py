"""Client Profile."""

from django.db import models 
from .utils import ModelApi 
from .users import User

class ProfileClient(ModelApi):
    title = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=200, default='ligth', blank=True, null=True)
    token_service = models.CharField(max_length=400, blank=True, null= True)
    code_dga_site = models.CharField(max_length=1200, blank=True, null=True)
    d1 = models.CharField(max_length=100, blank=True, null= True)
    d2 = models.CharField(max_length=100, blank=True, null= True)
    d3 = models.CharField(max_length=100, blank=True, null= True)
    d4 = models.CharField(max_length=100, blank=True, null= True)
    d5 = models.CharField(max_length=100, blank=True, null= True)
    d6 = models.CharField(max_length=100, blank=True, null= True)
    scale = models.IntegerField(blank=True, null= True)
    in1 = models.BooleanField(blank=True, default=True)
    in2 = models.BooleanField(blank=True, default=True)
    in3 = models.BooleanField(blank=True, default=True)
    in4 = models.BooleanField(blank=True, default=True)
    in5 = models.BooleanField(blank=True, default=True)
    in6 = models.BooleanField(blank=True, default=True)
    others_ind = models.BooleanField(blank=True, default=False)
    qr_dga = models.ImageField(blank=True, null=True)
    is_apr = models.BooleanField(blank=True, null=True, default=False)
    is_dga = models.BooleanField(blank=True, null=True)


    def __str__(self):
        return str(('{} - {}').format(self.title, self.user))

class VariableClient(ModelApi):
    profile = models.ForeignKey(ProfileClient, related_name='variable_profile', on_delete=models.CASCADE)
    str_variable = models.CharField(max_length=400)
    type_variable = models.CharField(max_length=1200)

    def __str__(self):
        return str(self.profile)

class RegisterPersons(ModelApi):
    profile = models.ForeignKey(ProfileClient, blank=True, null=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=300, blank=True, null= True)
    email = models.CharField(max_length=300, blank=True, null= True)
    phone = models.CharField(max_length=300, blank=True, null= True)

    def __str__(self):
        return str(self.name)


class DataHistoryFact(ModelApi):
    profile = models.ForeignKey(ProfileClient, blank=True, null=True, on_delete=models.CASCADE)
    month = models.CharField(max_length=300, blank=True, null=True)
    production = models.IntegerField(null=True, blank=True)
    billing = models.IntegerField(null=True, blank=True)
    constant_a = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.profile)



