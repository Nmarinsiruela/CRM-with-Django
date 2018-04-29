from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserCreateForm, UserUpdateForm

from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)
def index(request):
    user_list = User.objects.order_by('-id')[:5]
    context = {'user_list': user_list}
    return render(request, 'users/index.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete(request, user_selected_id):
    user_selected = get_object_or_404(User, pk=user_selected_id)
    if request.user.id is not user_selected.id:
        user_selected.delete()  
    return HttpResponseRedirect(reverse('users:index'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def user_detail(request, user_selected_id):
    user_selected = get_object_or_404(User, pk=user_selected_id)
    return render(request, 'users/detail.html', {'user_selected': user_selected})

@login_required
@user_passes_test(lambda u: u.is_staff)
def create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return HttpResponseRedirect(reverse('users:index'))
    else:
        form = UserCreateForm() 

    return render(request, 'users/create.html', {'form': form}) 

@login_required
@user_passes_test(lambda u: u.is_staff)
def update(request, user_selected_id=None):
    user_selected = get_object_or_404(User, pk=user_selected_id)
    if request.method == "POST":
        form = UserUpdateForm(data=request.POST, instance=user_selected)
        if form.is_valid():
            user_up = form.save(commit=False)
            user_up.save()
            return HttpResponseRedirect(reverse('users:detail', args=[user_selected_id]))
    else:
        form = UserUpdateForm(instance=user_selected)

    return render(request, 'users/update.html', {'form': form, 'user_selected': user_selected})
