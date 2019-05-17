# coding: utf-8
import collections

from _common.page_object import PageObject
from _common.xjb_decorator import dialog_close, dialog_close_afterwards, swipe_guide, robot_log
from huaxin_ui.ui_ios_xjb_1_8.home_page import HomePage

HOME_PAGE_NAVIGATOR = "accId_(UITabBarButton_)"  # 默认在home_page
FINACIAL_PAGE_NEVIGATOR = "accId_(UITabBarButton_item_1)"
FUND_PAGE_NEVIGATOR = "accId_(UITabBarButton_item_2)"
ASSETS_PAGE_NEVIGATOR = "accId_(UITabBarButton_item_3)"

current_page = []


class MainPage(PageObject):
    def __init__(self, web_driver):
        super(MainPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._current_xjb_page = None
        self._ui_flow = [] #dict的update会覆盖掉原来的值,所以这里是有list的append
        self._ui_flow_page = []  # 同ui_flow,这里只存储key部分
        self._ui_flow_page_name = collections.OrderedDict() #这里是为了获取return_page_afterwards中的return_page而定义的


    # main反射的方法
    def __getattr__(self, attribute):

        if hasattr(self._current_xjb_page, attribute):
            attribute_value = getattr(self._current_xjb_page, attribute)

            if callable(attribute_value):
                def wrapper(*args, **kwargs):
                    return_page = attribute_value(*args, **kwargs)

                    if not isinstance(return_page, PageObject):
                        pass
                    else:
                        self._ui_flow.append({return_page.__class__.__name__: return_page})
                        self._ui_flow_page_name.update({return_page.__class__.__name__: return_page})
                        self._ui_flow_page.append(return_page.__class__.__name__)
                        self.current_xjb_page = return_page

                    return return_page

                return wrapper

            return attribute_value
        else:
            return super(MainPage, self).__getattr__(attribute)

    @property
    def current_xjb_page(self):
        return self._current_xjb_page

    @current_xjb_page.setter
    def current_xjb_page(self, value):
        setattr(value, 'ui_flow', self.ui_flow)
        setattr(value, 'ui_flow_page_name', self.ui_flow_page_name)
        setattr(value, 'ui_flow_page', self.ui_flow_page)
        self._current_xjb_page = value

    @property
    def ui_flow(self):
        return self._ui_flow

    @property
    def ui_flow_page_name(self):
        return self._ui_flow_page_name

    @property
    def ui_flow_page(self):
        return self._ui_flow_page

    # main本身的方法
    @robot_log
    # @dialog_close_afterwards
    @swipe_guide
    def go_to_home_page(self):

        return_page = HomePage(self.web_driver)

        self._ui_flow.append({return_page.__class__.__name__: return_page})
        self._ui_flow_page_name.update({return_page.__class__.__name__: return_page})
        self._ui_flow_page.append(return_page.__class__.__name__)
        self.current_xjb_page = return_page

        return self.current_xjb_page

if __name__ == '__main__':
    a = []
    print a
    a.append({'A':'1'})
    print a
    a.append({'A':'2'})
    print a
    print a[-1]


