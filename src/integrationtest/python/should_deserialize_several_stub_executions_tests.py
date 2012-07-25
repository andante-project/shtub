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

import unittest

from os.path import join

import integrationtest_support

from shtub import deserialize_executions


class Test (integrationtest_support.IntegrationTestSupport):
    def test (self):
        self.prepare_default_testbed(['command_stub1', 'command_stub2'])
        self.create_command_wrapper('command_wrapper1', 'command_stub1', ['-arg1', '-arg2', '-arg3'], 'stdin1')
        self.create_command_wrapper('command_wrapper2', 'command_stub2', ['-arg6', '-arg7', '-arg8'], 'stdin2')
        
        with self.fixture() as fixture:
            fixture.expect('command_stub1', ['-arg1', '-arg2', '-arg3'], 'stdin1') \
                   .then_answer('Hello world 1', 'Hello error 1', 0)
            fixture.expect('command_stub2', ['-arg6', '-arg7', '-arg8'], 'stdin2') \
                   .then_answer('Hello world 2', 'Hello error 2', 0)
        
        actual_return_code1 = self.execute_command('command_wrapper1')
        actual_return_code2 = self.execute_command('command_wrapper2')
        
        self.assertEquals(0, actual_return_code1)
        self.assertEquals(0, actual_return_code2)

        path = join(self.base_dir, 'test-execution', 'recorded-calls')
        
        actual_calls = deserialize_executions(path)
        
        self.assertEquals(2, len(actual_calls))
        
        actual_first_call = actual_calls[0]
        
        self.assertEquals('command_stub1', actual_first_call.command)
        self.assertEquals(['-arg1', '-arg2', '-arg3'], actual_first_call.arguments)
        self.assertEquals('stdin1', actual_first_call.stdin)
        
        actual_second_call = actual_calls[1]
        
        self.assertEquals('command_stub2', actual_second_call.command)
        self.assertEquals(['-arg6', '-arg7', '-arg8'], actual_second_call.arguments)
        self.assertEquals('stdin2', actual_second_call.stdin)


if __name__ == '__main__':
    unittest.main()