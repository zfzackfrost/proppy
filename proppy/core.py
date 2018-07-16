# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Proppy Core ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

from .props import Property
from threading import Lock


class MetaProppy(type):
    """In order to use properties, a class must use this metaclass.

    """

    @classmethod
    def __process_propname(cls, propname):
        assert isinstance(propname, str)
        assert propname.endswith('_prop') or propname.endswith('__prop')
        if propname.endswith('__prop'):
            return propname[:-6]
        else:
            return propname[:-5]

    def __new__(cls, name, bases, d):
        tmp_d = d.copy()
        d['_____prop_initializers_____'] = {}
        for name, attr in tmp_d.items():
            if isinstance(attr, Property):
                instance_propname = cls.__process_propname(name)
                initializer = attr.make_property_init(instance_propname)

                getter = attr.make_getter(instance_propname)
                setter = attr.make_setter(instance_propname)

                d[instance_propname] = property(getter, setter)
                d['_____prop_initializers_____'][instance_propname
                                                 ] = initializer

        return type.__new__(cls, name, bases, d)

    def __init__(self, name, bases, d):
        initializers = d['_____prop_initializers_____']
        for name, init in initializers.items():
            init(self)

        self._lock = Lock()
        super(object, self).__init__()
