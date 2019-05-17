pybot -v app_path:$HOME/.jenkins/workspace/$JOB_NAME/huaxin/apps/android_xjb_3_0/hxxjb-uat-latest.apk \
-v platform_version:6.0 \
-v device_id:PBV7N16924004496 \
-v port:4726 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_UAT_USER_2 \
-d $HOME/.jenkins/workspace/$JOB_NAME $HOME/.jenkins/workspace/$JOB_NAME/huaxin/ui_android_xjb_3_0_unit_test/ui_android_xjb_3_0_tests.txt

pybot -v app_path:$HOME/.jenkins/workspace/$JOB_NAME/huaxin/apps/android_xjb_3_0/hxxjb-uat-latest.apk \
-v platform_version:6.0 \
-v device_id:PBV7N16924004496 \
-v port:4726 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_UAT_USER_2 \
-R $HOME/.jenkins/workspace/$JOB_NAME/output.xml \
-d $HOME/.jenkins/workspace/$JOB_NAME/log_2 $HOME/.jenkins/workspace/$JOB_NAME/huaxin/ui_android_xjb_3_0_unit_test/ui_android_xjb_3_0_tests.txt
rebot -d $HOME/.jenkins/workspace/$JOB_NAME/ -o $HOME/.jenkins/workspace/$JOB_NAME/output --merge $HOME/.jenkins/workspace/$JOB_NAME/output.xml $HOME/.jenkins/workspace/$JOB_NAME/log_2/output.xml

pybot -v app_path:$HOME/.jenkins/workspace/$JOB_NAME/huaxin/apps/android_xjb_3_0/hxxjb-uat-latest.apk \
-v platform_version:6.0 \
-v device_id:PBV7N16924004496 \
-v port:4726 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_UAT_USER_2 \
-R $HOME/.jenkins/workspace/$JOB_NAME/log_2/output.xml \
-d $HOME/.jenkins/workspace/$JOB_NAME/log_3 $HOME/.jenkins/workspace/$JOB_NAME/huaxin/ui_android_xjb_3_0_unit_test/ui_android_xjb_3_0_tests.txt
rebot -d $HOME/.jenkins/workspace/$JOB_NAME/ -o $HOME/.jenkins/workspace/$JOB_NAME/output --merge $HOME/.jenkins/workspace/$JOB_NAME/output.xml $HOME/.jenkins/workspace/$JOB_NAME/log_3/output.xml

/bin/cp -r $HOME/.jenkins/workspace/${JOB_NAME}/huaxin/*.jpg $HOME/.jenkins/workspace/${JOB_NAME}