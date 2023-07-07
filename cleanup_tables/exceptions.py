class DateFormatException(Exception):
    """
    Exception to manage the error when the `clean_up_rule` does not have the right format.
    """

    def __init__(self, clean_up_rule):
        self.clean_up_rule = clean_up_rule

    def __unicode__(self):
        message = 'Date rule "{0}" does not have the right format.'.format(self.clean_up_rule)
        return message


class DateFieldTypeException(Exception):
    """
    Exception to manage the error when the `date_field` is not of the date type.
    """

    def __init__(self, field_name):
        self.field_name = field_name

    def __unicode__(self):
        message = 'Field name "{0}" is not of the date type.'.format(self.field_name)
        return message
