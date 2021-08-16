import datetime
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.contrib import messages
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404,reverse
from homeapp.forms import *
from .models import *
from django.db.models import Aggregate,Sum,Avg,Min,Max,F
from homeapp.filters import LoanFilter
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

# Create your views here.
@login_required
def index(request):
    loan = Client.objects.filter(is_complete = False)
    total_loan = loan.aggregate(Sum('amount'))
    expenses = Expenses.objects.all()
    totalexpense = expenses.aggregate(Sum('amount'))
    monthlysaving = ShareMemberSaving.objects.all()
    totalmonthlysaving = monthlysaving.aggregate(Sum('amount'))
    sharevalue = ShareMember.objects.all()
    totalsharevalue = sharevalue.values('totalshare').aggregate(Sum('totalshare'))
    totalshareprice = (totalsharevalue['totalshare__sum']*100)

    savings = OtherSaving.objects.all()
    totalsaving = savings.aggregate(Sum('amount'))
    cloan = Client.objects.filter(is_complete=True)
    totalcloan = cloan.aggregate(Sum('amount'))


    if totalcloan['amount__sum'] is not None:
        coop_debit =(totalsaving['amount__sum'] + totalshareprice + totalmonthlysaving['amount__sum'] + totalcloan['amount__sum'])
    else:
        coop_debit = (totalsaving['amount__sum'] + totalshareprice + totalmonthlysaving['amount__sum'])

    if total_loan['amount__sum'] is not None:
        coop_credit = totalexpense['amount__sum'] + total_loan['amount__sum']
    else:
        coop_credit = totalexpense['amount__sum']

    #performing operation between query sets 
    net_worth = coop_debit-coop_credit

    context ={
        'coop_debit':coop_debit,
        'monthlysaving':monthlysaving,
        'totalmonthlysaving':totalmonthlysaving,
        'totalshareprice':totalshareprice,
        'total_loan':total_loan,
        'totalsaving':totalsaving,
        'totalexpense':totalexpense,
        'net_worth':net_worth,

    }

    return render(request,'home/index.html',context)
@login_required
def result(request):
    sharevalue = ShareMember.objects.all()
    totalsharevalue = sharevalue.values('totalshare').aggregate(Sum('totalshare'))
    totalshareprice = (totalsharevalue['totalshare__sum']*100)
    sharemember = ShareMember.objects.all()
    context = {
        'sharemember':sharemember,
        'totalsharevalue':totalsharevalue,
        'totalshareprice':totalshareprice,
    }
    return render(request,'home/sharememberinfo.html',context)
@login_required
def ShareMemberCreator(request):
    form = ShareMemberForm()
    if request.method == 'POST':
        form = ShareMemberForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'सयेर सदस्य थपियो,धन्यावाद !')
            return HttpResponseRedirect(reverse('homeapp:result'))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/sharemembercreator.html',context)
@login_required
def MemberSavingFunction(request,pk):
    member = get_object_or_404(ShareMember,id = pk)
    saving = member.sharemembersaving_set.all()
    savingId = ShareMemberSaving.objects.filter(name_id=pk)
    savingPerYear = savingId.values('year').annotate(c=Sum(F('amount'))).order_by('year')
    data = saving.values('year').annotate(interest_year=Sum(F('amount')*F('interestfactor'))).order_by('year')

    cinterest = saving.values('year').annotate(compoundi=(Sum(F('amount')*F('interestfactor'))+0.18*Sum(F('amount')))).order_by('year')
    
    ci_list = []
    for i in cinterest:
        x = i['compoundi']
        ci_list.append(x)

    print(f'the list is:{ci_list}')
    # total amount of particular saver
    total_amount = saving.aggregate(Sum('amount'))
    context = {
        'member':member,
        'saving':saving,
        'savingPerYear':savingPerYear,
        'data':data,
        'total_amount':total_amount,
        'cinterest':cinterest,

    }
    return render (request,'home/sharemembersaving.html',context)
@login_required
def MemberSavingCreator(request,pk):
    member= get_object_or_404(ShareMember,id=pk)
    form = MemberSavingForm(initial={'name':member})
    if request.method== 'POST':
        form = MemberSavingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'सेयर सदस्यको मासिक बचत सफलता पुर्वक सुरक्षित गरियो।')
            return HttpResponseRedirect(reverse('homeapp:ShareMemberSaving',kwargs={'pk':pk}))

    context = {
        'form':form,
    }
    return render(request,'formtemplate/savingcreator.html',context)
