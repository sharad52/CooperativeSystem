from os import name
from django.urls import path
from .views import *

app_name = 'homeapp'

urlpatterns = [
    path('',index,name='index'),
    path('ShareMemberCreator/',ShareMemberCreator,name='ShareMemberCreator'),
    path('result/',result,name="result"),
    path('ShareMemberSaving/<int:pk>/',MemberSavingFunction,name="ShareMemberSaving"),
    path('LoanInfo/',LoanHandlerFunction,name="LoanInfo"),
    path('ClientNameCreator/',ClientNameCreator,name="ClientNameHandler"),
    path('CreateLoan/',ClientLoanCreator,name="ClientLoanCreator"),
    path('ViewLoan/<int:pk>/',LoanViewerFunction,name="IndividualLoan"),
    path('CreatePayment/<int:pk>/<str:client_id>/',SchedulePayCreator,name="SchedulePayment"),
    path('exportPDFReport/',export_pdf,name="ExportPdf"),
    path('ClientLoanPDFReport/',ClientLoanPdf,name="CLoanPdf"),
    path('Co-operativeExpenses/',ExpenseHandlerFunction,name="ExpenseHandler"),
    path('Co-operativeSavings/',OtherSavingFunction,name="OtherSaving"),
    path('CreateExpenses/',ExpenseCreator,name="CreateExpense"),
    path("CreateOtherSaving/",OtherSavingCreator,name="CreateOtherSaving"),
    path("Co-operativeExpenseReport/",Expense_pdf,name="ExpensePdf"),
    path("Co-operativeSavingReport/",OtherSaving_pdf,name="OtherSavingPdf"),
    path("ShareMemberSavingCreator/<int:pk>/",MemberSavingCreator,name="MemberSaving"),
    path('UpdateShareMemberSaving/update/<int:pk>/<str:item_id>/',UpdateMonthlySaving,name="UpdateSaving"),
    path('result/AddShare/<int:pk>/',AddShareFunc,name="ShareAdd"),
    path('result/RemoveShare/<int:pk>/',RemoveShareFunc,name="ShareRemove"),
    path('UpdateShareMember/<int:pk>/',UpdateShareMember,name="UpdateMember"),
    path('UpdateClientLoan/<int:pk>/',UpdateClientLoan,name="UpdateClientLoan"),
    path('gonext/',GoNext,name="GoNext"),
    path('GoPrevious/',GoPrevious,name="GoPrevious"),
    path('EMICalculation',EMICalculator,name="EmiCalc"),
    path('DrawProfit/<int:pk>/',DrawProfit,name="ProfitDraw"),
    path('CompleteLoanItem/<int:pk>/',CompleteLoan,name="MarkComplete"),
    path('DrawMonthlySaving/<int:pk>/',DrawMonthlySaving,name = "DrawSaving"),

]