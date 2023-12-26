from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.query_utils import Q
from base.models import *
from backend.models import Project
from django.contrib.auth.models import User
from backend.serializers import *


# Create your views here.
class ProjectStatisticsAPIView(APIView):
    def get(self, request):
        freelancers = Profile.objects.filter(user_type=1).count()
        employers = Profile.objects.filter(user_type=2).count()
        projects = Project.objects.all().count()

        return Response(
            {"freelancers": freelancers, "employers": employers, "projects": projects}
        )


class PostProjectAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            title = data.get("title")
            description = data.get("description")
            category = data.get("category")
            skills = data.get("skills", [])
            duration = data.get("duration")
            created_by = data.get("created_by")
            currency = data.get("currency")
            payment_type = data.get("payment_type")
            budget = data.get("budget")
            amount = data.get("amount")
            project_file = data.get("project_file")

            budget_instance = (
                Budget.objects.get(id=budget) if budget is not None else None
            )
            category_instance = Category.objects.get(id=category)
            skills_instance = Skill.objects.filter(id__in=skills)
            print("==============skills instance", skills_instance)
            user_instance = User.objects.get(id=created_by)

            project = Project.objects.create(
                title=title,
                description=description,
                category=category_instance,
                duration=duration,
                created_by=user_instance,
                currency=currency,
                payment_type=payment_type,
                budget=budget_instance,
                amount=amount,
                project_file=project_file,
            )

            project.skills.set(skills_instance)
            project.save()
            serializer = ProjectSerializer(project)
            return Response(
                {"status": 201, "message": "project created", "data": serializer.data}
            )
        except Exception as e:
            return Response(
                {"status": 500, "message": f"Internal Server Error: {str(e)}"}
            )


class BudgetListAPIView(APIView):
    def get(self, request):
        budgets = Budget.objects.filter(is_active=True, is_deleted=False)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)
