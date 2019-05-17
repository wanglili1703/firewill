# coding: utf-8

import os

import re
import subprocess

import time
import tempfile
import os
import re
import time
import xml.etree.cElementTree as ET

from _common.global_config import GlobalConfig


class Adb(object):
    def __init__(self):

        env = {'LESS': '-R', 'M2': '/Users/linkinpark/java_project/apache-maven-3.3.9/bin', 'LC_CTYPE': 'zh_CN.UTF-8',
               'LOGNAME': 'linkinpark', 'USER': 'linkinpark',
               'PATH': '/Users/linkinpark/.virtualenvs/test/bin:/Applications/Appium.app/Contents/Resources/node/bin/node/:/Users/linkinpark/android-sdk-macosx/platform-tools/:/Users/linkinpark/java_project/apache-maven-3.3.9/bin:/Applications/oracle/product/instantclient_64/11.2.0.4.0/bin:/Applications/oracle/product/instantclient_64/11.2.0.4.0/bin:/Applications/oracle/product/instantclient_64/11.2.0.4.0/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
               'HOME': '/Users/linkinpark', 'VIRTUALENVWRAPPER_SCRIPT': '/usr/local/bin/virtualenvwrapper.sh',
               'ZSH': '/Users/linkinpark/.oh-my-zsh',
               'LD_LIBRARY_PATH': '/Applications/oracle/product/instantclient_64/11.2.0.4.0',
               'TERM_PROGRAM': 'iTerm.app',
               'LANG': 'zh_CN.UTF-8', 'TERM': 'xterm-256color',
               'Apple_PubSub_Socket_Render': '/private/tmp/com.apple.launchd.4Vx2eSgQ0F/Render', 'COLORFGBG': '7;0',
               'JAVA_8_HOME': '/Library/Java/JavaVirtualMachines/jdk1.8.0_40.jdk/Contents/Home',
               'ORACLE_HOME': '/Applications/oracle/product/instantclient_64/11.2.0.4.0', 'SHLVL': '1',
               'PROJECT_HOME': '/Users/linkinpark/Devel', 'XPC_FLAGS': '0x0', 'ITERM_SESSION_ID': 'w1t0p0',
               '_': '/Users/linkinpark/.virtualenvs/test/bin/python',
               'M2_HOME': '/Users/linkinpark/java_project/apache-maven-3.3.9',
               'JAVA_HOME': '/Library/Java/JavaVirtualMachines/jdk1.8.0_40.jdk/Contents/Home',
               'WORKON_HOME': '/Users/linkinpark/.virtualenvs', 'XPC_SERVICE_NAME': '0',
               'VERSIONER_PYTHON_PREFER_32_BIT': 'no',
               'SSH_AUTH_SOCK': '/private/tmp/com.apple.launchd.ADGNcGWuw3/Listeners',
               'VIRTUAL_ENV': '/Users/linkinpark/.virtualenvs/test', 'ORACLE_BASE': '/Applications/oracle',
               'DYLD_LIBRARY_PATH': '/Applications/oracle/product/instantclient_64/11.2.0.4.0', 'SHELL': '/bin/zsh',
               'PS1': '(test)${ret_status} %{$fg[cyan]%}%c%{$reset_color%} $(git_prompt_info)',
               'ITERM_PROFILE': 'Default',
               'ANDROID_HOME': '/Users/linkinpark/android-sdk-macosx',
               'TMPDIR': '/var/folders/14/lxlby3ts3jv9r4yw3m42rwyw0000gn/T/',
               'VIRTUALENVWRAPPER_PROJECT_FILENAME': '.project',
               'LSCOLORS': 'Gxfxcxdxbxegedabagacad',
               'JAVA_7_HOME': '/Library/Java/JavaVirtualMachines/jdk1.7.0_79.jdk/Contents/Home',
               'VIRTUALENVWRAPPER_HOOK_DIR': '/Users/linkinpark/.virtualenvs', 'OLDPWD': '/',
               'VERSIONER_PYTHON_VERSION': '2.7',
               '__CF_USER_TEXT_ENCODING': '0x1F5:0x19:0x34', 'PWD': '/etc', 'PAGER': 'less',
               'VIRTUALENVWRAPPER_WORKON_CD': '1'}

        os.environ.update(env)

    def adb_cmd_call(self, cmd):
        # os.system(cmd)
        subprocess.call(cmd, shell=True, executable='/bin/zsh')

    def adb_cmd_output(self, cmd):
        # os.system(cmd)
        r = subprocess.check_output(cmd, shell=True, executable='/bin/zsh')
        return r

    def install_app(self, device_id, app_path):
        cmd = 'adb -s %s install -r %s' % (device_id, app_path)
        self.adb_cmd_call(cmd)

    def uninstall_apk(self, device_id, package_name):
        cmd = 'adb -s %s uninstall %s' % (device_id, package_name)
        self.adb_cmd_call(cmd)

    def is_package_installed(self, device_id, package_name):
        cmd = "adb -s %s shell pm list packages" % device_id
        package_names = self.adb_cmd_output(cmd)
        return re.search(package_name, package_names)

    def launch_app(self, device_id, package_name):
        cmd = "adb -s %s shell monkey -p '%s' -c android.intent.category.LAUNCHER 1" % (device_id, package_name)
        self.adb_cmd_call(cmd)

    def kill_process_by_name(self, name):
        cmd = "ps aux | grep %s" % name
        f = os.popen(cmd)
        txt = f.readlines()
        if len(txt) == 0:
            print "no process \"%s\"!!" % name
            return
        else:
            for line in txt:
                colum = line.split()

                if '-P' in colum:
                    print colum
                    pid = colum[1]

                    cmd = "kill -9 %s" % pid
                    self.adb_cmd_call(cmd)

                    rc = os.system(cmd)
                    if rc == 0:
                        print "exec \"%s\" success!!" % cmd
                    else:
                        print "exec \"%s\" failed!!" % cmd

    def list_android_device(self):
        cmd = 'adb devices'
        self.adb_cmd_call(cmd)
        cmd = 'adb shell getprop ro.build.version.release'
        self.adb_cmd_call(cmd)


