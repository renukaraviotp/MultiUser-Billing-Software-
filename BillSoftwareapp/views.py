from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from . models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.utils.text import capfirst
from datetime import date
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
from xhtml2pdf import pisa
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

# Create your views here.

def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')

def contact(request):
  return render(request, 'contact.html')


def service(request):
  return render(request, 'service.html')


def homepage(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmpp = company.objects.get(id=staff.company.id)
  context={
   'staff':staff,
    'cmpp':cmpp,
  }
  return render(request, 'companyhome.html',context)


def staffhome(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmpp = company.objects.get(id=staff.company.id)
  context={
   'staff':staff,
    'cmpp':cmpp,
  }
  return render(request, 'staffhome.html',context)

def register(request):
  return render(request, 'register.html')

def registercompany(request):
  return render(request, 'registercompany.html')

def registerstaff(request):
  return render(request, 'registerstaff.html')

def login(request):
  return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')



def registeruser(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_name = request.POST['username']
        email_id = request.POST['email']
        mobile = request.POST['phoneno']
        passw = request.POST['pass']
        c_passw = request.POST['re_pass']
        profile_pic=request.FILES.get('image')

        if passw != c_passw:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Sorry, Username already exists')
            return redirect('register')

        if User.objects.filter(email=email_id).exists():
            messages.error(request, 'Sorry, Email already exists')
            return redirect('register')

        # If everything is okay, save the data
        user_data = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=user_name,
            email=email_id,
            password=passw
        )
        user_data.save()

        data = User.objects.get(id=user_data.id)
        cust_data = company(contact=mobile,profile_pic=profile_pic, user=data)
        cust_data.save()

        demo_staff=staff_details(company=cust_data,
                                   email=email_id,
                                   position='company',
                                   user_name=user_name,
                                   password=passw,
                                   contact=mobile)
        demo_staff.save()

        # messages.success(request, 'Registration successful')
        return redirect('registercompany')

    return render(request, 'register.html')
  
def add_company(request):
  
  if request.method == 'POST':
    email=request.POST['email']
    user=User.objects.get(email=email)
    
    c =company.objects.get(user = user)
    c.company_name=request.POST['companyname']

    c.address=request.POST['address']
    c.city=request.POST['city']
    c.state=request.POST['state']
    c.country=request.POST['country']
    c.pincode=request.POST['pincode']
    c.pan_number=request.POST['pannumber']
    c.gst_type=request.POST['gsttype']
    c.gst_no=request.POST['gstno']

    code=get_random_string(length=6)
    if company.objects.filter(Company_code = code).exists():
       code2=get_random_string(length=6)
       c.Company_code=code2
    else:
      c.Company_code=code
   
    c.save()

    staff = staff_details.objects.get(email=email,position='company',company=c)
    staff.first_name = request.POST['companyname']
    staff.last_name = ''
    staff.save()

    return redirect('login')  
  return render(request,'registercompany.html') 

def staff_registraction(request):
  if request.method == 'POST':
    fn=request.POST['fname']
    ln=request.POST['lname']
    email=request.POST['email']
    un=request.POST['username']
    ph=request.POST['phoneno']
    pas=request.POST['pass']
    code=request.POST['companycode']

    if company.objects.filter(Company_code=code).exists():
      com=company.objects.get(Company_code=code)
    else:
        messages.info(request, 'Sorry, Company code is Invalide')
        return redirect('registerstaff')
    img=request.FILES.get('image')

    if staff_details.objects.filter(user_name=un).exists():
      messages.info(request, 'Sorry, Username already exists')
      return redirect('registerstaff')
    elif staff_details.objects.filter(email=email).exists():
      messages.info(request, 'Sorry, Email already exists')
      return redirect('registerstaff')
    else:
      
      staff=staff_details(first_name=fn,last_name=ln,email=email,user_name=un,contact=ph,password=pas,img=img,company=com)
      staff.save()
      return redirect('login')

  else:
    print(" error")
    return redirect('registerstaff')
  

  
def loginurl(request):
  if request.method == 'POST':
    user_name = request.POST['username']
    passw = request.POST['pass']
    
    log_user = auth.authenticate(username = user_name,
                                  password = passw)
    
    if log_user is not None:
      auth.login(request, log_user)
        
    if staff_details.objects.filter(user_name=user_name,password=passw,position='company').exists():
      data = staff_details.objects.get(user_name=user_name,password=passw,position='company') 

      request.session["staff_id"]=data.id
      if 'staff_id' in request.session:
        if request.session.has_key('staff_id'):
          staff_id = request.session['staff_id']
          print(staff_id)
 
        return redirect('homepage')  

    if staff_details.objects.filter(user_name=user_name,password=passw,position='staff').exists():
      data = staff_details.objects.get(user_name=user_name,password=passw,position='staff')   

      request.session["staff_id"]=data.id
      if 'staff_id' in request.session:
        if request.session.has_key('staff_id'):
          staff_id = request.session['staff_id']
          print(staff_id)
 
          return redirect('staffhome')  
    else:
      messages.info(request, 'Invalid Username or Password. Try Again.')
      return redirect('login')  
  else:  
   return redirect('login')   
  
  

@login_required(login_url='login')  
def profile(request):
    if request.user.is_authenticated:
        try:
            com = company.objects.get(user=request.user)
            context = {'company': com}
            return render(request, 'profile.html', context)
        except company.DoesNotExist:
            messages.error(request, 'Company not found for the authenticated user.')
            return redirect('login')
    else:
        messages.info(request, 'Please log in to view your profile.')
        return redirect('login')
    

def editprofile(request,pk):
  com= company.objects.get(id = pk)
  context={
     'company':com
  }
  return render(request, 'editprofile.html',context)

def edit_profilesave(request,pk):
  com= company.objects.get(id = pk)
  user1 = User.objects.get(id = com.user_id)

  if request.method == "POST":

      user1.first_name = capfirst(request.POST.get('f_name'))
      user1.last_name  = capfirst(request.POST.get('l_name'))
      user1.email = request.POST.get('email')
      com.contact = request.POST.get('cnum')
      com.address = capfirst(request.POST.get('ards'))
      com.company_name = request.POST.get('comp_name')
      user1.email = request.POST.get('comp_email')
      com.city = request.POST.get('city')
      com.state = request.POST.get('state')
      com.country = request.POST.get('country')
      com.pincode = request.POST.get('pinc')
      com.gst_type = request.POST.get('gsttype')
      com.gst_no = request.POST.get('gstno')
      com.pan_number = request.POST.get('pan')
      if len(request.FILES)!=0 :
          com.profile_pic = request.FILES.get('file')

      com.save()
      user1.save()
      return redirect('profile')

  context = {
      'company' : com,
      'user1' : user1,
  } 

  return render(request,'editprofile.html',context)

def base(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)
  context = {
              'staff' : staff

          }
  return render(request, 'base.html',context)

def staffprofile(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)
  context = {
              'staff' : staff

          }
  return render(request,'profilestaff.html',context)

def editstaffprofile(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)
  context={
     'staff':staff
  }
  return render(request, 'editstaff.html',context)

def edit_staffprofilesave(request):
  staff_id = request.session['staff_id']
  staff =  staff_details.objects.get(id=staff_id)

  if request.method == "POST":

      staff.first_name = capfirst(request.POST.get('f_name'))
      staff.last_name  = capfirst(request.POST.get('l_name'))
      staff.email = request.POST.get('email')
      staff.contact = request.POST.get('cnum')
      if len(request.FILES)!=0 :
          staff.img = request.FILES.get('file')

      staff.save()
      return redirect('staffprofile')

  context = {
      'staff' : staff
  } 

  return render(request,'editstaff.html',context)

def parties_default(request):
  return render(request,'parties_default.html')

def parties_add_page(request):
  return render(request,'parties_add_page.html')



def credit_default(request): 
  return render(request,'credit_default.html')

def credit_add(request):
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  todaydate = date.today().isoformat()
  party = Parties.objects.filter(company_id=cmp.id)
  item=ItemModel.objects.filter(company_id=cmp.id) 
  item_units = ItemUnitModel.objects.filter(company=cmp)
  last_ref = Creditnote.objects.filter(company=cmp).order_by('-returnno').first()
  if last_ref:
        refno = last_ref.returnno + 1
  else:
        refno = 1
  context = {
        'refno': refno,
        'party':party,
        'item':item,
        'todaydate':todaydate,
        'item_units':item_units
    }
  return render(request, 'credit_add.html',context)


def get_sales_invoice_details(request, party_id):
    try:
        # Assuming 'party_id' is the foreign key to the Party model in your SalesInvoice model
        sales_invoice = SalesInvoice.objects.filter(party__id=party_id).latest('date')

        # Assuming 'invoice_no' and 'date' are fields in your SalesInvoice model
        data = {
            'billNo': sales_invoice.invoice_no,
            'billDate': sales_invoice.date.strftime('%Y-%m-%d'),  # Format the date as needed
        }
        return JsonResponse(data)
    except SalesInvoice.DoesNotExist:
        return JsonResponse({'error': 'Sales invoice not found'}, status=404)
      
def creditbilldata(request):
    try:
        partyid = request.POST['id']
        party_instance = Parties.objects.get(id=partyid)

        # Initialize lists to store multiple bill numbers and dates
        bill_numbers = []
        bill_dates = []

        try:
            # Retrieve all instances for the party
            bill_instances = SalesInvoice.objects.filter(party=party_instance)

            # Loop through each instance and collect bill numbers and dates
            for bill_instance in bill_instances:
                bill_numbers.append(bill_instance.invoice_no)
                bill_dates.append(bill_instance.date)

        except SalesInvoice.DoesNotExist:
            pass

        # Return a JSON response with the list of bill numbers and dates
        if not bill_numbers and not bill_dates:
            return JsonResponse({'bill_numbers': ['nobill'], 'bill_dates': ['nodate']})

        return JsonResponse({'bill_numbers': bill_numbers, 'bill_dates': bill_dates})

    except KeyError:
        return JsonResponse({'error': 'The key "id" is missing in the POST request.'})

    except Parties.DoesNotExist:
        return JsonResponse({'error': 'Party not found.'})
    
def credit_bill_date(request):
    selected_bill_no = request.POST.get('billNo', None)
    print(selected_bill_no)

    try:

        # Get the latest SalesInvoice with the specified bill_number and party
        bill = SalesInvoice.objects.filter(invoice_no=selected_bill_no).latest('date')
        bill_date = bill.date.strftime('%Y-%m-%d')
        print(bill_date)
        
    except SalesInvoice.DoesNotExist:
        return JsonResponse({'error': 'Bill number not found'}, status=400)
    except SalesInvoice.MultipleObjectsReturned:
        return JsonResponse({'error': 'Multiple SalesInvoices found for the same bill number'}, status=400)

    return JsonResponse({'bill_date': bill_date})

      
# def get_sales_invoice_details(request):
#     if request.method == 'POST':
#         pid = request.POST.get('pid')
        
#         # Fetch bill details from the database based on the party_id
#         try:
#             invoice = SalesInvoice.objects.get(party=pid)
#             response_data = {
#                 'bill_number': invoice.invoice_no,
#                 'bill_date': invoice.date.strftime('%Y-%m-%d'),  # Assuming date is a DateTimeField
#             }
#             return JsonResponse(response_data)
#         except SalesInvoice.DoesNotExist:
#             return JsonResponse({'error': 'Invoice not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_bill_details(request):
    if request.method == 'POST' and request.is_ajax():
        party_id = request.POST.get('party_id')
        try:
            # Assuming SalesInvoice has a ForeignKey to the Party model and fields invoice_no and date
            invoice = SalesInvoice.objects.filter(party=party_id).latest('id')  # Get the latest invoice for the party
            bill_details = {
                'billNo': invoice.invoice_no,
                'billDate': invoice.date.strftime('%Y-%m-%d'),  # Convert date to string format if needed
            }
            return JsonResponse(bill_details)
        except SalesInvoice.DoesNotExist:
            return JsonResponse({'error': 'No bill found for this party.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


def item_details(request):
    item_id = request.GET.get('id')
    item = get_object_or_404(ItemModel, id=item_id)
    

    hsn = item.item_hsn
    price = item.item_sale_price
    gst = item.item_gst
    igst = item.item_igst
    qty = item.item_current_stock
    print(hsn)
    print(price)
    print(gst)
    print(igst)
    print(qty)
    return JsonResponse({'hsn': hsn, 'price': price, 'gst': gst, 'igst': igst, 'qty': qty})
  
# def item_dropdown(request):
#     options={}
#     option_objects=ItemModel.objects.all()
#     for option in option_objects:
#       options[option.id]=[option.item_name]
#     return JsonResponse(options)
      


def party_save(request):
    
    sid = request.session.get('staff_id')
    staff = staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    user = cmp.id
    
    if request.method == 'POST':
        partyname = request.POST['partyname'].capitalize()
        mobilenumber = request.POST['mobilenumber']
        gstin = request.POST['gstin']
        gstintype = request.POST['gstintype']
        state = request.POST['state']
        email = request.POST['email']
        Date = request.POST['date']
        address = request.POST['address']
        balance = request.POST['balance']
        buttonn = request.POST['buttonn']
        if balance == '' or balance == '0' :
                 
              party = Parties(party_name = partyname,phone_number = mobilenumber, gstin = gstin,
                              gst_type = gstintype, billing_address = address, state = state,
                              email = email, date = Date,company_id=user,staff_id=staff.id)
              party.save()

              history = History(company_id=user,party_id=party.id,staff_id=staff.id,action='CREATED')
              history.save()
              
        else:
              if request.POST['pay_recieve'] != '':
                  pay_recieve = request.POST['pay_recieve']

                  if pay_recieve == 'receive':
                      party = Parties(party_name = partyname,phone_number = mobilenumber, gstin = gstin,
                                      gst_type = gstintype, billing_address = address, state = state,
                                      email = email, date = Date,opening_balance = balance,to_recieve = True,
                                      company_id=user,staff_id=staff.id)
                      party.save()
                      history = History(company_id=user,party_id=party.id,staff_id=staff.id,action='CREATED')
                      history.save()

                  elif pay_recieve == 'pay':
                      neg_balance = -int(balance)
                      party = Parties(party_name = partyname,phone_number = mobilenumber, gstin = gstin,
                                      gst_type = gstintype, billing_address = address, state = state,
                                      email = email, date = Date,opening_balance = neg_balance,to_pay = True,
                                      company_id=user,staff_id=staff.id)
                      party.save()
                      history = History(company_id=user,party_id=party.id,staff_id=staff.id,action='CREATED')
                      history.save()
                  else:
                      party = Parties(party_name = partyname,phone_number = mobilenumber, gstin = gstin,
                                      gst_type = gstintype, billing_address = address, state = state,
                                      email = email, date = Date,staff_id=staff.id,company_id=user)
                      party.save()
                      history = History(company_id=user,party_id=party.id,staff_id=staff.id,action='CREATED')
                      history.save()

        if buttonn == 'new':
              return redirect('credit_add')
        elif buttonn == 'old':
              return redirect('credit_add') 
            
def item_save(request):
    
  if request.method == 'POST':
    sid = request.session.get('staff_id')
    staff = staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    itemname=request.POST['item_name']
    hsn=request.POST['hsn']
    unit=request.POST['unit']
    saleprice=request.POST['saleprice']
    purchaseprice=request.POST['purchaseprice']
    intra_st=request.POST['intra_st']
    inter_st=request.POST['inter_st']
    item=ItemModel(item_name=itemname,item_hsn=hsn,item_unit=unit,item_sale_price=saleprice,item_purchase_price=purchaseprice,item_gst=intra_st,item_igst=inter_st,staff=staff,company=cmp)
    item.save()
    return redirect('credit_add') 
  

def itemdetails(request):
    itmid = request.GET['id']
    itm = ItemModel.objects.get(id=itmid)
    hsn = itm.item_hsn
    gst = itm.item_gst
    igst = itm.item_igst
    price = itm.item_sale_price
    qty = itm.item_current_stock
    return JsonResponse({'hsn': hsn, 'gst': gst, 'igst': igst, 'price': price, 'qty': qty})
# def saveparty(request):
#     if request.method == 'POST':
#         # Retrieve session and company information
#         sid = request.session.get('staff_id')
#         staff = staff_details.objects.get(id=sid)
#         company_obj = company.objects.get(id=staff.company.id)

#         # Retrieve party data from POST request
#         party_name = request.POST.get('partyname', '').capitalize()
#         mobile_number = request.POST.get('mobilenumber', '')
#         gstin = request.POST.get('gstin', '')
#         gstintype = request.POST.get('gstintype', '')
#         state = request.POST.get('state', '')
#         email = request.POST.get('email', '')
#         date = request.POST.get('date', '')
#         address = request.POST.get('address', '')
#         balance = request.POST.get('balance', '')

#         # Check if party already exists
#         if Parties.objects.filter(phone_number=mobile_number, company=company_obj).exists():
#             return JsonResponse({'success': False, 'message': 'Contact number already exists'})
#         elif Parties.objects.filter(email=email, company=company_obj).exists():
#             return JsonResponse({'success': False, 'message': 'Email already exists'})
#         elif Parties.objects.filter(gstin=gstin, company=company_obj).exists():
#             return JsonResponse({'success': False, 'message': 'GST number already exists'})
#         else:
#             if balance == '' or balance == '0':
#                 party = Parties(party_name=party_name, phone_number=mobile_number, gstin=gstin,
#                                 gst_type=gstintype, billing_address=address, state=state,
#                                 email=email, date=date, company=company_obj, staff_id=staff.id)
#                 party.save()

#                 history = History(company=company_obj, party_id=party.id, staff_id=staff.id, action='CREATED')
#                 history.save()
#                 return JsonResponse({'success': True, 'id': party.id})
#             else:
#                 if request.POST.get('pay_recieve') != '':
#                     pay_recieve = request.POST.get('pay_recieve')

#                     if pay_recieve == 'receive':
#                         party = Parties(party_name=party_name, phone_number=mobile_number, gstin=gstin,
#                                         gst_type=gstintype, billing_address=address, state=state,
#                                         email=email, date=date, opening_balance=balance, to_recieve=True,
#                                         company=company_obj, staff_id=staff.id)
#                         party.save()
#                         history = History(company=company_obj, party_id=party.id, staff_id=staff.id, action='CREATED')
#                         history.save()
#                         return JsonResponse({'success': True, 'id': party.id})
#                     elif pay_recieve == 'pay':
#                         neg_balance = int(balance)
#                         party = Parties(party_name=party_name, phone_number=mobile_number, gstin=gstin,
#                                         gst_type=gstintype, billing_address=address, state=state,
#                                         email=email, date=date, opening_balance=neg_balance, to_pay=True,
#                                         company=company_obj, staff=staff)
#                         party.save()
#                         history = History(company=company_obj, party_id=party.id, staff_id=staff.id, action='CREATED')
#                         history.save()
#                         return JsonResponse({'success': True, 'id': party.id})
#                     else:
#                         party = Parties(party_name=party_name, phone_number=mobile_number, gstin=gstin,
#                                         gst_type=gstintype, billing_address=address, state=state,
#                                         email=email, date=date, staff_id=staff.id, company=company_obj)
#                         party.save()
#                         history = History(company=company_obj, party_id=party.id, staff_id=staff.id, action='CREATED')
#                         history.save()
#                         return JsonResponse({'success': True, 'id': party.id})
#     else:
#         return JsonResponse({'success': False, 'message': 'Invalid request method'})

def saveparty(request):
    sid = request.session.get('staff_id')
    staff = staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)

    party_name = request.POST['name']
    email = request.POST['email']
    
    phone_number = request.POST.get('mobile', None)
    state = request.POST['splystate']
    address = request.POST['baddress']
    gst_type = request.POST['gsttype']
    gst_no = request.POST['gstin']
    openingbalance = request.POST.get('openbalance')
    payment = request.POST.get('paytype')
    End_date = request.POST.get('enddate', None)
    
    
    part = Parties(
        party_name=party_name,
        gstin=gst_no,
        phone_number=phone_number,
        gst_type=gst_type,
        state=state,
        billing_address=address,
        email=email,
        opening_balance=openingbalance,
        to_pay=(payment == 'to_pay'),  # Set to True if payment is 'to_pay'
        to_recieve=(payment == 'to_receive'),        
        date=End_date,
        company=cmp,
        staff=staff,

        
    )
    part.save()
    history_action =  "Created"
    history = History(
        staff=staff,
        company=cmp,
        party=part,
        action=history_action,
    )
    history.save()
    
  
    
    partyobj = Parties.objects.filter(company=cmp).values('id', 'party_name')
    print(partyobj)

    party_list = [{'id': employee['id'], 'name': employee['party_name']} for employee in partyobj]
    print(party_list)

    return JsonResponse({'party_list':party_list, 'success': True, 'message': 'Customer saved successfully.'})
  
def check_gstin_exists(request):
    gstin = request.GET.get('gstin')
    sid = request.session.get('staff_id')
    staff = staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    gsttype = request.GET.get('gsttype')  
    print(gsttype)

    if gsttype != "Unregistered or Consumer":
        if Parties.objects.filter(company=cmp, gstin=gstin).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})
      
def check_email_exists(request):
    email= request.GET.get('email')
    if Parties.objects.filter(email=email).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists':False})
  
  
def check_phone_number_exists(request):
    phone_number = request.GET.get('phone_number')
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    if Parties.objects.filter(company=cmp,phone_number=phone_number).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})

