# coding: utf-8
import collections

from _common.page_object import PageObject
from selenium.common.exceptions import NoSuchElementException

from _common.xjb_decorator import dialog_close, dialog_close_afterwards, swipe_guide, robot_log, message_dialog_close
from huaxin_ui.ui_ios_xjb_3_0.home_page import HomePage
from huaxin_ui.ui_ios_xjb_3_0.login_page import LoginPage

PUSH_MESSAGE = "axis_IOS_好"
CLICK_START = "accId_UIAButton_(bottomButton)"
WELCOME_START = "swipe_accId_//"
WELCOME_STOP = "swipe_accId_(bottomButton)"

POP_UP = "accId_UIAButton_(UIButton_delete)[POP]"
ASSETS = "accId_UIAButton_(UITabBarButton_item_4)"
LOGIN = "accId_UIAButton_(UIButton_登录)"

USER_NAME = "accId_UIATextField_AID_login_mobile"
PASSWORD = "accId_UIASecureTextField_AID_login_password"
LOGIN_BUTTON = "accId_UIAButton_AID_login_btn"

SETTINGS_BUTTON = "accId_UIAButton_UIBarButtonItemLocationRight"
LOGOUT_BUTTON = "accId_UIAButton_安全退出"
LOGOUT = "accId_UIAButton_退出"

current_page = []


class MainPage(PageObject):
    def __init__(self, web_driver):
        super(MainPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._current_xjb_page = None
        self._ui_flow = []
        self._ui_flow_page = []
        self._ui_flow_page_name = collections.OrderedDict()

    def ui_flow_msg(self):
        print '\r\n'
        print 'ui_flow_is_ '
        for i in self.ui_flow:
            print i

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

                        self.ui_flow_msg()

                    return return_page

                return wrapper

            return attribute_value
        else:
            self.ui_flow_msg()
            raise Exception('%s has no func %s' % (self._current_xjb_page, attribute))

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

    @robot_log
    # @dialog_close_afterwards
    # @swipe_guide
    def go_to_home_page_(self):

        self.perform_actions(
            # PUSH_MESSAGE,
            WELCOME_START, WELCOME_STOP, 'L',
            CLICK_START,
            POP_UP,
            ASSETS,
        )

        return_page = HomePage(self.web_driver)

        self._ui_flow.append({return_page.__class__.__name__: return_page})
        self._ui_flow_page_name.update({return_page.__class__.__name__: return_page})
        self._ui_flow_page.append(return_page.__class__.__name__)
        self.current_xjb_page = return_page

        return self.current_xjb_page

    @robot_log
    @message_dialog_close
    def go_to_home_page(self):

        return_page = HomePage(self.web_driver)

        self._ui_flow.append({return_page.__class__.__name__: return_page})
        self._ui_flow_page_name.update({return_page.__class__.__name__: return_page})
        self._ui_flow_page.append(return_page.__class__.__name__)
        self.current_xjb_page = return_page

        return self.current_xjb_page

    @robot_log
    @message_dialog_close
    def go_to_login_page_(self):

        self.perform_actions(
            ASSETS,
        )

        if self.element_exist("(长时间未操作，需要重新登录)", "find_element_by_accessibility_id"):
            self.perform_actions("xpathIOS_UIAButton_//UIACollectionView//UIAButton[@label='确认']")
        else:
            if self.element_is_displayed("(UIButton_登录)", "find_element_by_accessibility_id"):
                self.perform_actions(LOGIN)
            else:
                # 先退出然后在登陆
                self.perform_actions(SETTINGS_BUTTON,
                                     LOGOUT_BUTTON,
                                     LOGOUT,
                                     ASSETS,
                                     LOGIN)

        return_page = LoginPage(self.web_driver)

        self._ui_flow.append({return_page.__class__.__name__: return_page})
        self._ui_flow_page_name.update({return_page.__class__.__name__: return_page})
        self._ui_flow_page.append(return_page.__class__.__name__)
        self.current_xjb_page = return_page

        return self.current_xjb_page
