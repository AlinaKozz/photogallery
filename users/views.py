from django import forms as dj_forms
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout
from users import forms
from users.models import Image
from users.forms import ImageForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=dj_forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=dj_forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise dj_forms.ValidationError(
                self.error_messages['password_mismatch'], code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


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
    user_images = Image.objects.filter(user=request.user)
    image_form = ImageForm()
    return render(request, 'users/image_index.html', context={'image_form': image_form})


@login_required
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
            user=request.user,
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