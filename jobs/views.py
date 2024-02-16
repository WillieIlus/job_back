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

class TopJobs(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobFilter

class JobList(ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'slug'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
    

class JobListByUser(ListAPIView):
    serializer_class = JobSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.kwargs['user']
        return Job.objects.filter(user=self.request.user)


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

        # Check if it's been more than 30 minutes since the last impression for the same IP
        if (
                job.last_impression_at is None
                or timezone.now() - job.last_impression_at > timedelta(minutes=30)
        ):
            source_ip = self.request.META.get('REMOTE_ADDR')

            # Check if there is no previous impression from the same IP within 30 minutes
            if not Impression.objects.filter(
                    job=job, source_ip=source_ip, created_at__gte=timezone.now() - timedelta(minutes=30)
            ).exists():
                job.view_count += 1
                job.update_last_viewed()

                impression = Impression(job=job, source_ip=source_ip)
                impression.save()


class ClickList(ListCreateAPIView):
    serializer_class = ClickSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Click.objects.filter(job_id=job_id)

    def perform_create(self, serializer):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(id=job_id)
        serializer.save(job=job)
        job.click_count += 1
        job.save()

        # Save source IP and session ID
        source_ip = self.request.META.get('REMOTE_ADDR')
        session_id = self.request.session.session_key
        serializer.save(source_ip=source_ip, session_id=session_id)

        # Check if it's been more than 30 minutes since the last click for the same IP
        if (
                job.last_click_at is None
                or timezone.now() - job.last_click_at > timedelta(minutes=30)
        ):
            source_ip = self.request.META.get('REMOTE_ADDR')

            # Check if there is no previous click from the same IP within 30 minutes
            if not Click.objects.filter(
                    job=job, source_ip=source_ip, created_at__gte=timezone.now() - timedelta(minutes=30)
            ).exists():
                job.click_count += 1
                job.update_last_clicked()

                click = Click(job=job, source_ip=source_ip)
                click.save()


class ImpressionDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ImpressionSerializer
    lookup_field = 'slug'

class ClickDetail(RetrieveUpdateDestroyAPIView):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    lookup_field = 'slug'


