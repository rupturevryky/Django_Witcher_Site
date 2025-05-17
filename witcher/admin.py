from django.contrib import admin
from .models import Witcher, AlchemyItem, SchoolUser, Monster, Contract

@admin.register(SchoolUser)
class SchoolUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'rank', 'created_at')
    list_filter = ('school', 'rank')
    search_fields = ('user__username',)

@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('name', 'description')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('monster', 'reward', 'status', 'completed_by', 'completed_at')
    list_filter = ('status', 'monster__type')
    search_fields = ('monster__name', 'completed_by__username')
