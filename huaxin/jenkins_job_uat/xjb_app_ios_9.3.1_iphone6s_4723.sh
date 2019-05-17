#!/usr/bin/env bash
pybot -v app_path:$HOME/xjb/build/DerivedData/Build/Products/Debug-iphoneos/HXXjb.app \
-v platform_version:9.3.1 \
-v device_id:a2c995b55b69e2059b475e2c9b8ddc6f2811a0d0 \
-v port:4723 \
-v package_name:com.shhxzq.xjbDev \
-v account:XJB_UAT_USER_1 \
-d $HOME/.jenkins/workspace/$JOB_NAME $HOME/.jenkins/workspace/$JOB_NAME/huaxin/ui_ios_xjb_3_0_unit_test/ui_ios_xjb_3_0_tests.txt

pybot -v app_path:$HOME/xjb/build/DerivedData/Build/Products/Debug-iphoneos/HXXjb.app \
-v platform_version:9.3.1 \
-v device_id:a2c995b55b69e2059b475e2c9b8ddc6f2811a0d0 \
-v port:4723 \
-v package_name:com.shhxzq.xjbDev \
-v account:XJB_UAT_USER_1 \
-R $HOME/.jenkins/workspace/$JOB_NAME/output.xml \
-d $HOME/.jenkins/workspace/$JOB_NAME/log_2 $HOME/.jenkins/workspace/$JOB_NAME/huaxin/ui_ios_xjb_3_0_unit_test/ui_ios_xjb_3_0_tests.txt
rebot -d $HOME/.jenkins/workspace/$JOB_NAME/ -o $HOME/.jenkins/workspace/$JOB_NAME/output --merge $HOME/.jenkins/workspace/$JOB_NAME/output.xml $HOME/.jenkins/workspace/$JOB_NAME/log_2/output.xml

pybot -v app_path:$HOME/xjb/build/DerivedData/Build/Products/Debug-iphoneos/HXXjb.app \
-v platform_version:9.3.1 \
-v device_id:a2c995b55b69e2059b475e2c9b8ddc6f2811a0d0 \
-v port:4723 \
-v package_name:com.shhxzq.xjbDev \
-v account:XJB_UAT_USER_1 \
-R $HOME/.jenkins/workspace/$JOB_NAME/log_2/output.xml \
-d $HOME/.jenkins/workspace/$JOB_NAME/log_3 $HOME/.jenkins/workspace/$JOB_NAME/huaxin/ui_ios_xjb_3_0_unit_test/ui_ios_xjb_3_0_tests.txt
rebot -d $HOME/.jenkins/workspace/$JOB_NAME/ -o $HOME/.jenkins/workspace/$JOB_NAME/output --merge $HOME/.jenkins/workspace/$JOB_NAME/output.xml $HOME/.jenkins/workspace/$JOB_NAME/log_3/output.xml

# /bin/cp -r $HOME/.jenkins/workspace/${JOB_NAME}/huaxin/*.jpg $HOME/.jenkins/workspace/${JOB_NAME}
find $HOME/.jenkins/workspace/${JOB_NAME}/huaxin/ -name "*.jpg" -exec /bin/cp {} $HOME/.jenkins/workspace/${JOB_NAME} \;