from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import EmailValidator
from slugify import slugify
import uuid

# Create your models here.

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    email = models.EmailField(validators=[EmailValidator()])

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # change default 'user_set' to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    

class Novel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(blank=True, unique=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='novels')
    published_at = models.DateTimeField(auto_now_add=True)
    free_chapters = models.PositiveIntegerField(default=3)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=[ 'author','title'], name='unique_author_title')]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            #Check if slug already exists in the database
            while Novel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter +=1

            self.slug = slug

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"
        
    

class Chapter(models.Model):
    number = models.IntegerField()
    novel = models.ForeignKey(Novel, on_delete= models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)

    class Meta:

        # This constraint prevent from having the 2 chapter with same number in a single novel 
        constraints = [models.UniqueConstraint(fields = ['novel', 'number'], name='unique-chapter-per-novel')
                       ]
        
        # Always comes sorted by chapter number
        ordering = ['number']

        ##This creates a database index on novel and number columns.
        indexes = [models.Index(fields=['novel', 'number'])]

    def __str__(self):
        return f"{self.novel.title} - chapter {self.number}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default = False)
    coins = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} commented {self.comment[:30]} in {self.novel.title} novel"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='novel_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'novel']

    def __str__(self):
        return f"{self.user.username} liked {self.novel.title}"
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.UUIDField(default=uuid.uuid4)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.novel.title} - {self.status}"
    

class PurchasedNovel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_novels')
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='purchased_users')
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'novel']

    def __str__(self):
        return f"{self.user.username} purchased {self.novel.title}"


    

    






