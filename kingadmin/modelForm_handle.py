from django.forms import ModelForm


def create_model_form(admin_class,form_add=False):
    class Meta:
        model = admin_class.model
        fields = "__all__"
        if not form_add:
            exclude = admin_class.readonly_fields
            admin_class.form_add = False
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj =  cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})

        return ModelForm.__new__(cls)

    dynamic_form = type('dynamic_model_form',(ModelForm,),{"Meta":Meta,"__new__":__new__})

    return dynamic_form