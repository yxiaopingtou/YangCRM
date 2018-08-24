from django.shortcuts import render,redirect
from django.conf import settings
from django.urls import resolve
from crm.permission_url_name import perm_dic


def perm_check(*args,**kwargs):
    request = args[0]
    request_url_obj = resolve(request.path)
    request_url_name = request_url_obj.url_name
    match_results = [None,]
    match_key = None
    # if request.user.is_authenticated() is False:
    #     return redirect(settings.LOGIN_URL)

    for permission_key,permission_url in perm_dic.items():
        permission_url_name = permission_url[0]
        permission_url_method = permission_url[1]
        permission_url_fields = permission_url[2]
        permission_url_field_data = permission_url[3]
        if len(permission_url)>4:
            permission_url_func = permission_url[4]
        else:
            permission_url_func = None


            if request_url_name == permission_url_name:
                if request.method == permission_url_method:
                    request_method = getattr(request, permission_url_method)

                    field_match = False
                    for permission_field in permission_url_fields:
                        if request_method.get(permission_field,None):
                            field_match = True
                        else:
                            field_match = False
                            print("field is not match..")
                    else:
                        field_match = True

                    field_data_match = False
                    for k,v in permission_url_field_data:
                        if request_method.get(k,None) == str(v):
                            field_data_match = True
                        else:
                            field_data_match = False
                            print("field_data is not match..")
                            break
                    else:
                        field_data_match = True


                    if permission_url_func:
                        url_func_match = permission_url_func(request)
                    else:
                        url_func_match = True

                    match_results = [field_match,field_data_match,url_func_match]
                    if all(match_results):
                        match_key = permission_key
                        break

    if all(match_results):
        app_name, per_name = match_key.split("_",1)
        print("--->matched ", match_results, match_key)
        print(app_name, per_name)
        perm_obj = '%s.%s' % (app_name, match_key)
        print("perm str:", perm_obj)
        print(request.user.has_perm(perm_obj))
        if request.user.has_perm(perm_obj):
            print('当前用户有此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False

    else:
        print("未匹配到权限项，当前用户无权限")





def check_permission(func):
    def inner(*args,**kwargs):
        if perm_check(*args,**kwargs):
            return func(*args,**kwargs)
        else:
            request = args[0]
            return render(request,"error.html")
    return inner