from django.urls import path,include
from. import views 
from django.views.generic import RedirectView
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),

    path('proposal_list/', views.proposal_list, name='proposal_list'),
    path('add_proposal/',views.add_proposal, name='add_proposal'),
    path('add_section/<int:proposal_id>/',views.add_section, name='add_section'),
    path('edit_proposal/<int:proposal_id>/', views.edit_proposal, name='edit_proposal'),
    path('edit_section/<int:proposal_id>/<int:section_id>/', views.edit_section, name='edit_section'),
    path('delete_section/<int:proposal_id>/', views.delete_section, name='delete_section'),
    path('generate_pdf/<int:proposal_id>/',views.generate_pdf, name='generate_pdf'),
    path('register/',views.register, name='register'),
    path('logout/',views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),



]
