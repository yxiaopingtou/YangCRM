from kingadmin.admin_base import BaseKingAdmin
from crm import models
from kingadmin.sites import site
print('crm kingadmin ............')

class CustomerAdmin(BaseKingAdmin):
    list_display = ['name',
                    'contact_type',
                    'contact',
                    'source',
                    'referral_from',
                    'consult_content',
                    'status',
                    'consultant',
                    'date']
    list_filter = ['contact_type', 'status', 'source', 'consultant', 'date']
    search_fields = ['name','contact']
    readonly_fields = ['status', 'consultant']
    filter_horizontal = ['consult_courses', ]
    action_form = ['update_status',]
    def update_status(self,request,querysets):
        querysets.update(status=1)

class CourseAdmin(BaseKingAdmin):
    list_display = ['name',
                    'price',
                    'period',
                    'online']
    search_fields = ['name', 'period']
    action_form = ['update_status', ]

    def update_status(self, request, querysets):
        querysets.update(status=1)



site.register(models.Customer, CustomerAdmin)
site.register(models.CustomerFollowUp)
site.register(models.UserProfile)
site.register(models.Course,CourseAdmin)
site.register(models.Menu)
site.register(models.Student)
site.register(models.ClassList)
site.register(models.Enrollment)
site.register(models.Contract)
