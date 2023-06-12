from django.test import TestCase
from django.core.exceptions import ValidationError

from groups.models import Group


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.group_data = {
            "name": "cachorro",
            "scientific_name": "Canis lupus familiaris",
        }
        cls.group = Group.objects.create(**cls.group_data)

    def test_name_max_length(self):
        """Verifica as propriedades max_length de `name` e `scientific_name`"""

        expected_max_length = 20
        result = Group._meta.get_field("name").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result, msg)

    def test_scientific_name_max_length(self):
        """Verifica as propriedades max_length de `name` e `scientific_name`"""

        expected_max_length = 50
        result = Group._meta.get_field("scientific_name").max_length
        msg = f"Verifique se a propriedade `max_length` de scientific_name foi definida como {expected_max_length}"

        self.assertEqual(expected_max_length, result, msg)

    def test_unique_name(self):
        """Verifica se o `name` já existe"""

        newGroup = {
            "name": "cachorro",
            "scientific_name": "Canis lupus",
        }

        group = Group(**newGroup)
        msg = "Group with this Name already exists."

        with self.assertRaisesMessage(ValidationError, msg):
            group.full_clean()

    def test_unique_scientific_name(self):
        """Verifica as propriedades unique de `name` e `scientific_name`"""

        newGroup = {
            "name": "gato",
            "scientific_name": "Canis lupus familiaris",
        }

        group = Group(**newGroup)
        msg = "Group with this Scientific name already exists."

        with self.assertRaisesMessage(ValidationError, msg):
            group.full_clean()

    def test_group_fields(self):
        """Verifica se os campos foram preenchidos corretamente"""

        msg_name = "Verifique se os valores do campo `name` estão corretos"
        msg_scientific_name = (
            "Verifique se os valores do campo `scientific_name` estão corretos"
        )

        self.assertEqual(self.group.name, self.group_data["name"], msg_name)
        self.assertEqual(
            self.group.scientific_name,
            self.group_data["scientific_name"],
            msg_scientific_name,
        )
