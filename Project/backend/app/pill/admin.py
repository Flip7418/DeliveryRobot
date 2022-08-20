from django.contrib import admin

from pill.models import BodyPart, Pill, Simptom, SimptomPill, Text


@admin.register(BodyPart)
class BodyPartAdmin(admin.ModelAdmin):
    pass


@admin.register(Pill)
class PillAdmin(admin.ModelAdmin):
    pass


@admin.register(Simptom)
class SimptomAdmin(admin.ModelAdmin):
    list_filter = ('body_part', )


@admin.register(SimptomPill)
class SimptomPillAdmin(admin.ModelAdmin):
    pass


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass