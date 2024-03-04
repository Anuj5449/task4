from .serializers import UserSerializer
from .models import User
from  rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
import logging
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .utils import EmailThread
from .tokens import  account_activation_token
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from .permission import IsOwnerAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('mylogger')

@api_view(http_method_names=['POST'])
def user_creat(request):
    if request.method == 'POST':
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            obj.is_acive = False
            obj.save()
            
            domain = get_current_site(request=request).domain
            token = account_activation_token.make_token(obj)
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            relative_url = reverse('activate',kwarg = {'uid': uid, 'token' : token})
            absolute_url = f'http://%s'%(domain+relative_url,)
            message = "Hello %s,\n\tThank you for creating account with us. please click the link below"\
                " to activate your account.\n%s"%(obj.username, absolute_url,)
            subject =  "Activate Your Account"
            EmailThread(subject=subject, message=message, recipient=[obj.email],from_email=settings.EMAIL_HOST_USER).start()
            return Response({"Message":"please check ypur email to activate  your account"},status=201)
        except  Exception as e:
            print(e)
            logger.error("Error in craeting user")
            return Response(data=serializer.errors, status=404)
        
        
@api_view()
def useraccountActivate(request,uid,token):
    if request.method ==  'GET':
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk = user_id)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist)as e:
            return Response(data={'details':'there is an error'},status=400)
        if account_activation_token.check_token(user=user, token=token):
            user.is_active = True
            user.save()
            return Response(data={'details':'account activated succesfully'}, status=200)
        return Response(data={'details':'Account link invalid'},status=400)
    
@api_view(http_method_names=["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerAuthenticated])
def fetchData(request):
    if request.method == 'GET':
        try:
            obj = User.objects.all()
            serializer = UserSerializer(obj, many = True)
            logging.info('User fetched succesfully')
            return Response(data=serializer.data, status=201)
        except: 
            logger.info('User created with error')
            return Response(data={'details':'it has some errors'}, status=400)
        
@api_view(['PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerAuthenticated])
def manageUser(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        try:
             serializer = UserSerializer(obj)
             logger.info("User  data retrieved successfully")
             return Response(data=serializer.data, status=201)
        except:
            logger.info('user created with error')
            return Response(data={'details':'it has some error'})
        
    if request.method=='PUT': #update the whole object
        try:
            serializer = UserSerializer(data=request.data,instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info("User updated successfully")
            return Response(data=serializer.data, status=205)
        except:
            logger.error('it has some errors ')
            return Response(data=serializer.errors,status=404)
            
    if request.method=='PATCH': #update the whole object
        try:
            serializer = UserSerializer(data=request.data,instance=obj,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info("User updated successfully")
            return Response(data=serializer.data, status=205)
        except:
            logger.error('it has some errors ')
            return Response(data=serializer.errors,status=404)

    if request.method == 'DELETE':
        try:
            obj.delete()
            logger.warning("User deleted successfully")
            return Response(data=None,status=204)
        except:
            logger.error("Error in user deletion ")
            return Response(data={'details':'No content found'}, status=206)
       