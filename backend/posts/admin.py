from django.contrib import admin
from .models import Owner, BoardingHouse, Room, Tenant, Guardian, Transaction, FaceImage

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address', 'phone_number')
    search_fields = ('first_name', 'last_name', 'address', 'phone_number')

@admin.register(BoardingHouse)
class BoardingHouseAdmin(admin.ModelAdmin):
    list_display = ('bh_name', 'address', 'capacity', 'number_of_tenants', 'number_of_rooms', 'owner')
    search_fields = ('bh_name', 'address', 'owner__first_name', 'owner__last_name')
    list_filter = ('capacity', 'number_of_tenants', 'number_of_rooms')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('boarding_house', 'room_number', 'capacity', 'available_beds')
    search_fields = ('boarding_house__bh_name', 'room_number')
    list_filter = ('capacity', 'available_beds')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'age', 'course_profession', 'school_company', 'address', 'phone_number', 'monthly_due', 'monthly_due_date', 'room', 'initial_payment')
    search_fields = ('first_name', 'last_name', 'gender', 'course_profession', 'school_company', 'address', 'phone_number')
    list_filter = ('gender', 'age', 'course_profession', 'school_company')

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'address', 'relationship', 'tenant')
    search_fields = ('first_name', 'last_name', 'phone_number', 'address', 'relationship', 'tenant__first_name', 'tenant__last_name')
    list_filter = ('relationship',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'transaction_date', 'transaction_time', 'mode_of_payment', 'amount_paid', 'month_status', 'tenant')
    search_fields = ('transaction_id', 'transaction_date', 'transaction_time', 'mode_of_payment', 'amount_paid', 'tenant__first_name', 'tenant__last_name')
    list_filter = ('transaction_date', 'transaction_time', 'mode_of_payment', 'amount_paid', 'month_status')

@admin.register(FaceImage)
class FaceImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'tenant', 'time_stamp')
    search_fields = ('image_id', 'tenant__first_name', 'tenant__last_name')
    list_filter = ('time_stamp',)
