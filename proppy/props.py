# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Property Types ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


class Property:
    """Base class for all properties.

    This can be used directly for simple properties
    with behaviour similar to a normal Python variable.
    In other cases (i.e. more advanced property features
    are requiered), a subclass of `Property` should be
    used.

    Note
        `Property` objects don't store any data themselves, other than
        their default value. They simply define the rules for creating,
        reading and writing a property of a given type.

    """

    def __init__(self, default_value):
        """Initialize the property.

        Arguments:
            default_value (anything): The initial value of the property

        """
        self.__default_value = default_value

    def make_property_init(self, propname):
        """Creates a function that intializes the property

        Arguments:
            propname (str): The name of the instance-level variable that the property will be accessed from

        Returns:
            callable: A function that creates the instance level variable the property with the specified property
            name. The name of the instance level variable that is created should be the value of `propname` with a
            single underscore before it. The function that is returned takes a single argument: `self`.

        """
        this = self

        def initializer(self):
            setattr(self, '_' + propname, this.__default_value)

        return initializer

    def make_getter(self, propname):
        """Creates a function that gets the property

        Arguments:
            propname (str): The name of the instance-level variable that the property is accessed from

        Returns:
            callable: A function that gets the instance level variable for the property with the specified property name.
            The name of the instance level variable that is retrieved should be the value of `propname` with a single
            underscore before it. The function that is returned takes a single argument: `self`.

        """

        def getter(self):
            return getattr(self, '_' + propname)

        return getter

    def make_setter(self, propname):
        """Creates a function that sets the property

        Arguments:
            propname (str): The name of the instance-level variable that the property is accessed from

        Returns:
            callable: A function that sets the instance level variable for the property with the specified property name.
            The name of the instance level variable that is written to should be the value of `propname` with a single
            underscore before it. The function that is returned (the setter) takes two arguments: `self` and a the new
            value.

        """

        def setter(self, value):
            setattr(self, '_' + propname, value)

        return setter


# ~~~~~~~~~~~~~~~~~~~~~~~~~~ `Property` Subclasses ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


class WriteOnceProperty(Property):
    """Property that allows only a single assignment, other than the default value.

    This property type has a getter and setter like any other property. However,
    the setter sets a flag after the first assignment that disables further changes
    to the value. Since the default value is handled separately from the setter,
    the initial value of a `WriteOnceProperty` (set in the constructor) does not
    count as the single allowed assignment.

    """

    def __init__(self, default_value):
        """Initialize the property.

        Arguments:
            default_value (anything): The initial value of the property

        """
        self.__default_value = default_value

    def make_property_init(self, propname):
        """Creates a function that intializes the property

        Arguments:
            propname (str): The name of the instance-level variable that the property will be accessed from

        Returns:
            callable: A function that creates the instance level variable the property with the specified property
            name. The name of the instance level variable that is created should be the value of `propname` with a
            single underscore before it. The function that is returned takes a single argument: `self`.

        """
        this = self

        def initializer(self):
            setattr(self, '_' + propname, this.__default_value)
            setattr(self, '_' + propname + '__written', False)

        return initializer

    def make_getter(self, propname):
        """Creates a function that gets the property

        Arguments:
            propname (str): The name of the instance-level variable that the property is accessed from

        Returns:
            callable: A function that gets the instance level variable for the property with the specified property name.
            The name of the instance level variable that is retrieved should be the value of `propname` with a single
            underscore before it. The function that is returned takes a single argument: `self`.

        """

        def getter(self):
            return getattr(self, '_' + propname)

        return getter

    def make_setter(self, propname):
        """Creates a function that sets the property

        Arguments:
            propname (str): The name of the instance-level variable that the property is accessed from

        Returns:
            callable: A function that sets the instance level variable for the property with the specified property name.
            The name of the instance level variable that is written to should be the value of `propname` with a single
            underscore before it. The function that is returned (the setter) takes two arguments: `self` and a the new
            value.

        """

        def setter(self, value):
            has_written = getattr(self, '_' + propname + '__written')
            if not has_written:
                setattr(self, '_' + propname, value)
                setattr(self, '_' + propname + '__written', True)

        return setter


