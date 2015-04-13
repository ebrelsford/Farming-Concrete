from itertools import groupby

from django.forms.models import ModelChoiceIterator, ModelMultipleChoiceField


class GroupedModelChoiceIterator(ModelChoiceIterator):

    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
            if self.field.cache_choices:
                if self.field.choice_cache is None:
                    self.field.choice_cache = [
                        (self.field.group_label(group),
                         [self.choice(ch) for ch in choices])
                        for group, choices in groupby(self.queryset.all(),
                                                      key=lambda row: getattr(row, self.field.group_by_field))
                    ]
                    for choice in self.field.choice_cache:
                        yield choice
        else:
            for group, choices in groupby(self.queryset.all(),
                                          key=lambda row: getattr(row, self.field.group_by_field)):
                if group is not None:
                    #Line added
                    yield (self.field.group_label(group),
                           [self.choice(ch) for ch in choices])


class GroupedModelMultipleChoiceField(ModelMultipleChoiceField):

    def __init__(self, group_by_field, group_label=None, *args, **kwargs):
        """
        group_by_field is the name of a field on the model group_label is a
        function to return a label for each choice group
        """
        super(GroupedModelMultipleChoiceField, self).__init__(*args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices 
        return GroupedModelChoiceIterator(self)

    choices = property(_get_choices, ModelMultipleChoiceField._set_choices)
