from .serializers import TaskApiSerializer
from .models import TaskApi
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.throttling import ScopedRateThrottle

# Create your views here.
    
class TaskApiListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskApiSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'task'


    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TaskApi.objects.none()

        return TaskApi.objects.filter(user=self.request.user)

    def get_permissions(self):
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
            
class TaskApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskApiSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return TaskApi.objects.all()
        return TaskApi.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]
