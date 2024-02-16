from . import views
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
# from .views import AutocompletePartiesView


urlpatterns = [

    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('service', views.service, name='service'),
    path('register', views.register, name='register'),
    path('registercompany', views.registercompany, name='registercompany'),
    path('registerstaff', views.registerstaff, name='registerstaff'),
    path('login', views.login, name='login'),
    path('registeruser', views.registeruser, name='registeruser'),
    path('add_company', views.add_company, name='add_company'),
    path('staff_registraction', views.staff_registraction, name='staff_registraction'),
    path('homepage', views.homepage, name='homepage'),
    path('staffhome', views.staffhome, name='staffhome'),
    path('loginurl', views.loginurl, name='loginurl'),
    path('logout', views.logout, name='logout'),
    path('base', views.base, name='base'),
    path('profile', views.profile, name='profile'),
    path('editprofile/<int:pk>/', views.editprofile, name='editprofile'),
    path('edit_profilesave/<int:pk>/', views.edit_profilesave, name='edit_profilesave'),
    path('editstaffprofile', views.editstaffprofile, name='editstaffprofile'),
    path('edit_staffprofilesave/', views.edit_staffprofilesave, name='edit_staffprofilesave'),
    path('staffprofile', views.staffprofile, name='staffprofile'),
    path('parties_default',views.parties_default,name='parties_default'),
    path('parties_add_page',views.parties_add_page,name='parties_add_page'),
    path('credit_default',views.credit_default,name='credit_default'),
    path('credit_add',views.credit_add,name='credit_add'),
    path('transactiontable',views.transactiontable,name='transactiontable'),
    path('credit_save',views.credit_save,name='credit_save'),
    path('get_sales_invoice_details/<int:party_id>/', views.get_sales_invoice_details, name='get_sales_invoice_details'),
    path('party_save',views.party_save,name='party_save'),
    path('item_save',views.item_save,name='item_save'),
    path('item_details',views.item_details,name='item_details'),
    path('item_dropdown',views.item_dropdown,name='item_dropdown'),
    path('save_item',views.save_item,name='save_item'),
    path('get_tax_rate/', views.get_tax_rate, name='get_tax_rate'),
    path('itemdetails',views.itemdetails,name='itemdetails'),
    path('saveitem',views.saveitem,name='saveitem'),
    path('edit_credit/<int:pk>',views.edit_credit,name='edit_credit'),
    path('update_creditnote/<int:pk>',views.update_creditnote,name='update_creditnote'),
    path('template1/<int:pk>',views.template1,name='template1'),
    path('template2/<int:pk>',views.template2,name='template2'),
    path('template3/<int:pk>',views.template3,name='template3'),
    path('credithistory/<int:pk>',views.credithistory,name='credithistory'),
    path('delete_credit/<int:pk>',views.delete_credit,name='delete_credit'),
    
    
    # path('credit_details/<int:pk>',views.credit_details,name='credit_details'),
    
    
    
        
   

]