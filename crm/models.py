from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64, verbose_name='姓名')
    role = models.ManyToManyField('Role')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


    class Meta:
        permissions = {
            ('crm_table_obj_list','可以查看kingadmin下的customer表')
        }












# class UserProfile(models.Model):
#     """用户表"""
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     name = models.CharField(max_length=64,verbose_name='姓名')
#     role = models.ManyToManyField('Role')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "用户表"
#         verbose_name_plural = "用户表"













class Customer(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=64,default=None)
    contact_type_choice = ((0,'qq'),(1,'微信'),(2,'手机'))
    contact_type = models.SmallIntegerField(choices=contact_type_choice,default=0)
    contact = models.CharField(max_length=64,unique=True,verbose_name = '手机号或qq号')
    source_choice = ((0,'QQ群'),
                     (1,'51CTO'),
                     (2,'百度推广'),
                     (3,'知乎'),
                     (4,'转介绍'),
                     (5,'其它'),
                     )
    source = models.SmallIntegerField(choices=source_choice)
    referral_from = models.ForeignKey('self',blank=True,null=True,verbose_name = '转介绍',on_delete=models.CASCADE)
    consult_courses = models.ManyToManyField('Course',verbose_name = '咨询课程')
    consult_content = models.TextField(verbose_name="咨询内容")
    status_choice = ((0,'未报名'),
                     (1, '已报名'),
                     (2, '已退学'),
                     )
    status = models.SmallIntegerField(choices=status_choice)
    consultant = models.ForeignKey('UserProfile',verbose_name = '课程顾问',on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "客户信息表"
        verbose_name_plural = "客户信息表"

class CustomerFollowUp(models.Model):
    """客户跟进表"""
    customer = models.ForeignKey('Customer',on_delete=models.CASCADE)
    content = models.TextField(verbose_name="跟踪内容")
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE,verbose_name='跟进人')
    status_choices = ((0, '近期无报名计划'),
                      (1, '一个月内报名'),
                      (2, '2周内内报名'),
                      (3, '已报名'),
                      )
    status = models.SmallIntegerField(choices=status_choices)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "客户跟进表"
        verbose_name_plural = "客户跟进表"

class Student(models.Model):
    """学员表"""
    customer = models.OneToOneField('Customer',on_delete=models.CASCADE)
    class_grades = models.ManyToManyField('ClassList')

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name = "学员表"
        verbose_name_plural = "学员表"

class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64,verbose_name='课程名称',unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='课程周期(月)',default=5)
    online = models.TextField(verbose_name='课程大纲')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程表"
        verbose_name_plural = "课程表"

class ClassList(models.Model):
    """班级表"""
    branch = models.ForeignKey('Branch',on_delete=models.CASCADE)
    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    class_type_choice = ((0,'脱产'),
                         (1,'周末'),
                         (2,'网络'),
                         )
    class_type = models.SmallIntegerField(choices=class_type_choice,default=0)
    semester = models.SmallIntegerField(verbose_name='学期')
    teacher = models.ManyToManyField('UserProfile',verbose_name='讲师')
    start_date = models.DateField(verbose_name='开班日期')
    graduate_date = models.DateField(verbose_name='毕业日期',blank=True,null=True)
    contract = models.ForeignKey("Contract",on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return "%s(%s)期" %(self.course.name,self.semester)

    class Meta:
        unique_together=('branch','course','class_type','semester')
        verbose_name = "班级表"
        verbose_name_plural = "班级表"


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length=64, unique=True)
    addr = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "校区表"
        verbose_name_plural = "校区表"

class CourseRecord(models.Model):
    """上课记录表"""
    teacher = models.ManyToManyField('UserProfile', verbose_name='讲师')
    class_grade = models.ForeignKey('ClassList',on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name='课程节次')
    title = models.CharField('本节主题',max_length=64)
    content  = models.TextField('本节内容')
    has_homework = models.BooleanField('本节有作业',default=True)
    homework = models.TextField('作业内容',blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return "%s第(%s)节" %(self.class_grade,self.day_num)

    class Meta:
        unique_together = ('class_grade','day_num')
        verbose_name = "上课记录表"
        verbose_name_plural = "上课记录表"

class StudyRecord(models.Model):
    """学习记录表"""
    course_record = models.ForeignKey("CourseRecord", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)

    score_choices = ((100, "A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (-50, "D"),
                     (0, "N/A"),  # not avaliable
                     (-100, "COPY"),  # not avaliable
                     )
    score = models.SmallIntegerField(choices=score_choices, default=0)
    show_choices = ((0, '缺勤'),
                    (1, '已签到'),
                    (2, '迟到'),
                    (3, '早退'),
                    )
    show_status = models.SmallIntegerField(choices=show_choices, default=1)
    note = models.TextField("成绩备注", blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.course_record, self.student, self.score)

    class Meta:
        verbose_name = "学习记录表"
        verbose_name_plural = "学习记录表"

class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64,unique=True)
    menu = models.ManyToManyField('Menu',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = "角色表"


class Menu(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64, unique=True)
    url_type_choice = ((0,'absolute'),(1,'dynamic'))
    url_type = models.SmallIntegerField(choices=url_type_choice)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name','url_name')
        verbose_name = "动态菜单"
        verbose_name_plural = "动态菜单"


class Enrollment(models.Model):
    """学员报名表"""
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    class_grade = models.ForeignKey("ClassList",on_delete=models.CASCADE)
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False,blank=True,null=True)
    contract_approved = models.BooleanField(default=False,blank=True,null=True)
    contract_agreed_date = models.DateTimeField(blank=True,null=True)
    contract_approved_date = models.DateTimeField(blank=True,null=True)
    Enrollment_url = models.CharField(max_length=64,blank=True,null=True)

    class Meta:
        unique_together=("customer","class_grade")

class Contract(models.Model):
    """合同表"""
    name = models.CharField(max_length=64)
    content = models.TextField()

    date = models.DateTimeField(auto_now_add=True)


class PaymentRecord(models.Model):
    """存储学员缴费记录"""
    enrollment = models.ForeignKey("Enrollment", on_delete=models.CASCADE)
    payment_type_choices = ((0, '报名费'), (1, '学费'), (2, '退费'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices, default=0)
    amount = models.IntegerField("费用", default=500)
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.enrollment

