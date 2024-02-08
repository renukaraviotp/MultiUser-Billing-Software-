from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    Company_code = models.CharField(max_length=100,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    gst_type = models.CharField(max_length=255,null=True,blank=True)
    gst_no = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/patient')


class staff_details(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    user_name = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    img = models.ImageField(null=True,blank = True,upload_to = 'image/staff')    
    position = models.CharField(max_length=255,null=True,blank=True,default='staff')


class Parties(models.Model):
    party_name = models.CharField(max_length =255)
    phone_number = models.CharField(max_length = 10)
    gstin = models.CharField(max_length =16)
    gst_type = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    opening_balance = models.FloatField(default = 0)
    to_pay = models.BooleanField(null=True)
    to_recieve = models.BooleanField(null = True)
    date =  models.DateField(null = True)
    company = models.ForeignKey(company,on_delete=models.CASCADE,default='')
    staff = models.ForeignKey(staff_details,on_delete=models.CASCADE,default='')
    
class History(models.Model):
    staff = models.ForeignKey(staff_details,on_delete=models.CASCADE,default='')
    company = models.ForeignKey(company,on_delete=models.CASCADE,default='')
    party = models.ForeignKey(Parties,on_delete=models.CASCADE,default='')
    action = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now().date())
    
class SalesInvoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details, on_delete=models.CASCADE,null=True,blank=True)
    party = models.ForeignKey(Parties, on_delete=models.CASCADE,null=True,blank=True)
    party_name = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    invoice_no = models.IntegerField(default=0,null=True,blank=True)
    date = models.DateField()
    state_of_supply = models.CharField(max_length=255,null=True,blank=True)
    paymenttype = models.CharField(max_length=255,null=True,blank=True)
    cheque = models.CharField(max_length=255,null=True,blank=True)
    upi = models.CharField(max_length=255,null=True,blank=True)
    accountno = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(max_length=255,null=True,blank=True)
    subtotal = models.CharField(max_length=100,default=0, null=True)
    igst = models.CharField(max_length=100,default=0, null=True)
    cgst = models.CharField(max_length=100,default=0, null=True)
    sgst = models.CharField(max_length=100,default=0, null=True)
    total_taxamount = models.CharField(max_length=100,default=0)
    adjustment = models.CharField(max_length=100,default=0, null=True)
    grandtotal = models.FloatField(default=0, null=True)
    paidoff = models.CharField(null=True,blank=True,max_length=255)
    totalbalance = models.CharField(null=True,blank=True,max_length=255)


class ItemModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company,on_delete= models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete= models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=255,null=True)
    item_hsn = models.PositiveIntegerField(null=True)
    item_unit = models.CharField(max_length=255,null=True)
    item_type = models.CharField(max_length=255,null=True)
    item_taxable = models.CharField(max_length=255,null=True)
    item_gst = models.CharField(max_length=255,null=True)
    item_igst = models.CharField(max_length=255,null=True)
    item_sale_price = models.PositiveIntegerField(null=True)
    item_current_stock = models.PositiveBigIntegerField(default=0)
    item_purchase_price = models.PositiveBigIntegerField()
    item_stock_in_hand = models.PositiveBigIntegerField(default=0)
    item_at_price = models.PositiveBigIntegerField(default=0)
    item_date = models.DateField(null=True)


class ItemUnitModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company,on_delete= models.CASCADE,null=True,blank=True)
    unit_name = models.CharField(max_length=255,null=True)


class ItemTransactionModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company,on_delete= models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete= models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(ItemModel,on_delete=models.CASCADE,null=True,blank=True)
    trans_type = models.CharField(max_length=255,null=True)
    trans_invoice = models.PositiveBigIntegerField(null=True,blank=True)
    trans_user_name = models.CharField(max_length=255,null=True)
    trans_date = models.DateTimeField(null=True)
    trans_qty = models.PositiveBigIntegerField(default=0)
    trans_current_qty = models.PositiveBigIntegerField(default=0)
    trans_adjusted_qty = models.PositiveBigIntegerField(default=0)
    trans_price = models.PositiveBigIntegerField(default=0)
    trans_status = models.CharField(max_length=255,null=True)
    trans_created_date = models.DateTimeField(auto_now_add=True,null=True)



class ItemTransactionHistory(models.Model):
    staff = models.ForeignKey(staff_details,on_delete=models.CASCADE,blank=True,null=True)
    company = models.ForeignKey(company,on_delete=models.CASCADE,blank=True,null=True)
    item = models.ForeignKey(ItemModel,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateField(auto_now_add=True,null=True)
    action = models.CharField(max_length=255,null=True)
    done_by_name = models.CharField(max_length=255,null=True)

class SalesInvoiceItem(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details, on_delete=models.CASCADE,null=True,blank=True)
    salesinvoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE,null=True,blank=True)
    hsn = models.IntegerField(default=0,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,null=True,blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,null=True,blank=True)
    tax =  models.CharField(max_length=255,null=True,blank=True)
    totalamount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00,null=True,blank=True)


class Creditnote(models.Model):
    party=models.ForeignKey(Parties,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete=models.CASCADE,default='')
    salesinvoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE,null=True,blank=True)
    party_name = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    invoice_no = models.IntegerField(default=0,null=True,blank=True)
    idate = models.DateField(null=True)
    state_of_supply = models.CharField(max_length=255,null=True,blank=True)
    date=models.DateField(null=True)
    returnno=models.IntegerField(default=0,null=True,blank=True)
    gstin = models.CharField(max_length =16,null=True) 
    subtotal=models.FloatField(default=0,null=True,blank=True)
    sgst=models.FloatField(default=0,null=True,blank=True)
    cgst=models.FloatField(default=0,null=True,blank=True)
    igst=models.FloatField(default=0,null=True,blank=True)
    taxamount=models.FloatField(default=0,null=True,blank=True)
    roundoff=models.FloatField(default=0,null=True,blank=True)
    grandtotal=models.FloatField(default=0,null=True,blank=True)
    description=models.CharField(max_length =50,null=True) 
    
class CreditnoteItem(models.Model):
    credit=models.ForeignKey(Creditnote,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete=models.CASCADE,default='')
    product=models.CharField(max_length =50,null=True)  
    hsn=models.CharField(max_length =50,null=True) 
    qty=models.IntegerField(default=0,null=True,blank=True)
    price=models.IntegerField(default=0,null=True,blank=True)
    tax=models.CharField(max_length =50,null=True) 
    discount=models.FloatField(default=0,null=True,blank=True)
    total=models.FloatField(default=0,null=True,blank=True)
    
class CreditnoteHistory(models.Model):
    party=models.ForeignKey(Parties,on_delete=models.CASCADE,null=True,blank=True)
    credit=models.ForeignKey(Creditnote,on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(company, on_delete=models.CASCADE,null=True,blank=True)
    staff = models.ForeignKey(staff_details,on_delete=models.CASCADE,default='')
    action=models.CharField(max_length=255,null=True)
        
    