# def party_dropdown(request):
#     sid = request.session.get('staff_id')
#     staff = staff_details.objects.get(id=sid)
#     company_obj = company.objects.get(id=staff.company.id)
#     parties = Parties.objects.filter(company=company_obj)

#     id_list = [party.id for party in parties]
#     party_list = [party.party_name for party in parties]

#     return JsonResponse({'id_list': id_list, 'party_list': party_list})

def party_dropdown(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  part = Parties.objects.filter(company=cmp) 

  id_list = []
  party_list = []
  for p in part:
    id_list.append(p.id)
    party_list.append(p.party_name)

  return JsonResponse({'id_list':id_list, 'party_list':party_list })
  
def saveitemc(request):
  if request.method == 'POST':
    sid = request.session.get('staff_id')
    staff = staff_details.objects.get(id=sid)
    company_obj = staff.company

    name = request.POST.get('name')
    print(name)
    unit = request.POST.get('unit')
    hsn = request.POST.get('hsn')
    taxref = request.POST.get('taxref')
    sell_price = request.POST.get('sell_price')
    cost_price = request.POST.get('cost_price')
    intra_st = request.POST.get('intra_st')
    inter_st = request.POST.get('inter_st')
    itmdate = request.POST.get('itmdate')
    stock = request.POST.get('stock')
    itmprice = request.POST.get('itmprice')
    minstock = request.POST.get('minstock')

    # if not hsn:
    #     hsn = None

    # Check if HSN exists for the given company
    if ItemModel.objects.filter(company=company_obj, item_hsn=hsn).exists():
        return JsonResponse({'success': False, 'message': 'HSN already exists'})

    itm = ItemModel(
        item_name=name, item_hsn=hsn, item_unit=unit, item_type='Type', item_taxable=taxref, item_gst=intra_st,
        item_igst=inter_st, item_sale_price=sell_price, item_purchase_price=cost_price, item_current_stock=stock,
        item_stock_in_hand=stock, item_at_price=itmprice, item_date=itmdate, company=company_obj, user=company_obj.user
    )
    itm.save()

    return JsonResponse({'success': True})
  
  return JsonResponse({'success': False, 'message': 'Invalid request method'})


def item_dropdownc(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  print(sid, staff, cmp)
  options = {}
  option_objects = ItemModel.objects.filter(company=cmp)
  for option in option_objects:
      options[option.id] = [option.id, option.item_name]
  return JsonResponse(options)

def save_item(request):
    if request.method == 'POST':
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        company_obj = staff.company
        item_name = request.POST.get('item_name', '').strip()
        hsn = request.POST.get('hsn', '').strip()
        unit = request.POST.get('unit', '').strip()
        taxref = request.POST.get('taxref', '').strip()
        sell_price = request.POST.get('sell_price', '').strip()
        cost_price = request.POST.get('cost_price', '').strip()
        intra_st = request.POST.get('intra_st', '').strip()
        inter_st = request.POST.get('inter_st', '').strip()
        itmdate = request.POST.get('itmdate', '').strip()
        stock = request.POST.get('stock', '').strip()
        itmprice = request.POST.get('itmprice', '').strip()
        minstock = request.POST.get('minstock', '').strip()
        # Retrieve other form fields similarly
        
        # Perform any validation if needed
        if not item_name:
            return JsonResponse({'success': False, 'message': 'Item name is required'})
        if not hsn:
            return JsonResponse({'success': False, 'message': 'HSN is required'})
        if ItemModel.objects.filter(company=company_obj, item_hsn=hsn).exists():
          return JsonResponse({'success': False, 'message': 'HSN already exists'})
        
        # Save item to database
        try:
            item = ItemModel(item_name=item_name, item_hsn=hsn, item_unit=unit, item_type='Type', item_taxable=taxref, item_gst=intra_st,
        item_igst=inter_st, item_sale_price=sell_price, item_purchase_price=cost_price, item_current_stock=stock,
        item_stock_in_hand=stock, item_at_price=itmprice, item_date=itmdate, company=company_obj, user=company_obj.user
    )
            # Set additional fields similarly
            
            item.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def item_dropdowne(request):
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    # Retrieve items from the database
    items = ItemModel.objects.filter(company=cmp)
    
    # Prepare data for dropdown
    id_list = [item.id for item in items]
    item_list = [item.item_name for item in items]
    
    return JsonResponse({'id_list': id_list, 'item_list': item_list})



# def savecredititem(request):
#     sid = request.session.get('staff_id')
#     staff =  staff_details.objects.get(id=sid)
#     cmp = company.objects.get(id=staff.company.id)
#     if request.method == 'POST':
#         item_name = request.POST.get('item_name')
#         hsn = request.POST.get('hsn')
#         qty = request.POST.get('qty')
#         tax_ref = request.POST.get('taxref')
#         intra_st = request.POST.get('intra_st')
#         inter_st = request.POST.get('inter_st')
#         sale_price = request.POST.get('saleprice')
#         purchase_price = request.POST.get('purprice')


#         # Check if the HSN already exists
#         if ItemModel.objects.filter(item_hsn=hsn).exists():
#             return JsonResponse({'success': False, 'message': 'HSN Number already exists'})
#         else:
#             # Save new item
#             item = ItemModel(
#             item_name=item_name,
#             item_hsn=hsn,
#             item_current_stock=qty,
#             item_taxable=tax_ref,
#             item_gst=intra_st,
#             item_igst=inter_st,
#             item_sale_price=sale_price,
#             item_purchase_price=purchase_price,
#             staff=staff,
#             company=cmp
#         )
#         item.save()
#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'success': False, 'message': 'Invalid request method'})

# def credititem_dropdown(request):
#   sid = request.session.get('staff_id')
#   staff =  staff_details.objects.get(id=sid)
#   cmp = company.objects.get(id=staff.company.id)
#   print(sid, staff, cmp)
#   options = {}
#   option_objects = ItemModel.objects.filter(company=cmp)
#   for option in option_objects:
#       options[option.id] = [option.id, option.item_name]
#   return JsonResponse(options)
  


def credit_save(request):
    if request.method == 'POST':
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)

        # Retrieve party details if available
        party_id = request.POST.get('partyname')
        party = None
        if party_id:
            party = Parties.objects.get(id=party_id)

        # Check if 'billNo' exists in POST data and assign value accordingly
        # bill_no = request.POST.get('billNo', None)
        # if bill_no == 'nobill':
        #     bill_no = None
        checkbtn=request.POST.get('abc', None)
        if checkbtn == 'on':
          if request.POST.get('billNod') == 'nobill':
             bill_no = None
          else:
            bill_no = request.POST.get('billNod')
        else:
           bill_no = request.POST.get('billNo')
        if checkbtn == 'on':
          if request.POST.get('billDated') == 'nodate':
            bill_date = None
          else:
            bill_date = request.POST.get('billDated')
        else:
          bill_date = request.POST.get('billDate')

        # Check if 'billDate' exists in POST data and assign value accordingly
        # bill_date_str = request.POST.get('billDate', None)
        # bill_date = None
        # if bill_date_str:
        #     bill_date = parse_date(bill_date_str)

        # Create an instance of Creditnote model and save the data
        credit_note = Creditnote(
            party_name=party.party_name if party else None,
            contact=party.phone_number if party else None,
            address=party.billing_address if party else None,
            invoice_no=bill_no,
            idate=bill_date,
            state_of_supply=request.POST.get('placosupply'),
            date=request.POST.get('date'),
            gstin=request.POST.get('gstin'),
            subtotal=request.POST.get('subtotal'),
            sgst=request.POST.get('sgst'),
            cgst=request.POST.get('cgst'),
            igst=request.POST.get('igst'),
            taxamount=request.POST.get('taxamount'),
            roundoff=request.POST.get('adj'),
            grandtotal=request.POST.get('grandtotal'),
            description=request.POST.get('des'),
            returnno=request.POST.get('returnno'),
            staff=staff,
            company=cmp,
            party=party
        )

        # Save the instance
        credit_note.save()
        history = CreditnoteHistory(company=cmp, staff=staff, credit=credit_note, action='Created')
        history.save()

        # Save credit note items
        product = request.POST.getlist("product[]")
        qty = request.POST.getlist("qty[]")
        discount = request.POST.getlist("discount[]")
        total = request.POST.getlist("total[]")
        hsn = request.POST.getlist("hsn[]")
        tax = request.POST.getlist("tax[]")
        price = request.POST.getlist("price[]")

        if len(product) == len(qty) == len(discount) == len(total) == len(hsn) == len(tax) == len(price):
            mapped = zip(product, qty, discount, total, hsn, tax, price)
            for ele in mapped:
                itm = ItemModel.objects.get(id=ele[0])
                CreditnoteItem.objects.create(
                    item=itm,
                    product=itm.item_name,
                    qty=ele[1],
                    discount=ele[2],
                    total=ele[3],
                    hsn=ele[4],
                    tax=ele[5],
                    price=ele[6],
                    company=cmp,
                    credit=credit_note,
                    staff=staff
                )

        Creditnote.objects.filter(company=cmp, staff=staff).update(returnno=F('returnno'))

        if 'Next' in request.POST:
            return redirect('transactiontable')

        if "Save" in request.POST:
            return redirect('credit_add')

    else:
        return render(request, 'credit_add.html')


  
# def save_item(request):
#   sid = request.session.get('staff_id')
#   staff =  staff_details.objects.get(id=sid)
#   cmp = company.objects.get(id=staff.company.id)
#   if request.method == 'POST':
#         item_name = request.POST.get('item_name')
#         hsn = request.POST.get('hsn')
#         qty = request.POST.get('qty')
#         tax_ref = request.POST.get('taxref')
#         intra_st = request.POST.get('intra_st')
#         inter_st = request.POST.get('inter_st')
#         sale_price = request.POST.get('saleprice')
#         purchase_price = request.POST.get('purprice')

#         # Perform any additional validation or processing here

#         # Create an instance of your model and save it to the database
#         item = ItemModel(
#             item_name=item_name,
#             item_hsn=hsn,
#             item_current_stock=qty,
#             item_taxable=tax_ref,
#             item_gst=intra_st,
#             item_igst=inter_st,
#             item_sale_price=sale_price,
#             item_purchase_price=purchase_price,
#             staff=staff,
#             company=cmp
#         )
#         item.save()

#         # Redirect to a success page or return a success message
#         return redirect("credit_add")

#     # Handle GET requests or any other cases
#   return render(request, 'credit_add.html') 
  
  
def get_tax_rate(request):
    if request.method == 'GET':
        product_id = request.GET.get('id')
        credit_note_id = request.GET.get('credit_note_id')

        if product_id and credit_note_id:
            item = get_object_or_404(ItemModel, id=product_id)
            credit_note = get_object_or_404(Creditnote, id=credit_note_id)

            # Assuming you have a field named place_of_supply in your CreditNote model
            place_of_supply = credit_note.place_of_supply

            # Set tax_rate based on place of supply
            if place_of_supply == 'State':
                tax_rate = item.item_gst
            else:
                tax_rate = item.item_igst

            return JsonResponse({'tax_rate': tax_rate})
    
    return JsonResponse({'error': 'Invalid request'})


def transactiontable(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  credit=Creditnote.objects.filter(company=cmp)
  item=Creditnote.objects.filter(company_id=cmp.id)
  return render(request,'transaction_table.html',{'credit':credit,'item':item})

def edit_credit(request,pk):
  toda = date.today()
  tod = toda.strftime("%Y-%m-%d")
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  party = Parties.objects.filter(company=cmp)
  item = ItemModel.objects.filter(company=cmp)
  crd = Creditnote.objects.get(id=pk,company=cmp)
  crditem = CreditnoteItem.objects.filter(credit=crd,company=cmp)
  item_units = ItemUnitModel.objects.filter(company=cmp)
  cdate = crd.date.strftime("%Y-%m-%d")
  print(crd.idate)
  context = {
    'staff':staff,  
    'crd':crd, 
    'crditem':crditem, 
    'party':party, 
    'item':item,
    'tod':tod,
    'cdate':cdate,
    'item_units':item_units
    }
  print(item)
  
  return render(request,'edit_credit.html',context)


# def update_creditnote(request, pk):
#     if request.method == 'POST':
#         sid = request.session.get('staff_id')
#         staff = staff_details.objects.get(id=sid)
#         cmp = company.objects.get(id=staff.company.id)

#         # Retrieve party details if available
#         party_id = request.POST.get('partyname')
#         party = get_object_or_404(Parties, id=party_id) if party_id else None
        

#         # crd = get_object_or_404(Creditnote, id=pk, company=cmp)
#         crd=Creditnote.objects.get(id=pk,company=cmp)
#         checkbtn=request.POST.get('abc', None)
#         if checkbtn == 'on':
#           if request.POST.get('billNod') == 'nobill':
#              crd.invoice_no = None
#           else:
#             crd.invoice_no = request.POST.get('billNod')
#         else:
#            crd.invoice_no = request.POST.get('billNo')
#         if checkbtn == 'on':
#           if parse_date(request.POST.get('billDated')) == 'nodate':
#             crd.idate = None
#           else:
#             crd.idate = parse_date(request.POST.get('billDated'))
#         else:
#           crd.idate = parse_date(request.POST.get('billDate'))
#         crd.party = party
#         crd.contact = party.phone_number if party else None
#         crd.address = party.billing_address if party else None
#         crd.date = parse_date(request.POST.get('date1', None))
#         # crd.invoice_no = request.POST.get('billNo')
#         # crd.idate = parse_date(request.POST.get('billDate', None))
#         crd.state_of_supply = request.POST.get('placosupply')
#         crd.subtotal = float(request.POST.get('subtotal', 0))
#         crd.grandtotal = request.POST.get('grandtotal')
#         crd.igst = request.POST.get('igst')
#         crd.cgst = request.POST.get('cgst')
#         crd.sgst = request.POST.get('sgst')
#         crd.taxamount = request.POST.get("taxamount")
#         crd.roundoff = request.POST.get("adj")
#         crd.description = request.POST.get("des")

#         crd.save()
        
#         product = request.POST.getlist("product[]")
#         qty = request.POST.getlist("qty[]")
#         total = request.POST.getlist("total[]")
#         discount = request.POST.getlist("discount[]")
#         hsn = request.POST.getlist("hsn[]")
#         tax = request.POST.getlist("tax[]")
#         price = request.POST.getlist("price[]")

#         # Iterate over form data to handle each item row
#         for i in range(len(product)):
#             # Retrieve or create the item
#             item = ItemModel.objects.get(id=product[i])

#             # Create or update CreditnoteItem
#             CreditnoteItem.objects.update_or_create(
#                 credit=crd,
#                 company=cmp,
#                 item=item,
#                 defaults={
#                     'qty': qty[i],
#                     'total': total[i],
#                     'discount': discount[i],
#                     'hsn': hsn[i],
#                     'tax': tax[i],
#                     'price': price[i],
#                     'staff': staff
#                 }
#             ) 
          

#         CreditnoteHistory.objects.create(credit=crd,company=cmp,staff=staff,action='Updated')
#         return redirect('transactiontable')

#     return redirect('transactiontable')

def update_creditnote(request, pk):
    if request.method == 'POST':
        sid = request.session.get('staff_id') 
        staff = get_object_or_404(staff_details, id=sid)
        cmp = get_object_or_404(company, id=staff.company.id)

        # Retrieve party details if available
        party_id = request.POST.get('partyname')
        party = get_object_or_404(Parties, id=party_id) if party_id else None
        

        crd = Creditnote.objects.get(id=pk,company=cmp)
        crd.party = party
        crd.contact = party.phone_number if party else None
        crd.address = party.billing_address if party else None
        crd.date = parse_date(request.POST.get('date1', None))
        checkbtn=request.POST.get('abc', None)
        if checkbtn == 'on':
          if request.POST.get('billNod') == 'nobill':
             crd.invoice_no = None
          else:
            crd.invoice_no = request.POST.get('billNod')
        else:
           crd.invoice_no = request.POST.get('billNo')
        if checkbtn == 'on':
          if parse_date(request.POST.get('billDated')) == 'nodate':
            crd.idate = None
          else:
            crd.idate = parse_date(request.POST.get('billDated'))
        else:
          crd.idate = parse_date(request.POST.get('billDate'))
        crd.state_of_supply = request.POST.get('placosupply')
        crd.subtotal = float(request.POST.get('subtotal', 0))
        crd.grandtotal = request.POST.get('grandtotal')
        crd.igst = request.POST.get('igst')
        crd.cgst = request.POST.get('cgst')
        crd.sgst = request.POST.get('sgst')
        crd.taxamount = request.POST.get("taxamount")
        crd.roundoff = request.POST.get("adj")
        crd.description = request.POST.get("des")

        crd.save()
        
        product = tuple(request.POST.getlist("product[]"))
        qty = tuple(request.POST.getlist("qty[]"))
        total = tuple(request.POST.getlist("total[]"))
        discount = tuple(request.POST.getlist("discount[]"))
        hsn = tuple(request.POST.getlist("hsn[]"))
        tax = tuple(request.POST.getlist("tax[]"))
        price = tuple(request.POST.getlist("price[]"))

        CreditnoteItem.objects.filter(credit=crd,company=cmp).delete()
        print('11')
        if len(product) == len(qty) == len(discount) == len(total) == len(hsn) == len(tax) == len(price):
          print('22')
          mapped=zip(product, qty, discount, total, hsn, tax, price)
          print('33')
          mapped=list(mapped)
          print('44')
          for ele in mapped:
            print('555')
            itm = ItemModel.objects.get(id=ele[0])
            print('66')
    
            CreditnoteItem.objects.create(product =itm.item_name,qty=ele[1],discount=ele[2],total=ele[3],hsn=ele[4],tax=ele[5],price=ele[6],credit=crd,company=cmp,item=itm,staff=staff)
            print('77')

        CreditnoteHistory.objects.create(credit=crd,company=cmp,staff=staff,action='Updated')
        return redirect('transactiontable')

    return redirect('transactiontable')




def template1(request,pk):
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)   
  cd=Creditnote.objects.get(id=pk)
  crditem = CreditnoteItem.objects.filter(credit=cd,company=cmp)
  return render(request,'creditnote1.html',{'cd':cd,'crditem':crditem})

def template2(request,pk):
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)  
  cd=Creditnote.objects.get(id=pk)
  crditem = CreditnoteItem.objects.filter(credit=cd,company=cmp)
  return render(request,'creditnote2.html',{'cd':cd,'crditem':crditem})

