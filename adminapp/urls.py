from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('adminhome',views.admindex,name="adminhome"),
path('adminnav',views.adminnav,name="adminnav"),
 path('add_category', views.add_category, name='add_category'),
  path('category_list', views.category_list, name='category_list'),
    path('delete/<int:category_id>', views.delete_category, name='delete_category'),
path('color_list/', views.color_list, name='color_list'),
    path('delete/color/<int:color_id>/', views.delete_color, name='delete_color'),
    path('size_list/', views.size_list, name='size_list'),
    path('delete/size/<int:size_id>/', views.delete_size, name='delete_size'),
     path('products_list/', views.products_list, name='products_list'),  # Product list
    path('add_product/', views.add_product, name='add_product'),    # Add product form
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),  # Delete product
    
  path('designers/', views.designer_list, name='designer_list'),
    path('add_designer', views.add_designer, name='add_designer'),
    path('designer/edit/<int:designer_id>/', views.edit_designer, name='edit_designer'),



   # path('edit_designer/<int:designer_id>/', views.get_designer_details, name='edit_designer'),
 path('edit_designer/<int:designer_id>/', views.get_designer_details, name='edit_designer'),



    path('designer/delete/<int:pk>/', views.delete_designer, name='delete_designer'),
     path('logout/', views.logout_view, name='logout'),
     path('newrequest/', views.newrequest, name='newrequest'),
     path('design_request_detail_view/<int:request_id>/', views.design_request_detail_view, name='design_request_detail_view'),
     path('notify_design_request_create', views.notify_design_request_create, name='notify_design_request_create'),
path('orders_on_process/', views.orders_on_process, name='orders_on_process'),
  #  path('change_order_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('payment_completed/', views.payment_completed, name='payment_completed'),
path('completed_orders/', views.completed_orders, name='completed_orders'),
path('cancelled_orders/', views.cancelled_orders, name='cancelled_orders'),

 path("customer_templates/", views.customer_templates, name="customer_templates"),
    path("delete-template/<int:template_id>/", views.delete_template, name="delete_template"),
     path("customer_reviews/", views.customer_reviews, name="customer_reviews"),
     path('add_free_template', views.add_free_template, name='add_free_template'),
    path('free_template_list', views.free_template_list, name='free_template_list'),  # ✅ Correct

     path('delete/<int:free_template_id>', views.delete_free_template, name='delete_free_template'),
     path('feedbacks/', views.customer_feedbacks, name='feedbacks')



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

