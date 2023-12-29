from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse

from .models import Job, JobApplication, Impression, Click
from .serializers import (
    JobSerializer, JobApplicationSerializer, ImpressionSerializer, ClickSerializer
)
from .filters import JobFilter

class JobList(ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        for job in self.get_queryset():
            # Check if it's been more than 30 minutes since the last view for the same IP
            if (
                job.last_viewed_at is None
                or timezone.now() - job.last_viewed_at > timedelta(minutes=30)
            ):
                source_ip = request.META.get('REMOTE_ADDR')

                # Check if there is no previous impression from the same IP within 30 minutes
                if not Impression.objects.filter(
                    job=job, source_ip=source_ip, created_at__gte=timezone.now() - timedelta(minutes=30)
                ).exists():
                    job.view_count += 1
                    job.update_last_viewed()

                    impression = Impression(job=job, source_ip=source_ip)
                    impression.save()

        return response

class JobDetail(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        job = self.get_object()

        # Check if it's been more than 30 minutes since the last click for the same IP
        if (
                job.last_clicked_at is None
                or timezone.now() - job.last_clicked_at > timedelta(minutes=30)
        ):
            source_ip = request.META.get('REMOTE_ADDR')

            # Check if there is no previous click from the same IP within 30 minutes
            if not Click.objects.filter(
                    job=job, source_ip=source_ip, created_at__gte=timezone.now() - timedelta(minutes=30)
            ).exists():
                job.click_count += 1
                job.update_last_clicked()

                click = Click(job=job, source_ip=source_ip)
                click.save()

        return response

class JobApplicationList(ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    lookup_field = 'slug'

class JobApplicationDetail(RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    lookup_field = 'slug'

class ImpressionList(ListCreateAPIView):
    serializer_class = ImpressionSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Impression.objects.filter(job_id=job_id)

    def perform_create(self, serializer):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(id=job_id)
        serializer.save(job=job)
        job.view_count += 1
        job.save()

class ImpressionDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ImpressionSerializer
    lookup_field = 'slug'

class ClickList(ListCreateAPIView):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Click.objects.filter(job_id=job_id)

    def perform_create(self, serializer):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(id=job_id)
        serializer.save(job=job)
        job.view_count += 1
        job.save()

class ClickDetail(RetrieveUpdateDestroyAPIView):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    lookup_field = 'slug'