def template3(request,pk):
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)  
  cd=Creditnote.objects.get(id=pk)
  crditem = CreditnoteItem.objects.filter(credit=cd,company=cmp)
  return render(request,'creditnote3.html',{'cd':cd,'crditem':crditem})

def credithistory(request,pk):
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)  
  cd=Creditnote.objects.get(id=pk)
  history=CreditnoteHistory.objects.filter(credit=cd,company=cmp)
  context = {'staff':staff,'history':history,'cd':cd}
  return render(request,'credithistory.html',context)


def delete_credit(request,pk):
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id) 
  crd = Creditnote.objects.get(id=pk)
  CreditnoteItem.objects.filter(credit=crd,company=cmp).delete()
  crd.delete()
  return redirect('transactiontable')

def pdftomailcredit(request,pk):
  if request.user:
        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']

                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']
                print(emails_list)
                sid = request.session.get('staff_id')
                staff = staff_details.objects.get(id=sid)
                cmp = company.objects.get(id=staff.company.id) 
                
                cd = Creditnote.objects.get(id=pk,company=cmp)
                itm = CreditnoteItem.objects.filter(credit=cd,company=cmp)
                context = {'cd':cd, 'cmp':cmp,'itm':itm}
                template_path = 'creditmail.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'CREDIT NOTE - {cd.returnno}.pdf'
                subject = f"CREDIT NOTE - {cd.returnno}"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached CREDIT NOTE - File-{cd.returnno}. \n{email_message}\n\n--\nRegards,\n{cmp.company_name}\n{cmp.address}\n{cmp.state} - {cmp.country}\n{cmp.contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                # msg = messages.success(request, 'Credit note file has been shared via email successfully..!')
                return redirect('template1',pk=pk)

        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect('template1',pk=pk)
          
def partydata(request):
    if request.method == 'POST':
        cid = request.POST.get('id')
        part = Parties.objects.get(id=cid)
        phno = part.phone_number
        address = part.billing_address
        pay = part.to_pay
        bal = part.opening_balance
        return JsonResponse({'phno': phno, 'address': address, 'pay': pay, 'bal': bal})
    else:
        return JsonResponse({'error': 'Invalid request method'})


  
def saveitemcr(request):
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    company_obj = staff.company

    name = request.POST['name']
    print(name)
    unit = request.POST['unit']
    print(unit)
    hsn = request.POST['hsn']
    print(hsn)
    taxref = request.POST['taxref']
    print(taxref)
    sell_price = request.POST['sell_price']
    print(sell_price)
    cost_price = request.POST['cost_price']
    print(cost_price)
    intra_st = request.POST['intra_st']
    print(intra_st)
    inter_st = request.POST['inter_st']
    print(inter_st)

    if taxref != 'Taxable':
        intra_st = 'GST0[0%]'
        print(intra_st)
        inter_st = 'IGST0[0%]'
        print(inter_st)

    itmdate = request.POST.get('itmdate')
    print(itmdate)
    stock = request.POST.get('stock')
    print(stock)
    itmprice = request.POST.get('itmprice')
    print(itmprice)
    minstock = request.POST.get('minstock')
    print(minstock)

    if not hsn:
        hsn = None

    # Check if HSN exists for the given company
    if ItemModel.objects.filter(company=company_obj, item_hsn=hsn).exists():
        return JsonResponse({'success': False, 'message': 'HSN already exists for this company'})

    itm = ItemModel(
        item_name=name, item_hsn=hsn, item_unit=unit, item_taxable=taxref, item_gst=intra_st, item_igst=inter_st,
        item_sale_price=sell_price, item_purchase_price=cost_price, item_current_stock=stock, item_at_price=itmprice,
        item_date=itmdate, company=company_obj, user=company_obj.user
    )
    itm.save()
    print(itm)

    return JsonResponse({'success': True})


def item_dropdowncr(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  product = ItemModel.objects.filter(company=cmp,user=cmp.user)

  id_list = []
  product_list = []
  items = {}
  for p in product:
    id_list.append(p.id)
    product_list.append(p.item_name)
    items[p.id] = [p.id, p.item_name]
  return JsonResponse(items)

def check_hsnc(request):
    hsn= request.POST.get('hsn')
    print(hsn)
    
    if ItemModel.objects.filter(item_hsn=hsn).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists':False})


def check_phone_no(request):
    phone_number = request.GET.get('phone_number')
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    if Parties.objects.filter(company=cmp,phone_number=phone_number).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
  
def check_emailc(request):
    email= request.GET.get('email')
    if Parties.objects.filter(email=email).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists':False})

def check_gstc(request):
    gstin = request.GET.get('gstin')
    sid = request.session.get('staff_id')
    staff = staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    gsttype = request.GET.get('gsttype')  
    print(gsttype)

    if gsttype != "Unregistered or Consumer":
        if Parties.objects.filter(company=cmp, gstin=gstin).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})
  
