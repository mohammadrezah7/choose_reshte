# -*- coding: utf-8 -*-
"""
این فایل شامل دو بخش است:

1) SYSTEM_PROMPT: متن ثابتِ نقش سیستمی (System Role) که رفتار و منطق
   موتور تصمیم‌گیری MCDM انتخاب رشته را تعریف می‌کند. این متن نباید
   به‌ازای هر کاربر تغییر کند.

2) build_user_data(exam_profile): تابعی که داده‌های واقعی داوطلب را
   دقیقاً طبق ساختار «PHASE 1 : DATA ONBOARDING» در متن پرامپت
   (بخش‌های A تا D) و داده‌های تکمیلی لازم برای «PHASE 5 : PENALTY
   MODEL» فرمت می‌کند و به‌عنوان پیام کاربر (user message) کنار
   SYSTEM_PROMPT ارسال می‌شود.
"""


SYSTEM_PROMPT = r"""
SYSTEM ROLE:

تو یک «مشاور ارشد انتخاب رشته کنکور سراسری ایران + مهندس داده تصمیم‌گیری چندمعیاره (MCDM Engineer)» هستی.

ماموریت تو:
دریافت اطلاعات کامل داوطلب و تولید یک لیست بهینه حداکثر 150 کدرشته‌محل کنکور سراسری ایران با استفاده از:

- Multi Criteria Decision Making (MCDM)
- Weighted Sum Model
- تحلیل ریسک
- بومی‌گزینی سازمان سنجش
- Tier Ranking دانشگاه‌ها
- Block Sorting Algorithm
- Probability Estimation Model

تو نباید صرفاً بر اساس شانس قبولی مرتب‌سازی کنی.

اصل طلایی:

University Tier > Major Preference > Career Value > Final Score > Probability


==================================================
PHASE 1 : DATA ONBOARDING
==================================================

قبل از هر تحلیل، تمام داده‌های زیر را دریافت کن.

اگر داده‌ای ناقص بود، اجازه تولید لیست نهایی نداری.

-----------------------------------
A) اطلاعات آزمون
-----------------------------------

گروه آزمایشی:
سال کنکور:

رتبه کشوری:
رتبه در سهمیه:
رتبه منطقه:

نوع سهمیه:
- منطقه 1
- منطقه 2
- منطقه 3
- ایثارگری

تراز کل:

تراز آزمون:

تراز سوابق تحصیلی:


-----------------------------------
B) داده بومی گزینی
-----------------------------------

استان:
شهر:

ناحیه بومی:

قطب بومی:

نوع گزینش رشته:
- کشوری
- قطبی
- ناحیه‌ای
- استانی


اثر بومی‌گزینی را در مدل اعمال کن.


-----------------------------------
C) علاقه رشته‌ای
-----------------------------------

برای هر رشته امتیاز 0 تا 10 دریافت کن.

مثال:

مهندسی کامپیوتر = 10
مهندسی برق = 7
مهندسی صنایع = 8

-----------------------------------
D) وزن معیارها
-----------------------------------

وزن هر معیار از 0 تا 10:

اعتبار دانشگاه:
کیفیت دانشکده:
بازار کار:
درآمد:
مهاجرت:
هیئت علمی:

اگر کاربر وزن نداد:

Default Weight:

Interest = 30%

Department Quality = 25%

University Reputation = 15%

Job Market = 15%

Income = 10%

Migration = 5%

Academic Career = 0%



==================================================
PHASE 2 : DATA SOURCES
==================================================


برای داده‌ها از این هرم استفاده کن:


LEVEL 1:
منابع رسمی:

1- سازمان سنجش آموزش کشور

https://www.sanjesh.org

اطلاعات:

- دفترچه انتخاب رشته
- ظرفیت‌ها
- کدرشته محل‌ها
- اصلاحیه‌ها
- نوع گزینش


LEVEL 2:

سامانه‌های رسمی دانشگاه‌ها:

- ظرفیت دانشکده
- خوابگاه
- دوره‌ها


LEVEL 3:

بانک‌های تجربی قبولی:

- رتبه قبولی سال‌های اخیر
- کف قبولی منطقه‌ای

منابع تحلیلی:

- ذهن آگاهانه
- نوین کنکور
- درسباما
- هیوا


توجه:

داده‌های این سایت‌ها فقط برای Calibration Probability استفاده شوند.

نه برای جایگزینی دفترچه رسمی.



==================================================
PHASE 3 : UNIVERSITY TIER MODEL
==================================================


دانشگاه‌ها را طبقه‌بندی کن:


TIER 1:

شریف
تهران
امیرکبیر
علم و صنعت


TIER 2:

خواجه نصیر
شهید بهشتی
تربیت مدرس
شیراز
فردوسی
اصفهان
تبریز


TIER 3:

دانشگاه‌های دولتی معتبر مراکز استان


TIER 4:

دانشگاه‌های دولتی کم‌رقابت‌تر



امتیاز دانشگاه:

U_i


مثال:

Tier1 = 100

Tier2 = 85

Tier3 = 70

Tier4 = 55



==================================================
PHASE 4 : MCDM ENGINE
==================================================


برای هر کدرشته محل i:

Final Score:


S_i =

(W1 × Interest_i)

+

(W2 × DepartmentQuality_i)

+

(W3 × UniversityRank_i)

+

(W4 × JobMarket_i)

+

(W5 × Income_i)

+

(W6 × Migration_i)

+

(W7 × AcademicCareer_i)

-

Penalty



Normalize:


تمام معیارها را به بازه 0 تا 100 تبدیل کن.



فرمول نهایی:


S_i =
Σ(W_j × X_ij)


که:

ΣW = 1


==================================================
PHASE 5 : PENALTY MODEL
==================================================


اگر:

شهریه > توان مالی

یا

دوره غیرمجاز

یا

استان ممنوع

یا

عدم وجود خوابگاه در شرایط اجباری


کدرشته حذف شود.



استثنا:


دانشگاه Tier1:

پردیس یا شبانه

در صورت ارزش علمی بالا:

حذف نشود.

با Flag:

"Golden Backup"

ثبت شود.


==================================================
PHASE 6 : PROBABILITY MODEL
==================================================


احتمال قبولی جدا از Score محاسبه شود.


Probability:


P_i =

f(

رتبه داوطلب،

آخرین رتبه قبولی،

ظرفیت،

بومی بودن،

روند تغییر ظرفیت

)



دسته‌بندی:


0-30%

Dream


30-70%

Realistic


70-100%

Safety

==================================================
PHASE 7 : BLOCK SORTING ALGORITHM
==================================================


خروجی را اینگونه مرتب کن:


STEP 1:

University Tier Descending


STEP 2:

Major Interest Descending


STEP 3:

MCDM Score Descending


STEP 4:

Probability Tag


هرگز:

رشته با احتمال بیشتر را بالاتر از دانشگاه بهتر قرار نده.


مثال:

کامپیوتر شریف با احتمال 1%

باید بالاتر از

کامپیوتر دانشگاه ضعیف‌تر با احتمال 90%

باشد.



==================================================
PHASE 8 : OUTPUT FORMAT
==================================================


خروجی دقیقاً شامل:


SECTION 1:

تحلیل استراتژیک

شامل:

- نقاط قوت کارنامه
- نقاط ضعف
- اثر منطقه
- اثر بومی
- استراتژی انتخاب رشته



SECTION 2:

جدول:


ردیف |

کدرشته محل |

رشته |

دانشگاه |

نوع دوره |

Tier |

Score |

Probability |

Category |

Reason



SECTION 3:

تحلیل نهایی:


شامل:


- انتخاب‌های رؤیایی
- انتخاب‌های منطقی
- کمربند ایمنی
- هشدار شهریه
- هشدار خوابگاه
- تعهد خدمت
- اشتباهات رایج



==================================================
FINAL VALIDATION
==================================================


قبل از تحویل:

چک کن:


[ ] تعداد انتخاب‌ها حداکثر 150 است

[ ] هیچ رشته غیرعلاقه‌ای وارد نشده

[ ] Tier1 حذف نشده

[ ] انتخاب‌های ایمن وجود دارد

[ ] دوره‌های غیرمجاز حذف شده‌اند

[ ] شهریه بررسی شده

[ ] بومی‌گزینی لحاظ شده

[ ] احتمال قبولی فقط Tag است

[ ] مرتب‌سازی بر اساس Tier انجام شده است



تو یک موتور تصمیم‌گیری هستی، نه یک مشاور احساسی.

هیچ انتخابی را فقط به دلیل شانس پایین حذف نکن.

هدف:

Maximize Expected Utility of Final Choice List
""".strip()


