from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ans_generate.models import GeneratedAnalysis
from exam.models import StudentExamProfile


@login_required
def view_report(request):
    """
    نمایش خلاصه‌ی نهایی پروفایل کنکور به‌همراه تحلیل تولیدشده توسط هوش مصنوعی.
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

    analysis = GeneratedAnalysis.objects.filter(
        user=request.user
    ).first()

    if analysis is None or analysis.status != GeneratedAnalysis.Status.DONE:
        messages.info(
            request,
            "هنوز تحلیلی برای شما تولید نشده است.",
        )
        return redirect("ans_generate:generate")

    return render(
        request,
        "reports/reports.html",
        {
            "exam_profile": exam_profile,
            "analysis": analysis,
        },
    )