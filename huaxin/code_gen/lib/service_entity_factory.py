import random
import time
from code_gen.lib.service_helper import ServiceHelper

class EntityFactory(object):

    def __init__(self, status=None, cookies=None, concurrent_mode=False):
        self.service_helper = ServiceHelper()
        self.cookies = cookies
        self.concurrent_mode = concurrent_mode
        self.status = status

    def get_entity(self, entity_cls, *args, **kwargs):
        if self.concurrent_mode:
            kwargs.update(service_helper=self.service_helper)
        if self.cookies:
            kwargs.update(cookies=self.cookies)
        try:
            entity = entity_cls(*args, **kwargs)
            if 'V1ServicesCommonAcquiredeviceidEntity' in str(entity) or 'V1ServicesRegisterGetmobilecodeEntity' in str(entity) or 'V1ServicesRegisterConfirmEntity' in str(entity) or 'V1ServicesCardSettradepasswordEntity' in str(entity) or 'V1ServicesCardMatchchannelEntity' in str(entity) or 'V1ServicesCardGetmobilecodeEntity' in str(entity) or 'V1ServicesCardNewbindingEntity' in str(entity):
                pass
            else:
                # time.sleep(random.uniform(1, 10))
                # if 4 < random.uniform(1, 15) < 10:
                return entity
        except TypeError as e:
            original_message = '(original message: %s)' % e
            if self.concurrent_mode:
                error_message = "Add default arg 'service_helper=None' to %s's __init__ with concurrent mode\n" % entity_cls.__name__ + original_message
            else:
                error_message = entity_cls.__name__ + str(e)
            raise TypeError(error_message)

        return entity
