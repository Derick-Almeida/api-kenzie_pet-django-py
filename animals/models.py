from math import log
from django.db import models


class AnimalsSex(models.TextChoices):
    MALE = "Macho"
    FEMALE = "Fêmea"
    OTHER = "Não informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15,
        choices=AnimalsSex.choices,
        default=AnimalsSex.OTHER,
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="animals",
        null=True,
    )
    traits = models.ManyToManyField("traits.Trait", related_name="animals")

    def convert_dog_age_to_human_years(self):
        return round(16 * log(self.age) + 31)
