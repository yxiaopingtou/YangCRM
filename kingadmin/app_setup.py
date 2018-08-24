from django import conf



def kingadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        app_list = app_name.split('.')
        try:
            mod = __import__("%s.kingadmin" % app_list[0])
            print(111)
        except ImportError:
            pass

