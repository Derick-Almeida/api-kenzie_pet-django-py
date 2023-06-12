from rest_framework import serializers

from animals.exceptions import NonUpdatableKeyError
from .models import AnimalsSex, Animal
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from groups.models import Group
from traits.models import Trait


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=AnimalsSex.choices,
        default=AnimalsSex.OTHER,
    )
    age_in_human_years = serializers.SerializerMethodField()

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, obj: Animal) -> str:
        return obj.convert_dog_age_to_human_years()

    def create(self, validated_data: dict) -> Animal:
        group_data = validated_data.pop("group")
        traits_data = validated_data.pop("traits")

        group = Group.objects.get_or_create(**group_data)
        animal = Animal.objects.create(**{**validated_data, "group": group[0]})

        for trait in traits_data:
            new_trait = Trait.objects.get_or_create(**trait)
            animal.traits.add(new_trait[0])

        return animal

    def update(self, instance: Animal, validated_data: dict) -> Animal:
        forbidden_keys = ["sex", "group", "traits"]
        errors = {}

        for key, value in validated_data.items():
            if key in forbidden_keys:
                errors[key] = f"You can not update {key} property."
            else:
                setattr(instance, key, value)

        if bool(errors):
            raise NonUpdatableKeyError(errors)

        instance.save()

        return instance
