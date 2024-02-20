#!/usr/bin/python3
'''
    base_model.py

    Class BaseModel that defines common attributes/methods for other classes
'''


import uuid
import datetime


class BaseModel:
    '''
        Defines all common attributes/methods for other classes
    '''

    def __init__(self, *args, **kwargs):
        '''
            Initialize new instance
        '''
        date_format = '%Y-%m-%dT%H:%M:%S.%f'

        if kwargs:
            kwargs.pop('__class__', None)  # Remove __class__ from kwargs
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.datetime.strptime(
                        value, date_format))  # Convert string to datetime obj
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at

    def save(self):
        '''
            Update timestamp to the current date and time
        '''
        self.updated_at = datetime.datetime.now()

    def __str__(self):
        '''
            Returns string representation
        '''
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        '''
            Returns dictionary representation
        '''
        my_dict = self.__dict__.copy()
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        my_dict['__class__'] = type(self).__name__  # Add class name to dict

        return my_dict
