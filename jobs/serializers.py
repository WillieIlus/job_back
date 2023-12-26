from rest_framework import serializers

from .models import Job, JobApplication, Impression, Click

from accounts.models import User
from companies.models import Company
from locations.models import Location
from categories.models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    company = CompanySerializer(required=False)
    location = LocationSerializer(required=False)
    category = CategorySerializer(required=False)
    applicants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    timesince = serializers.SerializerMethodField(required=False)
    get_job_type = serializers.CharField(source='job_type', required=False)
    get_created_at = serializers.DateTimeField(source='created_at', required=False)
    days_left = serializers.SerializerMethodField(required=False)
    plan_title = serializers.ReadOnlyField(source='plan.title')
    views_count = serializers.IntegerField(read_only=True)
    click_count = serializers.IntegerField(read_only=True)

    def get_timesince(self, obj):
        return obj.timesince()

    def get_days_left(self, obj):
        return obj.days_left()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'is_active', 'slug')


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('id', 'job', 'user', 'resume', 'cover_letter', 'is_active', 'created_at')
        read_only_fields = ('created_at', 'is_active')


class ImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impression
        fields = ('id', 'job', 'source_ip', 'session_id', 'created_at')
        read_only_fields = ('created_at',)


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ('id', 'job', 'source_ip', 'session_id', 'created_at')
        read_only_fields = ('created_at',)
