# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Proppy Core ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

from .props import Property


class Proppy:
    """In order to use properties, a class must extend this class

    Note:
        Since this is a normal class you can use it with multiple inheritance.
        You are free to extend `Proppy` *and* other classes as well. Keep in mind,
        the typical rules of multiple inheritance in Python still apply.

    """

    @classmethod
    def __process_propname(cls, propname):
        assert isinstance(propname, str)
        assert propname.endswith('_prop') or propname.endswith('__prop')
        if propname.endswith('__prop'):
            return propname[:-6]
        else:
            return propname[:-5]

    def __init__(self):
        """Initialize properties.

        Iterates through `__dict__` to find all the properties
        defined in this class. Then, creates instance instance
        level variables for each one.
        """
        d = dict(self.__class__.__dict__)
        print(str(d))
        for name, attr in d.items():
            if isinstance(attr, Property):
                instance_propname = Proppy.__process_propname(name)

                initializer = attr.make_property_init(instance_propname)

                initializer(self)

                getter = attr.make_getter(instance_propname)
                setter = attr.make_setter(instance_propname)

                setattr(self, instance_propname + '__getter', getter)
                setattr(self, instance_propname + '__setter', setter)

                getter = getattr(self, instance_propname + '__getter')
                setter = getattr(self, instance_propname + '__setter')
                setattr(
                    self.__class__, instance_propname,
                    property(getter, setter)
                )
