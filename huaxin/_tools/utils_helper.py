# coding: utf-8
from jpype import *
import os.path

print os.path.abspath('.')

# jarpath = os.path.join(os.path.abspath('.'), /Users/wanglili/Downloads/apache-jmeter-3.0/dependencies/')
# print jarpath
jvmpath = getDefaultJVMPath()
print jvmpath
startJVM(jvmpath, "-ea", "-Djava.class.path=%s" % ('/Users/wanglili/signature/out/artifacts/signature_jar/signature.jar'))

#
# # ubuntu 中startJVM("/home/geek/Android/jdk1.6.0_43/jre/lib/i386/server/libjvm.so","-ea", "-Djava.class.path=%s" % (jarpath + 'XXX.jar'))
generate_signature = JClass("GenerateSignature")
jd = generate_signature()

#
# jd = JPackage("com.shhxzq.kernel.security").SecurityUtils  # 两种创建jd的方法

privateKey = "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCsw0Ok68hlWDicqwfLSR+NiOdmVjYx2VekXZiZT7nLw4qVYsbOhBRUC2" \
             "fE2XNPFNBcaeKuZmFrpGSDqSVs0goPi7xiQSbGQep2EOeq87jk3ZsKXAdtPvX1XmHTepY5+xmZBMQbVah1Vtzjjlf/iFjcyPupACCALz0Ylez" \
             "7u9pv8m3AY/i0YU08xPUx9a19IUzj24xEr2K2kYe1J7edKI57BSaOYPgOCxj3msVk+Gj6cUCF+dB0AX8ECROh0QWEGLsRobQt4oUhAwusPN0kgQQg9" \
             "Uy6M/UjQEQotn86JRKPwvXJcyq53EoFvgqm/PtzWvWWbxHmVdj19vEM/n9GpQmnAgMBAAECggEAUwxKqCzv2Efgbu+If6BXGqKFGhy3UJ86Ejkr8" \
             "gbxOZJ2O/mPuBal7wDMkUQ2uf03bDU6UrvEeQo9h0z4QKd3TqHNnS3UhdmJ69eUhglDCEG/FevHZiyt75W/UPnM3XJni7dOzhUPNdjbtkfm5V+V2" \
             "AyFbWgyN2x94iOwGBLlnooQN+RsQoVliXXygbYF6XYwsWmbMlB9mRhoEzonzmsmBo2nnOrAARjNtw4tjmCGkI9K67QXE6pxK8ogtxteGduk4xDnGv" \
             "VD2hMc2HUB6qtTYZZlefzOOXadmSeL8FhzKUD5H5es5mYKLIuYGfr9wV6yLmf4OkAMM45hXHrNMQrLgQKBgQDniHuxffyqpDr5WnEIKDpEBG7I43D" \
             "mM0rle28GbawL/juGg36LCsZgDhlwlgCM4wF758JrOI0Oyvtj3VJav6DIsTTsZl0G9TliY4zKdZgaEHdb6Axej0vQa1QMS201C+HTT+HaQz4s4eF6g" \
             "Lg/i6LcXUF50zniMG5Fy7BpUiexcwKBgQC/BOdVlnX94DbOiMokXFhTT0jGyxyNmM9FK4gbVpjRIgHOgIdwr9trbJgL5d3RCAwVRKTYfiPrbTpPao5" \
             "bSSKJdwAikEtivkIhEGBKEoYeWwqPTm4/79YZ5rAG02Ed2928JfYayF+SZI/yRARQSDgielz+5g6FG+hzQqLoOTPp/QKBgA+0HRebwPBd9TYGYVY5T" \
             "EJivpTXgEfMwM6xwYUBGUMy+hyUfJe3ol7PdgBB3EWx+97IiFI3YrHXKJfMYhKPnrsd8cX652JabYrzz4/HzAowhbfxFC2xsGWxceDnmL+ZT7bCW0" \
             "Ivf18R7vYdFuIQeXpSxOcbYXiq6j/Hoe5yyQhrAoGAASO/WZRfOdeHnC3WvubKJB0Z+w2lKvcZbXk4A6m9manRRvEfXb2+2mI4egGyFBgvMkVJkn0W" \
             "K8ZoDac+GC9UhGtwVcR0nq8x586YNHjt0eqLIpW+NKVyqo7kx/Wk46+3H/M+B6TgZRgyf6iGOhBkPVhri53FwmeLOHzSSf5lX+UCgYAt+fOZA/h/" \
             "lG6EB/nnvbANCvVrXGUJkp8oGJKS9uIUUdk3AU3tB9JQfnwE0y676nI8m9DtOUoeee8N543JKKckMtNtzbYe+/yDvR8mIow3DwBSb7kQEYqWJ0+DWP" \
             "LVZ66MYOAMXmaj7bB1MmW8FwZl+/M4qV6wSt6jK/qD3JfqXg=="

# src = "cardNo=6217850800053330077&apDate=20170317&apTime=103000&amount=0.00"
# jprint = java.lang.System.out.println
# jprint(jd.sign(privateKey, src))
signature = jd.generate("6235954021000345789", "20170317", "0.00")

# print signature
# JDClass = JClass("com.shhxzq.kernel.security.SecurityUtils.sign(privateKey, src)")

shutdownJVM()
