from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout
from users.models import Image
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from users.forms import UserCreationForm


def signup(request):
    if request.method == "POST":

        user = User()
        userForm = UserCreationForm(request.POST, instance=user)
        if userForm.is_valid():
            userData = userForm.cleaned_data
            user.username = userData['username']
            user.set_password(userData['password1'])
            userForm.save()

            user_auth = authenticate(username=userData['username'], password=userData['password1'])
            auth_login(request, user_auth)

            return redirect("/users/images/index")

        return render(request, template_name="users/register.html",
                      context={"userForm": userForm})

    return render(request, template_name="users/register.html", context={"userForm": UserCreationForm()})


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password1', '')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/users/images/index")
        else:
            args['login_error'] = "The user is not found"
            return render_to_response('users/login.html', args)
    else:
        return render_to_response('users/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def index_view(request):
    return render(request, 'users/image_index.html')


@login_required
@csrf_exempt
def images_view(request):
    if request.method == 'POST':

        image_url = request.POST['url']

        image = Image.objects.create(
            user=request.user,
            url=image_url
        )

        return JsonResponse({
            'url': image.url
        })

    elif request.method == 'GET':
        images = Image.objects.filter(user=request.user).values('id', 'url')
    return JsonResponse(list(images), safe=False)
