from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
import sys 
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import auth
from custom_user.forms import CustomUserForm
from searchmodel import SearchModel

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'wafwebapp/index.html', {})

def home(request):
    return render(request, 'wafwebapp/home.html', {})

def results(request):
    dep =request.GET.get('departure',None)
    arr =request.GET.get('arrival',None)
    if dep is not None and arr is not None:
        # =SearchModel(dep, arr)
        model  =SearchModel(dep, arr)
        if str(request.user) != 'AnonymousUser':
            print('seach by', request.user.id,request.user.email)
        else:
            print('seach by', request.user)
        searchresults = model.returnResult()
        print(searchresults)
        return render(request, 'wafwebapp/result.html', {'searchresults':searchresults})
    else:
        searchresults = ['valami gebasz']
        return render(request, 'wafwebapp/result.html', {'searchresult':searchresults})
    
@csrf_protect  
def login(request):
    
    args = {}
    print(request.user)
    print(str(request.user) == 'AnonymousUser')
    if str(request.user) == 'AnonymousUser':
        form = CustomUserForm()
        form.email =request.GET.get('subscribe',None)
        args['regform'] = form 
    else:
        args['user'] = request.user
    return render(request, 'wafwebapp/login.html',
                                 args)
@csrf_protect    
def registration(request):
    args = {}
    if request.method == 'POST':
        print('POST request')
        form = CustomUserForm(request.POST)
        if form.is_valid():
            print('form is valid')
            print(form.__dict__)
            print(form.cleaned_data)
            form.save()
            user = auth.authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            if user is not None:
                auth.login(request, user)
                return redirect('/waf')
        
    else:
        form = CustomUserForm()
        
        args['form'] = form    
    
    
    return render(request, 'wafwebapp/login.html',
                             args)
    
@csrf_protect
def auth_view(request):
    """
    After submitting the login request
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        return render(request, 'wafwebapp/index.html', {})
    else:
        return render(request, 'wafwebapp/index.html', {})
    
# HTTP Error 404
def page_not_found(request):
    response = render('wafwebapp/404.html',
    context_instance=RequestContext(request)
    )

    response.status_code = 404

    return response   

if __name__=='__main__':
    print('\n'.join(sys.path))