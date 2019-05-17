appium --address 127.0.0.1 --port 4722 --session-override --platform-name iOS --platform-version 1.6.5& \

pybot -v app_path:$HOME/firewill/apps/ios_xjb_1_8/hxxjb-ios-uat-latest.app \
-v platform_version:9.3 \
-v device_id:56a36d750ab8d2c6e5b73365099bdbf7bc05d9d2 \
-v port:4722 \
-v package_name:com.shhxzq.xjbDev \
-v account:XJB_UAT_USER_4 \
-d $HOME/firewill $HOME/firewill/ui_ios_xjb_1_8_unit_test/ui_ios_xjb_1_8_tests.txt