from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import conf
from crm import models,modelform_handle
from crm.permission import check_permission
import os,datetime,json

# Create your views here.

@login_required
def index(req):

    return render(req, "crm/homepage.html")

@check_permission
@login_required
def stu_enrollment(req):
    customer_list = models.Customer.objects.all()
    class_list = models.ClassList.objects.all()
    enrollment_agreed = models.Enrollment.objects.filter(contract_agreed=True)

    if req.method == "POST":
        customer_id = req.POST.get("customer_id")
        class_id = req.POST.get("class_id")
        has_enrollment = models.Enrollment.objects.filter(Q(customer_id=customer_id)&Q(class_grade_id=class_id)).count()
        if has_enrollment:
            enrollment_error="此客户报名表已经存在！"
            enroll_obj = models.Enrollment.objects.filter(Q(customer_id=customer_id) & Q(class_grade_id=class_id))
            enrollment_url = enroll_obj.values("Enrollment_url")[0]
        else:
            enroll_obj  = models.Enrollment.objects.create(customer_id=customer_id,class_grade_id=class_id,consultant_id=req.user.userprofile.id)
            has_enrolled = models.Student.objects.filter(customer_id = customer_id).count()
            if has_enrolled:
                enroll_error = "此客户已经报名！"
            else:
                enrollment_url = "http://localhost:8000/crm/enrollment/%s/"%(enroll_obj.id)
                enroll_obj.Enrollment_url=enrollment_url
                enroll_obj.save()


    return render(req, "crm/stu_enrollment.html", locals())


@check_permission
@login_required
def enrollment(req,enroll_obj_id):
    enroll_obj = models.Enrollment.objects.filter(id=enroll_obj_id)[0]


    file_upload_path = os.path.join(conf.settings.BASE_DIR, "file_upload", "enrollment", enroll_obj_id)
    if not os.path.isdir(file_upload_path):
        os.mkdir(file_upload_path)
    file_upload_list = os.listdir(file_upload_path)
    if enroll_obj.contract_agreed:
        return HttpResponse("已成功提交，正等待审核....")
    elif enroll_obj.contract_approved:
        return HttpResponse("审核通过.")
    if req.method == "POST":
        print(req.POST)
        customer_obj = modelform_handle.CustomerForm(instance=enroll_obj.customer, data=req.POST)
        if not req.POST.get("contract_agreed"):
            is_agreed_error = "你还没有同意合同！"
        elif not file_upload_list:
            is_upload_file = "请上传相关证件文件！"
        else:
            if customer_obj.is_valid():
                print("yes")
                enroll_obj.contract_agreed = True
                enroll_obj.contract_agreed_date = datetime.datetime.now()
                enroll_obj.save()
                customer_obj.save()
                return HttpResponse("已成功提交，正等待审核....")
    else:
        customer_obj = modelform_handle.CustomerForm(instance=enroll_obj.customer)

    return render(req, "crm/enrollment.html", locals())


@check_permission
@login_required
def enrollment_file_upload(req,enroll_obj_id):
    response_dict = {"status":True,"err_msg":None}
    if req.method == "POST":
        file_obj = req.FILES.get("file")
        file_upload_path = os.path.join(conf.settings.BASE_DIR,"file_upload","enrollment",enroll_obj_id)
        if not os.path.isdir(file_upload_path):
            os.mkdir(file_upload_path)

        if len(os.listdir(file_upload_path)) <= 2:
            with open(os.path.join(file_upload_path,file_obj.name),"wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

        else:
            response_dict["err_msg"]='max upload limit is 2'
            response_dict["status"]=False
            return HttpResponse(json.dumps(response_dict))

        return HttpResponse(json.dumps(response_dict))


@check_permission
@login_required
def enrollment_approved(req,enrollment_id):
    enroll_obj = models.Enrollment.objects.filter(id=enrollment_id)[0]
    enroll_form = modelform_handle.EnrollmentForm(instance=enroll_obj)
    file_upload_path = os.path.join(conf.settings.BASE_DIR, "file_upload", "enrollment", enrollment_id)
    file_upload_list = os.listdir(file_upload_path)
    if req.method == "POST":
        if not req.POST.get("reject"):
            if req.POST.get("contract_approved") != "2":
                approved_error = "请确认已审核"
            else:
                enroll_form = modelform_handle.EnrollmentForm(instance=enroll_obj,data=req.POST)
                if enroll_form.is_valid():
                    enroll_obj.contract_approved_date = datetime.datetime.now()
                    enroll_obj.save()
                    student = models.Student.objects.create(customer_id=enroll_obj.customer.id)
                    student.class_grades.add(enroll_obj.class_grade.id)
                    student.save()
                    return HttpResponse("审核完成!")
        else:
            return HttpResponse("驳回完成!")


    return render(req, "crm/enrollment_approved.html",locals())
