#   shtub - shell command stub
#   Copyright (C) 2012 Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    this module provides the class Execution, which represents a call to the
    command stub.
"""

__author__ = 'Alexander Metzner, Michael Gruber, Udo Juettner'


class Execution (object):
    """
        Represents the parameters of a call to the command stub.
    """
    
    def __init__ (self, command, arguments, stdin):
        """
            initializes a new execution with the given properties.
            If arguments is not given it will be initialized as empty list.
        """
        
        self.command   = command
        self.arguments = arguments or []
        self.stdin     = stdin
    
    
    def as_dictionary (self):
        """
            returns a dictionary representation of the execution.
        """
        
        return {'command'   : self.command,
                'arguments' : self.arguments,
                'stdin'     : self.stdin}
    
    
    def fulfills (self, expectation):
        """
            tests if the execution fulfills the given expectation by comparing
            the command, the input from stdin and if at least the arguments
            of the expectation are given.
        """
        
        if self.command != expectation.command:
            return False
        
        if expectation.stdin != self.stdin:
            return False
        
        for argument in expectation.arguments:
            if argument not in self.arguments:
                return False
        
        return True


    def __eq__ (self, other):
        """
            returns True if the given execution has exactly the same properties.
        """
        
        return   self.command == other.command \
           and     self.stdin == other.stdin \
           and self.arguments == other.arguments

    
    def __ne__ (self, other):
        """
            returns True when __eq__ returns False or False when __eq__ returns
            True. 
        """
        
        return not(self == other)

    
    def __str__ (self):
        """
            returns a string representation using as_dictionary.
        """
        
        return 'Execution %s' % (self.as_dictionary())

    
    @staticmethod
    def from_dictionary (dictionary):
        """
            returns a new execution object with the properties from the given
            dictionary.
        """
        
        return Execution(dictionary['command'],
                         dictionary['arguments'],
                         dictionary['stdin'])
