from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Profile
from ans_generate.models import GeneratedAnalysis
from exam.models import StudentExamProfile


@login_required
def dashboard_view(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None

    profile_completion = 0

    if profile:
        profile_fields = [
            profile.phone_number,
            profile.national_code,
            profile.birth_date,
            profile.city,
            profile.province,
        ]

        completed_fields = sum(
            1 for field in profile_fields
            if field not in (None, "")
        )

        total_fields = len(profile_fields)

        if total_fields > 0:
            profile_completion = round(
                (completed_fields / total_fields) * 100
            )

    exam_profile = StudentExamProfile.objects.filter(
        user=user
    ).first()

    exam_completion = 0
    interested_majors_count = 0
    has_criterion_weights = False

    if exam_profile:
        exam_fields = [
            exam_profile.full_name,
            exam_profile.gender,
            exam_profile.exam_group,
            exam_profile.exam_year,
            exam_profile.province,
            exam_profile.city,
            exam_profile.quota,
            exam_profile.national_rank,
            exam_profile.final_score,
        ]

        completed_fields = sum(
            1 for field in exam_fields
            if field not in (None, "")
        )

        exam_completion = round(
            (completed_fields / len(exam_fields)) * 100
        )

        interested_majors_count = exam_profile.interested_majors.count()
        has_criterion_weights = bool(
            getattr(exam_profile, "criterion_weights", None)
        )

    analysis = GeneratedAnalysis.objects.filter(
        user=user
    ).first()

    context = {
        "profile": profile,
        "profile_completion": profile_completion,

        "exam_profile": exam_profile,
        "exam_completion": exam_completion,
        "interested_majors_count": interested_majors_count,
        "has_criterion_weights": has_criterion_weights,

        "analysis": analysis,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )