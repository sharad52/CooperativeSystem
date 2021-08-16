from django.contrib import admin
from .models import ShareMember,ShareMemberSaving,ClientName,Client,OtherSaving,Expenses,ClientSchedulePayment

# Register your models here.
@admin.register(ClientSchedulePayment)
class SchedulePayAdmin(admin.ModelAdmin):
    pass

@admin.register(ShareMember)
class ShareMemberAdmin(admin.ModelAdmin):
    pass

@admin.register(ShareMemberSaving)
class ShareMemberSavingAdmin(admin.ModelAdmin):
    pass

@admin.register(ClientName)
class ClientNameAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass



@admin.register(OtherSaving)
class OtherSavingAdmin(admin.ModelAdmin):
    pass

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    pass
