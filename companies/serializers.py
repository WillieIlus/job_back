from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    get_location = serializers.CharField(source='location', required=False)
    get_category = serializers.CharField(source='category', required=False)
    get_user = serializers.CharField(source='user', required=False)


    class Meta:
        model = Company
        fields =  'name', 'slug', 'logo', 'website', 'description', 'job_count', 'get_user', 'get_location', 'get_category', 'created_at', 'updated_at'
        read_only_fields = ('slug', 'created_at', 'updated_at')
