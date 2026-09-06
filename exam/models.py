from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StudentExamProfile(models.Model):

    class Gender(models.TextChoices):
        MALE = "male", "مرد"
        FEMALE = "female", "زن"

    class ExamGroup(models.TextChoices):
        MATHEMATICS = "math", "ریاضی و فنی"
        EXPERIMENTAL = "experimental", "علوم تجربی"
        HUMANITIES = "humanities", "علوم انسانی"
        ART = "art", "هنر"
        LANGUAGES = "languages", "زبان‌های خارجی"

    class Quota(models.TextChoices):
        REGION_1 = "region_1", "منطقه ۱"
        REGION_2 = "region_2", "منطقه ۲"
        REGION_3 = "region_3", "منطقه ۳"
        MARTYR_5 = "martyr_5", "ایثارگران ۵ درصد"
        MARTYR_25 = "martyr_25", "ایثارگران ۲۵ درصد"
        OTHER = "other", "سایر"

    class SelectionType(models.TextChoices):
        NATIONAL = "national", "کشوری"
        POLE = "pole", "قطبی"
        AREA = "area", "ناحیه‌ای"
        PROVINCE = "province", "استانی"

    class Course(models.TextChoices):
        DAYTIME = "daytime", "روزانه"
        NIGHT = "night", "نوبت دوم / شبانه"
        CAMPUS = "campus", "پردیس خودگردان"
        AZAD = "azad", "دانشگاه آزاد"
        PAYAME_NOOR = "payame_noor", "پیام‌نور"
        NON_PROFIT = "non_profit", "غیرانتفاعی"
        OTHER = "other", "سایر"

    class AllowedStatus(models.TextChoices):
        ALLOWED = "allowed", "مجاز"
        NOT_ALLOWED = "not_allowed", "غیرمجاز"
        UNKNOWN = "unknown", "نامشخص"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_profile",
        verbose_name="کاربر",
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="نام و نام خانوادگی داوطلب",
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        verbose_name="جنسیت",
    )

    exam_group = models.CharField(
        max_length=20,
        choices=ExamGroup.choices,
        verbose_name="گروه آزمایشی",
    )

    exam_year = models.PositiveIntegerField(
        verbose_name="سال کنکور",
    )

    province = models.CharField(
        max_length=100,
        verbose_name="استان محل سکونت",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="شهر محل سکونت",
    )

    quota = models.CharField(
        max_length=30,
        choices=Quota.choices,
        verbose_name="سهمیه",
    )

    region = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="منطقه",
    )

    native_area = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="ناحیه بومی",
    )

    native_pole = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="قطب بومی",
    )

    selection_type = models.CharField(
        max_length=20,
        choices=SelectionType.choices,
        blank=True,
        verbose_name="نوع گزینش رشته",
    )

    rank_in_quota = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="رتبه در سهمیه",
    )

    rank_in_region = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="رتبه در منطقه",
    )

    national_rank = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="رتبه کشوری",
    )

    total_score = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="تراز کل",
    )

    exam_score = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="تراز کنکور / آزمون اختصاصی",
    )

    academic_record_score = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="تراز سوابق تحصیلی",
    )

    final_score = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="تراز نهایی / نمره کل نهایی",
    )

    allowed_daytime = models.CharField(
        max_length=20,
        choices=AllowedStatus.choices,
        default=AllowedStatus.UNKNOWN,
        blank=True,
        verbose_name="مجاز بودن روزانه",
    )

    allowed_night = models.CharField(
        max_length=20,
        choices=AllowedStatus.choices,
        default=AllowedStatus.UNKNOWN,
        blank=True,
        verbose_name="مجاز بودن نوبت دوم / شبانه",
    )

    allowed_campus = models.CharField(
        max_length=20,
        choices=AllowedStatus.choices,
        default=AllowedStatus.UNKNOWN,
        blank=True,
        verbose_name="مجاز بودن پردیس خودگردان",
    )

    allowed_azad = models.CharField(
        max_length=20,
        choices=AllowedStatus.choices,
        default=AllowedStatus.UNKNOWN,
        blank=True,
        verbose_name="مجاز بودن دانشگاه آزاد",
    )

    allowed_payame_noor = models.CharField(
        max_length=20,
        choices=AllowedStatus.choices,
        default=AllowedStatus.UNKNOWN,
        blank=True,
        verbose_name="مجاز بودن پیام‌نور",
    )

    allowed_non_profit = models.CharField(
        max_length=20,
        choices=AllowedStatus.choices,
        default=AllowedStatus.UNKNOWN,
        blank=True,
        verbose_name="مجاز بودن غیرانتفاعی",
    )

    allowed_other = models.CharField(
        max_length=20,
        choices=AllowedStatus.choices,
        default=AllowedStatus.UNKNOWN,
        blank=True,
        verbose_name="مجاز بودن سایر دوره‌ها",
    )

    only_declared_majors = models.BooleanField(
        default=False,
        verbose_name="فقط رشته‌های اعلام‌شده بررسی شوند",
    )

    max_annual_tuition = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name="حداکثر شهریه قابل پرداخت سالانه (تومان)",
    )

    can_pay_night = models.BooleanField(
        default=False,
        verbose_name="توان پرداخت شهریه شبانه",
    )

    can_pay_campus = models.BooleanField(
        default=False,
        verbose_name="توان پرداخت شهریه پردیس",
    )

    can_pay_azad = models.BooleanField(
        default=False,
        verbose_name="توان پرداخت شهریه دانشگاه آزاد",
    )

    can_pay_payame_noor = models.BooleanField(
        default=False,
        verbose_name="توان پرداخت شهریه پیام‌نور",
    )

    can_pay_non_profit = models.BooleanField(
        default=False,
        verbose_name="توان پرداخت شهریه غیرانتفاعی",
    )

    max_distance_km = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="حداکثر فاصله از محل سکونت (کیلومتر)",
    )

    accepted_provinces = models.TextField(
        blank=True,
        verbose_name="استان‌های مورد قبول",
    )

    rejected_provinces = models.TextField(
        blank=True,
        verbose_name="استان‌های غیرقابل قبول",
    )

    preferred_cities = models.TextField(
        blank=True,
        verbose_name="شهرهای مورد علاقه",
    )

    rejected_cities = models.TextField(
        blank=True,
        verbose_name="شهرهای غیرقابل قبول",
    )

    geographic_distance_is_important = models.BooleanField(
        default=True,
        verbose_name="فاصله جغرافیایی اهمیت دارد",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین ویرایش",
    )

    class Meta:
        verbose_name = "پروفایل انتخاب رشته"
        verbose_name_plural = "پروفایل‌های انتخاب رشته"

    def __str__(self):
        return f"{self.full_name} - کنکور {self.exam_year}"