@login_required
def UpdateMonthlySaving(request,pk,item_id):
    member = get_object_or_404(ShareMember,id=pk)
    saving = get_object_or_404(ShareMemberSaving,id=item_id)
    form = UpdateSavingForm( instance = saving)
    if request.method == 'POST':
        form = UpdateSavingForm(request.POST ,instance=saving)
        if form.is_valid():
            form.save()
            messages.info(request,'मासिक बचत सम्पादन भयो।')
            return HttpResponseRedirect(reverse('homeapp:ShareMemberSaving',kwargs = {'pk':pk}))

    context = {
        'form':form,

    }
    return render(request,'formtemplate/updatesaving.html',context)

@login_required
def AddShareFunc(request,pk):
    member = get_object_or_404(ShareMember,id=pk)
    form = AddShareForm(request.POST or None,instance=member)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.totalshare += instance.add_share
        instance.save()
        return HttpResponseRedirect(reverse('homeapp:result'))
    context ={
        'form':form,
    }
    return render(request,'formtemplate/addshare.html',context)
@login_required
def RemoveShareFunc(request,pk):
    member = get_object_or_404(ShareMember,id=pk)
    form = RemoveShareForm(request.POST or None,instance=member)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.totalshare<=0:
            return redirect('homeapp:GoNext')
        elif instance.remove_share > instance.totalshare:
            return redirect('homeapp:GoPrevious')
        else:
            instance.totalshare -= instance.remove_share
            instance.save()
            return HttpResponseRedirect(reverse('homeapp:result'))
    context ={
        'form':form,
    }
    return render(request,'formtemplate/removeshare.html',context)
@login_required
def DrawProfit(request,pk):
    member = get_object_or_404(ShareMember,id=pk)
    form = DrawProfitForm(request.POST or None,instance=member)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.munafa += instance.drawprofit
        instance.profit -= instance.munafa
        instance.save()
        return HttpResponseRedirect(reverse('homeapp:result'))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/drawprofit.html',context)
##this function check wheather the loan is complete or not 
@login_required
def CompleteLoan(request,pk):
    loanitem = get_object_or_404(Client,id=pk)
    form = CompleteLoanForm(request.POST or None,instance=loanitem)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_complete = True
        instance.save()
        messages.success(request,'लगानी रकम चुक्ता भयो')
        return HttpResponseRedirect(reverse('homeapp:LoanInfo'))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/completeloan.html',context)

def GoNext(request):
    context = {}
    return render(request,'respond/responder.html',context)

def GoPrevious(request):
    context = {}
    return render(request,'respond/responder1.html',context)
@login_required
def EMICalculator(request):
    context = {
        
    }
    return render(request,'EMI/home.html',context)
@login_required    
def UpdateShareMember(request,pk):
    member = get_object_or_404(ShareMember,id=pk)
    form = UpdateMemberForm(instance=member)
    if request.method == 'POST':
        form = UpdateMemberForm(request.POST or None,instance=member)
        if form.is_valid():
            form.save()
            messages.success(request,'सेयर सदस्य सम्पादन भयो,धन्यावाद।')
            return HttpResponseRedirect(reverse('homeapp:result'))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/updatemember.html',context)
@login_required
def ClientNameCreator(request):
    form = ClientNameForm()
    if request.method == 'POST':
        form = ClientNameForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'नया ऋणि थपियो,धन्यावाद !')
            return HttpResponseRedirect(reverse('homeapp:LoanInfo'))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/clientnamecreator.html',context)
@login_required
def LoanViewerFunction(request,pk):
    clientinfo = get_object_or_404(ClientName,id=pk)
    loanset = Client.objects.filter(name_id=pk)
    clientloan = get_object_or_404(Client,name_id=pk)#loan detail taken by clientname
    payset=clientloan.clientschedulepayment_set.all()#set of payment made under clientloan
    #totalamount paid by client on schedule payment

    loancount = clientinfo.client_set.all().count()
    amountsum = loanset.aggregate(Sum('amount'))
    totalpayment=payset.aggregate(Sum('payment_amount'))
    #comparing values of schdeulepayment and amount sum
    aval = amountsum['amount__sum']
    tval = totalpayment['payment_amount__sum']
    status = ''

    if aval == tval:
        status ='रकम चुक्ता भयो ।'
    else:
        status ='रकम चुक्ता भयको छैन ।'

    context = {
        'amountsum':amountsum,
        'clientinfo':clientinfo,
        'loanset':loanset,
        'loancount':loancount,
        'payset':payset,
        'totalpayment':totalpayment,

        'status':status,
        'aval':aval,
        'tval':tval,
    }
    return render(request,'home/loandetails.html',context)

def DrawMonthlySaving(request,pk):
    form = DrawSavingForm()
    
    context = {
        'form':form,
    }
    return render(request,'formtemplate/drawmonthlysaving.html',context)
