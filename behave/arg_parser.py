"""Object for parsing command line strings into Python objects.

Extends default ArgumentParser to pass validation errors to the output
"""

import sys as _sys
from argparse import ArgumentError, ArgumentParser, ArgumentTypeError
from gettext import gettext as _


class BehaveArgParser(ArgumentParser):
    def _get_value(self, action, arg_string):
        type_func = self._registry_get('type', action.type, action.type)

        if not callable(type_func):
            msg = _('%r is not callable')
            raise ArgumentError(action, msg % type_func)

        # convert the value to the appropriate type
        try:
            result = type_func(arg_string)

        # ArgumentTypeErrors indicate errors
        except ArgumentTypeError:
            name = getattr(action.type, '__name__', repr(action.type))
            msg = str(_sys.exc_info()[1])
            raise ArgumentError(action, msg)

        # TypeErrors or ValueErrors also indicate errors
        except (TypeError, ValueError) as e:
            name = getattr(action.type, '__name__', repr(action.type))
            args = {'type': name, 'value': arg_string, 'traceback': e}
            msg = _('invalid %(type)s value: %(value)r: %(traceback)s')
            raise ArgumentError(action, msg % args)

        # return the converted value
        return result
