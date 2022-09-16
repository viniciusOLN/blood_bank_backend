from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date

def age_of_user(value):
    age = (date.today() - value).days / 365
    
    return age

class MyUser(User):
    """Usuario baseado no modelo User com campos adicionais"""

    DONATOR = 'don'
    NURSE = 'nur'
    ADMIN = 'adm'
    USER_TYPES = [(DONATOR, 'donator'), (NURSE, 'nurse'), (ADMIN, 'admin')]
    
    birth_date = models.DateField('Data de Nascimento')   
    user_type = models.CharField(max_length=3, choices=USER_TYPES, default=DONATOR)
    

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
    user = models.ForeignKey(MyUser,
							 on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    cpf = models.CharField('CPF', max_length=14, unique=False, blank=True, null=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    telephone1 = models.CharField(max_length=11)
    telephone2 = models.CharField(max_length=11, null=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE)

class Nurse(models.Model):
    user = models.ForeignKey(MyUser,
							 on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
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

    def validate(self):
        for exam in self.exams_set.all():
            if exam.state_exam != Exams.EXAM_VALID:
                return False
        return True


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
