from django import forms
from django.db.models.base import Model
from django.forms import fields, widgets
from homeapp.models import *

class MemberSavingForm(forms.ModelForm):
    class Meta:
        model = ShareMemberSaving
        fields = '__all__'
        exclude = ['interestfactor',]
        
    def save(self,commit=False):
        obj =super().save(commit=False)
        objects = []
        MONTHS = ['बैशाख','जेष्ठ','असार','साउन','भदौ','असोज','कार्तिक','मङ्सिर','पौष','माघ','फाल्गुन','चैत्र']
        if obj.pk is None:
            for m in MONTHS:
                if obj.month == m:
                    share = ShareMemberSaving(name=obj.name,year=obj.year,month = m, amount = obj.amount)
                else:
                    share = ShareMemberSaving(name=obj.name,year=obj.year,month = m, amount = 0)

                objects.append(share)
            for obj in objects:
                obj.save()
        else:
            obj.save()

class UpdateSavingForm(forms.ModelForm):
    class Meta:
        model = ShareMemberSaving
        exclude = ['interestfactor',]

class AddShareForm(forms.ModelForm):
    class Meta:
        model = ShareMember
        fields = ['add_share',]
class RemoveShareForm(forms.ModelForm):
    class Meta:
        model = ShareMember
        fields = ['remove_share',]

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'
        widgets = {
            'expense_date' : forms.DateInput(attrs={'id':'datepicker-first'}),
        }

class OtherSavingForm(forms.ModelForm):
    class Meta:
        model = OtherSaving
        fields = '__all__'
        widgets = {
            'deposit_date' : forms.DateInput(attrs={'id':'datepicker-first'}),
        }

class ClientNameForm(forms.ModelForm):
    class Meta:
        model = ClientName
        fields = '__all__'

class CompleteLoanForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['loan_rate','loan_drawn_date']

class ClientLoanForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['is_complete']
        widgets = {
            'loan_drawn_date' : forms.DateInput(attrs={'id':'datepicker-first'}),
        }

class UpdateClientLoanForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['is_complete']
        widgets = {
            'loan_drawn_date' : forms.DateInput(attrs={'id':'datepicker-first'}),
        }

class ShareMemberForm(forms.ModelForm):
    class Meta:
        model = ShareMember
        exclude = ['add_share','remove_share','profit','drawprofit','munafa']
        widgets = {
            'share_purchase_date' : forms.DateInput(attrs={'id':'datepicker-first'}),
        }

class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = ShareMember
        exclude = ['add_share','remove_share','drawprofit','munafa','profit']
        widgets = {
            'share_purchase_date' : forms.DateInput(attrs={'id':'datepicker-first'}),
        }

class SchedulePaymentForm(forms.ModelForm):
    class Meta:
        model = ClientSchedulePayment
        fields = "__all__"
        widgets = {
            'payment_date': forms.DateInput(attrs={'id':'datepicker-first'}),
        }

class DrawProfitForm(forms.ModelForm):
    class Meta:
        model = ShareMember
        fields = ['drawprofit',]


##form without model
class DrawSavingForm(forms.Form):
    amount = forms.IntegerField(label="निकाल्न चाहेको रकम राख्नुहोस्")
    amount_date = forms.DateField(label='मिति',help_text="format: YY-MM-DD")

    class Meta:
        widgets = {
            'amount_date':forms.DateInput(attrs={'id':'datepicker-second'}),
        }