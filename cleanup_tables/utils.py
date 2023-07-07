class CommonFileUtilsMethodsMixin(object):
    """
    Common File Utils methods
    """

    @staticmethod
    def get_basename(path):
        """
            Method to get base name
        :param path: the path of file
        :return: basename
        """
        import os
        return os.path.basename(path)

    @staticmethod
    def get_filename(filename, extension):
        """
            Returns the correct name of a file to save
        :param filename: name of a file
        :param extension: extension of a file
        :return:  (string) orrect name
        """
        filename if extension in filename else filename + extension
        return filename

    @staticmethod
    def read_file(file):
        """
            Read a file and return its content
        :param file: on Memory
        :return: ContentFile
        """
        from django.core.files.base import ContentFile
        content_file = ContentFile(file.read())
        return content_file

    @staticmethod
    def open_file(path, mode="rb"):
        """
        Open File from path
        :param path: the path from file to Open
        :param mode: the mode to read or write file
        :return: The file on Memory with the extension
        """
        extension = CommonFileUtilsMethodsMixin.get_file_extension(filename=path)
        file_to_open = open(path, mode=mode)
        return file_to_open, extension

    @staticmethod
    def get_file_extension(filename):
        """
        Get the extension from filename
        :param filename:
        :return:
        """
        return ".{0}".format(str(filename).split(".")[-1])

    @staticmethod
    def get_string_from_file(path, filename):
        """
        Get the file from the path in string mode
        :param path: the path from the file selected
        :param filename: the filename to read and return
        :return: the string with the content from the file selected
        """
        import os

        return open(os.path.join(path, filename), 'r')

    @staticmethod
    def get_base_path(filename=__file__):
        """
        Get the current base patch from File
        :param filename: the file assigned to get the current base patch
        :return: the path where the current file from module is located
        """
        import os

        return os.path.realpath(os.path.dirname(filename))

    @staticmethod
    def rename_filename_extension(filename, old_extension, new_extension):
        """
        Change extension of a file name
        :param filename: the original file name.
        :param old_extension: old extension to be replaced.
        :param new_extension: new extension to be added.
        :return: file name with the new extension.
        """
        return str(filename).replace(old_extension, new_extension)


class CommonUtilsMethodsMixin(object):
    """
    Class to share common utils methods
    """
    file = CommonFileUtilsMethodsMixin

    @staticmethod
    def get_current_date():
        """
        Get the current datetime
        :return: the current date
        """
        import datetime

        return datetime.datetime.today()

    @staticmethod
    def get_range_dates_by_days(amount):
        """
        Get the Range dates using days
        :return: the initial and final dates using the amount as days diff
        """
        import datetime
        final_date = CommonUtilsMethodsMixin.get_current_date()
        initial_date = final_date + datetime.timedelta(days=amount)

        return initial_date, final_date

    @staticmethod
    def convert_string_to_decimal(value):
        """
        Function to convert a string on Decimal value
        :param value: the string value to convert
        :return: the Decimal value converted
        """
        from decimal import Decimal, InvalidOperation

        try:
            value_str = value.strip().replace(",", '.')
            value_decimal = Decimal(value=value_str)
            return value_decimal
        except (TypeError, InvalidOperation) as err:
            raise ValueError(err)

    @staticmethod
    def convert_string_to_boolean(value):
        """
        Function to convert the string to boolean
        :param value: the string value to convert
        :return: the boolean value converted
        """
        return True if 'YES' in str(value).strip().upper() else False

    @staticmethod
    def convert_string_to_datetime(value, date_format):
        """
        Function to convert the date string to datetime object
        :param value: the string value to convert
        :param date_format: the date format used
        :return: the datetime object
        """
        import datetime

        try:
            return datetime.datetime.strptime(value, date_format)
        except (ValueError, TypeError) as err:
            raise err