def check_unit(request):
    newUnit = request.GET.get('newUnit', '').upper()
    exists = ItemUnitModel.objects.filter(unit_name=newUnit).exists()
    return JsonResponse({'exists': exists})
  
def check_unitc(request):
    newUnit = request.GET.get('newUnit', '').upper()
    exists = ItemUnitModel.objects.filter(unit_name=newUnit).exists()
    return JsonResponse({'exists': exists})
    
def allunits(request):
    try:
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)
        itmunits = ItemUnitModel.objects.filter(company=cmp)
        
        # Fetch all units from ItemUnitModel
        units = itmunits.values_list('unit_name', flat=True)
        
        # Convert the QuerySet to a list
        units_list = list(units)
        
        # Return the list as JSON response
        return JsonResponse({'units': units_list})
    except Exception as e:
        # Handle exceptions if any
        return JsonResponse({'error': str(e)})
      
def allunitsc(request):
    try:
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)
        itmunits = ItemUnitModel.objects.filter(company=cmp)
        
        # Fetch all units from ItemUnitModel
        units = itmunits.values_list('unit_name', flat=True)
        
        # Convert the QuerySet to a list
        units_list = list(units)
        
        # Return the list as JSON response
        return JsonResponse({'units': units_list})
    except Exception as e:
        # Handle exceptions if any
        return JsonResponse({'error': str(e)})
      
