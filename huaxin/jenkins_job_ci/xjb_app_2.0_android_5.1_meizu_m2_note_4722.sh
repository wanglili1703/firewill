pybot -v app_path:$HOME/jenkins_workspace/workspace/$JOB_NAME/huaxin/apps/android_xjb_2_0/hxxjb-ptest-latest.apk \
-v platform_version:5.1 \
-v device_id:810EBMC43NGC \
-v port:4722 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_CI_USER_2 \
-d $HOME/jenkins_workspace/workspace/$JOB_NAME $HOME/jenkins_workspace/workspace/$JOB_NAME/huaxin/ui_android_xjb_2_0_unit_test/ui_android_xjb_2_0_tests.txt

/bin/cp -r $HOME/jenkins_workspace/workspace/${JOB_NAME}/huaxin/*.jpg $HOME/jenkins_workspace/workspace/${JOB_NAME}