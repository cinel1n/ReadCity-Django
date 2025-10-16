import io
from .models import *
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import BooksModel


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksModel
        fields = ('title', 'author',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('subcategory1', 'subcategory2',)


# class BookModel:
#     def __init__(self, title, author):
#         self.title = title
#         self.author = author


# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     author = serializers.CharField()
#     price = serializers.IntegerField()
#     num_score = serializers.IntegerField()
#     category = serializers.CharField()


'''
class CategorySerializer(serializers.Serializer):
    subcategory1 = serializers.CharField(max_length=100)
    subcategory2 = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return CategoryModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.subcategory1 = validated_data.get('subcategory1', instance.subcategory1)
        instance.subcategory2 = validated_data.get('subcategory1', instance.subcategory2)

        instance.save()
        return instance


def encode():
    model = BookModel('11/22/63', 'Стивен Кинг')
    model_sr = BookSerializer(model)
    print(model_sr.data, model_sr, sep='\n')

    json = JSONRenderer().render(model_sr.data)
    print(json)


def decode():
    stream = io.BytesIO(b'{"title":"11/22/63","author":"\xd0\xa1\xd1\x82\xd0\xb8\xd0\xb2\xd0\xb5\xd0\xbd \xd0\x9a\xd0\xb8\xd0\xbd\xd0\xb3"}')
    data = JSONParser().parse(stream)
    serializer = BookSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)
'''