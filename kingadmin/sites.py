from kingadmin.admin_base import BaseKingAdmin

class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}

    def register(self,models_class,admin_class=None):
        app_name = models_class._meta.app_label   #获取该model所属的app名
        model_name = models_class._meta.model_name  #获取该model的类名
        if not admin_class:
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()
        admin_class.model = models_class

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class



site = AdminSite()