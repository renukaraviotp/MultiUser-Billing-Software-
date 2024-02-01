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
from django.http import HttpResponse

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
  item=ItemModel.objects.all() 
  return render(request, 'credit_add.html', {'party': party,'todaydate':todaydate,'item':item}) 


def get_sales_invoice_details(request, party_id):
    try:
        sales_invoice = SalesInvoice.objects.get(party_id=party_id)
        data = {
            'billNo': sales_invoice.invoice_no,
            'billDate': sales_invoice.date.strftime('%Y-%m-%d'),  # Format the date as needed
        }
        return JsonResponse(data)
    except SalesInvoice.DoesNotExist:
        return JsonResponse({'error': 'Sales invoice not found'}, status=404)


def item_details(request):
    item_id = request.GET.get('id')
    item = get_object_or_404(ItemModel, id=item_id)
    

    hsn = item.item_hsn
    price = item.item_purchase_price
    gst = item.item_gst
    igst = item.item_igst
    qty = item.item_current_stock
    print(hsn)
    print(price)
    print(gst)
    print(igst)
    print(qty)
    return JsonResponse({'hsn': hsn, 'price': price, 'gst': gst, 'igst': igst, 'qty': qty})
  
def item_dropdown(request):
    options={}
    option_objects=ItemModel.objects.all()
    for option in option_objects:
      options[option.id]=[option.item_name]
    return JsonResponse(options)
      


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
  sid = request.session.get('staff_id')
  staff = staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  user = cmp.id
    
  if request.method == 'POST':
    itemname=request.POST['itemname']
    hsn=request.POST['hsn']
    unit=request.POST['unit']
    saleprice=request.POST['saleprice']
    purchaseprice=request.POST['purchaseprice']
    intra_st=request.POST['intra_st']
    inter_st=request.POST['inter_st']
    item=ItemModel(item_name=itemname,item_hsn=hsn,item_unit=unit,item_sale_price=saleprice,item_purchase_price=purchaseprice,item_gst=intra_st,item_igst=inter_st)
    item.save()
    return redirect('credit_add') 
  

def itemdetails(request):
  itmid = request.GET['id']
  itm = ItemModel.objects.get(id=itmid)
  hsn = itm.item_hsn
  gst = itm.item_gst
  igst = itm.item_igst
  price = itm.item_purchase_price
  qty = itm.item_current_stock
  return JsonResponse({'hsn':hsn, 'gst':gst, 'igst':igst, 'price':price, 'qty':qty})

def saveitem(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)

  name = request.POST['name']
  unit = request.POST['unit']
  hsn = request.POST['hsn']
  taxref = request.POST['taxref']
  sell_price = request.POST['sell_price']
  cost_price = request.POST['cost_price']
  intra_st = request.POST['intra_st']
  inter_st = request.POST['inter_st']

  if taxref != 'Taxable':
    intra_st = 'GST0[0%]'
    inter_st = 'IGST0[0%]'

  itmdate = request.POST.get('itmdate')
  stock = request.POST.get('stock')
  itmprice = request.POST.get('itmprice')
  minstock = request.POST.get('minstock')

  if not hsn:
    hsn = None

  itm = ItemModel(item_name=name, item_hsn=hsn,item_unit=unit,item_taxable=taxref, item_gst=intra_st,item_igst=inter_st, item_sale_price=sell_price, 
                item_purchase_price=cost_price,item_current_stock=stock,item_at_price=itmprice,item_date=itmdate,
              company=cmp,user=cmp.user)
  itm.save() 
  return JsonResponse({'success': True})


def item_dropdown(request):
  sid = request.session.get('staff_id')
  staff =  staff_details.objects.get(id=sid)
  cmp = company.objects.get(id=staff.company.id)
  product = ItemModel.objects.filter(company=cmp,user=cmp.user)

  id_list = []
  product_list = []
  for p in product:
    id_list.append(p.id)
    product_list.append(p.item_name)
  return JsonResponse({'id_list':id_list, 'product_list':product_list})
  

 



# def credit_save(request):
#   sid = request.session.get('staff_id')
#   staff = staff_details.objects.get(id=sid)
#   cmp = company.objects.get(id=staff.company.id)
#   user=cmp.id
#   party = Parties.objects.filter(company_id=cmp.id)
#   if request.method == 'GET':
#     date=request.GET['date']
#     gsttype=request.GET['gsttype']
#     credit=Creditnote(state_of_supply=gsttype,date = date,company_id=user,staff_id=staff.id) 
#     credit.save()
#     returnno=credit.id
#     return render(request, 'credit_add.html', {'party': party,'returnno':returnno}) 
  
def save_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        hsn = request.POST.get('hsn')
        qty = request.POST.get('qty')
        tax_ref = request.POST.get('taxref')
        intra_st = request.POST.get('intra_st')
        inter_st = request.POST.get('inter_st')
        sale_price = request.POST.get('saleprice')
        purchase_price = request.POST.get('purprice')

        # Perform any additional validation or processing here

        # Create an instance of your model and save it to the database
        item = ItemModel(
            item_name=item_name,
            item_hsn=hsn,
            item_current_stock=qty,
            item_taxable=tax_ref,
            item_gst=intra_st,
            item_igst=inter_st,
            item_sale_price=sale_price,
            item_purchase_price=purchase_price
        )
        item.save()

        # Redirect to a success page or return a success message
        return redirect("credit_add")

    # Handle GET requests or any other cases
    return render(request, 'credit_add.html') 
  
  
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
  return render(request,'transaction_table.html')




    