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


class Budget(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    price_from = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    price_to = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}-({self.price_from} - {self.price_to})"


class Project(BaseModel):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    skills = models.ManyToManyField(Skill, blank=True, null=True)
    duration = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    currency = models.IntegerField(
        choices=PROJECT_CURRENCY, default=1, null=True, blank=True
    )
    payment_type = models.IntegerField(choices=PAYMENT_TYPE, null=True, blank=True)
    budget = models.ForeignKey(
        "backend.Budget", null=True, blank=True, on_delete=models.SET_NULL
    )
    application_deadline = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=300, null=True, blank=True)
    project_file = models.FileField(upload_to="projects/", null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Bid(BaseModel):
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True, related_name="bids"
    )
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    proposal = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"Bid for {self.project.title} by {self.bidder.username}"
