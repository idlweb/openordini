from adaptor.fields import CharField, BooleanField, DateField, FloatField

class OOCsvCharField(CharField):

    def __init__(self, limit=50, *args, **kwargs):
    
        if limit:
            kwargs["transform"] = lambda val: val[:limit]

        super(OOCsvCharField, self).__init__(*args, **kwargs)


class OOCsvBooleanField(BooleanField):

    def __init__(self, *args, **kwargs):
        is_true = (lambda val: (val == "1"))

        kwargs["is_true"] = is_true

        super(OOCsvBooleanField, self).__init__(*args, **kwargs)


class OOCsvDateField(DateField):
    
    def get_prep_value(self, value, instance=None):

        # catch earlier the case of null date, because the default DateField
        # does not allow it with self.default = None

        if not value and self.null:
            return self.default

        return super(OOCsvDateField, self).get_prep_value(value, instance)

class OOCsvFloatField(FloatField):
    
    def get_prep_value(self, value, instance=None):

        # catch earlier the case of null date, because the default DateField
        # does not allow it with self.default = None

        if not value and self.null:
            return self.default

        return super(OOCsvFloatField, self).get_prep_value(value, instance)
