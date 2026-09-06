from django.urls import path

from . import views


app_name = "exam"


urlpatterns = [
    path(
        "",
        views.exam_profile_view,
        name="exam_profile",
    ),

    path(
        "interested-major/add/",
        views.interested_major_create,
        name="interested_major_add",
    ),

    path(
        "interested-major/<int:pk>/delete/",
        views.interested_major_delete,
        name="interested_major_delete",
    ),

    path(
        "rejected-major/add/",
        views.rejected_major_create,
        name="rejected_major_add",
    ),

    path(
        "rejected-major/<int:pk>/delete/",
        views.rejected_major_delete,
        name="rejected_major_delete",
    ),

    path(
        "criterion-weights/",
        views.criterion_weight_view,
        name="criterion_weights",
    ),

    path(
        "accepted-course/add/",
        views.accepted_course_add,
        name="accepted_course_add",
    ),

    path(
        "accepted-course/<int:pk>/delete/",
        views.accepted_course_delete,
        name="accepted_course_delete",
    ),

    path(
        "summary/",
        views.exam_profile_summary,
        name="summary",
    ),

    path(
        "save-all/",
        views.exam_profile_save_all,
        name="save_all",
    ),
]