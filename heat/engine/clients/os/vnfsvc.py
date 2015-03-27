# Copyright 2014 Tata Consultancy Services Ltd.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from vnfsvcclient.common import exceptions
from vnfsvcclient.vnfsvc import v1_0 as vnfsvcV10
from vnfsvcclient.v1_0 import client as vc

from heat.common import exception
from heat.engine.clients import client_plugin
from heat.engine import constraints
from heat.openstack.common import uuidutils


class VnfsvcClientPlugin(client_plugin.ClientPlugin):
   
    exceptions_module = exceptions

    def _create(self):

        con = self.context

        endpoint_type = self._get_client_option('vnfsvc', 'endpoint_type')
        endpoint = self.url_for(service_type='vnfservice',
                                endpoint_type=endpoint_type)
        
        args = {
            'auth_url': con.auth_url,
            'service_type': 'vnfservice',
            'token': self.auth_token,
            'endpoint_url': endpoint,
            'endpoint_type': endpoint_type,
            'ca_cert': self._get_client_option('vnfsvc', 'ca_file'),
            'insecure': self._get_client_option('vnfsvc', 'insecure')
        }

        return vc.Client(**args)

    def is_not_found(self, ex):
        if isinstance(ex, (exceptions.NotFound)):
            return True

        return (isinstance(ex, exceptions.VnfsvcClientException) and
                ex.status_code == 404)

    def is_conflict(self, ex):
        if not isinstance(ex, exceptions.VnfsvcClientException):
            return False
        return ex.status_code == 409

    def is_over_limit(self, ex):
        if not isinstance(ex, exceptions.VnfsvcClientException):
            return False
        return ex.status_code == 413

    def find_vnfsvc_resource(self, props, key, key_type):
        return vnfsvcV10.find_resourceid_by_name_or_id(
            self.client(), key_type, props.get(key))