def addunitc(request):
    if request.method == 'POST':
        sid = request.session.get('staff_id')
        staff =  staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)
        new_unit_name = request.POST.get('newUnit')

        if new_unit_name:
           
            new_unit_name = new_unit_name.upper()

            
            if not ItemUnitModel.objects.filter(unit_name=new_unit_name).exists():
                
                new_unit = ItemUnitModel(user=cmp.user,company=cmp,unit_name=new_unit_name)
                new_unit.save()

                messages.success(request, 'Unit added successfully')
                return JsonResponse({'status': 'success', 'message': 'Unit added successfully'})
            else:
                messages.error(request, 'Unit already exists')
                return JsonResponse({'status': 'error', 'message': 'Unit already exists'})
        else:
            messages.error(request, 'Unit name cannot be empty')
            return JsonResponse({'status': 'error', 'message': 'Unit name cannot be empty'})

    return redirect('credit_add')
  
def credithistoryc(request):
  pid = request.POST['id']
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id) 
  crd = Creditnote.objects.get(returnno=pid,company=cmp)
  hst = CreditnoteHistory.objects.filter(credit=crd,company=cmp).last()
  name = hst.staff.first_name + ' ' + hst.staff.last_name 
  action = hst.action
  return JsonResponse({'name':name,'action':action,'pid':pid})

