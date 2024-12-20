from django.urls import path
from .views import toggle_user_status,  CourseLessonsView,EnrollmentStatusView,ConfirmPaymentView,InitiatePaymentAPIView, CategoryListCreateView, CategoryUpdateDeleteView,UserListView,update_tutor_approval_status,list_tutors,CourseDetailView,AddLessonView,AddCourseView,CourseListView,TutorCourseListView,CourseDetailUser
from .views import get_courses
urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryUpdateDeleteView.as_view(), name='category-update-delete'),
    path('api/courses/', get_courses, name='get_courses'),
     path('api/users/', UserListView.as_view(), name='user-list'),
     path('api/users/<int:user_id>/toggle-status/', toggle_user_status, name='toggle_user_status'),
      path('api/tutors/', list_tutors, name='list_tutors'),
    path('api/tutors/<int:user_id>/toggle-status/', update_tutor_approval_status, name='toggle_tutor_status'),
    path("courses/add/", AddCourseView.as_view(), name="add-course"),
      path('tutorcourses/', TutorCourseListView.as_view(), name='course-list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('coursedetail/<int:pk>/',CourseDetailView.as_view(), name='course-detail'),
     path('lessons/add/<int:course_id>/', AddLessonView.as_view(), name='add-lesson'),
     path('courses/<int:course_id>/', CourseDetailUser.as_view(), name='course_detail'),
     path('initiate-payment/', InitiatePaymentAPIView.as_view(), name='initiate-payment'),
       path("confirm-payment/", ConfirmPaymentView.as_view(), name="confirm-payment"),
       path('enrollment-status/<int:course_id>/', EnrollmentStatusView.as_view(), name='enrollment-status'),
      path('courses/<int:course_id>/lessons/', CourseLessonsView.as_view(), name='course_lessons'),
]
    
