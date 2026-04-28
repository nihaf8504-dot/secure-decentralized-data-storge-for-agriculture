from django.db import models
from django.contrib.auth.models import User
import hashlib
import time


class Block(models.Model):
    index = models.IntegerField(blank=True, null=True)
    timestamp = models.FloatField(blank=True, null=True)
    data = models.TextField()
    previous_hash = models.CharField(max_length=256, blank=True)
    hash = models.CharField(max_length=256, blank=True)

    # ✅ NEW FIELD
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_hash(self):
        block_string = (
            str(self.index) +
            str(self.timestamp) +
            self.data +
            self.previous_hash
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

def save(self, *args, **kwargs):

    is_new = self.pk is None  # 🔥 check if new block

    if is_new:
        # GENESIS BLOCK
        if not Block.objects.exists():
            self.index = 0
            self.previous_hash = "0"
        else:
            last_block = Block.objects.order_by('-index').first()
            self.index = last_block.index + 1
            self.previous_hash = last_block.hash

        # timestamp only for new block
        self.timestamp = time.time()

        # ✅ hash only when creating
        self.hash = self.calculate_hash()

    # ❌ DO NOT recalculate hash on update

    super().save(*args, **kwargs)
    


from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create Block'),
        ('MODIFY', 'Modify Block'),
        ('TAMPER', 'Tampering Detected'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    block = models.ForeignKey('Block', on_delete=models.CASCADE, null=True, blank=True)

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - Block {self.block} - {self.timestamp}"
