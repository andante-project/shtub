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

import integrationtest_support


class Tests (integrationtest_support.IntegrationTestSupport):
    def test (self):
        self.prepare_default_testbed(['command_stub'])
        self.create_command_wrapper('command_wrapper', 'command_stub', ['-arg1', '-arg2', '-arg3'], 'stdin')

        with self.fixture() as when:
            when.calling('command_stub').with_arguments('-arg1', '-arg2', '-arg3').and_input('stdin') \
                .then_answer('Hello world!', 'Hello error!', 0) \
                .then_return(1)

        actual_return_code1 = self.execute_command('command_wrapper')
        actual_return_code2 = self.execute_command('command_wrapper')

        self.assertEqual(0, actual_return_code1)
        self.assertEqual(0, actual_return_code2)

        with self.verify() as verify:
            verify.called('command_stub').with_arguments('-arg1', '-arg2', '-arg3').and_input('stdin')
            verify.called('command_stub').with_arguments('-arg1', '-arg2', '-arg3').and_input('stdin')


if __name__ == '__main__':
    unittest.main()
