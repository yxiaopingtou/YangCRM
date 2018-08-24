from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import json,re
from kingadmin.sites import site
from kingadmin import app_setup
from kingadmin import modelForm_handle
from crm.permission import check_permission

app_setup.kingadmin_auto_discover()
print("sites:",site.enabled_admins)

# Create your views here.

@login_required
def king_admin(req):

    return render(req,"kingadmin_html/model_table.html",{"site":site})


@check_permission
@login_required
def table_obj_list(req,app_name,model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    querysets = admin_class.model.objects.all()

    querysets,filter_condition = get_filter_list(req,querysets)
    admin_class.filter_condition = filter_condition

    querysets,order_dict = get_orderby_list(req,querysets,admin_class)
    admin_class.order_dict = order_dict

    querysets,search_content = search_list(req,querysets,admin_class)
    admin_class.search_content = search_content

    per_page = admin_class.list_per_page
    querysets,page_cur = get_page_list(req,querysets,per_page)

    if req.method == "POST":
        delete_objs_id = req.POST.get("delete_id")
        if delete_objs_id:
            id_list = re.findall("\d+",delete_objs_id)
            print(id_list)
            querysets_post = admin_class.model.objects.filter(id__in=id_list)
            querysets_post.delete()
        else:
            action = req.POST.get("action")
            selected_id = json.loads(req.POST.get("selected_id"))
            selected_list = []
            for id in selected_id:
                selected_list.append(id[0])
            print(selected_list)
            querysets_post = admin_class.model.objects.filter(id__in=selected_list)
            action_func = getattr(admin_class,"%s"%action)
            return action_func(req,querysets_post)
    #print(admin_class.action_form)
    return render(req,'kingadmin_html/table_mesg.html',{"admin_class":admin_class,
                                                        "queryset":querysets,
                                                        "page_cur":page_cur})



@check_permission
@login_required
def get_filter_list(req,querysets):
    filter_condition = {}
    for key,val in req.GET.items():
        if key in ("_page","_O","search"):
            continue
        if val:
            filter_condition[key] = val
    print("filter_condition:",filter_condition)
    filter_queryset = querysets.filter(**filter_condition)

    return filter_queryset,filter_condition

def get_page_list(req,queryset,per_page):
    page_num = req.GET.get("_page")
    if per_page:
        p = Paginator(queryset,per_page)
        page_cur = p.get_page(page_num)
        queryset = page_cur.object_list
        return queryset,page_cur
    else:
        return queryset,''



@check_permission
@login_required
def get_orderby_list(req,querysets,admin_class):
    order_num = req.GET.get("_O")
    print("order_num:",order_num)
    order_dict = {}
    if order_num:
        order_name = admin_class.list_display[abs(int(order_num))-1]
        order_name_n = order_name
        if order_num.startswith('-'):
            order_name_n = '-%s'%order_name
        querysets =  querysets.order_by(order_name_n)
        order_dict[order_name] = order_num
        return querysets,order_dict
    else:
        return querysets,order_dict




@check_permission
@login_required
def search_list(req,querysets,admin_class):
    search_content = req.GET.get("search")
    if search_content:
        q = Q()
        q.connector = "OR"
        for search_column in admin_class.search_fields:
            search_column = "%s__contains"%search_column
            print(search_column)
            q.children.append((search_column,search_content))

        querysets= querysets.filter(q)
        print(querysets)
        return querysets,search_content
    else:
        search_content = ''
        return querysets,search_content

@check_permission
@login_required
def table_obj_change(req,app_name,model_name,data_id):
    admin_class = site.enabled_admins[app_name][model_name]
    change_obj = admin_class.model.objects.get(id=data_id)
    dynamic_form = modelForm_handle.create_model_form(admin_class)
    if req.method == "GET":
        form_obj = dynamic_form(instance=change_obj)
    elif req.method == "POST":
        form_obj = dynamic_form(instance=change_obj,data = req.POST)

        if form_obj.is_valid():
            form_obj.save()
            return redirect("/kingadmin/%s/%s/" % (app_name, model_name))

    return render(req,"kingadmin_html/table_change.html",locals())

@check_permission
@login_required
def table_obj_add(req,app_name,model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    dynamic_form = modelForm_handle.create_model_form(admin_class,form_add=True)
    if req.method == "GET":
        form_obj = dynamic_form()
    elif req.method == "POST":
        form_obj = dynamic_form(data=req.POST)
        print(form_obj.is_valid())
        if form_obj.is_valid():
            form_obj.save()
            print('wwwwwwwww')
            return redirect("/kingadmin/%s/%s/" % (app_name, model_name))

    return render(req, "kingadmin_html/table_add.html", locals())

@check_permission
@login_required
def table_obj_delete(req,app_name,model_name,data_id):
    admin_class = site.enabled_admins[app_name][model_name]
    delete_objs = admin_class.model.objects.filter(id=data_id)
    print(delete_objs)
    if req.method == "POST":
        delete_objs.delete()
        return redirect("/kingadmin/%s/%s"%(app_name,model_name))

    return render(req,"kingadmin_html/table_delete.html",locals())








def acc_login(req):


    error_msg = ""
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        user = authenticate(username=username,password=password)
        if user:
            login(req,user)
            for role in req.user.role.all().select_related():
                for menu in role.menu.select_related():
                    print(menu.name,menu.url_type,menu.url_name)
            return redirect(req.GET.get('next','/'))
        else:
            error_msg = "用户名或密码错误"
            return render(req,"login.html",{"error_msg":error_msg})

    else:
        return render(req, "login.html", {"error_msg": error_msg})

def acc_logout(req):
    logout(req)
    return redirect("/login/")