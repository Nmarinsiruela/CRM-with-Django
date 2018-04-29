from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required, permission_required
from .models import Customer
from .forms import CustomerForm
 
# @permission_required('user.is_staff', login_url='/accounts/login')
@login_required
def index(request):
    '''
    Shows the latest 5 Customers created.
    '''
    latest_customer_list = Customer.objects.order_by('-id')[:5]
    context = {'latest_customer_list': latest_customer_list}
    return render(request, 'crm/index.html', context)

@login_required
def delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return HttpResponseRedirect(reverse('crm:index'))

@login_required
def customer_detail(request, customer_id):
    '''
    Access into the full customer information.
    '''
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'crm/detail.html', {'customer': customer})

@login_required
def create(request):
    '''
    Creates a new Customer.
    Requires: Name, Surname.
    Automatically generates: ID, Referenced_user.
    Optional: Profile picture.
    '''
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.referenced_user = request.user
            c.save()
            return HttpResponseRedirect(reverse('crm:index'))
    else:
        form = CustomerForm() 
    return render(request, 'crm/create.html', {'form': form}) 

@login_required
def update(request, customer_id=None):
    '''
    Creates an existing Customer.
    Requires: Name, Surname.
    Automatically generates: ID, Referenced_user.
    Optional: Profile picture.
    '''
    customer_selected = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(data=request.POST, instance=customer_selected)
        if form.is_valid():
            customer_updated = form.save(commit=False)
            customer_updated.referenced_user = request.user
            customer_updated.save()
            return HttpResponseRedirect(reverse('crm:detail', args=[customer_id]))
    else:
        form = CustomerForm(instance=customer_selected)
    return render(request, 'crm/update.html', {'form': form, 'customer': customer_selected})
