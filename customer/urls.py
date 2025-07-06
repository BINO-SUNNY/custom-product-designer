from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create_design_request/', views.create_design_request, name='create_design_request'),
    path('customerhome/', views.customerhome, name='customerhome'),

    path('get-products/<int:category_id>/', views.get_products, name='get_products'),
    path('get-sizes-colors/<int:product_id>/', views.get_sizes_colors, name='get_sizes_colors'),
    path('get-templates/', views.get_templates, name='get_templates'),
      path('myaccount/', views.myaccount, name='myaccount'),
      path('submit_review/<int:order_id>/', views.submit_review, name='submit_review'),
       path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
       path('my_templates/', views.my_templates, name='my_templates'),
       path('fetch_users_for_template/<int:template_id>/', views.fetch_users_for_template, name="fetch_users_for_template"),
           path('update-profile/', views.update_profile, name="update_profile"),
    path('change-password/', views.change_password, name="change_password"),
       path('generate_qr/<int:order_id>/', views.generate_qr, name='generate_qr'),

       path('update_payment_status/<int:order_id>/', views.update_payment_status, name='update_payment_status'),

path('feedback/', views.feedback_view, name='feedback'),

path('wallet_view/', views.wallet_view, name='wallet_view'),
    path('get_wallet_amount_for_user/', views.get_wallet_amount_for_user, name='get_wallet_amount_for_user'),
    path('withdraw/', views.withdraw_money, name='withdraw_money'), 
    path('get-free-templates/', views.get_free_templates, name='get_free_templates'),
    path('delete-template/<int:template_id>/', views.delete_template, name='delete_template'),

    path('upload_color_image/', views.upload_color_image, name='upload_color_image'),
  
    # path('create-design-request/', create_design_request, name='create_design_request'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