def check_itmname(request):
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    item_name= request.GET.get('item_name')
    
    if ItemModel.objects.filter(item_name=item_name,company=cmp).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists':False})
  
def check_hsnc(request):
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    hsn= request.POST.get('hsn')
    print(hsn)
    
    if ItemModel.objects.filter(item_hsn=hsn,company=cmp).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists':False})
  
def saveitemcr(request):
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    company_obj = staff.company

    name = request.POST['name']
    print(name)
    unit = request.POST['unit']
    print(unit)
    hsn = request.POST['hsn']
    print(hsn)
    taxref = request.POST['taxref']
    print(taxref)
    sell_price = request.POST['sell_price']
    print(sell_price)
    cost_price = request.POST['cost_price']
    print(cost_price)
    intra_st = request.POST['intra_st']
    print(intra_st)
    inter_st = request.POST['inter_st']
    print(inter_st)

    if taxref != 'Taxable':
        intra_st = 'GST0[0%]'
        print(intra_st)
        inter_st = 'IGST0[0%]'
        print(inter_st)

    itmdate = request.POST.get('itmdate')
    print(itmdate)
    stock = request.POST.get('stock')
    print(stock)
    itmprice = request.POST.get('itmprice')
    print(itmprice)
    minstock = request.POST.get('minstock')
    print(minstock)

    if not hsn:
        hsn = None

    # Check if HSN exists for the given company
    if ItemModel.objects.filter(company=company_obj, item_hsn=hsn).exists():
        return JsonResponse({'success': False, 'message': 'HSN already exists for this company'})

    itm = ItemModel(
        item_name=name, item_hsn=hsn, item_unit=unit, item_taxable=taxref, item_gst=intra_st, item_igst=inter_st,
        item_sale_price=sell_price, item_purchase_price=cost_price, item_current_stock=stock, item_at_price=itmprice,
        item_date=itmdate, company=company_obj, user=company_obj.user
    )
    itm.save()
    print(itm)

    return JsonResponse({'success': True})


