from rest_framework import serializers
from .models import User, Novel, UserProfile, Chapter, Comment, Like
from django.contrib.auth.password_validation import validate_password

class UserCreateSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True, min_length = 8)
    confirm_password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'confirm_password', 'email','bio', 'avatar']

        ##field level validation

    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError('Email already exists')
            
        return value
        
    def validate_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError('Username already exists. Please choose a new one')
            
        return value
        
        
        ## object level validation
    """ Objects level validations are used to check the validations between serializer data."""

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
            
        return data
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password) ## This method hash the password.

        user.save() ## This save the data to the database.
        return user

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment', 'novel']

class UserPreviewSerializer(serializers.ModelSerializer):
    user_comments = CommentSerializer(many=True)
    class Meta:
        model = User
        fields = ['username','email','bio', 'avatar', 'user_comments']



class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = ['number', 'title', 'content']


class NovelSerializer(serializers.ModelSerializer):

    chapters = ChapterSerializer(many=True)

    total_chapters =  serializers.SerializerMethodField(read_only = True)
    comments = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Novel
        fields = ['title', 'description', 'chapters', 'total_chapters', 'comments', 'total_likes']

    def get_total_chapters(self, obj):
        return obj.chapters.count()
    
    def create(self, validated_data):
        chapters_data = validated_data.pop('chapters', [])

        novel = Novel.objects.create(**validated_data)

        for chapter_data in chapters_data:
            Chapter.objects.create(novel = novel, **chapter_data)
        
        return novel
    
    def get_total_likes(self,obj):
        return obj.novel_likes.count()
    
    def get_comments(self, obj):
        return [f"{comment.comment} by {comment.user.username}" for comment in obj.comments.all()]
    



            
            


