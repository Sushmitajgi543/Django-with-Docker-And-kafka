from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
# from .producers import KafkaProducer

# # Kafka producer instance
# kafka_producer = KafkaProducer('localhost:9092', 'user_activity_topic')
#
# # Signal receiver to produce Kafka message on user login
# @receiver(user_logged_in)
# def user_logged_in_handler(sender, request, user, **kwargs):
#     message = {'event': 'user_login', 'username': user.username}
#     kafka_producer.produce_message(key='user_login', value=message)
class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow super admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser



# def send_kafka_message(request):
#     producer = KafkaProducer('localhost:9092', 'your_kafka_topic')
#     producer.produce_message('message_key', 'your_message_value')
#     return HttpResponse('Kafka message sent successfully!')
#
# def consume_kafka_message(request):
#     consumer = KafkaConsumer('localhost:9092', 'your_consumer_group', 'your_kafka_topic')
#     consumer.consume_messages()
#     return HttpResponse('Kafka messages consumed successfully!')

# get and post only admin
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSuperAdmin]


# put and delete and get single
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


# signup users
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # login user and admin both
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = CustomUserSerializer(user)
            # Produce a Kafka message when a user logs in
            print()
            # produce_message("user-login", user.username, "User logged in")
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'id': user.id,'useranme':user.username})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

