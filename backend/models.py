from django.db import models
from base.models import BaseModel, Category, Skill, Location, Employer
from django.contrib.auth.models import User



PROJECT_DURATION = ((1, "ASAP"), (2, "Within a Week"), (3, "A Month"), (4, "Custom"))
PROJECT_CURRENCY = ((1, "TZS"), (2, "Dollar"))
PAYMENT_TYPE = ((1, "pay_by_hour"), (2, "pay_fixed_price"))
PROJECT_BUDGET = (
    (1, "Basic(20,000Tsh - 50,000Tsh/hour)"),
    (2, "Standard(30,000Tsh - 60,000Tsh/hour)"),
    (3, "Custom"),
)

BID_STATUS = (
    (0, "Submitted"),
    (1, "In Review"),
    (2, "Success"),
    (3, "Denied")
)

PROJECT_STATUS = (
    (0, "New"),
    (1, "Pending"),
    (2, "In Review"),
    (3, "Approved"),
    (4, "Rejected"),
    (5, "On Going"),
    (6, "Completed"),
    (7, "Closed"),
    (8, "Returned"),
)

PAYMENT_STATUS = (
    (0, "Not Paid"),
    (1, "Paid")
)

EXPERIENCE_OF_FREELANCERS = (
    (0, '1 year'),
    (1, '2 years')
)

SIZE_OF_PROJECT = (
    (1, 'Small'),
    (2, 'Medium')
)


class Budget(BaseModel):
    price_from = models.CharField(
        max_length=300, blank=True, null=True
    )
    price_to = models.CharField(
        max_length=300, blank=True, null=True
    )

    def __str__(self):
        return f"{self.price_from} - {self.price_to}"


class Project(BaseModel):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True, related_name="project"
    )
    skills = models.ManyToManyField(Skill, blank=True, null=True)
    duration = models.ForeignKey("backend.Duration", on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    employer = models.ForeignKey("base.Employer", on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.IntegerField(
        choices=PROJECT_CURRENCY, default=1, null=True, blank=True
    )
    payment_type = models.IntegerField(choices=PAYMENT_TYPE, null=True, blank=True)
    budget = models.ForeignKey(
        "backend.Budget", null=True, blank=True, on_delete=models.SET_NULL
    )
    application_deadline = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=300, null=True, blank=True)
    location = models.ForeignKey("base.Location", on_delete=models.SET_NULL, null=True, blank=True)
    projectId = models.CharField(max_length=300, null=True, blank=True)
    experience = models.ForeignKey("base.Experience", on_delete=models.SET_NULL, null=True, blank=True)
    size = models.IntegerField(choices=SIZE_OF_PROJECT, null=True, blank=True)
    status = models.IntegerField(choices=PROJECT_STATUS, default=0, null=True, blank=True)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=0, null=True, blank=True)
    project_file = models.FileField(upload_to="projects/", null=True, blank=True)
    is_applied = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Duration(BaseModel):
    title = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title
class Bid(BaseModel):
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True, related_name="bids"
    )
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    duration = models.ForeignKey("backend.Duration", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    proposal = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=BID_STATUS, null=True, blank=True, default=0)
    identity = models.CharField(null=True, blank=True, max_length=30)
    is_accepted = models.BooleanField(default=False, null=True, blank=True)
    attachment = models.FileField(null=True, blank=True, upload_to="attachments/")

    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"Bid for {self.id}"


# class Testimonial(BaseModel):
#     # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     message = models.TextField(null=True, blank=True)
#
#     class Meta:
#         verbose_name = "Testimonial"
#         verbose_name_plural = "Testimonials"
#
#     def __str__(self):
#         return f"Testimonial for {self.message}"



