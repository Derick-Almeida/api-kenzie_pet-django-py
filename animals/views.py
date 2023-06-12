from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from .serializers import AnimalSerializer
from .models import Animal


class AnimalView(APIView):
    def post(self, req: Request) -> Response:
        serializer = AnimalSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)


class AnimalDetailView(APIView):
    def patch(self, req: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal, req.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def get(self, req: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal)

        return Response(serializer.data)

    def delete(self, req: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
