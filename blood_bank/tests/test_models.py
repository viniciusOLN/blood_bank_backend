import uuid
from django.test import TestCase
from blood_bank.models import (
    Address,
    CollectionBags,
    Donation,
    Donator,
    Exams,
    Nurse,
    Tubes,
)
from datetime import datetime


class DonationModelTests(TestCase):
    def setUp(self):
        collection_bag = CollectionBags.objects.create(num_bag=uuid.uuid4())
        tube = Tubes.objects.create(num_tube=uuid.uuid4())
        address1 = Address.objects.create(
            city='parnaiba',
            state='piaui',
            street='rua das flores',
            neighborhood='bairro de Fátima',
            number='1024',
            reference_point='perto da mercearia do seu zé',
        )
        address2 = Address.objects.create(
            city='parnaiba',
            state='piaui',
            street='outra rua',
            neighborhood='outro bairro',
            number='1025',
            reference_point='longe da mercearia do seu zé',
        )
        donator = Donator.objects.create(
            blood_type=Donator.BLOOD_A_NEGATIVE,
            address=address1,
            telephone1='123',
            telephone2='159',
            birth_date=datetime.now(),
        )
        nurse = Nurse.objects.create(
            address=address2, telephone1='456', telephone2='789'
        )
        self.donation = Donation.objects.create(
            local='Avenida Jetulio vargas',
            real_weight=60.0,
            temperature=36.1,
            serial_number_collection_bag=collection_bag,
            test_tube=tube,
            donator=donator,
            nurse=nurse,
            entry_time=datetime.now(),
            exit_time=datetime.now(),
        )
        self.exam1 = Exams.objects.create(
            name='exam1',
            description='something',
            donation=self.donation,
            state_exam=Exams.EXAM_VALID,
        )
        self.exam2 = Exams.objects.create(
            name='exam1',
            description='something',
            donation=self.donation,
            state_exam=Exams.EXAM_VALID,
        )

    def test_validate_donation(self):
        """Validate deve retornar true porque todos os exames estão válidos"""
        self.assertTrue(self.donation.validate())  # Donation should be valid

    def test_validate_donation_should_be_false(self):
        """
        Teste validate de donation deve ser falso porque tem pelo menos um
        exame está inválido
        """
        self.exam2.state_exam = Exams.EXAM_NOT_VALID
        self.exam2.save()
        self.assertFalse(self.donation.validate())

    def test_validate_donation_with_waiting_state(self):
        self.exam2.state_exam = Exams.EXAM_WAITING
        self.exam2.save()
        self.assertFalse(self.donation.validate())
