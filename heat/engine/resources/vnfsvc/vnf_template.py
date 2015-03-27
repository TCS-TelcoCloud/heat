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

from heat.openstack.common.gettextutils import _
from heat.engine import clients
from heat.engine import constraints
from heat.engine import properties
from heat.engine.resources.vnfsvc import vnfsvc
from heat.openstack.common import log as logging


logger = logging.getLogger(__name__)

class Service(vnfsvc.VNFSvcResource):
    """
    A resource for the Service Name resource in VNFsvc .
    """

    PROPERTIES = (
        NAME,DESCRIPTION,QUALITY_OF_SERVICE,ATTRIBUTES,
    ) = (
        'name', 'description','quality_of_service', 'attributes'
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('Service name to create the cluster'),
            required=True,
            update_allowed=True
        ),
        DESCRIPTION: properties.Schema(
            properties.Schema.STRING,
            _('Description of the service'),
            required=True,
            update_allowed=True
        ),
        QUALITY_OF_SERVICE: properties.Schema(
            properties.Schema.STRING,
            _('quality of service'),
            required=True,
            update_allowed=True
        ),
        ATTRIBUTES: properties.Schema(
            properties.Schema.MAP,
            _('attributes'),
            required=True,
            update_allowed=True
        )


    }

    attributes_schema = {
        'name': _('Name of service'),
        'description': _('Description of the service'),
        'quality_of_service': _('quality of service'),
        'attributes': _('attributes'),
    }

    update_allowed_keys = ('Properties',)

    def _show_resource(self):
         device = self.vnfsvc().show_vnf(self.resource_id)['service']
         if device == {}:
            return

    def handle_create(self):
        service_props={}
        global service
        props = self.prepare_properties(
            self.properties,
            self.physical_resource_name())
        service_props['name']=props['name']
        service_props['description']=props['description']
        service_props['quality_of_service']=props['quality_of_service']
        service_props['attributes'] = props['attributes']
        service_final = self.vnfsvc().create_service({'service': service_props})['service']
        self.resource_id_set(service_final['id'])
        print service_final
        if 'check' in service_final.keys():
            raise Exception("VNFSVC EXCEPTION HAS OCCURED :" + service_final['check'])

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        if prop_diff:
            self.vnfsvc().update_service(
                self.resource_id, {'service': prop_diff})

    def handle_delete(self):
        client = self.vnfsvc()
        global service
        try:
            client.delete_service(self.resource_id)
            return
        except Exception as ex:
            self.client_plugin().ignore_not_found(ex)


def resource_mapping():
    return {
        'OS::VNFSvc::Service': Service,
    }
        
