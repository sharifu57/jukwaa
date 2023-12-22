from django.db import models
from base.models import BaseModel, Category, Skill
from django.contrib.auth.models import User


PROJECT_DURATION = ((1, "ASAP"), (2, "Within a Week"), (3, "A Month"), (4, "Custom"))
PROJECT_CURRENCY = ((1, "TZS"), (2, "Dollar"))
PAYMENT_TYPE = ((1, "pay_by_hour"), (2, "pay_fixed_price"))
PROJECT_BUDGET = (
    (1, "Basic(20,000Tsh - 50,000Tsh/hour)"),
    (2, "Standard(30,000Tsh - 60,000Tsh/hour)"),
    (3, "Custom"),
)


class Project(BaseModel):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, blank=True, null=True)
    duration = models.IntegerField(choices=PROJECT_DURATION, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    currency = models.IntegerField(
        choices=PROJECT_CURRENCY, default=1, null=True, blank=True
    )
    payment_type = models.IntegerField(choices=PAYMENT_TYPE, null=True, blank=True)
    budget = models.IntegerField(choices=PROJECT_BUDGET, null=True, blank=True)
    amount = models.CharField(max_length=300, null=True, blank=True)
    project_file = models.FileField(upload_to="projects/", null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
