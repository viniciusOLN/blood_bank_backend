from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from cpf_field.models import CPFField
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    DONATOR = 'don'
    NURSE = 'nur'
    ADMIN = 'adm'

    USER_TYPES = [(DONATOR, 'donator'), (NURSE, 'nurse'), (ADMIN, 'admin')]

    USERNAME_FIELD = 'email'

    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    cpf = CPFField(max_length=11)
    user_type = models.CharField(max_length=3, choices=USER_TYPES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


class Donator(models.Model):
    BLOOD_A_POSITIVE = 'a+'
    BLOOD_A_NEGATIVE = 'a-'
    BLOOD_B_POSITIVE = 'b+'
    BLOOD_B_NEGATIVE = 'b-'
    BLOOD_AB_POSITIVE = 'ab+'
    BLOOD_AB_NEGATIVE = 'ab-'
    BLOOD_O_POSITIVE = 'o+'
    BLOOD_O_NEGATIVE = 'o-'

    BLOOD_TYPE = [
        (BLOOD_A_POSITIVE, 'A positive'),
        (BLOOD_A_NEGATIVE, 'A negative'),
        (BLOOD_B_POSITIVE, 'B positive'),
        (BLOOD_B_NEGATIVE, 'B negative'),
        (BLOOD_AB_POSITIVE, 'AB positive'),
        (BLOOD_AB_NEGATIVE, 'AB negative'),
        (BLOOD_O_POSITIVE, 'O positive'),
        (BLOOD_O_NEGATIVE, 'O negative'),
    ]

    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    telephone1 = models.CharField(max_length=11)
    telephone2 = models.CharField(max_length=11, null=True)
    birth_date = models.DateField()


class Nurse(models.Model):
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    telephone1 = models.CharField(max_length=11)
    telephone2 = models.CharField(max_length=11, null=True)


class Address(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    number = models.IntegerField(null=True)
    reference_point = models.CharField(max_length=50)


class Allergies(models.Model):
    RESPIRATORY_ALLERGIES = 'res'
    SKIN_ALLERGIES = 'ski'
    EYE_ALLERGIES = 'eye'
    FOOD_ALLERGIES = 'foo'
    DRUG_ALLERGIES = 'dru'

    ALLERGY_CATEGORIES = [
        (RESPIRATORY_ALLERGIES, 'respiratory allergies'),
        (SKIN_ALLERGIES, 'skin allergies'),
        (EYE_ALLERGIES, 'eye allergies'),
        (FOOD_ALLERGIES, 'food allergies'),
        (DRUG_ALLERGIES, 'drug allergies'),
    ]

    donator = models.ForeignKey(Donator, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=3, choices=ALLERGY_CATEGORIES)
    subject = models.CharField(max_length=30)


class Donation(models.Model):
    date = models.DateField(auto_now_add=True)
    local = models.CharField(max_length=100)
    real_weight = models.FloatField()
    temperature = models.FloatField()
    serial_number_collection_bag = models.ForeignKey(
        'CollectionBags', on_delete=models.CASCADE, null=False
    )
    test_tube = models.ForeignKey(
        'Tubes', on_delete=models.CASCADE, null=False
    )
    donator = models.ForeignKey(Donator, on_delete=models.CASCADE, null=False)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, null=False)
    entry_time = models.DateTimeField()
    exit_time = models.DateField()

    # validate exams related to this donation. (implement later)
    def validate(self):
        pass


class Tubes(models.Model):
    num_tube = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.num_tube = uuid.uuid4()
        super().save(*args, **kwargs)


class CollectionBags(models.Model):
    num_bag = models.SlugField(max_length=100, unique=True, default='123')

    def save(self, *args, **kwargs):
        self.num_bag = uuid.uuid4()
        super().save(*args, **kwargs)


class Exams(models.Model):
    EXAM_VALID = 'y'
    EXAM_NOT_VALID = 'n'
    EXAM_WAITING = 'w'

    STATE_EXAM = [
        (EXAM_VALID, 'exam valid'),
        (EXAM_NOT_VALID, 'exam not valid'),
        (EXAM_WAITING, 'waiting exam result'),
    ]
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    donation = models.ForeignKey(
        Donation, on_delete=models.CASCADE, null=False
    )
    state_exam = models.CharField(max_length=3, choices=STATE_EXAM)
