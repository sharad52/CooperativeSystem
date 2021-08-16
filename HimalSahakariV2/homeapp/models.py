from django.db import models
import nepali_datetime


# Create your models here.
class ShareMember(models.Model):
    member_id = models.IntegerField('सदस्य नं')
    name = models.CharField('नाम',max_length=100)
    share_purchase_date = models.DateField('सेयर खरिद मिती')
    totalshare = models.IntegerField('जम्मा सेयर',default=0)
    add_share = models.IntegerField('सेयर थप्नुहोस',default=0)
    remove_share = models.IntegerField('सेयर घटाउनुहोस्',default=0)
    rate = models.IntegerField('ब्याजदर',default=12,help_text='% मा राख्नुहोस्')
    munafa = models.IntegerField(default=0)
    profit = models.IntegerField('मुनाफा',default=0)
    drawprofit = models.IntegerField('निकाल्न चाहेको मुनाफा रकम',default=0)

    def ShareDuration(self):
        year =  (nepali_datetime.date.today().year - self.share_purchase_date.year)*12 
        month = nepali_datetime.date.today().month - self.share_purchase_date.month
        number_of_months = year + month
        return number_of_months

    def ShareAmount(self):
        return self.totalshare*100

    def Profit(self):
        r = self.rate/1200
        return (self.ShareAmount()*r*self.ShareDuration()-self.munafa)
        

    def total(self):
        return self.ShareAmount()+ self.Profit()

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.profit = self.Profit()
        super(ShareMember,self).save(*args,**kwargs)

    class Meta:
        ordering = ["member_id"]
        db_table = "sharemember"

class ShareMemberSaving(models.Model):
    MONTHS = (
        ('बैशाख','बैशाख'),
        ('जेष्ठ','जेष्ठ'),
        ('असार','असार'),
        ('साउन','साउन'),
        ('भदौ','भदौ'),
        ('असोज','असोज'),
        ('कार्तिक','कार्तिक'),
        ('मङ्सिर','मङ्सिर'),
        ('पौष','पौष'),
        ('माघ','माघ'),
        ('फाल्गुन','फाल्गुन'),
        ('चैत्र','चैत्र')
    )
    YEAR_CHOICES = []
    for r in range(2073,2100):
        YEAR_CHOICES.append((r,r))
    name = models.ForeignKey(ShareMember,on_delete=models.CASCADE,verbose_name='नाम')
    year = models.IntegerField('बर्ष',('year'), choices=YEAR_CHOICES)
    month = models.CharField(max_length=50,choices=MONTHS,verbose_name='महिना')
    amount = models.FloatField(default=0,verbose_name='रकम')
    interestfactor = models.FloatField(null=True,blank=True)

    def save(self,*args,**kwargs):
        if self.month == 'बैशाख':
            self.interestfactor = 12*0.015
        elif self.month == 'जेष्ठ':
            self.interestfactor = 11*0.015
        elif self.month == 'असार':
            self.interestfactor = 10*0.015
        elif self.month == 'साउन':
            self.interestfactor = 9*0.015
        elif self.month == 'भदौ':
            self.interestfactor = 8*0.015
        elif self.month == 'असोज':
            self.interestfactor = 7*0.015
        elif self.month == 'कार्तिक':
            self.interestfactor = 6*0.015
        elif self.month == 'मङ्सिर':
            self.interestfactor = 5*0.015
        elif self.month == 'पौष':
            self.interestfactor = 4*0.015
        elif self.month == 'माघ':
            self.interestfactor = 3*0.015
        elif self.month == 'फाल्गुन':
            self.interestfactor = 2*0.015
        elif self.month == 'चैत्र':
            self.interestfactor = 1*0.015
        super(ShareMemberSaving,self).save(*args,**kwargs)
   
    def __str__(self):
        return str(f"{self.name.name}/{self.year}/{self.month} / {self.amount}")

    class Meta:
        ordering = ['id']
        db_table = "sharemembersaving"
        unique_together = [('name','year', 'month')]

class ClientName(models.Model):
    GENDER = (
        ('पुरुष','पुरुष'),
        ('महिला','महिला'),
        ('समलिङ्गी','समलिङ्गी')
    )
    name = models.CharField('नाम',max_length=100)
    gender = models.CharField('लिङ्ग',max_length=50,choices=GENDER)
    phone = models.CharField('फोन',max_length=100)
    email = models.EmailField('ईमेल',blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "clientname"
            

class Client(models.Model):
    name = models.ForeignKey(ClientName,on_delete=models.CASCADE,verbose_name="नाम")
    amount = models.IntegerField('रकम')
    loan_rate = models.IntegerField('ब्याजदर राख्नुहोस्',default=18)
    loan_drawn_date = models.DateField('ऋण लिएको मिती')
    is_complete = models.BooleanField('रकम चुक्ता भयो।',default=False)

    def __str__(self):
        return str(f"{self.name.name}- {self.amount}")

    def interest(self):
        year =  (nepali_datetime.date.today().year - self.loan_drawn_date.year)*12 
        month = nepali_datetime.date.today().month - self.loan_drawn_date.month
        number_of_months = year + month
        rate = (self.loan_rate/1200)
        interest_amount = self.amount*rate*number_of_months
        return interest_amount

    def total(self):
        total_amount = self.amount + self.interest()
        return total_amount

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

    class Meta:
        db_table = "client"
    

class ClientSchedulePayment(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE,verbose_name='ऋण बिबरण')
    payment_amount = models.IntegerField('किस्ता रकम')
    payment_date = models.DateField('किस्ता मिती')
    

    def __str__(self):
        return self.client.name.name

    class Meta:
        db_table = "schedulepayment"


class Expenses(models.Model):
    title = models.CharField('खर्च शिर्षक',max_length=100)
    amount = models.IntegerField('रकम')
    expense_date = models.DateField('खर्च मिती')
    remarks = models.TextField('कैफियत')

    def __str__(self):
        return str(f"{self.title}={self.amount}")

    class Meta:
        db_table = 'expenses'

class OtherSaving(models.Model):
    title = models.CharField('बचत शिर्षक',max_length=100)
    amount = models.IntegerField('रकम')
    deposit_date = models.DateField('बचत मिती')
    remarks = models.TextField('कैफियत')

    def __str__(self):
        return str(f"{self.title}={self.amount}")

    class Meta:
        db_table = 'othersaving'

