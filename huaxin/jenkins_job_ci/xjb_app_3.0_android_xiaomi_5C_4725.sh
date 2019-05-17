pybot -v app_path:/Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/huaxin/apps/android_xjb_3_0/hxxjb-ptest-latest.apk \
-v platform_version:6.0 \
-v device_id:ac3997d9 \
-v port:4725 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_CI_USER_2 \
-d /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/huaxin/ui_android_xjb_3_0_unit_test/ui_android_xjb_3_0_tests.txt

pybot -v app_path:/Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/huaxin/apps/android_xjb_3_0/hxxjb-ptest-latest.apk \
-v platform_version:6.0 \
-v device_id:ac3997d9 \
-v port:4725 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_CI_USER_2 \
-R /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/output.xml \
-d /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/log_2 /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/huaxin/ui_android_xjb_3_0_unit_test/ui_android_xjb_3_0_tests.txt
rebot -d /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/ -o /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/output --merge /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/output.xml /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/log_2/output.xml

pybot -v app_path:/Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/huaxin/apps/android_xjb_3_0/hxxjb-ptest-latest.apk \
-v platform_version:6.0 \
-v device_id:ac3997d9 \
-v port:4725 \
-v package_name:com.shhxzq.xjb \
-v account:XJB_CI_USER_2 \
-R /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/log_2/output.xml \
-d /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/log_3 /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/huaxin/ui_android_xjb_3_0_unit_test/ui_android_xjb_3_0_tests.txt
rebot -d /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/ -o /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/output --merge /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/output.xml /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/$JOB_NAME/log_3/output.xml

/bin/cp -r /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/${JOB_NAME}/huaxin/*.jpg /Users/linkinpark/jenkins_workspace/jenkins_workspace/workspace/${JOB_NAME}