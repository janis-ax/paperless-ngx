from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.templatetags.static import static

from .models import Sender, Tag, Document


class MonthListFilter(admin.SimpleListFilter):

    title = "Month"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "month"

    def lookups(self, request, model_admin):
        r = []
        for document in Document.objects.all():
            r.append((
                document.created.strftime("%Y-%m"),
                document.created.strftime("%B %Y")
            ))
        return sorted(set(r), key=lambda x: x[0], reverse=True)

    def queryset(self, request, queryset):

        if not self.value():
            return None

        year, month = self.value().split("-")
        return queryset.filter(created__year=year, created__month=month)


class TagAdmin(admin.ModelAdmin):

    list_display = ("name", "colour", "match", "matching_algorithm")
    list_filter = ("colour", "matching_algorithm")
    list_editable = ("colour", "match", "matching_algorithm")


class DocumentAdmin(admin.ModelAdmin):

    class Media:
        css = {
            "all": ("paperless.css",)
        }

    search_fields = ("sender__name", "title", "content")
    list_display = ("created_", "sender", "title", "tags_", "document")
    list_filter = ("tags", "sender", MonthListFilter)
    list_per_page = 25

    def created_(self, obj):
        return obj.created.date().strftime("%Y-%m-%d")

    def tags_(self, obj):
        r = ""
        for tag in obj.tags.all():
            colour = tag.get_colour_display()
            r += html_tag(
                "a",
                tag.slug,
                **{
                    "class": "tag",
                    "style": "background-color: {};".format(colour),
                    "href": "{}?tags__id__exact={}".format(
                        reverse("admin:documents_document_changelist"),
                        tag.pk
                    )
                }
            )
        return r
    tags_.allow_tags = True

    def document(self, obj):
        return html_tag(
            "a",
            html_tag(
                "img",
                src=static("documents/img/{}.png".format(obj.file_type)),
                width=22,
                height=22,
                alt=obj.file_type,
                title=obj.file_name
            ),
            href=obj.download_url
        )
    document.allow_tags = True

admin.site.register(Sender)
admin.site.register(Tag, TagAdmin)
admin.site.register(Document, DocumentAdmin)

# Unless we implement multi-user, these default registrations don't make sense.
admin.site.unregister(Group)
admin.site.unregister(User)


def html_tag(kind, inside=None, **kwargs):

    attributes = []
    for lft, rgt in kwargs.items():
        attributes.append('{}="{}"'.format(lft, rgt))

    if inside is not None:
        return "<{kind} {attributes}>{inside}</{kind}>".format(
            kind=kind, attributes=" ".join(attributes), inside=inside)

    return "<{} {}/>".format(kind, " ".join(attributes))
