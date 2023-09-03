from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        return str(obj.id)

    class Meta:
        model = Task
        fields = '__all__'