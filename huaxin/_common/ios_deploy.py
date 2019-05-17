# coding: utf-8

import os

import subprocess

import re

from _common.global_config import GlobalConfig


class IosDeploy(object):
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
        subprocess.call(cmd, shell=True, executable='/bin/zsh')

    def adb_cmd_output(self, cmd):
        r = subprocess.check_output(cmd, shell=True, executable='/bin/zsh')
        return r

    def list_ios_device(self):
        cmd = 'ios-deploy -c'
        self.adb_cmd_call(cmd)

    def is_package_installed(self, device_id, package_name):
        cmd = "ios-deploy --exists --id %s --bundle_id %s" % (device_id, package_name)
        return self.adb_cmd_output(cmd)

    def launch_app(self, device_id, app_path):
        # cmd = 'ios-deploy --debug --bundle %s' % app_path
        cmd = 'ios-deploy --noinstall --id %s --bundle %s' % (device_id, app_path)
        self.adb_cmd_call(cmd)

    def ios_device_info(self):
        cmd = 'instruments -s devices'
        self.adb_cmd_call(cmd)

    def xcode_info(self):
        cmd = 'xcode-select --print-path'
        self.adb_cmd_call(cmd)
        cmd = 'xcodebuild -version'
        self.adb_cmd_call(cmd)

    def uninstall_app(self, device_id, package_name):
        cmd = "ios-deploy --uninstall_only --id %s --bundle_id %s" % (device_id, package_name)
        self.adb_cmd_call(cmd)

    def install_app(self, device_id, app_path):
        cmd = "ios-deploy --uninstall --id %s --bundle %s" % (device_id, app_path)
        self.adb_cmd_call(cmd)

    def swith_xcode(self, xcode_path):
        cmd = 'sudo xcode-select -switch %s' % xcode_path
        self.adb_cmd_call(cmd)

    def show_xcode_build(self):
        cmd = 'xcodebuild -showsdks'
        self.adb_cmd_call(cmd)


if __name__ == '__main__':
    device_id = '56a36d750ab8d2c6e5b73365099bdbf7bc05d9d2' # iphone 6p
    # device_id = 'a2c995b55b69e2059b475e2c9b8ddc6f2811a0d0' # iphone 6
    # device_id = '01bfe3e8482902b110ddffaa22e12b7f910d4d8a'  #段老爷自己的手机
    # device_id = 'fea87ecb6f6c49a26b13a519dea6e58f6b3a96a6'
    # device_id = 'd90b21dc9cc8a80ddc28c40f8eae5efb9500a2bd'
    # package_name = 'com.shhxzq.xjbDev'
    package_name = 'com.shhxzq.xjbEnt'
    # app_path = GlobalConfig.RESOURCE_ROOT_PATH + '/apps/ios_xjb_1_8/hxxjb-ios-uat-latest.app'
    # app_path = '/Users/linkinpark/xjb/build/DerivedData/Build/Products/Debug-iphoneos/HXXjb.app'
    app_path = '/Users/wanglili/xjb/build/HXXjb.xcarchive/Products/Applications/HXXjb.app'
    # xcode_path = '/Applications/Xcode-8.1.app/Contents/Developer' #Xcode 8.1
    # xcode_path = '/Applications/Xcode-7.1.app/Contents/Developer'  # Xcode 7.1
    xcode_path = '/Applications/Xcode-7.3.1.app/Contents/Developer'  # Xcode 7.3.1
    m = IosDeploy()
    # m.list_ios_device()
    # m.launch_app(device_id=device_id, app_path=app_path)
    # m.ios_device_info()
    m.xcode_info()
    # print m.is_package_installed(device_id=device_id, package_name=package_name)
    # m.swith_xcode(xcode_path=xcode_path)
    # m.uninstall_app(device_id=device_id, package_name=package_name)
    m.install_app(device_id=device_id, app_path=app_path)
    # print m.is_package_installed(package_name=package_name)
    # m.show_xcode_build()
