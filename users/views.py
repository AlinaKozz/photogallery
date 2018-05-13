from django import forms as dj_forms
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext
# from django.urls import reverse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout
from users import forms
from users.models import Image
from users.forms import ImageForm
from django.contrib import auth


class UserForm(forms.ModelForm):
    username = dj_forms.CharField(max_length=30)
    password1 = forms.CharField(widget=dj_forms.PasswordInput, label="Password", min_length=6, max_length=15)
    password2 = forms.CharField(widget=dj_forms.PasswordInput, label="Enter your password again")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_pass2(self):
        if (self.cleaned_data["password2"] != self.cleaned_data.get("password1", "")):
            raise dj_forms.ValidationError("Passwords do not match")
        return self.cleaned_data["password2"]


def signup(request):
    if request.method == "POST":

        user = User()
        userForm = UserForm(request.POST, instance=user)
        if userForm.is_valid():
            userData = userForm.cleaned_data
            user.username = userData['username']
            user.set_password(userData['password1'])
            userForm.save()

            user_auth = authenticate(username=userData['username'], password=userData['password1'])
            auth_login(request, user_auth)

            return HttpResponseRedirect("/users/images/index")

        return render(request, template_name="users/register.html",
                      context={"userForm": userForm})

    return render(request, template_name="users/register.html", context={"userForm": UserForm()})


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/users/images/index")
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('users/login.html', args)
    else:
        return render_to_response('users/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def index_view(request):
    image_form = ImageForm()
    return render(request, 'users/image_index.html', context={'image_form': image_form})


@csrf_exempt
def images_view(request):
    if request.method == 'POST':
        image_form = ImageForm(request.POST)

        if not image_form.is_valid():
            return JsonResponse({'errors': image_form.errors})

        image_url = request.POST['url']
        description = request.POST['description']
        # geolocation = request.POST['geolocation']

        image = Image.objects.create(
            user_id=1,  # request.user.id
            description=description,
            geolocation='Minsk',
            url=image_url
        )

        return JsonResponse({
            'url': image.url
        })
    elif request.method == 'GET':
        images = Image.objects.values('id', 'url', 'description')
        return JsonResponse(list(images), safe=False)
