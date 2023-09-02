from . import views
from django.urls import path
urlpatterns=[
    path('',views.index,name='index'),
    path('course',views.course,name='course'),
    path('add_course',views.add_course,name='add_course'),
    path('student',views.student,name='student'),
    path('add_student',views.add_student,name='add_student'),
    path('log',views.log,name='log'),
    path('home',views.home,name='home'),
    path('show_details',views.show_details,name='show_details'),
    path('edit/<int:pk>',views.edit,name='edit'),
    path('edit_student/<int:pk>',views.edit_student,name='edit_student'),
    path('delete_student/<int:pk>',views.delete_student,name="delete_student"),
    path('logout/',views.logout,name='logout'),
    path('signup',views.signup,name='signup'),
    path('add_teacher',views.add_teacher,name='add_teacher'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('profile',views.profile,name='profile'),
    path('teacher_det',views.teacher_det,name='teacher_det'),
    path('delete_teacher/<int:pk>',views.delete_teacher,name='delete_teacher'),
    path('edit_teacher',views.edit_teacher,name="edit_teacher"),
]