def item_dropdowncr(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  product = ItemModel.objects.filter(company=cmp,user=cmp.user)

  id_list = []
  product_list = []
  items = {}
  for p in product:
    id_list.append(p.id)
    product_list.append(p.item_name)
    items[p.id] = [p.id, p.item_name]
  return JsonResponse(items)

def check_unitc(request):
    newUnit = request.GET.get('newUnit', '').upper()
    sid = request.session.get('staff_id')
    staff =  staff_details.objects.get(id=sid)
    cmp = company.objects.get(id=staff.company.id)
    exists = ItemUnitModel.objects.filter(unit_name=newUnit,company=cmp).exists()
    return JsonResponse({'exists': exists})
    
def allunits(request):
    try:
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)
        itmunits = ItemUnitModel.objects.filter(company=cmp)
        
        # Fetch all units from ItemUnitModel
        units = itmunits.values_list('unit_name', flat=True)
        
        # Convert the QuerySet to a list
        units_list = list(units)
        
        # Return the list as JSON response
        return JsonResponse({'units': units_list})
    except Exception as e:
        # Handle exceptions if any
        return JsonResponse({'error': str(e)})
      
def allunitsc(request):
    try:
        sid = request.session.get('staff_id')
        staff = staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)
        itmunits = ItemUnitModel.objects.filter(company=cmp)
        
        # Fetch all units from ItemUnitModel
        units = itmunits.values_list('unit_name', flat=True)
        
        # Convert the QuerySet to a list
        units_list = list(units)
        
        # Return the list as JSON response
        return JsonResponse({'units': units_list})
    except Exception as e:
        # Handle exceptions if any
        return JsonResponse({'error': str(e)})
      
