from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from api.models import UF
from api.serializers import ChoiceSerializer


# Create your views here.
class EstadosViewSet(views.APIView):

    def get(self, request, *args, **kwargs):
        
        ufs = ChoiceSerializer(UF, many=True).data
        return Response(ufs) 
