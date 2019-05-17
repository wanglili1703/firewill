pybot -v app_path:$HOME/jenkins_workspace/workspace/$JOB_NAME/huaxin/apps/android_xjb_1_8/hxxjb-uat-latest.apk \
-v platform_version:5.1 \
-v device_id:810EBMC43NGC \
-v port:4721 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_UAT_USER_3 \
-d $HOME/jenkins_workspace/workspace/$JOB_NAME $HOME/jenkins_workspace/workspace/$JOB_NAME/huaxin/ui_android_xjb_1_8_unit_test/ui_android_xjb_1_8_tests.txt

/bin/cp -r $HOME/jenkins_workspace/workspace/${JOB_NAME}/huaxin/*.jpg $HOME/jenkins_workspace/workspace/${JOB_NAME}