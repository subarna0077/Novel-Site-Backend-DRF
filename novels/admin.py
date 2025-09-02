from django.contrib import admin

# Register your models here.
from .models import User, Novel, Chapter, UserProfile, Comment, Like, Payment, PurchasedNovel

#Tabular inline allows u to edit the related model together on the same page with parent
#Since, chapter is related to its parent model Novel, when we open a Novel in a admin, we can add/edit it's chapters directly under
#novel form
class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0

@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display= ('title', 'author', 'published_at')
    prepopulated_fields={"slug": ("title",)}
    inlines = [ChapterInline]


admin.site.register(User)
admin.site.register(Chapter)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Payment)
admin.site.register(PurchasedNovel)