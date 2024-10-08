from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.query_utils import Q
from base.models import *
from backend.models import Project
from django.contrib.auth.models import User
from backend.serializers import *
import pendulum
import random
from backend.utils import *
from rest_framework.pagination import PageNumberPagination
from xml.etree import ElementTree as ET
from backend.services.payment_data import ProcessPaymentData, TigopesaPayment
from django.http import HttpResponse
from django.db.models import Prefetch, Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class ProjectStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        freelancers = Profile.objects.filter(user_type=1).count()
        employers = Profile.objects.filter(user_type=2).count()
        projects = Project.objects.all().count()

        return Response(
            {"freelancers": freelancers, "employers": employers, "projects": projects}
        )


class PostProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        try:
            title = data.get("title")
            description = data.get("description")
            category = data.get("category")
            skills = data.get("skills")
            duration = data.get("duration")
            created_by = data.get("created_by")
            # currency = data.get("currency")
            # payment_type = data.get("payment_type")
            amount = data.get("amount")
            deadline = data.get("application_deadline")
            location = data.get("location")
            budget = data.get("budget")
            project_file = data.get("project_file")

        except Exception as e:
            return Response({"status": 404, "message": f"Error f{e}"})

        try:
            category_instance = Category.objects.get(id=category)
        except Exception as e:
            return Response({"status": 404, "message": f"Category Error: {e}"})

        try:
            skills_instance = list(Skill.objects.filter(id__in=skills))
        except Exception as e:
            return Response({"status": 404, "message": f" Skills Error: {e}"})

        try:
            user_instance = User.objects.get(id=created_by)
        except Exception as e:
            return Response({'status': 404, 'message': f" User Error: {e}"})

        try:
            location_instance = Location.objects.get(id=location)
        except Exception as e:
            return Response({'status': 400, 'message': f"location error: {e}"})

        try:
            budget_instance = Budget.objects.get(id=budget)
        except Exception as e:
            return Response({'status': 400, 'message': f"Budget error: {e}"})

        try:
            duration_instance = Duration.objects.get(id=duration)
        except Experience as e:
            return Response({'status': 400, 'message': f"Duration error: {e}"})

        try:
            project = Project.objects.create(
                title=title,
                description=description,
                category=category_instance,
                duration=duration_instance,
                created_by=user_instance,
                location=location_instance,
                # currency=currency,
                # payment_type=payment_type,
                # amount=amount,
                budget=budget_instance,
                application_deadline=deadline,
                projectId=get_random_number(),
                project_file=project_file,
            )
            email = user_instance.email

            project.skills.set(skills_instance)
            project.save()
            try:
                payment = TigopesaPayment().process_payment(500, email)
                print("============payment response", payment)
                serializer = ProjectSerializer(project)
                return Response(
                    {
                        "status": 201,
                        "message": "project created(Wait for Approval)",
                        "data": serializer.data,
                    }
                )
            except Exception as e:
                return Response(
                    {
                        "status": 200,
                        "message": "Failed to create project with Error: {e}",
                    }
                )

        except Exception as e:
            return Response({"status": 400, "message": f"Failed to Create: {e}"})


class BudgetListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(is_active=True, is_deleted=False)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)


class GetMatchProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)

        except Category.DoesNotExist:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "Failed"}
            )

        # projects = (
        #     Project.objects.filter(
        #         category_id=category, is_active=True, is_deleted=False, status=3
        #     )
        #     .exclude(application_deadline=pendulum.today())
        #     .order_by("-created")
        # )

        projects = (
            Project.objects.filter(
                category_id=category, 
                is_active=True, 
                is_deleted=False,
                status=3
            ).order_by("-created")
        )

        if projects:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(projects, request)
            serializer = ProjectsListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        else:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "No data"}
            )


class GetProjectsByUserIdAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "User not Found"}
            )

        projects = Project.objects.filter(
            created_by=user, is_active=True, is_deleted=False
        ).order_by('-created')

        if projects:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(projects, request)
            serializer = ProjectsListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        else:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "No data"}
            )


class ViewOneProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": "no project"}
            )

        serializer = ProjectsListSerializer(project, many=False)
        return Response(serializer.data)


class CreateBidAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        print("=========print the data")
        print(data)
        print("========end print data")

        try:
            project = data.get("project")
            bidder = data.get("bidder")
            duration = data.get("duration")
            amount = data.get("amount")
            proposal = data.get("proposal")
            attachment = data.get("attachment")


            try:
                user = User.objects.get(id=bidder)
            except User.DoesNotExist:
                return Response({"status": 400, "message": "No user Available"})

            try:
                project_instance = Project.objects.get(id=project)
            except Project.DoesNotExist:
                return Response({"status": 400, "message": "Project Does not Exists"})

            try:
                duration_instance = Duration.objects.get(id=duration)

                print("=====================print duration instance =================")
                print(duration_instance)
                print("---------------end duration instance---------------")

            except Duration.DoesNotExist:
                return Response({"status": 400, "message": "Duration Does not Exists"})
            
            bid_user = Bid.objects.filter(
                is_active=True,
                is_deleted=False,
                bidder=user,
                project=project_instance,
                # duration=duration_instance,
                # proposal=proposal,
                # attachment=attachment,
            )

            if bid_user:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "You have already bib for this project"
                    }
                )

            else:
                new_bid = Bid.objects.create(
                    project_id=project_instance.id,
                    bidder_id=user.id,
                    duration_id=duration_instance.id,
                    amount=amount,
                    proposal=proposal,
                    attachment=attachment,
                    identity=str(user.id)
                )

                
                new_bid.save()
                serializer = BidSerializer(new_bid, many=False)
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": "Your bid have been sent successfully",
                        "data": serializer.data,
                    }
                )
        except Exception as e:
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"{e}"})



class ProjectBiddersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)

        except Project.DoesNotExist:
            return Response({"status": 400, "message": "project does not exists"})

        # bidders = Bid.objects.filter(
        #     project_id=project, is_active=True, is_deleted=False
        # ).exclude(bidder__profile__bio__isnull=True)

        bidders = Bid.objects.filter(
            project_id=project, is_active=True, is_deleted=False
        ).order_by('-created')

        serializer = BidListSerializer(bidders, many=True)

        return Response({"status": 200, "message": "success", "data": serializer.data})


class GetProjectsByCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        categories_with_projects_and_profiles = Category.objects.annotate(
            projects_count=Count('project', distinct=True),
            profiles_count=Count('profile', distinct=True)
        ).filter(is_active=True, is_deleted=False)

        serializer_data = []
        for category in categories_with_projects_and_profiles:
            category_data = {
                "id": category.id,
                "name": category.name,
                "projects_count": category.projects_count,  # Number of projects in this category
                "profiles_count": category.profiles_count,  # Number of profiles in this category
                # "projects": [
                #     {"id": project.id, "title": project.title}
                #     for project in category.project.all()
                # ],
            }
            serializer_data.append(category_data)

        return Response(serializer_data)


class GetAllProjectsAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(
            is_active=True, 
            is_deleted=False,
            status=3
        ).order_by("-created")
        projectsPerPage = 10

        if projects:
            paginator = PageNumberPagination()
            paginator.page_size = projectsPerPage
            result_page = paginator.paginate_queryset(projects, request)
            serializer = ProjectsListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"status": 400, "message": "No Data"})


class GetAllProjectsListAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(
            is_active=True, is_deleted=False, status=3
        ).order_by("-created")
        data = request.GET

        # print("==================data", data)
        category_ids = request.GET.getlist("category_ids")
        location_id = request.GET.get("location_id")
        min_amount = request.GET.get("min")
        max_amount = request.GET.get("max")

        if category_ids:
            projects = projects.filter(category__id__in=category_ids)
        if location_id:
            projects = projects.filter(location__id=location_id)
        if min_amount:
            projects = projects.filter(
                Q(budget__price_from__gte=min_amount) | Q(amount__gte=min_amount)
            )
        if max_amount:
            projects = projects.filter(
                Q(budget__price_to__lte=max_amount) | Q(amount__lte=max_amount)
            )

        if projects:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(projects, request)
            serializer = ProjectsListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"status": 400, "message": "No Data"})


class ProjectChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(is_active=True, is_deleted=False)[:10]
        serializer = ProjectsListSerializer(projects, many=True)
        return Response(serializer.data)
class AdminStatisticsDashboardAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.all()
        freelancers = Profile.objects.filter(user_type=1)
        employers = Profile.objects.filter(user_type=2)

        return Response({
            'status': 200,
            'message': 'success',
            'projects': projects.count(),
            'freelancers': freelancers.count(),
            'employers': employers.count()
        })


class ProjectStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(is_active=True, is_deleted=False)

        new_projects = projects.filter(status=0).count()
        pending_projects = projects.filter(status=1).count()
        approved_projects = projects.filter(status=3).count()
        rejected_projects = projects.filter(status=4).count()

        return Response(
            {
                'status': 200,
                'projects': projects.count(),
                'new_projects': new_projects,
                'pending_projects': pending_projects,
                'approved_projects': approved_projects,
                'rejected_projects': rejected_projects
            }
        )

# handle all the payment logics
class CreatePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.body
        # print("==============data", data)
        try:
            paymentData = ProcessPaymentData().sync_billpay(request)
            return HttpResponse(paymentData, content_type='text/xml')
        except Exception as e:
            error_response = ProcessPaymentData().generate_error_response("error100", "General Error")
            return HttpResponse(error_response, content_type='text/xml', status=404)
# end the handling of the payment logics

class GetOneProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'status': 400, 'message': 'project does not exist'})

        serializer = ProjectsListSerializer(project, many=False)
        return Response(serializer.data)

        # try:
        #     try:
        #         # Decrypt the projectId to get the original ID
        #         project_id = decrypt_id(encrypted_project_id)
        #
        #         print("-----------descrypt", project_id)
        #         project = Project.objects.get(id=project_id)
        #
        #         if project:
        #             serializer = ProjectsListSerializer(project, many=False)
        #             return Response(serializer.data)
        #         else:
        #             return Response({'status': 400, 'message': 'Failed to get Data'})
        #
        #     except Project.DoesNotExist:
        #         return Response({'status': 400, 'message': 'No Project Available'})
        #
        #
        # except Exception as e:
        #
        #     # Log the exception to console or a log file; adjust as needed for your setup
        #
        #     print(f"Error occurred: {e.__class__.__name__}: {str(e)}")
        #
        #     # Return a more informative error response
        #
        #     return Response({'status': 500, 'message': f'Error: {e.__class__.__name__}: {str(e)}'})


class UpdateProjectStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, projectId):
        try:
            project = Project.objects.get(id=projectId)
        except Project.DoesNotExist:
            return Response({'status': 400})

        status = request.data.get('status')
        if status == 3:
            project.status = status
            project.save()
            return Response({'status': 201, 'message': 'approved'})

        if status == 4:
            project.status = status
            project.save()
            return Response({'status': 201, 'message': 'rejected'})

        else:
            return Response({'status': 400, 'message': 'Invalid Status Input'})

class UserTotalPostedProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        projects = Project.objects.filter(created_by=user.id, is_active=True, is_deleted=False)
        serializer = ProjectsListSerializer(projects, many=True)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})


class GetProjectBiddersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id=None):
        try:
            project = Project.objects.get(id=project_id)

            if project:
                bidders = Bid.objects.filter(project=project, is_active=True, is_deleted=False)
                serializer = BidSerializer(bidders, many=True)
                return Response({'status': status.HTTP_200_OK}, serializer.data)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetAllDurationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        durations = Duration.objects.filter(is_active=True, is_deleted=False)
        serializer = DurationSerializer(durations, many=True)
        return Response(serializer.data)

class GetMyBidsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, bidder_id):
        try:
            user = User.objects.get(id=bidder_id)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': f"{e}"})
        bids = Bid.objects.filter(
            is_active=True,
            is_deleted=False,
            bidder_id=user.id
        ).order_by('-created')

        serializer = BidListSerializer(bids, many=True)
        return Response(serializer.data)
    
class GetMyProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        projects = Project.objects.filter(
            created_by_id=user.id, 
            is_active=True, 
            is_deleted=False
        ).order_by('-created')

        serializer = ProjectsListSerializer(projects, many=True)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})


class ProjectPagination(PageNumberPagination):
    page_size = 10  # Default number of projects per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class SystemProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(
            is_active=True,
            is_deleted=False,
        ).order_by('-created')

        paginator = ProjectPagination()
        paginated_projects = paginator.paginate_queryset(projects, request)
        serializer = ProjectsListSerializer(paginated_projects, many=True)

        return paginator.get_paginated_response(serializer.data)

class getRecentProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        projects = Project.objects.filter(
            is_active=True,
            is_deleted=False,

        ).exclude(status=3).order_by('-created')

        serializer = ProjectsListSerializer(projects, many=False)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})

class UpdateProjectStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, project_id, project_status):
        try:
            project = Project.objects.filter(
                id=project_id,
                is_active=True,
                is_deleted=False  # Assuming you meant is_deleted instead of id_deleted
            ).first()

            if not project:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'No project available'
                    }
                )

            if project_status == "1":
                project.status = project_status
                project.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Project Processed Successfully'
                    }
                )

            if project_status == "3":
                project.status = project_status
                project.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Project Approved Successfully'
                    }
                )

            if project_status == "4":
                project.status = project_status
                project.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Project Rejected'
                    }
                )

            if project_status == "6":
                project.status = project_status
                project.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Completed'
                    }
                )

            if project_status == "7":
                project.status = project_status
                project.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Closed'
                    }
                )

            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid Request'
                }
            )

        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': str(e)
                }
            )

class AllProjectsAPIView(APIView):

    def get(self, request):
        projects = Project.objects.filter(
            is_active=True,
            is_deleted=False,
        ).order_by('-created')

        paginator = ProjectPagination()
        paginated_projects = paginator.paginate_queryset(projects, request)
        serializer = ProjectsListSerializer(paginated_projects, many=True)

        return paginator.get_paginated_response(serializer.data)
