from django.conf import settings
from django.db import models


class GeneratedAnalysis(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "در حال پردازش"
        DONE = "done", "تکمیل‌شده"
        FAILED = "failed", "خطا"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="generated_analysis",
        verbose_name="کاربر",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="وضعیت",
    )

    prompt_used = models.TextField(
        blank=True,
        verbose_name="پرامپت ارسال‌شده",
    )

    raw_response = models.TextField(
        blank=True,
        verbose_name="پاسخ خام هوش مصنوعی",
    )

    error_message = models.TextField(
        blank=True,
        verbose_name="پیام خطا (در صورت وجود)",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین به‌روزرسانی",
    )

    class Meta:
        verbose_name = "تحلیل تولیدشده"
        verbose_name_plural = "تحلیل‌های تولیدشده"

    def __str__(self):
        return f"تحلیل {self.user.username} ({self.get_status_display()})"
