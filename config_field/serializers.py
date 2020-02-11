from rest_framework.serializers import Field


class ConfigSerializerMethodField(Field):
    """
    class Book(models.Model):
        name = 'test'
        desc = 'desc'

    class ExampleSerializer(self):
        book_name = ConfigSerializerMethodField(relation_field='book', get_field='name') (return "book_name": "test")
        full_data = ConfigSerializerMethodField(relation_field='book', get_field=['name', 'desc']) (return "book_name": "test desc")
    """

    def __init__(self, relation_field=None, get_field=None, split_value=None, split_index=None, to_lower=False,
                 to_capitalize=False, to_upper=False, to_strip=False, default='none', allow_null=False, ** kwargs):
        self.relation_field = relation_field  # deprecated
        self.get_field = get_field
        self.split_value = split_value
        self.split_index = split_index
        self.allow_null = allow_null
        self.default = default
        self.to_lower = to_lower
        self.to_strip = to_strip
        self.to_capitalize = to_capitalize
        self.to_upper = to_upper
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super(ConfigSerializerMethodField, self).__init__(**kwargs)

    def bind(self, field_name, parent):
        super(ConfigSerializerMethodField, self).bind(field_name, parent)

    def ensure_obj(self, obj):
        if isinstance(obj, dict):
            return self._create_dict_value(obj)

        if self.relation_field:
            try:
                obj = getattr(obj, self.relation_field)
            except AttributeError:
                return self.default
        if not obj:
            return self.default

        return self._create_model_value(obj)

    def _create_dict_value(self, obj):
        attr = None
        if '.' in self.get_field:
            return self.__split_by_pointer_value(obj)
        if isinstance(self.get_field, str):
            attr = obj.get(self.get_field)
        elif isinstance(self.get_field, list):
            values = [obj[field] for field in self.get_field if obj.get(field)]
            attr = " ".join(str(v) for v in values if v)
        if not attr and not self.allow_null:
            return self.default

        if self.split_value:
            return self.get_split(attr)

        return attr

    def __parse_dict_value(self, field, obj):
        attr = None
        if isinstance(field, str):
            attr = obj.get(field)
        if not attr and not self.allow_null:
            return self.default

        if self.split_value:
            return self.get_split(attr)

        return attr

    def __split_by_pointer_value(self, obj):
        attrs = self.get_field.split('.')
        data = None
        for attr in attrs:
            if isinstance(data, dict):
                obj = self.__parse_dict_value(attr, obj)
            else:
                obj = getattr(obj, attr)
            data = obj
        return data

    def _create_model_value(self, obj):
        attr = None
        if '.' in self.get_field:
            return self.__split_by_pointer_value(obj)
        if isinstance(self.get_field, str):
            attr = getattr(obj, self.get_field, self.default)
        elif isinstance(self.get_field, list):
            values = [getattr(obj, field, self.default) for field in self.get_field]
            attr = " ".join(str(v) for v in values if v)
        if not attr and not self.allow_null:
            return self.default

        if self.split_value:
            return self.get_split(attr)

        return attr

    def get_split(self, value):
        splitted = value.split(self.split_value)
        try:
            return splitted[self.split_index]
        except (TypeError, IndexError, ValueError):
            return self.default if not self.allow_null else None

    def _change_string(self, data: str) -> str:
        if self.to_lower:
            data = data.lower()
        elif self.to_capitalize:
            data = data.capitalize()
        elif self.to_upper:
            data = data.upper()
        if self.to_strip:
            data = data.strip()
        return data

    def to_representation(self, value):
        data = self.ensure_obj(value)
        if isinstance(data, str):
            return self._change_string(data)
        return data