if __name__ == '__main__':
    m = Adb()
    # m.uninstall_apk(device_id='PBV7N16924004496', package_name='com.shhxzq.xjb')  #华为
    m.uninstall_apk(device_id='ac3997d9', package_name='com.shhxzq.xjb')  # 小米
    # m.uninstall_apk(device_id='SH24NW104645', package_name='com.shhxzq.xjb')
    # m.uninstall_apk(device_id='95AQACQD7J9LP', package_name='com.shhxzq.xjb')
    # m.uninstall_apk(device_id='4DU4UWSO6PGYIJZS', package_name='com.shhxzq.xjb')   # 乐视
    # apk_path = GlobalConfig.RESOURCE_ROOT_PATH + '/apps/android_xjb_2_0/hxxjb-ptest-latest.apk'
    apk_path = GlobalConfig.RESOURCE_ROOT_PATH + '/apps/android_xjb_3_0/hxxjb-ptest-latest.apk'
    # apk_path = GlobalConfig.RESOURCE_ROOT_PATH + '/apps/android_xjb_3_0/hxxjb-product-latest.apk'
    # apk_path = GlobalConfig.RESOURCE_ROOT_PATH + '/apps/android_xjb_3_0/hxxjb-uat-latest.apk'
    # m.install_app('ae9b496c', apk_path)  #vivo
    # m.install_app('DU2MWW145H002092', apk_path)  #P7
    # m.install_app('141d7a62', apk_path)  #联想
    # m.install_app('PBV7N16924004496', apk_path)  #华为
    # m.install_app('ac3997d9', apk_path)  #华为
    # m.install_app('3eb2fc1f', apk_path)  #红米
    # m.install_app('SH24NW104645', apk_path)  #红米
    # m.install_app('7N2TDM1557021079', apk_path)  # honor
    # m.install_app('95AQACQD7J9LP', apk_path)  #魅族
    m.install_app('ac3997d9', apk_path)  #小米
    # m.install_app('4DU4UWSO6PGYIJZS', apk_path)  #乐视
    # m.install_app('546703b0', apk_path)  #DX小米
    # m.install_app('2895b262', apk_path)  #酷派
    # m.uninstall_apk(device_id='PBV7N16924004496', package_name='com.shhxzq.xjb')
    # apk_path = GlobalConfig.RESOURCE_ROOT_PATH + '/apps/android_xjb_3_0/hxxjb-uat-latest.apk'
    # m.install_app('ac3997d9', apk_path)  #小米
    # m.install_app('SJE0217411000903', apk_path)  #卞卞
    # m.install_app('ae9b496c', apk_path)  #vivo
    # m.install_app('546703b0', apk_path)  #vivo
    # m.install_app('PBV7N16924004496', apk_path)  #华为
    # m.kill_process_by_name('adb')
    # print os.environ
    # print m.is_package_installed('810EBMC43NGC', 'com.shhxzq.xjb')
    # m.list_android_device()
    # m.capture_device_screen(device_id='PBV7N16924004496')
    # print m.list_current_python_package()
    # m.appium_start(port='4726',version='1.5.3')
    # m.list_type_writing()
    # print m.get_default_type_writing()
    # m.test(device_id='ae9b496c',w_per=0.5,h_per=0.5)
