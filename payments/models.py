from django.db import models
import uuid
from django.contrib.auth.models import User
import secrets
from students.models import Level
from payments.paystack import Paystack as psk
# Create your models here.



# class Fee(models.Model):
#     name =  models.CharField(max_length=100)
#     amount = models.IntegerField()
#     level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self) -> str:
#         return f"{self.name} - {self.amount}"
    

class Fee(models.Model):
    name =  models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} "


class FeeAmount(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.fee.name} - {self.amount} - for  {self.level.level} level"




class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fee = models.ForeignKey(FeeAmount, on_delete=models.CASCADE)
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.fee.name}'
    
    class Meta:
        ordering = ['-timestamp']

# class Payments(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.IntegerField(blank=True, null=True)
#     ref  = models.CharField(max_length=300)
#     email = models.CharField(max_length=30)
#     verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return f"{self.user} - {self.amount}"
    
#     def save(self, *args, **kwargs):
#         while not self.ref:
#             ref = secrets.token_urlsafe(50)
#             object_with_similar_ref = Payments.objects.filter(ref=ref)
#             if not object_with_similar_ref:
#                 self.ref = ref
#         super().save(*args, **kwargs)
    
#     def amount_value(self):
#         return int(self.amount) * 100
    
#     def verify_payment(self):
#         paystack = psk()
#         status, result = paystack.verify_payment(self.ref, self.amount)
#         if status:
#             if result['amount'] / 100 == self.amount:
#                 self.verified = True
#                 self.save()
#         if self.verified:
#             return True
#         else:
#             return False
