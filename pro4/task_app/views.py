from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task
from .serializer import TaskSerializer
import logging
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('mylogger')
@api_view(http_method_names=['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    if request.method == 'POST':
        try:
            serializer = TaskSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # obj.tasks.set(request.data.get('tasks'))
            logger.info('Task Created SuccesFully')
            return Response(data=serializer.data, status=201)
        except Exception as e:
            print(e)
            logger.error('Error Creating Task')
            return Response(data=serializer.errors, status=404)
    
    if request.method == 'GET':
        try:
            obj = Task.objects.all()
            serializer = TaskSerializer(obj, many = True)
            logger.info('Tasks Fetch SuccesFully')
            return Response(data=serializer.data, status=200)
        except:  
            logger.error('Task Featchin Error')
            return Response(data=serializer.errors, status=404)
        
@api_view(http_method_names=('GET','PUT','PATCH','DELETE'))
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def details_api(request,pk):
    obj = get_object_or_404(Task,pk=pk)
    if request.method == 'GET':
        try:
            serializer = TaskSerializer(obj)
            logger.info('Task fetch Succesfully')
            return Response(data=serializer.data, status=200)
        except:
            logger.error('Error Fetching Task')
            return Response(data={'details':'Not Found'}, status=404)
    
    if request.method == 'PUT':
        try:
            serializer = TaskSerializer(data=request.data, instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Task Value Successfully Updated')
            return Response(data=serializer.data, status=205)
        except:
            logger.error('Error in Task Updation')
            return Response(data=serializer.errors, status=404)
    
    if request.method == 'PATCH':
        try:
            serializer = TaskSerializer(data=request.data, instance=obj, partial =True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Task Value Partially Updated')
            return Response(data=serializer.data, status=205)
        except:
            logger.error('Error in Task Updation')
            return Response(data=serializer.errors, status=400)
    if request.method == 'DELETE':
        try:
            obj.delete()
            logger.info('Task Value is Deleted')
            return Response(data=None, status=204)
        except:
            logger.error('Deleting Task Error')
            return Response(data={'details':'Not Found'}, status=404)
