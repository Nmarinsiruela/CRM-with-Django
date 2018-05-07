from django.contrib.auth.models import User
from .models import Customer
from .serializers import UserSerializer, ListCustomerSerializer, CreateCustomerSerializer, DetailCustomerSerializer, CreateUserSerializer, DetailUserSerializer
from rest_framework import generics, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

"""
    USER VIEWS
"""
class UserList(generics.ListAPIView):
    """
    Shows the list of users. It uses the generic List to show all the elements, sorted by creation, and showing ID and username.
    """
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    """
    Shows the form to create an user. It uses the generic Create to show the attributes of the model. 
    Required: Username, password.
    """
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

class UserDetail(APIView):
    """
    Shows all the data of the user. It's also used to Delete and Update.
    Delete - The user can't delete its own account.
    Update - The user can't change its own is_staff attribute. It also requires a valid username.
    """
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    queryset = User.objects.all()
    serializer_class = DetailUserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = DetailUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = DetailUserSerializer(user, data=request.data)
        if serializer.is_valid():
            
            # Having validated the previous data, it looks for the special case where the requested user is the same as the one logged in.
            if (user.id == self.request.user.id and serializer.validated_data['is_staff'] == False):
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                serializer.save()
                return Response(serializer.data)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)

        if (user.username != self.request.user.username):
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


"""
    CUSTOMER VIEWS
"""

class CustomerList(generics.ListAPIView):
    """
    Shows the list of customers. It uses the generic List to show all the elements, sorted by creation, and showing ID and name.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = ListCustomerSerializer
   
class CustomerCreate(generics.CreateAPIView):
    """
    Shows the form to create a customer. It uses the generic Create to show the attributes of the model. 
    It has an extra step, where it fills additional attributes of the Customer with the name of the current user.
    Required: name, surname.
    """
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user.username, last_modified_by_user=self.request.user.username)

class CustomerDetail(APIView):
    """
    Shows all the data of the customer. It's also used to Delete and Update.
    Update - It changes the 'last_modified_by_user' attribute, depending on the user that is currently logged in the system.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = DetailCustomerSerializer
    """
    Retrieve, update or delete a customer instance.
    """
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = DetailCustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = DetailCustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save(last_modified_by_user=self.request.user.username)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)