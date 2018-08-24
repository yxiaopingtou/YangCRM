from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate


# Create your views here.

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