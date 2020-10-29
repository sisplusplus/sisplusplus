from rest_framework import serializers
from .models import Faculty, Program

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['code','fullName']

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['code','fullName', 'faculty']
