from django.contrib import admin
from robot.models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    pass
