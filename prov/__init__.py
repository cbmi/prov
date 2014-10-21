__author__ = 'Trung Dong Huynh'
__email__ = 'trungdong@donggiang.com'
__version__ = '1.1.0'

__all__ = ["Error", "model", "read"]


class Error(Exception):
    """Base class for all errors in this package."""
    pass


class Serializer(object):
    def __init__(self, document=None):
        self.document = document

    def serialize(self, stream, **kwargs):
        """
        Abstract method for serializing
        """

    def deserialize(self, stream, **kwargs):
        """
        Abstract method for deserializing
        """


def read(source, format=None):
    """
    Convenience function returning a ProvDocument instance.

    It does a lazy format detection by simply using try/except for all known
    formats. The deserializers should fail fairly early when data of the
    wrong type is passed to them thus the try/except is likely cheap. One
    could of course also do some more advanced format autodetection but I am
    not sure that is necessary.

    The downside is that no proper error messages will be produced, use the
    format parameter to get the actual traceback.
    """
    # Lazy imports to not globber the namespace.
    from prov.model import ProvDocument

    from prov.serializers import Registry
    Registry.load_serializers()
    serializers = list(Registry.serializers.keys())

    if format:
        return ProvDocument.deserialize(source=source, format=format.lower())

    for format in serializers:
        try:
            return ProvDocument.deserialize(source=source, format=format)
        except:
            pass
    else:
        raise TypeError("Could not read from the source. To get a proper "
                        "error message, specify the format with the 'format' "
                        "parameter.")
