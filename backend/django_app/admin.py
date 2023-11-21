from django.contrib import admin
from . import models

admin.site.site_header = "Панель управления"
admin.site.index_title = "Администрирование сайта"
admin.site.site_title = "Администрирование"


class UserProfileAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'UserProfile' на панели администратора
    """

    list_display = ("user", "avatar")
    list_display_links = ("user",)
    list_editable = ()
    list_filter = ("user", "avatar")
    fieldsets = (
        (
            "Основное",
            {"fields": ("user", "avatar")},
        ),
        (
            "Техническое",
            {"fields": ()},
        ),
    )
    search_fields = ["user", "avatar"]


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Ideas)
admin.site.register(models.IdeaComments)
admin.site.register(models.IdeaRatings)
admin.site.register(models.Room)
admin.site.register(models.Message)
admin.site.register(models.Product)

# class PostAdmin(admin.ModelAdmin):
#     """
#     Настройки отображения, фильтрации и поиска модели:'Post' на панели администратора
#     """
#
#     list_display = ("author", "title", "description", "image", "is_active", "date_time")
#     list_display_links = (
#         "author",
#         "title",
#         "description",
#     )
#     list_editable = ("is_active",)
#     list_filter = ("author", "title", "description", "image", "is_active", "date_time")
#     fieldsets = (
#         (
#             "Основное",
#             {"fields": ("author", "title", "description", "image")},
#         ),
#         (
#             "Техническое",
#             {"fields": ("is_active", "date_time")},
#         ),
#     )
#     search_fields = ["title", "description"]


# admin.site.register(models.UserAuthToken)
