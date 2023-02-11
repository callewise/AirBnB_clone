#!/usr/bin/python3
"""A base class with common methods/attributes
for other classes
"""

import uuid
from datetime import datetime, time, date
from models import storage


class BaseModel:

    """Class from which all other classes will inherit
    BaseModel that defines all common attributes/methods for other classes
    PUBLIC INSTANCE ATTRIBUTES:
    id: string - assign with an uuid when an instance is created
        uuid.uuid4(): generate a unique id but cant forget to
        convert to string. The goal is to have a unique id for each BaseMode
    created_at:  datetime - assign with the current datetime when an instance
                 is created
    updated_at: datetime - assign with the current datetime when an instance
            is created and it will be updated every time you change your
            object
    __str__: should print: [<class name>] (<self.id>) <self.__dict__>
    PUBLIC INSTANCE METHODS
    save(self):
    to_dict(self):
    """

    def __init__(self, *args, **kwargs):
        """Initializes instance attributes

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns official string representation"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute updated_at
        with the current datetime
        """

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""

        new_dict = self.__dict__.copy()
        new_dict.update({
            "__class__": self.__class__.__name__,
            "updated_at": self.updated_at.isoformat(),
            "created_at": self.created_at.isoformat()
            })
        return new_dict
