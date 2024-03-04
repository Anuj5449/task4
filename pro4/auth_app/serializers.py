from rest_framework import serializers
from django.contrib.auth import get_user_model
from pro4.task_app.serializer import TaskSerializer


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    user_task = TaskSerializer(read_only=True, many=True)
    
    
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','password','email','gender','address','role','pincode','city','company','contact')
        
    def create(self, validated_data):
        obj = User.objects.create_user(**validated_data)
        obj.is_active = False
        obj.save()
        return obj
    