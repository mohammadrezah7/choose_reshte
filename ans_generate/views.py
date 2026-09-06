from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from exam.models import StudentExamProfile

from .models import GeneratedAnalysis
from .prompt import build_prompt
from .services import AIServiceError, call_ai


@login_required
def generate_analysis(request):
    """
    نمایش صفحه‌ی تأیید و تولید تحلیل هوش مصنوعی بر اساس پروفایل کنکور کاربر.
    """

    exam_profile = StudentExamProfile.objects.filter(
        user=request.user
    ).first()

    if exam_profile is None:
        messages.error(
            request,
            "ابتدا باید پروفایل انتخاب رشته‌ی خود را تکمیل کنید.",
        )
        return redirect("exam:exam_profile")

    if request.method != "POST":
        return render(
            request,
            "ans_generate/confirm.html",
            {"exam_profile": exam_profile},
        )

    prompt = build_prompt(exam_profile)

    analysis, _ = GeneratedAnalysis.objects.get_or_create(user=request.user)
    analysis.prompt_used = prompt
    analysis.status = GeneratedAnalysis.Status.PENDING
    analysis.error_message = ""
    analysis.save()

    try:
        result = call_ai(prompt)
    except AIServiceError as exc:
        analysis.status = GeneratedAnalysis.Status.FAILED
        analysis.error_message = str(exc)
        analysis.save()

        messages.error(
            request,
            "در تولید تحلیل خطایی رخ داد. لطفاً دوباره تلاش کنید.",
        )
        return redirect("ans_generate:generate")

    analysis.status = GeneratedAnalysis.Status.DONE
    analysis.raw_response = result
    analysis.save()

    return redirect("report:view_report")


@login_required
def analysis_status(request):
    """
    نمایش وضعیت فعلی تحلیل تولیدشده برای کاربر.
    """

    analysis = get_object_or_404(
        GeneratedAnalysis,
        user=request.user,
    )

    return render(
        request,
        "ans_generate/status.html",
        {"analysis": analysis},
    )
