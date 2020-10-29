from rest_framework import serializers
from .models import Faculty, Program

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['code','full_name']

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['code','full_name', 'faculty']