class InterestedMajor(models.Model):

    profile = models.ForeignKey(
        StudentExamProfile,
        on_delete=models.CASCADE,
        related_name="interested_majors",
        verbose_name="پروفایل داوطلب",
    )

    major_name = models.CharField(
        max_length=150,
        verbose_name="نام رشته",
    )

    interest_score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name="امتیاز علاقه از ۱۰",
    )

    class Meta:
        verbose_name = "رشته مورد علاقه"
        verbose_name_plural = "رشته‌های مورد علاقه"
        ordering = ["-interest_score", "major_name"]

    def __str__(self):
        return f"{self.major_name} ({self.interest_score}/10)"


class RejectedMajor(models.Model):

    profile = models.ForeignKey(
        StudentExamProfile,
        on_delete=models.CASCADE,
        related_name="rejected_majors",
        verbose_name="پروفایل داوطلب",
    )

    major_name = models.CharField(
        max_length=150,
        verbose_name="نام رشته",
    )

    class Meta:
        verbose_name = "رشته غیرقابل قبول"
        verbose_name_plural = "رشته‌های غیرقابل قبول"

    def __str__(self):
        return self.major_name


class CriterionWeight(models.Model):

    profile = models.OneToOneField(
        StudentExamProfile,
        on_delete=models.CASCADE,
        related_name="criterion_weights",
        verbose_name="پروفایل داوطلب",
    )

    interest = models.PositiveSmallIntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="وزن علاقه به رشته",
    )

    university_reputation = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="اعتبار کلی دانشگاه",
    )

    faculty_quality = models.PositiveSmallIntegerField(
        default=8,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="کیفیت تخصصی دانشکده / گروه آموزشی",
    )

    job_market = models.PositiveSmallIntegerField(
        default=7,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="بازار کار",
    )

    income_potential = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="پتانسیل درآمد",
    )

    immigration_potential = models.PositiveSmallIntegerField(
        default=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="امکان مهاجرت",
    )

    academic_career = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="امکان هیئت علمی",
    )

    class Meta:
        verbose_name = "وزن معیار انتخاب رشته"
        verbose_name_plural = "وزن معیارهای انتخاب رشته"

    def __str__(self):
        return f"وزن معیارهای {self.profile.full_name}"


class AcceptedCourse(models.Model):

    profile = models.ForeignKey(
        StudentExamProfile,
        on_delete=models.CASCADE,
        related_name="accepted_courses",
        verbose_name="پروفایل داوطلب",
    )

    course = models.CharField(
        max_length=30,
        choices=StudentExamProfile.Course.choices,
        verbose_name="دوره مورد قبول",
    )

    class Meta:
        verbose_name = "دوره مورد قبول"
        verbose_name_plural = "دوره‌های مورد قبول"
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "course"],
                name="unique_accepted_course_per_profile",
            )
        ]

    def __str__(self):
        return self.get_course_display()