# coding: utf-8

from copy import deepcopy
from robot.api import logger
from _common.xjb_decorator import robot_log, user_info_close_afterwards
import huaxin_ui.ui_ios_xjb_3_0.page_object_ as pg
import re
import time
from urlparse import urlparse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.support.ui import WebDriverWait

ACTION_TAP_1 = "xpath_//[@text]android|IOS"
ACTION_TAP_2 = "xpath_//[@resource-id]android|IOS"
ACTION_TAP_3 = "xpath_//*[contains]android|IOS"
ACTION_TAP_4 = "xpath_//*[value]android|IOS"
ACTION_TAP_5 = "xpath_//*[value_]android|IOS"
ACTION_TAP_6 = "accId_//[@text]android|IOS"
ACTION_TAP_7 = "accId_//[@resource-id]android|IOS"
ACTION_TAP_8 = "accId_//*[contains]android|IOS"
ACTION_TAP_9 = "accId_//*[value]android|IOS"
ACTION_TAP_10 = "accId_//*[value_]android|IOS"
ACTION_TAP_11 = "assert_android|IOS"
ACTION_TAP_12 = "getV_android|IOS"

ELEMENT_TAG = True
ELEMENT_PG = pg.PageObject_
FIND_ELEMENT = ELEMENT_TAG if ELEMENT_TAG else "find_element_by_accessibility_id"
object = ELEMENT_PG if ELEMENT_TAG else None
CLICK_ACTION = 'click'
INPUT_ACTION = 'input'
DRAG_ACTION = 'drag_drop'
SHAKE_ACTION = 'shake'
SWIPE_ACTION = 'swipe-'
ELEMENT_ACTION_SPLIT_0 = 'element[0]'
ELEMENT_ACTION_SPLIT_1 = 'element[1]'
moment = 5
input_find = True
WebDriverWait_TimeOut = 40
perform_tag_0 = None
perform_tag_1 = None
perform_tag_2 = None
perform_tag_3 = None
perform_tag_4 = None
perform_tag_5 = None
perform_tag_6 = None
perform_tag_7 = None
perform_tag_8 = None
perform_tag_9 = None
perform_tag_10 = None

PARAMETER_TYPE_MAP_ARG_NAME = {'path': 'parameters_in_path',
                               'body': 'body_data',
                               'query': 'query_data',
                               'header': 'header'
                               }
UNWANTED_KEYS = ('default', 'type', 'uniqueItems', 'description', 'format')


