from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.views import APIView

# Create your views here.


@api_view(["GET"])
def endpoints(request):
    data = ["/advocates", "advocates/:username"]
    return Response(data)


@api_view(["GET", "POST"])
def advocate_list(request):
    # Handle GET request
    if request.method == "GET":
        query = request.GET.get("query")
        if query == None:
            query = ""

        advocate = Advocate.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query)
        )
        serializer = AdvocateSerializer(advocate, many=True)
        return Response(serializer.data)

    # Handle POST requests
    if request.method == "POST":
        advocate = Advocate.objects.create(
            username=request.data["username"], bio=request.data["bio"]
        )
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def advocate_detail(request, username):
    advocate = Advocate.objects.get(username=username)

    if request.method == "GET":
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        advocate.username = request.data["username"]
        advocate.bio = request.data["bio"]

        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    if request.method == "DELETE":
        advocate.delete()
        return redirect(request, "/advocates")


# class AdvocateDetail(APIView):
#     def get_object(self, username):
#         try:
#             return Advocate.objects.get(username=username)
#         except Advocate.DoesNotExist:
#             raise Advocate

#     def get(self, request, username):
#         advocate = self.get_object(username)
#         serializer = AdvocateSerializer(advocate, many=False)

#         return Response(serializer.data)

#     def put(self, request, username):
#         advocate = self.get_object(username)

#         advocate.username = request.data["username"]
#         advocate.bio = request.data["bio"]

#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     def delete(self, request, username):
#         advocate = self.get_object(username)
#         advocate.delete()
#         return Response("Deleted")


@api_view(["GET"])
def company_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)

    return Response(serializer.data)
