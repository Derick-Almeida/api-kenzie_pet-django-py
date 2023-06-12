from math import log
from django.test import TestCase

from animals.models import Animal
from groups.models import Group
from traits.models import Trait


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_data = {
            "name": "Jorge",
            "age": 3,
            "weight": 30,
            "sex": "Macho",
        }
        cls.group_data = {
            "name": "cachorro",
            "scientific_name": "Canis lupus familiaris",
        }
        cls.trait_data = [{"name": "peludo"}, {"name": "médio porte"}]

        cls.group = Group.objects.create(**cls.group_data)
        cls.animal = Animal.objects.create(**{**cls.animal_data, "group": cls.group})
        cls.traits = [Trait.objects.create(**trait) for trait in cls.trait_data]
        cls.animal.traits.set(cls.traits)

    def test_name_max_length(self):
        """Verifica a propriedade max_length de `name`"""

        expected = 50
        result = Animal._meta.get_field("name").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected}"

        self.assertEqual(expected, result, msg)

    def test_sex_max_length(self):
        """Verifica a propriedade max_length de `sex`"""

        expected = 15
        result = Animal._meta.get_field("sex").max_length
        msg = f"Verifique se a propriedade `max_length` de sex foi definida como {expected}"

        self.assertEqual(expected, result, msg)

    def test_convert_dog_age_to_human_years_method(self):
        """Verificando se o método `convert_dog_age_to_human_years` retorna o esperado"""

        expected = round(16 * log(self.animal.age) + 31)
        result = self.animal.convert_dog_age_to_human_years()
        msg = "Verifique se o método `convert_dog_age_to_human_years` está retornando como esperado"

        self.assertEqual(expected, result, msg)

    def test_animal_fields(self):
        """Verifica se os campos foram preenchidos corretamente"""

        msg_name = "Verifique se os valores do campo `name` estão corretos"
        msg_age = "Verifique se os valores do campo `age` estão corretos"
        msg_weight = "Verifique se os valores do campo `weight` estão corretos"
        msg_sex = "Verifique se os valores do campo `sex` estão corretos"
        msg_group = "Verifique se os valores do campo `group` estão corretos"
        msg_trait = "Verifique se os valores do campo `trait` estão corretos"

        print(self.animal)

        self.assertEqual(self.animal.name, self.animal_data["name"], msg_name)
        self.assertEqual(self.animal.age, self.animal_data["age"], msg_age)
        self.assertEqual(self.animal.weight, self.animal_data["weight"], msg_weight)
        self.assertEqual(self.animal.sex, self.animal_data["sex"], msg_sex)
        self.assertEqual(self.group.name, self.group_data["name"], msg_group)
        self.assertEqual(
            self.group.scientific_name,
            self.group_data["scientific_name"],
            msg_group,
        )
        self.assertEqual(self.traits[0].name, self.trait_data[0]["name"], msg_trait)
        self.assertEqual(self.traits[1].name, self.trait_data[1]["name"], msg_trait)

    def test_animal_contain_unique_group(self):
        """Verificando se o `animal` possui apenas um `group`"""

        msg = "Verifique se os valores do campo `group` estão corretos"

        self.assertIs(self.group, self.animal.group, msg)

    def test_animal_contain_many_trait(self):
        """Verificando se o `animal` pode ter varias `trait`"""

        msg = "Verifique se os valores do campo `traits` estão corretos"

        for trait in self.traits:
            self.assertIn(self.animal, trait.animals.all(), msg)
