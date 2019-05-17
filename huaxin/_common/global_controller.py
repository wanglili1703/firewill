from _common.global_config import GlobalConfig


class GlobalController:
    DB_CONNECT = GlobalConfig.HuaXinMySql.DBC_UAT
    RESTFUL_CONNECT = GlobalConfig.RestfulEnvironment.HUAXIN_XJB_UAT
    RESTFUL_CONNECT_UAT = GlobalConfig.RestfulEnvironment.HUAXIN_XJB_UAT
    RESTFUL_CMS = GlobalConfig.RestfulEnvironment.HUAXIN_CMS_UAT
    XJB_CONNECT = GlobalConfig.XjbApp.Xjb_App_3_0_CI
    BEIDOU_CONNECT = GlobalConfig.HuaXinMySql.DBC_BEIDOU

