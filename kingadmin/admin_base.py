from django.shortcuts import render,redirect


class BaseKingAdmin():
    def __init__(self):
        if self.action_form_default[0] in self.action_form:
            return
        else:
            self.action_form.extend(self.action_form_default)


    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = ''
    readonly_fields = []
    filter_horizontal = []
    action_form = []
    action_form_default = ['delete_checked_action',]

    def delete_checked_action(self,request,querysets):
        delete_objs = querysets
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        delete_objs_id = []
        for obj in delete_objs:
            delete_objs_id.append(str(obj.id))
        return render(request,"kingadmin_html/table_delete.html",locals())