from django.template import Library
from django.utils.safestring import mark_safe
import datetime

register = Library()

@register.simple_tag
def get_data(obj,admin_class):
    """生成一条记录的html element"""

    ele = ""
    if admin_class.list_display:
        for column_name in admin_class.list_display:
            column_obj = admin_class.model._meta.get_field(column_name)#通过字符串column_name,获取model中同名字段对象
            if column_obj.choices:#判断该字段对象是否有choices属性
                column_data = getattr(obj,"get_%s_display" %column_name)() #获取该choices属性对应的值
            else:
                column_data = getattr(obj,column_name)
                if not column_data:
                    column_data=''
            td_ele = "<td>%s</td>" %column_data
            if admin_class.list_display.index(column_name) == 0:
                td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id,column_data)
            ele += td_ele
    else:
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, obj)

        ele += td_ele

    return mark_safe(ele)


@register.simple_tag
def filter_data(filter_column,admin_class):
    """生成一条数据的html element"""
    filter_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = "<select name='%s'>" % filter_column
        for choice in filter_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_condition:
                if str(choice[0]) == admin_class.filter_condition.get(filter_column):
                    selected = 'selected'
            option = "<option value='%s' %s>%s</option>" %(choice[0],selected,choice[1])
            filter_ele += option
        filter_ele += "</select>"
        return mark_safe(filter_ele)
    except AttributeError as e:
        filter_ele = "<select name='%s__gte'>" % filter_column
        time_now = datetime.datetime.now()
        time_list=(
            ('',"---------"),
            (time_now,"Today"),
            (time_now-datetime.timedelta(7),"一周"),
            (time_now.replace(day=1),"本月"),
            (time_now.replace(month=1 ,day=1),"本年"),
            ('',"ALL"),
        )
        for i in time_list:
            selected = ''
            if i[0]:
                time_to_str = i[0].strftime("%Y-%m-%d")
                if "%s__gte"%filter_column in admin_class.filter_condition:
                    if time_to_str == admin_class.filter_condition.get("%s__gte"%filter_column):
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" %(i[0].strftime("%Y-%m-%d"),selected,i[1])
            else:
                option = "<option value='%s' %s>%s</option>" %(i[0],selected,i[1])
            filter_ele += option
        filter_ele += "</select>"
        return mark_safe(filter_ele)

@register.simple_tag
def get_model_name(admin_class,get_model = False,get_table = False,add_or_change=True):
    """制作导航条"""
    app_name = "<a href=%s>%s</a>" %("/kingadmin/",admin_class.model._meta.app_label)
    model_name = "%s" %admin_class.model._meta.model_name
    model_name_a = "<a href='/kingadmin/%s/%s'>%s</a>" %(admin_class.model._meta.app_label,admin_class.model._meta.model_name,admin_class.model._meta.model_name)
    app_model = app_name+">"+model_name
    app_model_a_change = app_name+">"+model_name_a+">change"
    app_model_a_add = app_name+">"+model_name_a+">add"
    if not get_model:
        if not get_table:
            return mark_safe(app_model)
        else:
            if add_or_change:
                return mark_safe(app_model_a_change)
            else:
                return mark_safe(app_model_a_add)
    else:
        return model_name


@register.simple_tag
def get_page_ele(page_cur,admin_class):
    """分页"""
    list_per_page = admin_class.list_per_page
    ele = ""
    if list_per_page:

        if page_cur.has_previous():
            cur_pervious = page_cur.previous_page_number()
            ele += """<li class =""><a href="?_page=%s"> 上一页 </a></li>""" %cur_pervious

        for page in page_cur.paginator.page_range:
            active = ""
            if abs(page - page_cur.number) < int(list_per_page):
                if page == page_cur.number:
                    active = "active"
                page_ele="""<li class="%s"><a href="?_page=%s">%s</a></li>"""%(active,page,page)
                ele += page_ele

        if page_cur.has_next():
            cur_next = page_cur.next_page_number()
            ele += """<li class =""><a href="?_page=%s"> 下一页 </a></li>""" %cur_next

        return mark_safe(ele)
    else:
        return ''

@register.simple_tag
def get_display_href(iterm,admin_class):
    """获取list_display的href"""
    iterm_num = admin_class.list_display.index(iterm)+1
    order_position = "bottom"
    if iterm in admin_class.order_dict:
        if not admin_class.order_dict[iterm].startswith('-'):
            iterm_num = -iterm_num
            order_position = "top"

    filter_href = ""
    for k,v in admin_class.filter_condition.items():
        filter_href += "&%s=%s"%(k,v)

    ele = """<a href='?_O=%s%s&search=%s'>
                            %s
                            <span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>
                            </a>"""%(iterm_num,filter_href,admin_class.search_content,iterm,order_position)
    return mark_safe(ele)


@register.simple_tag
def get_readonly_data(field,form_obj):
    """获取只读数据"""
    column_obj = form_obj.instance._meta.get_field(field)
    if column_obj.choices:  # 判断该字段对象是否有choices属性
        column_data = getattr(form_obj.instance, "get_%s_display" % field)()

        return column_data
    else:
        return getattr(form_obj.instance,field)


@register.simple_tag
def get_horizontal_list(field_name,admin_class,form_obj):
    """获取filter_horizontal中没有selected的数据"""
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())

    selected_list = set(getattr(form_obj.instance,field_name).all())

    return obj_list-selected_list

@register.simple_tag
def get_horizontal_selected_list(field_name,form_obj):
    """获取filter_horizontal中被selected的数据"""

    selected_list = set(getattr(form_obj.instance,field_name).all())

    return selected_list


@register.simple_tag
def get_delete_url(form_obj,admin_class):
    """获取delete的url"""
    app_name = admin_class.model._meta.app_label
    model_name = admin_class.model._meta.model_name
    url = "/kingadmin/%s/%s/%s/delete" %(app_name,model_name,form_obj.instance.id)
    return url


@register.simple_tag
def get_related_delete_data(delete_obj,model_name,app_name):
    ele = "<ul>"

    related_list = delete_obj._meta.related_objects
    print(related_list)
    for related_Rel_obj in related_list:
        #print("related_Rel_obj",related_Rel_obj)
        if related_Rel_obj.get_internal_type() != "ManyToManyField":
            related_Rel_obj_name = related_Rel_obj.name
            related_obj = getattr(delete_obj, "%s_set" % related_Rel_obj_name).all()
            print("related_obj:", related_obj)
            ele += "<li><a href='/kingadmin/%s/%s/'>%s</a></li>"%(app_name,related_Rel_obj_name,related_Rel_obj_name)


            if related_obj:
                ele += "<ul>"
                for i in related_obj:
                    ele += "<li>%s</li>"%i
                    if related_Rel_obj_name != model_name:
                        print("i:",i)
                        app_name_related = i._meta.app_label
                        model_name_related = i._meta.model_name
                        ele += "%s"%get_related_delete_data(i,model_name_related,app_name_related)
                ele += "</ul>"

        else:
            related_Rel_obj_name = related_Rel_obj.name
            related_obj = getattr(delete_obj, "%s_set" % related_Rel_obj.name).all()
            ele += "<li><a href='/kingadmin/%s/%s/'>%s</a></li>" % (app_name, related_Rel_obj_name, related_Rel_obj_name)

            if related_obj:
                ele += "<ul>"
                for i in related_obj:
                    ele += "<li>%s</li>"%i
                ele += "</ul>"
    ele += "</ul>"

    return ele


@register.simple_tag
def get_back_url(delete_obj,app_name,model_name):
    return "/kingadmin/%s/%s/%s/change/"%(app_name,model_name,delete_obj[0].id)

