# config_field


## Requirements

* Python (3.6, 3.7)
* Django (1.11, 2.0, 2.1, 2.2)
* Django Rest Framework >= 3.8.2

## Installation

Install using `pip`...

    pip install config_field

## How to use

```python

# models
class Author(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)


# in shell
Author.objects.create(name='John Doe')
Book.objects.create(name='Fisrt Book', description='some words', author=Author.objects.first())


# serializers.py
from rest_framework import serializers
from config_field import ConfigSerializerMethodField
from .models import Book
```

### default serializer with SerializerMethodField
```
class BookSerialzier(serializers.ModelSerializer):
    author_first_name = serializers.SerializerMethodField()
    author_last_name = serializers.SerializerMethodField()
    author_country = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            'title',
            'description',
            'full_info',
            'author_first_name',
            'author_last_name',
            'author_country',
        )

    def get_author_country(self, obj):
        if obj.author:
            return obj.country
        return 'none'


    def get_author_first_name(self, obj):
        if obj.author:
            return obj.name.split(' ')[0]
        return 'none'

    
    def get_author_last_name(self, obj):
        if obj.author:
            return obj.name.split(' ')[1]
        return 'none'
            
    def get_title(self, obj):
        if obj.name:
            return obj.name
        return 'some book'
        
    def get_full_info(self, obj):
        if obj.name and obj.description:
            return " ".join(obj.name, obj.description)
        return 'none'
```

### rewrite with ConfigSerializerMethodField
```
class ConfigBookSerializer(serializers.ModelSerializer):
    author_country = ConfigSerializerMethodField(relation_field='author', get_field='county') # get author county field
    
    # get name field from model author with splitting by " " and get 0 index
    author_first_name = ConfigSerializerMethodField(relation_field='author', get_field='name', split_value=" ", split_index=0)
    
    # get name field from model author with splitting by " " and get 0 index
    author_last_name = ConfigSerializerMethodField(relation_field='author', get_field='name', split_value=" ", split_index=1)
    
    # get same object's attribute and change default value('some book') or attribute key('title')
    title = ConfigSerializerMethodField(get_field='name', default_value='some_book')
    
    # get same object's attributes and join them
    full_info = ConfigSerializerMethodField(get_field=['name', 'description'])
```

## params
* relation_field - relation field(author), can be None, if not specified - refers to initial object(deprecated)
* get_field - object's field, can't be None
* split_value -  value for splitting CharFields, can be None
* split_index -  index for split value, cant be None if split_value exists
* to_lower - if True and isinstance value = str, return value in lowercase
* to_capitalize - if True and isinstance value = str, return value in Capitalize
* to_upper - if True and isinstance value = str, return value in uppercase
* default - default 'none', if allow_empty=False or allow_null=True, return default_value
* allow_null - default False


## changelog
* version 0.2.1 (remove allow_empty, default_value params, relatrion_field param - deprecated)