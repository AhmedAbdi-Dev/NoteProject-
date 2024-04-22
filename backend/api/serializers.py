from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

##Class that serializes the user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

##Class that creates a new user.    
##Serializer will check to see if the model and the fields on the model and make sure it is valide and pass it to validated_data
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
##Class that serializes the note model, 
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'created_at', 'author')
        extra_kwargs = {'author': {'read_only': True}}