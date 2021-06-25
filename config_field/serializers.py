from rest_framework.serializers import Field

from .utils import remove_unacceptable_chars, REGEX_PATTERN_VALUES


class ConfigSerializerMethodField(Field):
    """
    class Book(models.Model):
        name = 'test'
        desc = 'desc'

    class ExampleSerializer(self):
        book_name = ConfigSerializerMethodField(relation_field='book', get_field='name') (return 'book_name': 'test')
        full_data = ConfigSerializerMethodField(relation_field='book', get_field=['name', 'desc']) (return 'book_name': 'test desc')
    """

    def __init__(
        self,
        get_field=None,
        split_value=None,
        split_index=None,
        to_lower=False,
        to_capitalize=False,
        to_upper=False,
        to_strip=False,
        default='none',
        allow_null=False,
        remove_unacceptable_chars=False,
        remove_pattern=REGEX_PATTERN_VALUES,
        **kwargs
    ):
        self.get_field = get_field
        self.split_value = split_value
        self.split_index = split_index
        self.allow_null = allow_null
        self.default_value = default
        self.to_lower = to_lower
        self.to_strip = to_strip
        self.to_capitalize = to_capitalize
        self.to_upper = to_upper
        self.remove_unacceptable_chars = remove_unacceptable_chars
        self.remove_pattern = remove_pattern
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super(ConfigSerializerMethodField, self).__init__(**kwargs)

    def bind(self, field_name, parent):
        super(ConfigSerializerMethodField, self).bind(field_name, parent)

    def ensure_obj(self, obj):
        if isinstance(obj, dict):
            return self._create_dict_value(obj)
        return self._create_model_value(obj)

    def _create_dict_value(self, obj):
        attr = None
        if '.' in self.get_field:
            return self.__split_by_pointer_value(self.get_field, obj)
        if isinstance(self.get_field, list):
            values = []
            for field in self.get_field:
                if '.' in field:
                    values.append(self.__split_by_pointer(field, obj))
                else:
                    values.append(obj[field]) if obj.get('field') else None
            attr = ' '.join(str(v) for v in values if v)
        elif isinstance(self.get_field, str):
            attr = obj.get(self.get_field)

        if attr is None and not self.allow_null:
            return self.default_value

        if self.split_value:
            return self.get_split(attr)

        return attr

    def __parse_dict_value(self, field, obj):
        attr = None
        if isinstance(field, str):
            attr = obj.get(field)
        if attr is None and not self.allow_null:
            return self.default_value

        if self.split_value:
            return self.get_split(attr)

        return attr

    def __split_by_pointer_value(self, field, obj):
        attrs = field.split('.')
        for attr in attrs:
            if isinstance(obj, dict):
                obj = self.__parse_dict_value(attr, obj)
            else:
                obj = getattr(obj, attr, self.default_value)
        return_data = self.default_value if not obj and not self.allow_null else obj
        if self.split_value:
            return self.get_split(return_data)
        return return_data

    def _create_model_value(self, obj):
        attr = None
        if '.' in self.get_field:
            return self.__split_by_pointer_value(self.get_field, obj)
        if isinstance(self.get_field, str):
            attr = getattr(obj, self.get_field, None)
        elif isinstance(self.get_field, list):
            values = [
                self.__split_by_pointer_value(field, obj)
                if '.' in field
                else getattr(obj, field, None)
                for field in self.get_field
            ]
            attr = ' '.join(str(v) for v in values if v)
        if attr is None and not self.allow_null:
            return self.default_value

        if self.split_value:
            return self.get_split(attr)
        return attr

    def get_split(self, value):
        splitted = value.split(self.split_value)
        try:
            return splitted[self.split_index]
        except (TypeError, IndexError, ValueError):
            return self.default_value if not self.allow_null else None

    def _change_string(self, data: str) -> str:
        if self.remove_unacceptable_chars:
            data = remove_unacceptable_chars(
                data, self.remove_pattern, self.default_value
            )
        if self.to_lower:
            data = data.lower()
        elif self.to_capitalize:
            data = data.capitalize()
        elif self.to_upper:
            data = data.upper()
        if self.to_strip:
            data = data.strip()
        return data or self.default_value

    def to_representation(self, value):
        data = self.ensure_obj(value)
        if isinstance(data, str):
            return self._change_string(data)
        return data
