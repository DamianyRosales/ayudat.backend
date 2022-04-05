from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser



class UserBase(AbstractBaseUser):
    USER_TYPE_CHOICES = (
      (0, 'admin'),
      (1, 'mod'),
      (2, 'professional'),
      (3, 'patient'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=0)

    email = models.EmailField(max_length=255, unique=True)

    fname = models.CharField(max_length=12, null=True)
    lname = models.CharField(max_length=12, null=True)
    
    def get_full_name(self):
        # Get full name
        return self.fname + ' ' + self.lname
    
    def get_short_name(self):
        # Get only the first name (for design purposes)
        return self.fname

    def __str__(self):
        return self.fname + ' ' + self.lname + '('+self.email+')'

class Admin(UserBase):
    pass

class Mod(UserBase):

    # Phone number must be entered in the format: '+999999999'. 
    # Up to 15 digits allowed.
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="")
    phone = models.CharField(db_column='PHONE',validators=[phone_validator], 
                             max_length=17, blank=True, null=True)

    # objects = UserProfileManager()


class Professional(UserBase):
    
    # CURP field 18 characters as max length
    curp_validator = RegexValidator(regex=r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$', message="")
    curp = models.CharField(max_length=18, unique=True,validators=[curp_validator], blank=True, null=True)

    # Phone number must be entered in the format: '+999999999'. 
    # Up to 15 digits allowed.
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="")
    phone = models.CharField(db_column='PHONE',validators=[phone_validator], 
                             max_length=17, blank=True,null=True)
    
    #FILE_DIR = 'documents/'+str(id)
    FILE_DIR = 'documents'

    # Cedula profesional
    document1 = models.FileField(db_column='EVIDENCE',upload_to=FILE_DIR, null=True)
    
    # Professional Picture
    document2 = models.FileField(db_column='PIC',upload_to=FILE_DIR, null=True)

    schedule = models.CharField(db_column='SCHEDULE', max_length=255, null=True)

    is_accepted = models.BooleanField(default=False)
    
    # objects = UserProfileManager()



class Patient(UserBase):

    phoneregex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="")
    phone = models.CharField(db_column='PHONE',validators=[phoneregex], 
                             max_length=17, blank=True, null=True)

    description = models.TextField(db_column='DESCRIPTION',max_length=500, null=True)
    
    # objects = UserProfileManager()
