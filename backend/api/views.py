from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note 
from .serializers import NoteSerializer, UserSerializer


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    ## cant create a new note without being authenticated
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ## Gets the current user
        user = self.request.user
        ## Returns all the notes that the user has created
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        ## if serializer is valid
        if serializer.is_valid():
            ## Creates a new note
            serializer.save(author=self.request.user)
        else:
            ## if serializer is not valid
            print(serializer.errors)



class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    ## cant delete a note without being authenticated
    permission_classes = [AllowAny]

    def get_queryset(self):
        ## Gets the current user
        user = self.request.user
        ## Returns all the notes that the user has created
        return Note.objects.filter(author=user)




# Create your views here. Class based view for creating a new user below is a generic view to create a user
class CreateUserView(generics.CreateAPIView):
    ## Gives us alist of all objects that we are going to use when creating a new user
    queryset = User.objects.all() 
    ## Gives us the serializer that we are going to use when creating a new user 
    serializer_class = UserSerializer
    ## Allows any user to create a new user
    permission_classes = [AllowAny]
    