@login_required
def ClientLoanCreator(request):
    form = ClientLoanForm()
    if request.method == 'POST':
        form = ClientLoanForm(request.POST or None)
        if form.is_valid:
            form.save()
            messages.success(request,'नयाँ ऋण बिबरण थपियो,धन्यावाद !')
            return HttpResponseRedirect(reverse('homeapp:LoanInfo'))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/clientloancreator.html',context)
@login_required
def LoanHandlerFunction(request):
    clients = ClientName.objects.all()
    clientdataitem = Client.objects.filter( is_complete = False).order_by('id')
    paginator = Paginator(clientdataitem,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    myFilter = LoanFilter(request.GET,queryset=clientdataitem)
    clientdataitem = myFilter.qs
    context ={
        'clients':clients,
        'clientdataitem':clientdataitem,
        'myFilter':myFilter,
        'page_obj':page_obj,
    }
    return render(request,'home/loaninfo.html',context)
@login_required
def UpdateClientLoan(request,pk):
    loan = get_object_or_404(Client,id=pk)
    form = UpdateClientLoanForm(instance=loan)
    if request.method == 'POST':
        form = UpdateClientLoanForm(request.POST or None,instance=loan)
        if form.is_valid():
            form.save()
            messages.info(request,'ऋण बिबरण थपियो,धन्याबाद ।')
            return HttpResponseRedirect(reverse('homeapp:LoanInfo'))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/updateclientloan.html',context)
@login_required
def SchedulePayCreator(request,pk,client_id):
    client = get_object_or_404(Client,id=pk)
    form = SchedulePaymentForm(request.POST or None,initial={'client':client})
    if request.method == 'POST':
        form = SchedulePaymentForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'नयाँ किस्ता थपियो,धन्यावाद !')
            return HttpResponseRedirect(reverse('homeapp:IndividualLoan',kwargs={'pk':client_id}))
    context = {
        'form':form,
    }
    return render(request,'formtemplate/paymentcreator.html',context)

@login_required
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['content-Disposition']= 'inline ; attachment;filename=ShareMemberInfo'+ \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']='binary'

    sharemember = ShareMember.objects.all()
    totalsharevalue = sharemember.values('totalshare').aggregate(Sum('totalshare'))
    totalshareprice = (totalsharevalue['totalshare__sum']*100)
    context = {
        'sharemember':sharemember,
        'totalsharevalue':totalsharevalue,
        'totalshareprice':totalshareprice,
    }
    html_string = render_to_string('reports/sharemember_report.html',context)
    html = HTML(string= html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

        return response

@login_required
def ClientLoanPdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['content-Disposition']= 'inline ; attachment;filename=clientloandetails'+ \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']='binary'

    loans = Client.objects.all()

    context = {
        'loans':loans,
    }
    html_string = render_to_string('reports/loanclient_report.html',context)
    html = HTML(string= html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

        return response

@login_required
def Expense_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['content-Disposition']= 'inline ; attachment;filename=expenseReport'+ \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']='binary'

    expenses = Expenses.objects.all()
    totalexpense = expenses.aggregate(Sum('amount'))
    context = {
        'expenses':expenses,
        'totalexpense':totalexpense,
    }
    html_string = render_to_string('reports/expense_report.html',context)
    html = HTML(string= html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

        return response

@login_required        
def OtherSaving_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['content-Disposition']= 'inline ; attachment;filename=ShareMemberInfo'+ \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']='binary'

    savings = OtherSaving.objects.all()
    totalsaving = savings.aggregate(Sum('amount'))
    context = {
        'savings':savings,
        'totalsaving':totalsaving,
    }
    html_string = render_to_string('reports/othersaving_report.html',context)
    html = HTML(string= html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

        return response

@login_required
def ExpenseCreator(request):
    form = ExpensesForm()
    if request.method == 'POST':
        form = ExpensesForm(request.POST or None)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('homeapp:ExpenseHandler'))
    context = {
        'form':form,

    }
    return render(request,'formtemplate/expensecreator.html',context)

@login_required
def OtherSavingCreator(request):
    form = OtherSavingForm()
    if request.method == 'POST':
        form = OtherSavingForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('homeapp:OtherSaving'))
    context = {
        'form':form,

    }
    return render(request,'formtemplate/othersavingcreator.html',context)

@login_required
def ExpenseHandlerFunction(request):
    expenses = Expenses.objects.all()
    totalexpense = expenses.aggregate(Sum('amount'))
    context = {
        'expenses':expenses,
        'totalexpense':totalexpense,
    }
    return render(request,'home/expense.html',context)


@login_required
def OtherSavingFunction(request):
    savings = OtherSaving.objects.all()
    totalsaving = savings.aggregate(Sum('amount'))
    context = {
        'savings':savings,
        'totalsaving':totalsaving,
    }
    return render(request,'home/othersaving.html',context)