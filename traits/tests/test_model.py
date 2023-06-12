from django.test import TestCase
from django.core.exceptions import ValidationError

from traits.models import Trait


class TraitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.trait_data = {"name": "Peludo"}
        cls.trait = Trait.objects.create(**cls.trait_data)

    def test_name_max_length(self):
        """Verifica a propriedade max_length de `name`"""

        expected = 20
        result = Trait._meta.get_field("name").max_length
        msg = f"Verifique se a propriedade `max_length` de name foi definida como {expected}"

        self.assertEqual(expected, result, msg)

    def test_unique_name(self):
        """Verifica se o `name` já existe"""

        trait = Trait(**self.trait_data)
        msg = f"Trait with this Name already exists."

        with self.assertRaisesMessage(ValidationError, msg):
            trait.full_clean()

    def test_trait_fields(self):
        """Verifica se os campos foram preenchidos corretamente"""

        msg_name = "Verifique se os valores do campo `name` estão corretos"

        self.assertEqual(self.trait.name, self.trait_data["name"], msg_name)
