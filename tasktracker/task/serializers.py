from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()
    owner = serializers.HyperlinkedRelatedField(
        view_name='profile-detail', 
        read_only=True
        ) 

    def get_id(self, obj):
        return str(obj.id)

    class Meta:
        model = Task
        fields = [
            'id',
            'description',
            'status',
            'priority',
            'category',
            'date_created',
            'due_date',
            'owner'
        ]