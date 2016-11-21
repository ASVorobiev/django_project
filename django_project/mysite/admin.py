# Register your models here.

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.safestring import mark_safe

from django_project.mysite import models
from django_project.mysite.models import Events, MysiteOrganizers, Locations, Customplaces




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
    def button(self, obj):
        return mark_safe('<input type="button" id="set_active_%(id)s" onclick="set_active(%(id)s)" value="Активировать"/>'
                         '<input type="button" id="set_active_with_priority_%(id)s" onclick="set_active_with_priority(%(id)s)" value="Активировать с приоритетом"/>'
                         '<input type="button" id="set_dismiss_%(id)s" onclick="set_dismiss(%(id)s)" value="Отклонить"/>'
                         '<input type="button" id="set_active_%(id)s" onclick="tag_it(%(id)s)" value="Taggit"/>' % {'id':  obj.id})

    button.short_description = 'Action'
    button.allow_tags = True

    def org(self, obj):
        return obj.organizator

    fieldsets = (
        (None, {
            'fields': ('location', 'owner', 'title', 'start_date', 'start_time', 'description', 'image', 'thumb', 'image_small', 'tag_it')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('category_id', 'duration', 'finish_date', 'is_perodic', 'shedule', 'place_comment',
                        'is_free', 'tickets', 'phone', 'url', 'priority', 'is_active',
                       'export_vk', 'is_deleted', 'created', 'modified'),
        }),
    )


    readonly_fields = ['modified', 'created', 'image_small']
    actions = ['is_active']
    # exclude = ['thumb']
    search_fields = ['title', 'description']
    models = Events

    # but = AdminActions().button



    def list_locations_name(self, obj):
        return obj.location.name

    list_locations_name.admin_order_field = 'start_date'  # Allows column order sorting
    list_locations_name.short_description = 'Город'  # Renames column head

    list_display = ['image_small', 'title', 'list_locations_name', 'description', 'start_date', 'start_time', 'button']
    list_filter = ('start_date', 'location_id__name', 'priority', 'is_active')
admin.site.register(Events, EventsAdmin)

class OrganizersAdmin(admin.ModelAdmin):
    search_fields = ['name']
    models = MysiteOrganizers
admin.site.register(MysiteOrganizers, OrganizersAdmin)

class CustomplacesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    models = Customplaces
admin.site.register(Customplaces, CustomplacesAdmin)

# def delete(request, app_label, model_name):
#     model = models.Events
#     opts = model._meta
#     if model is None:
#         raise Http404("App %r, model %r, not found" % (app_label, model_name))
#     if not request.user.has_perm(app_label + '.' + model._meta.get_change_permission()):
#         raise PermissionDenied
#
#     try:
#         cl = ChangeList(request, model)
#     except IncorrectLookupParameters:
#         if ERROR_FLAG in request.GET.keys():
#             return render_to_response('admin/invalid_setup.html', {'title': _('Database error')})
#         return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')
#
#     if 'delete_selected' in request.POST and model_name in request.POST:
#         deleted = []
#         for obj in cl.get_query_set().filter(id__in=request.POST.getlist(model_name)):
#             obj.delete()
#             deleted.append('"%s"' % str(obj))
#         request.user.message_set.create(
#             message=_('The %(name)s %(obj)s were deleted successfully.') % {'name': opts.verbose_name_plural,
#                                                                             'obj': ", ".join(deleted)})
#
#     if 'delete_shown' in request.POST and 'qs_obj' in request.POST:
#         deleted = []
#         for obj in cl.get_query_set().filter(id__in=request.POST.getlist('qs_obj')):
#             obj.delete()
#             deleted.append('"%s"' % str(obj))
#         request.user.message_set.create(
#             message=_('The %(name)s %(obj)s were deleted successfully.') % {'name': opts.verbose_name_plural,
#                                                                             'obj': ", ".join(deleted)})
#
#     if 'delete_all' in request.POST and cl.get_query_set().count() > 0:
#         for obj in cl.get_query_set():
#             obj.delete()
#         request.user.message_set.create(
#             message=_('All %(name)s were deleted successfully.') % {'name': opts.verbose_name_plural})
#
#     return HttpResponseRedirect('..')
#
#
# change_list = staff_member_required(never_cache(change_list))