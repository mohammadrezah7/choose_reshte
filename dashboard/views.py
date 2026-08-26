from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Profile


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


    exam_data = None
    exam_completion = 0

    latest_analysis = None
    analysis_count = 0

    reports_count = 0

    context = {
        "profile": profile,

        "profile_completion": profile_completion,

        "exam_data": exam_data,
        "exam_completion": exam_completion,

        "latest_analysis": latest_analysis,
        "analysis_count": analysis_count,

        "reports_count": reports_count,
    }

    return render(
        request,
        "dashboard/index.html",
        context
    )