PROMPT_TEMPLATE = """
تو یک مشاور متخصص انتخاب رشته‌ی کنکور هستی.
بر اساس اطلاعات زیر، بهترین رشته‌ها و دانشگاه‌ها را به داوطلب پیشنهاد بده
و دلیل هر پیشنهاد را به‌طور شفاف توضیح بده.

# اطلاعات داوطلب
نام: {full_name}
گروه آزمایشی: {exam_group}
سال کنکور: {exam_year}
استان و شهر: {province}، {city}
سهمیه: {quota}
رتبه کشوری: {national_rank}
تراز نهایی: {final_score}

# دوره‌های مورد قبول داوطلب
{accepted_courses}

# رشته‌های مورد علاقه
{interested_majors}

# رشته‌های غیرقابل قبول
{rejected_majors}

# وزن معیارهای انتخاب رشته (از ۰ تا ۱۰)
{criterion_weights}

# محدودیت‌های جغرافیایی و مالی
حداکثر فاصله قابل قبول: {max_distance_km} کیلومتر
حداکثر شهریه سالانه قابل پرداخت: {max_annual_tuition} تومان
استان‌های مورد قبول: {accepted_provinces}
استان‌های غیرقابل قبول: {rejected_provinces}

لطفاً پاسخ را به زبان فارسی و به‌صورت ساختاریافته (لیست رشته‌ها به ترتیب
اولویت همراه با توضیح) ارائه بده.
""".strip()


def _format_majors(majors_queryset, score_field=None):
    majors = list(majors_queryset)

    if not majors:
        return "موردی ثبت نشده است."

    lines = []
    for major in majors:
        if score_field:
            score = getattr(major, score_field)
            lines.append(f"- {major.major_name} (امتیاز علاقه: {score}/10)")
        else:
            lines.append(f"- {major.major_name}")

    return "\n".join(lines)


def _format_courses(courses_queryset):
    courses = list(courses_queryset)

    if not courses:
        return "موردی ثبت نشده است."

    return "\n".join(
        f"- {course.get_course_display()}" for course in courses
    )


def _format_weights(criterion_weights):
    if criterion_weights is None:
        return "وزن معیاری ثبت نشده است (مقادیر پیش‌فرض در نظر گرفته شود)."

    return (
        f"- علاقه به رشته: {criterion_weights.interest}\n"
        f"- اعتبار دانشگاه: {criterion_weights.university_reputation}\n"
        f"- کیفیت دانشکده: {criterion_weights.faculty_quality}\n"
        f"- بازار کار: {criterion_weights.job_market}\n"
        f"- پتانسیل درآمد: {criterion_weights.income_potential}\n"
        f"- امکان مهاجرت: {criterion_weights.immigration_potential}\n"
        f"- امکان هیئت علمی: {criterion_weights.academic_career}"
    )


def build_prompt(exam_profile):
    """
    پرامپت نهایی را با استفاده از داده‌های پروفایل داوطلب (exam.StudentExamProfile)
    می‌سازد و آن را به‌صورت رشته برمی‌گرداند.
    """

    criterion_weights = getattr(exam_profile, "criterion_weights", None)

    return PROMPT_TEMPLATE.format(
        full_name=exam_profile.full_name,
        exam_group=exam_profile.get_exam_group_display(),
        exam_year=exam_profile.exam_year,
        province=exam_profile.province,
        city=exam_profile.city,
        quota=exam_profile.get_quota_display(),
        national_rank=exam_profile.national_rank or "ثبت نشده",
        final_score=exam_profile.final_score or "ثبت نشده",
        accepted_courses=_format_courses(exam_profile.accepted_courses.all()),
        interested_majors=_format_majors(
            exam_profile.interested_majors.all(),
            score_field="interest_score",
        ),
        rejected_majors=_format_majors(exam_profile.rejected_majors.all()),
        criterion_weights=_format_weights(criterion_weights),
        max_distance_km=exam_profile.max_distance_km or "بدون محدودیت",
        max_annual_tuition=exam_profile.max_annual_tuition or "بدون محدودیت",
        accepted_provinces=exam_profile.accepted_provinces or "ثبت نشده",
        rejected_provinces=exam_profile.rejected_provinces or "ثبت نشده",
    )
