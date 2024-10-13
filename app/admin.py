# from django.contrib import admin
# from .models import *
# # Register your models here.



# class GalleryImageInline(admin.TabularInline):
#     model = GalleryImage
#     extra = 3 # Number of empty forms to display

# class GalleryAdmin(admin.ModelAdmin):
#     list_display = ('event', 'date', 'image_count')
#     list_filter = ('date',)
#     search_fields = ('event', 'description')
#     list_per_page = 10
#     date_hierarchy = 'date'
#     ordering = ('-date',)
#     inlines = [GalleryImageInline]

#     def image_count(self, obj):
#         return obj.images.count()
#     image_count.short_description = 'Number of Images'

# admin.site.register(Gallery, GalleryAdmin)










# admin.site.register(Event)
# # admin.site.register(Message)
# admin.site.register(Faq)
