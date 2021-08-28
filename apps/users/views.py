from django.shortcuts import render , redirect
from .models import validaremail , Users , Userslevels
import bcrypt
from django.contrib import messages
from apps.wall.models import messages as Messages , comments
# Create your views here.

def index(request):
    return render (request,'login/index.html')

def signin(request):
    if 'id' in request.session:
        return redirect("dashboard")
    if request.method == 'POST':
        email = request.POST["email"]
        usuario = validaremail(email=email)
        validacionpw = None
        if usuario:
            validacionpw = bcrypt.checkpw(request.POST["password"].encode(), usuario.password.encode())
        if validacionpw:
            request.session["id"] = usuario.id
            return redirect("dashboard")
        messages.error(request, "La contraseña y/o email no son validos", "loginerror")
    return render(request , "login/login.html")

def register(request):
    if request.method == "POST":
        erros = Users.objects.basic_validator(request.POST)
        if len(erros) >0:
            for key, value in erros.items():
                messages.error(request, value, key)
            return render(request,"login/register.html")
        if not Userslevels.objects.all():
            Userslevels.objects.create(name="admin",level=9)
            Userslevels.objects.create(name="normal",level=1)
            print("Se creo los datos en level")
        if not Users.objects.all():
            level = Userslevels.objects.get(level=9)
            print("Usuario Admin")
        else:
            level = Userslevels.objects.get(level=1)
            print("Usuario normal")
        encrippw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = Users.objects.create(
        first_name = request.POST["fname"],
        last_name = request.POST["lname"],
        email = request.POST["email"].lower(),
        password = encrippw.decode(),
        user_level_id=level.id
        )
        user.save()
        if not "id" in request.session:
            request.session["id"] = user.id
        return redirect("dashboard")
    return render(request, "login/register.html")

def log_out(request):
    if "id" in request.session:
        del request.session["id"]
    return redirect("index_login")

def user_edit(request):
    if request.session['id']:
        context = {
            'user' : Users.objects.get(id=request.session['id'])
        }
        return render (request, 'dashboard/useredit.html', context)

def update_info(request):
    if request.method == 'POST':
        if request.session['id']:
            errors = Users.objects.basic_validator_updateinfo(request.POST,request.session['id'])
            if len(errors) >0:
                for key, value in errors.items():
                    messages.error(request, value, key)
                return redirect ("user_edit")
            user = Users.objects.get(id=request.session['id'])
            user.email = request.POST['email']
            user.first_name = request.POST['fname']
            user.last_name = request.POST['lname']
            user.save()
    return redirect ("dashboard")

def update_desc(request):
    if request.method == 'POST':
        if request.session['id']:
            errors = Users.objects.basic_validator_updatedesc(request.POST)
            if len(errors) >0:
                for key, value in errors.items():
                    messages.error(request, value, key)
                return redirect ("user_edit")
            user = Users.objects.get(id=request.session['id'])
            user.description = request.POST['description']
            user.save()
    return redirect ("dashboard")

def update_password(request):
    if request.method == 'POST':
        if request.session['id']:
            errors = Users.objects.basic_validator_updatepw(request.POST)
            if len(errors) >0:
                for key, value in errors.items():
                    messages.error(request, value, key)
                return redirect ("user_edit")
            user = Users.objects.get(id=request.session['id'])
            encrippw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user.password = encrippw.decode()
            user.save()
    return redirect("dashboard")

def remove_user(request, user_id):
    user = Users.objects.get(id=request.session['id'])
    if user.user_level.level == 9:
        if request.method == 'POST':
            userdelete = Users.objects.get(id=user_id)
            userdelete.delete()
        if request.method == 'GET':
            return render (request, "dashboard/userdelete.html")
    return redirect ("dashboard")

def new_user(request):
    return render (request,"dashboard/register.html")

def edit_user_info(request, user_id):
    user = Users.objects.get(id=request.session['id'])
    if user.user_level.level == 9:
        context ={
            'user' : Users.objects.get(id=user_id),
            'levels' : Userslevels.objects.all()
        }
        if request.method == 'POST':
            errors = Users.objects.basic_validator_updateinfo(request.POST,user_id)
            if len(errors) >0:
                for key, value in errors.items():
                    messages.error(request, value, key)
                return render (request, "dashboard/adminuseredit.html", context)
            user = Users.objects.get(id=request.session['id'])
            user.email = request.POST['email']
            user.first_name = request.POST['fname']
            user.last_name = request.POST['lname']
            user.user_level_id = request.POST['user_level']
            user.save()
            return redirect ("dashboard")
        return render (request, "dashboard/adminuseredit.html", context)
    return redirect ("dashboard")

def admin_update_password(request, user_id):
    if request.method == 'POST':
        user = Users.objects.get(id=request.session['id'])
        if user.user_level.level == 9:
            errors = Users.objects.basic_validator_updatepw(request.POST)
            if len(errors) >0:
                for key, value in errors.items():
                    messages.error(request, value, key)
                return redirect ("user_edit")
            user = Users.objects.get(id=user_id)
            encrippw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user.password = encrippw.decode()
            user.save()
    return redirect("dashboard")


def dashboard(request):
    if request.session['id']:
        user = Users.objects.get(id=request.session['id'])
        context = {
            'users' : Users.objects.all()
        }
        if user.user_level.level == 9:
            return render (request, 'dashboard/dashboardadmin.html', context)
        return render (request, 'dashboard/dashboarduser.html', context)
    return redirect ("signin_view")

def user_view(request, user_id):
    context = {
        'user' : Users.objects.get(id=user_id)
    }
    return render (request, "dashboard/showuser.html", context)

def message_new(request, user_id):
    if request.method == "POST":
        Messages.objects.create(
            message= request.POST['message'],
            user_id=user_id,
            user_message_id=request.session['id']
        )
    return redirect("dashboard")

def comment_new(request):
    if request.method == "POST":
        comments.objects.create(comment=request.POST['comment'],user_id=request.session['id'],message_id=request.POST['message_id'])
    return redirect("dashboard")