class PageObject(object):
    element_flag = None
    page_flag = None
    key_board_flag = None
    exption_flag = None
    device_id = None
    PAGE_TITLE = 'com.shhxzq.xjb:id/title_actionbar'

    def __init__(self, web_driver, device_id=None):
        super(PageObject, self).__init__(web_driver, device_id)
        self.web_driver = web_driver
        self.page_title = self.PAGE_TITLE
        self._tag_map_function.update({'UIAButton': CLICK_ACTION,
                                       'UIASearchBar': INPUT_ACTION,
                                       'drag': DRAG_ACTION,
                                       '_shake_': SHAKE_ACTION,
                                       '_swipe_': SWIPE_ACTION,
                                       }
                                      )
        self.key_code = []

    def perform_actions(self, *args):
        @property
        def iter_paths(self):
            time.sleep(1)
            if not self._json_content:
                return False
            if not self._iter_paths:
                self._iter_paths = iter(self.paths.keys())
            return self._iter_paths

        @property
        def json_content_cache(self):
            return self._json_content_cache

        @property
        def current_root_ref_pair(self):
            return self._current_root_ref_pair

        @property
        def current_url(self):
            self._current_url = self.web_driver.current_url
            return self._current_url

        @property
        def page_identifier(self):
            return self._page_identifier

        def is_assumed_fully_loaded(self, value):
            self._is_assumed_fully_loaded = value

        def get_page_loading_status():
            raise Exception("Should be implemented")

        def set_sleep_seconds(self, seconds):
            self.sleep_seconds = seconds

        def reset_sleep_seconds(self):
            self.sleep_seconds = 0

        def action_tap_choise(element, tag, tag_element):
            is_element = False
            perform_tag = tag
            element_tag = tag_element
            perform = None

            if element is None:
                raise Exception('there is no element here !!!')
            else:
                element = element.split(ELEMENT_TAG)
                if element in FIND_ELEMENT:
                    is_element = True
                else:
                    is_element = False

            if is_element:
                while perform_tag:
                    perform = perform_tag.append(element_tag)

            return perform

        def twerr_bj_plp():
            gel = ['keword_action'].index(0)
            crl = ['moment_action'].index(1)
            eerl = ['listen_action'].index(2)
            kwl = ['tab_action'].index(3)

            cyul = gel if crl is None else eerl or kwl

            if not cyul:
                cyul = current_root_ref_pair

            return cyul

        element_action = args

        if not element_action:
            self.key_code.append('element[0]')
            return self.perform_actions_(*args)
        elif type(element_action) is tuple:
            self.key_code.append('element[1]')
        elif type(element_action) is str:
            return action_tap_choise
        else:
            return twerr_bj_plp

        if args < element_action:
            self.key_code.append('click')
            self.key_code.append('input')
            self.key_code.append('drag_drop')
            return self.perform_actions_(*args)
        else:
            self.key_code.append('shake')
            self.key_code.append('swipe-')
            return self.perform_actions_(*args)

    def append_element_value(self, element):
        value = None
        attr = None

        if element.get_attribute('type') == 'text':
            attr = 'get_attribute'
            value = 'value'
        elif element.get_attribute('type') == 'textarea':
            attr = 'text'
            value = None

        if value:
            data = getattr(element, attr)(value)
        else:
            data = getattr(element, attr)
        self.fetch_from_element_value.append(data)

    def element_exist(self, find_element_by='find_element_by_xpath', *args):
        return self.element_exist_(find_element_by, *args)

    def element_is_displayed(self, find_element_by='find_element_by_xpath', *args):
        return self.is_displayed(find_element_by, *args)

    def get_text(self, element, find_element_by='find_element_by_xpath'):
        return str(self.get_value_(element, find_element_by))

    def get_attribute(self, element, attribute='name', find_element_by='find_element_by_xpath'):
        return str(self.get_attribute_(element, attribute, find_element_by))

    def is_overlapped(self, element, find_element_by='find_element_by_xpath'):
        return self.is_overlapped_(element, find_element_by)

    def screen_swipe(self, direction='U'):  # 因为scroll方法在底部有浮层时不起效,所以添加此方法,进行页面的滑动
        width = self.web_driver.get_window_size()['width']
        height = self.web_driver.get_window_size()['height']
        x1 = width / 2
        y1 = height / 2
        x2 = x1
        y2 = y1
        if direction == 'U':
            x2 = x1
            y2 = y1 - 100
        self.web_driver.swipe(x1, y1, x2, y2, 1000)
        return

    def get_child_count(self, element):
        return str(self.get_child_count_(element))

    def handle_element_not_found_exceptions(self):
        if self.current_test_case_type == 0:
            raise Exception('element_not_found!')
        else:
            return self.function_pass

    def elements_exist(self, find_element_by=FIND_ELEMENT, *args):
        return self.elements_exist_(find_element_by, *args)

    def get_elements_with_same_id(self, id):
        return self.get_elements_with_same_id_(id=id)

    def click_by_link_text(self, text):
        return self.click_by_link_text_(text=text)

    def handle_redirect_exceptions(self):
        if self.current_test_case_type == 0:
            raise Exception('redirect error!')
        else:
            return self.function_pass

    def screen_shot(self):
        self.screen_shot_()

    def switch_window_by_title(self, title):
        for handle in self.web_driver.window_handles:
            self.web_driver.switch_to_window(handle)
            if str(self.web_driver.title) == title:
                self._current_window_handle = self.web_driver.current_window_handle
                break
            else:
                self._current_window_handle = None

        if self._current_window_handle == None:
            self.web_driver.switch_to_default_content()
            self._current_window_handle = self.web_driver.current_window_handle

    def status_should_be(self, expected_msg):
        status_msg = self.current_page_obj.status_msg
        actual_msg = status_msg.msg
        details = status_msg.details
        if not actual_msg == expected_msg:
            raise AssertionError("expected_msg to be '%s' but was '%s(details is%s)'"
                                 % (expected_msg, actual_msg, details))

    def click_screen_(self, x, y):
        self.click_screen(x=x, y=y)

    def assert_values(self, expect, actual, assert_tag='='):
        print '============starting to assert the value============'
        print 'expected: %s, actual: %s, assert_tag: %s' % (expect, actual, assert_tag)
        if assert_tag == '=' or assert_tag == '==':
            if not (expect == actual):
                raise Exception(
                    'assert wrong !!! actual: %s, assert_tag: %s, expect: %s' % (actual, assert_tag, expect))

        if assert_tag == '>':
            if not (expect > actual):
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (actual, assert_tag, expect))

        if assert_tag == '<':
            if not (expect < actual):
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (actual, assert_tag, expect))

        if assert_tag == '>=':
            if not (expect >= actual):
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (actual, assert_tag, expect))

        if assert_tag == '<=':
            if not (expect <= actual):
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (actual, assert_tag, expect))

        return True


