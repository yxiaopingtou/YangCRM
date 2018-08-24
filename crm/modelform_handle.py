from django.forms import ModelForm
from django import forms
from crm import models

class EnrollmentForm(ModelForm):
    class Meta:
        model = models.Enrollment
        fields="__all__"
        exclude=["contract_approved_date"]
        readonly_list = ["customer","class_grade","consultant","contract_agreed","contract_agreed_date","Enrollment_url"]

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj =  cls.base_fields[field_name]
            if field_name in cls.Meta.readonly_list:
                field_obj.widget.attrs.update({'disabled': 'true','class':'form-control'})
            else:
                field_obj.widget.attrs.update({'class':'form-control'})

        return ModelForm.__new__(cls)

    def clean(self):
        """判断只读字段是否被修改"""

        if self.errors:
            forms.ValidationError(("Please fix errors before re-submit."))
        if self.instance.id is not None:
            for field in self.Meta.readonly_list:
                if field == "consult_courses":
                    instance_data = getattr(self.instance,field)
                    cleaned_data = self.cleaned_data.get(field)
                    if instance_data != cleaned_data:
                        self.add_error(field,"Readonly Field: field should be '{value}' ,not '{new_value}' ".\
                                             format(**{'value':instance_data,'new_value':cleaned_data}))

class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields="__all__"
        exclude=["consult_content","consult_courses"]
        readonly_list = ["contact_type","source","referral_from","status","consultant"]

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj =  cls.base_fields[field_name]
            if field_name in cls.Meta.readonly_list:
                field_obj.widget.attrs.update({'disabled': 'true','class':'form-control'})
            else:
                field_obj.widget.attrs.update({'class':'form-control'})

        return ModelForm.__new__(cls)

    def clean(self):
        """判断只读字段是否被修改"""

        if self.errors:
            forms.ValidationError(("Please fix errors before re-submit."))
        if self.instance.id is not None:
            for field in self.Meta.readonly_list:
                if field == "consult_courses":
                    instance_data = getattr(self.instance,field)
                    cleaned_data = self.cleaned_data.get(field)
                    if instance_data != cleaned_data:
                        self.add_error(field,"Readonly Field: field should be '{value}' ,not '{new_value}' ".\
                                             format(**{'value':instance_data,'new_value':cleaned_data}))
