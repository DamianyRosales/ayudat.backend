from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.auth.hashers import make_password

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Usuario debe tener email.')
        
        #user = User.objects.create(email=email,password = make_password(password))

        user = self.model(email=self.normalize_email(email), password=make_password(password))
        # user.set_password(make_password(password))
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserBase(AbstractBaseUser):
    
    email = models.EmailField(max_length=255, unique=True,null=True,blank=True)

    fname = models.CharField(max_length=30, null=True,blank=True)
    lname = models.CharField(max_length=30, null=True,blank=True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True

    def get_full_name(self):
        # Get full name
        return self.fname + ' ' + self.lname
    
    def get_short_name(self):
        # Get only the first name (for design purposes)
        return self.fname

    def __str__(self):
        return self.email


class Admin(UserBase):
    userType = models.SmallIntegerField(default=0)
    pass


class Mod(UserBase):
    userType = models.SmallIntegerField(default=1)
    # Phone number must be entered in the format: '+999999999'. 
    # Up to 15 digits allowed.
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="")
    phone = models.CharField(db_column='PHONE',validators=[phone_validator], 
                             max_length=17, blank=True, null=True)

    objects = UserProfileManager()

class Professional(UserBase):
    userType = models.SmallIntegerField(default=2)
    # CURP field 18 characters as max length
    curp_validator = RegexValidator(regex=r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$', message="")
    curp = models.CharField(max_length=18, unique=True,validators=[curp_validator], blank=True, null=True)

    # Phone number must be entered in the format: '+999999999'. 
    # Up to 15 digits allowed.
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="")
    phone = models.CharField(db_column='PHONE',validators=[phone_validator], 
                             max_length=17, blank=True,null=True)
    
    #FILE_DIR = 'documents/'+str(id)
    FILE_DIR = 'cedulas/'
    FILE_DIR2 = 'profiles/'
    
    # Cedula profesional
    document1 = models.FileField(db_column='EVIDENCE',upload_to=FILE_DIR, null=True, max_length=255, blank=True)
    
    # Professional Picture
    document2 = models.FileField(db_column='PIC',upload_to=FILE_DIR2,  max_length=255, null=True,blank=True)

    schedule = models.CharField(db_column='SCHEDULE', max_length=255, null=True)

    is_accepted = models.BooleanField(default=False)
    objects = UserProfileManager()
    def __str__(self):
        return self.fname + ' ' + self.lname + '('+self.email+')'
    

class Patient(UserBase):
    userType = models.SmallIntegerField(default=3)
    phoneregex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="")
    phone = models.CharField(db_column='PHONE',validators=[phoneregex], 
                             max_length=17, blank=True, null=True)

    description = models.TextField(db_column='DESCRIPTION',max_length=500, null=True)
    objects = UserProfileManager()
    def __str__(self):
        return self.fname + ' ' + self.lname + '('+self.email+')'


# @receiver(post_save,sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender,instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)