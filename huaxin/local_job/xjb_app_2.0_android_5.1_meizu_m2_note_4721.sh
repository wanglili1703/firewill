appium --address 127.0.0.1 --port 4721 --session-override --platform-name Android --platform-version 1.5.3& \

pybot -v app_path:$HOME/firewill/huaxin/apps/android_xjb_2_0/hxxjb-uat-latest.apk \
-v platform_version:5.1 \
-v device_id:810EBMC43NGC \
-v port:4721 \
-v package_name:com.shhxzq.xjb \
-d $HOME/firewill/huaxin $HOME/firewill/huaxin/ui_android_xjb_2_0_unit_test/ui_android_xjb_2_0_tests.txt