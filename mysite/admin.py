from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from mysite import models
from mysite.models import Person, Events, Locations


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a> %s ' % \
                          (image_url, image_url, file_name, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class ImageWidgetAdmin(admin.ModelAdmin):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(ImageWidgetAdmin, self).formfield_for_dbfield(db_field, **kwargs)

class IndividualBirdAdmin(ImageWidgetAdmin):
    image_fields = ['thumbNail', 'detailImage']

class MyUpload(admin.ModelAdmin):
    list_display = ['pic']
    readonly_fields = ('upload_date',)


class PersonsAdmin(admin.ModelAdmin):
    readonly_fields = ('image_small',)
    list_display = ('first_name', 'last_name', 'image', 'image_small')


class EventsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('location', 'title', 'description', 'image', 'start_date', 'start_time',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('category_id', 'duration', 'finish_date', 'is_perodic', 'shedule', 'place_id', 'place_comment',
                       'organizer_id', 'is_free', 'tickets', 'tags', 'phone', 'url', 'priority', 'is_active',
                       'export_vk', 'is_deleted', 'created', 'modified'),
        }),
    )
    readonly_fields = ['modified', 'created']
    actions = ['is_active']
    #exclude = ['thumb']
    search_fields = ['title', 'description']
    models = Events

    def list_locations_name(self, obj):
        return obj.location.name
    list_locations_name.admin_order_field = 'start_date'  #Allows column order sorting
    list_locations_name.short_description = 'Город'  # Renames column head

    list_display = ['image_small', 'title', 'list_locations_name',  'description', 'start_date', 'start_time', ]
    list_filter = ('start_date', 'location_id__name')

admin.site.register(Person, PersonsAdmin)
#admin.site.register(Upload, MyUpload)
admin.site.register(Events, EventsAdmin)


