from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape

from rest_framework import viewsets
from .serializers import PostSerializer
from .serializers import CalliSerializer

from .models import Post
from .models import Calli
from rest_framework import permissions
from .main import main
from .main import ready
import tensorflow as tf

global graph
graph = tf.get_default_graph()
font_list, model_list, z_list = ready()


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
            input_text = self.request.data['input_text']
            font = int(self.request.data['font'])
            latter_attach = int(self.request.data['latter_attach'])
            definition = int(self.request.data['definition'])
            color = int(self.request.data['color'])
            
            with graph.as_default():
                main(font_list, model_list, z_list, font, input_text, latter_attach, definition, color)
            # serializer.save()


def index(request):
    return HttpResponse("Hello, World!")