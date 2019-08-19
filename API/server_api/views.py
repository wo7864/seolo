from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape

from rest_framework import viewsets
from .serializers import PostSerializer
from .serializers import CalliSerializer

from .models import Post
from .models import Calli
from rest_framework import permissions
from .keras_load_model import excute
from .keras_load_model import ready
import tensorflow as tf


model_list, z_list, alphabet = ready()
graph = tf.get_default_graph()

model_list[0].summary()

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        print(self.request.post)
        serializer.save(user=self.request.user)


class CalliView(viewsets.ModelViewSet):
    global graph, model_list
    with graph.as_default():
        queryset = Calli.objects.all()
        serializer_class = CalliSerializer

        def perform_create(self, serializer):
            name = self.request.data['name']
            param1 = self.request.data['param1']
            param2 = self.request.data['param2']
            param3 = self.request.data['param3']
            param4 = self.request.data['param4']
            param5 = self.request.data['param5']

            excute(model_list, z_list, alphabet, name, int(param1), int(param2), int(param3), int(param4),
                   int(param5))
            serializer.save()


def index(request):
    return HttpResponse("Hello, World!")