def addunitc(request):
    if request.method == 'POST':
        sid = request.session.get('staff_id')
        staff =  staff_details.objects.get(id=sid)
        cmp = company.objects.get(id=staff.company.id)
        new_unit_name = request.POST.get('newUnit')

        if new_unit_name:
           
            new_unit_name = new_unit_name.upper()

            
            if not ItemUnitModel.objects.filter(unit_name=new_unit_name,company=cmp).exists():
                
                new_unit = ItemUnitModel(user=cmp.user,company=cmp,unit_name=new_unit_name)
                new_unit.save()

                
                return JsonResponse({'status': 'success', 'message': 'Unit added successfully'})
            else:
                
                return JsonResponse({'status': 'error', 'message': 'Unit already exists'})
        else:
            
            return JsonResponse({'status': 'error', 'message': 'Unit name cannot be empty'})
      
      
      
      

# def get_party_details(request):
#     if request.method == 'POST' and request.is_ajax():
#         party_id = request.POST.get('id')
#         try:
#             party = Parties.objects.get(id=party_id)
#             party_details = {
#                 'phno': party.phone_number,
#                 'address': party.billing_address,
#                 'pay': party.to_pay,
#                 'bal': party.opening_balance
#             }
#             return JsonResponse(party_details)
#         except Parties.DoesNotExist:
#             return JsonResponse({'error': 'Party not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)


# def credit_details(request,pk):
#   cd=Creditnote.objects.get(id=pk)
#   return render(request,'transaction_table.html',{'cd':cd})  




    