from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CriterionWeightForm,
    InterestedMajorForm,
    RejectedMajorForm,
    StudentExamProfileForm,
)
from .models import (
    AcceptedCourse,
    CriterionWeight,
    InterestedMajor,
    RejectedMajor,
    StudentExamProfile,
)


@login_required
def exam_profile_view(request):
    """
    نمایش و ایجاد پروفایل انتخاب رشته کاربر.
    """

    profile = StudentExamProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":
        form = StudentExamProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            exam_profile = form.save(commit=False)
            exam_profile.user = request.user
            exam_profile.save()

            return redirect("exam:exam_profile")

    else:
        form = StudentExamProfileForm(
            instance=profile
        )

    return render(
        request,
        "exam/profile.html",
        {
            "form": form,
            "exam_profile": profile,
        },
    )


@login_required
def interested_major_create(request):
    """
    ثبت یک رشته مورد علاقه برای کاربر فعلی.
    """

    profile = get_object_or_404(
        StudentExamProfile,
        user=request.user
    )

    if request.method == "POST":
        form = InterestedMajorForm(request.POST)

        if form.is_valid():
            interested_major = form.save(commit=False)
            interested_major.profile = profile
            interested_major.save()

            return redirect("exam:exam_profile")

    else:
        form = InterestedMajorForm()

    return render(
        request,
        "exam/interested_major_form.html",
        {
            "form": form,
        },
    )


@login_required
def interested_major_delete(request, pk):
    """
    حذف رشته مورد علاقه متعلق به کاربر فعلی.
    """

    profile = get_object_or_404(
        StudentExamProfile,
        user=request.user
    )

    major = get_object_or_404(
        InterestedMajor,
        pk=pk,
        profile=profile,
    )

    if request.method == "POST":
        major.delete()

    return redirect("exam:exam_profile")


@login_required
def rejected_major_create(request):
    """
    ثبت یک رشته غیرقابل قبول برای کاربر فعلی.
    """

    profile = get_object_or_404(
        StudentExamProfile,
        user=request.user
    )

    if request.method == "POST":
        form = RejectedMajorForm(request.POST)

        if form.is_valid():
            rejected_major = form.save(commit=False)
            rejected_major.profile = profile
            rejected_major.save()

            return redirect("exam:exam_profile")

    else:
        form = RejectedMajorForm()

    return render(
        request,
        "exam/rejected_major_form.html",
        {
            "form": form,
        },
    )


@login_required
def rejected_major_delete(request, pk):
    """
    حذف رشته غیرقابل قبول متعلق به کاربر فعلی.
    """

    profile = get_object_or_404(
        StudentExamProfile,
        user=request.user
    )

    major = get_object_or_404(
        RejectedMajor,
        pk=pk,
        profile=profile,
    )

    if request.method == "POST":
        major.delete()

    return redirect("exam:exam_profile")


@login_required
def criterion_weight_view(request):
    """
    ایجاد یا ویرایش وزن معیارهای انتخاب رشته.
    """

    profile = get_object_or_404(
        StudentExamProfile,
        user=request.user
    )

    criterion_weights = CriterionWeight.objects.filter(
        profile=profile
    ).first()

    if request.method == "POST":
        form = CriterionWeightForm(
            request.POST,
            instance=criterion_weights
        )

        if form.is_valid():
            weights = form.save(commit=False)
            weights.profile = profile
            weights.save()

            return redirect("exam:criterion_weights")

    else:
        form = CriterionWeightForm(
            instance=criterion_weights
        )

    return render(
        request,
        "exam/criterion_weights.html",
        {
            "form": form,
            "criterion_weights": criterion_weights,
        },
    )


@login_required
def accepted_course_add(request):
    """
    اضافه کردن یک دوره تحصیلی مورد قبول.
    """

    profile = get_object_or_404(
        StudentExamProfile,
        user=request.user
    )

    if request.method == "POST":
        course = request.POST.get("course")

        valid_courses = {
            value
            for value, _ in StudentExamProfile.Course.choices
        }

        if course in valid_courses:
            AcceptedCourse.objects.get_or_create(
                profile=profile,
                course=course,
            )

        return redirect("exam:exam_profile")

    return render(
        request,
        "exam/accepted_course_form.html",
        {
            "courses": StudentExamProfile.Course.choices,
        },
    )


@login_required
def accepted_course_delete(request, pk):
    """
    حذف دوره مورد قبول متعلق به کاربر فعلی.
    """

    profile = get_object_or_404(
        StudentExamProfile,
        user=request.user
    )

    accepted_course = get_object_or_404(
        AcceptedCourse,
        pk=pk,
        profile=profile,
    )

    if request.method == "POST":
        accepted_course.delete()

    return redirect("exam:exam_profile")


@login_required
def exam_profile_summary(request):
    """
    نمایش خلاصه کامل اطلاعات انتخاب رشته کاربر.
    """

    profile = get_object_or_404(
        StudentExamProfile.objects.select_related(
            "user"
        ).prefetch_related(
            "interested_majors",
            "rejected_majors",
            "accepted_courses",
        ),
        user=request.user,
    )

    criterion_weights = CriterionWeight.objects.filter(
        profile=profile
    ).first()

    return render(
        request,
        "exam/summary.html",
        {
            "exam_profile": profile,
            "interested_majors": profile.interested_majors.all(),
            "rejected_majors": profile.rejected_majors.all(),
            "accepted_courses": profile.accepted_courses.all(),
            "criterion_weights": criterion_weights,
        },
    )


@login_required
def exam_profile_save_all(request):
    """
    ذخیره یکجای داده‌های اصلی، در صورت نیاز توسط یک فرم چندمرحله‌ای.
    """

    if request.method != "POST":
        return redirect("exam:exam_profile")

    profile = StudentExamProfile.objects.filter(
        user=request.user
    ).first()

    form = StudentExamProfileForm(
        request.POST,
        instance=profile
    )

    if not form.is_valid():
        return render(
            request,
            "exam/profile.html",
            {
                "form": form,
                "exam_profile": profile,
            },
        )

    with transaction.atomic():
        exam_profile = form.save(commit=False)
        exam_profile.user = request.user
        exam_profile.save()

    return redirect("exam:exam_profile")