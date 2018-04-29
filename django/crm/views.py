from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required, permission_required
from .models import Customer
 
# @permission_required('user.is_staff', login_url='/accounts/login')
@login_required
def index(request):
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
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'crm/detail.html', {'customer': customer})


