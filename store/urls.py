from django.urls import path
from .views import LessonListView,EnrollmentStatusView,ConfirmPaymentView,InitiatePaymentAPIView, CategoryListCreateView, CategoryUpdateDeleteView,UserListView,toggle_user_status,list_tutors,toggle_tutor_status,CourseDetailView,AddLessonView,AddCourseView,CourseListView,TutorCourseListView,AdminCourseListView,CourseDetailUser

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryUpdateDeleteView.as_view(), name='category-update-delete'),
    path('admin/courses/', AdminCourseListView.as_view(), name='admin-course-list'),
     path('api/users/', UserListView.as_view(), name='user-list'),
     path('api/users/<int:user_id>/toggle-status/', toggle_user_status, name='toggle_user_status'),
      path('api/tutors/', list_tutors, name='list_tutors'),
    path('api/tutors/<int:user_id>/toggle-status/', toggle_tutor_status, name='toggle_tutor_status'),
    path("courses/add/", AddCourseView.as_view(), name="add-course"),
      path('tutorcourses/', TutorCourseListView.as_view(), name='course-list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('coursedetail/<int:pk>/',CourseDetailView.as_view(), name='course-detail'),
     path('lessons/add/<int:course_id>/', AddLessonView.as_view(), name='add-lesson'),
     path('courses/<int:course_id>/', CourseDetailUser.as_view(), name='course_detail'),
     path('initiate-payment/', InitiatePaymentAPIView.as_view(), name='initiate-payment'),
       path("confirm-payment/", ConfirmPaymentView.as_view(), name="confirm-payment"),
       path('enrollment-status/<int:course_id>/', EnrollmentStatusView.as_view(), name='enrollment-status'),
     path('course/<int:course_id>/lessons/', LessonListView.as_view(), name='lesson-list'),
]
    