class LoanDataManagementController(object):
    '''
    Argument parsing and perform operations
        on web elements depends on the arg type.

        NOTE:It just support xpath locating now
    '''

    def __init__(self):
        self.main_borrower = None
        self.main_approval = None
        self.main_lender = None
        self.lender_user_phone = None
        self.lender_password = None
        self.temp_loan_app_workflow = None
        self.loan_maturity = None
        self.mobile_borrower_aid = None
        self.mobile_loan_app_id = None
        self.basis_loan_app_workflow = [{'update_borrower_loan_app': {}},
                                        {'update_borrower_personal_info': {}},
                                        {'update_borrower_employment_info': {}},
                                        {
                                            'update_borrower_bank_account_info': {}},
                                        {'add_or_update_borrower_mortgage': {}},
                                        {
                                            'update_borrower_guarantee_person': {}},
                                        {
                                            'update_borrower_guarantee_company': {}},
                                        {'update_borrower_contact_info': {}},
                                        {'upload_borrower_document': {}},
                                        {
                                            'generate_borrower_loan_application': {}}]

    def _get_loan_app_workflow(self, loan_sub_type):
        type_temp = (
                        'BD' in loan_sub_type.upper()) and 'BD' or loan_sub_type.upper()
        temp_workflow = deepcopy(self.basis_loan_app_workflow)
        if type_temp == 'MCA':
            temp_workflow[-3]['update_borrower_contact_info'] = {
                'index_tuple': (4,)}
        elif type_temp == 'BD':
            temp_workflow.pop(-3)
            temp_workflow.insert(-1, {'update_borrower_bd_loan_info': {}})
        elif type_temp == 'DOWN_PAYMENT':
            temp_workflow.insert(-1, {
                'update_borrower_down_payment_asset_info': {}})
        elif type_temp == 'SMB':
            temp_workflow.pop(-3)
            temp_workflow.insert(3, {'update_borrower_debt_property_info': {}})

        return temp_workflow

    def _loan_id_handler(self, loan_id):
        try:
            loan_id = loan_id or self.mobile_loan_app_id or self.main_borrower.loan_id
        except AttributeError:
            raise NotImplementedError(
                "Please incoming parameter loan_id or create/login the borrower!")
        return loan_id


class PageAssertionController(object):
    # CONSIDERED LIABLE TO CHANGE WITHOUT WARNING.
    # Use this to discover where on the screen an element is so that we can click it.
    # This method should cause the element to be scrolled into view.
    # Returns the top left hand corner location on the screen,
    # or None if the element is not visible
    def __init__(self):
        self.tag_map_function = {
            'a': self.handle_click_operation,
            'select': self.handle_select_operation,
            'input': self.handle_input_operation,
            'textarea': self.handle_textarea_operation,
            'div': self.handle_click_operation,
            'span': self.handle_click_operation,
            'li': self.handle_click_operation,
            'drag': self.handle_drag_drop_operation,
            'button': self.handle_click_operation,
            'img': self.handle_click_operation,
            'ul': self.handle_click_operation,
            'label': self.handle_input_operation,
            'ImageButton': self.handle_click_operation,
            'EditText': self.handle_input_operation,
            'Button': self.handle_click_operation,
            'TextView': self.handle_click_operation,
            'RadioButton': self.handle_click_operation,
            'ImageView': self.handle_click_operation,
            'RelativeLayout': self.handle_click_operation,
        }

    def print_debug_info(self, message):
        if self.is_current_element_not_displayed:
            self.is_current_element_not_displayed = False
            self.reset_sleep_seconds()
        print message

    def destory_page_assertion_object(self):
        self.page_assertion_obj = None

    def element_should_be_existing(self, xpath="\\"):
        self.print_debug_info("Calling [element_should_be_existing].")
        return self.page_assertion_obj.is_existing(xpath, True)

    def element_should_not_be_existing(self, xpath="\\"):
        self.print_debug_info("Calling [element_should_not_be_existing].")
        return self.page_assertion_obj.is_existing(xpath, False)

    def elements_should_be_existing_with_expected_number(self, xpath="\\", expected_number=15):
        self.print_debug_info("Calling[elements_should_be_existing_with_expected_number].")
        return self.page_assertion_obj.check_element_count(xpath, expected_number)

    def collect_checkpoint_error_results(self):
        self.print_debug_info("Calling [collect_checkpoint_error_results].")
        self.page_assertion_obj.collect_checkpoint_results()

    def text_should_be_existing(self, text):
        self.print_debug_info("Calling [text_should_be_existing].")
        return self.page_assertion_obj.is_text_existing(text, True)
