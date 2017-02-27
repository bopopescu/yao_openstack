# Copyright 2016 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_lib import constants

from neutron.tests.common.exclusive_resources import port
from neutron.tests.functional import base


class TestExclusivePort(base.BaseLoggingTestCase):
    def test_port(self):
        port_1 = self.useFixture(port.ExclusivePort(
            constants.PROTO_NAME_TCP)).port
        port_2 = self.useFixture(port.ExclusivePort(
            constants.PROTO_NAME_TCP)).port

        self.assertIsInstance(port_1, str)
        self.assertNotEqual(port_1, port_2)