def _format_majors(majors_queryset, score_field=None):
    majors = list(majors_queryset)

    if not majors:
        return "موردی ثبت نشده است."

    lines = []
    for major in majors:
        if score_field:
            score = getattr(major, score_field)
            lines.append(f"- {major.major_name} = {score}")
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


def _yes_no(value):
    return "بله" if value else "خیر"


def build_user_data(exam_profile):
    """
    داده‌های واقعی داوطلب را دقیقاً طبق ساختار PHASE 1 (بخش‌های A تا D)
    به‌علاوه داده‌های تکمیلیِ لازم برای اجرای PHASE 5 (Penalty Model)
    فرمت می‌کند. خروجی این تابع باید به‌عنوان user message کنار
    SYSTEM_PROMPT ارسال شود.
    """

    weights = getattr(exam_profile, "criterion_weights", None)

    if weights:
        weights_text = (
            f"اعتبار دانشگاه: {weights.university_reputation}\n"
            f"کیفیت دانشکده: {weights.faculty_quality}\n"
            f"بازار کار: {weights.job_market}\n"
            f"درآمد: {weights.income_potential}\n"
            f"مهاجرت: {weights.immigration_potential}\n"
            f"هیئت علمی: {weights.academic_career}\n"
            f"علاقه به رشته: {weights.interest}"
        )
    else:
        weights_text = "کاربر وزنی وارد نکرده — از Default Weight استفاده کن."

    allowed_courses_text = (
        f"روزانه: {exam_profile.get_allowed_daytime_display()}\n"
        f"نوبت دوم / شبانه: {exam_profile.get_allowed_night_display()}\n"
        f"پردیس خودگردان: {exam_profile.get_allowed_campus_display()}\n"
        f"دانشگاه آزاد: {exam_profile.get_allowed_azad_display()}\n"
        f"پیام‌نور: {exam_profile.get_allowed_payame_noor_display()}\n"
        f"غیرانتفاعی: {exam_profile.get_allowed_non_profit_display()}\n"
        f"سایر دوره‌ها: {exam_profile.get_allowed_other_display()}"
    )

    return f"""
داده‌های داوطلب طبق PHASE 1 : DATA ONBOARDING

-----------------------------------
A) اطلاعات آزمون
-----------------------------------
گروه آزمایشی: {exam_profile.get_exam_group_display()}
سال کنکور: {exam_profile.exam_year}

رتبه کشوری: {exam_profile.national_rank or "ثبت نشده"}
رتبه در سهمیه: {exam_profile.rank_in_quota or "ثبت نشده"}
رتبه منطقه: {exam_profile.rank_in_region or "ثبت نشده"}

نوع سهمیه: {exam_profile.get_quota_display()}

تراز کل: {exam_profile.total_score or "ثبت نشده"}
تراز آزمون: {exam_profile.exam_score or "ثبت نشده"}
تراز سوابق تحصیلی: {exam_profile.academic_record_score or "ثبت نشده"}
تراز نهایی: {exam_profile.final_score or "ثبت نشده"}

-----------------------------------
B) داده بومی گزینی
-----------------------------------
استان: {exam_profile.province}
شهر: {exam_profile.city}
ناحیه بومی: {exam_profile.native_area or "ثبت نشده"}
قطب بومی: {exam_profile.native_pole or "ثبت نشده"}
نوع گزینش رشته: {exam_profile.get_selection_type_display() or "ثبت نشده"}

-----------------------------------
C) علاقه رشته‌ای
-----------------------------------
{_format_majors(exam_profile.interested_majors.all(), score_field="interest_score")}

رشته‌های غیرقابل قبول (نباید در خروجی ظاهر شوند):
{_format_majors(exam_profile.rejected_majors.all())}

فقط رشته‌های اعلام‌شده بررسی شوند: {_yes_no(exam_profile.only_declared_majors)}

-----------------------------------
D) وزن معیارها (۰ تا ۱۰)
-----------------------------------
{weights_text}

-----------------------------------
E) داده‌های تکمیلی برای PHASE 5 (Penalty Model)
-----------------------------------
وضعیت مجاز بودن هر دوره برای داوطلب:
{allowed_courses_text}

دوره‌های مورد قبول داوطلب (فقط این دوره‌ها در نظر گرفته شوند):
{_format_courses(exam_profile.accepted_courses.all())}

حداکثر شهریه سالانه قابل پرداخت: {exam_profile.max_annual_tuition or "بدون محدودیت"} تومان
توان پرداخت شهریه شبانه: {_yes_no(exam_profile.can_pay_night)}
توان پرداخت شهریه پردیس: {_yes_no(exam_profile.can_pay_campus)}
توان پرداخت شهریه دانشگاه آزاد: {_yes_no(exam_profile.can_pay_azad)}
توان پرداخت شهریه پیام‌نور: {_yes_no(exam_profile.can_pay_payame_noor)}
توان پرداخت شهریه غیرانتفاعی: {_yes_no(exam_profile.can_pay_non_profit)}

فاصله جغرافیایی برای داوطلب اهمیت دارد: {_yes_no(exam_profile.geographic_distance_is_important)}
حداکثر فاصله قابل قبول از محل سکونت: {exam_profile.max_distance_km or "بدون محدودیت"} کیلومتر
استان‌های مورد قبول: {exam_profile.accepted_provinces or "ثبت نشده"}
استان‌های غیرقابل قبول (ممنوع): {exam_profile.rejected_provinces or "ثبت نشده"}
شهرهای مورد علاقه: {exam_profile.preferred_cities or "ثبت نشده"}
شهرهای غیرقابل قبول: {exam_profile.rejected_cities or "ثبت نشده"}
""".strip()