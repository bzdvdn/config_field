# config_field


# Requirements

* Python (3.6, 3.7)
* Django (1.11, 2.0, 2.1, 2.2)
* Django Rest Framework >= 3.8.2

# Installation

Install using `pip`...

	pip install config_field

# How to use

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
Author.obejcts.create(name='John Doe')
Book.objects.create(name='Fisrt Book', description='some words', author=Author.objects.first())


# serializers.py
from rest_framework import serializers
from config_field import ConfigSerializerMethodField
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    # get name field from modle author with splitting by " " and get 0 index
    author_first_name = ConfigSerializerMethodField(relation_field='author', get_field='name', split_value=" ", split_index=0)
	# get name field from modle author with splitting by " " and get 0 index
	author_last_name = ConfigSerializerMethodField(relation_field='author', get_field='name', split_value=" ", split_index=1)
	author_country = ConfigSerializerMethodField(relation_field='author', get_field='county') # get author county field

    class Meta:
        model = Book
		fields = (
			'name',
			'description',
			'author_first_name',
			'author_last_name',
			'author_country',
		)
```

# params
* relation_field - relation field(author), can be None
* get_field - object field, can't be None
* split_value -  value for splitting ChaFields, can be None
* split_index -  index for split value, cant be None if split_value exits
* allow_empty - default True
* default_value - default 'none', if allow_empty=False, return default_value
