from django.contrib import admin

from .models import (
    AcceptedCourse,
    CriterionWeight,
    InterestedMajor,
    RejectedMajor,
    StudentExamProfile,
)


class ExamGroupFilter(admin.SimpleListFilter):
    title = "گروه آزمایشی"
    parameter_name = "exam_group"

    def lookups(self, request, model_admin):
        # همه گزینه‌های ثابت مدل را نمایش می‌دهد،
        # حتی اگر برای بعضی از آن‌ها رکوردی وجود نداشته باشد.
        return StudentExamProfile.ExamGroup.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(exam_group=self.value())

        return queryset


class InterestedMajorInline(admin.TabularInline):
    model = InterestedMajor
    extra = 3


class RejectedMajorInline(admin.TabularInline):
    model = RejectedMajor
    extra = 1


class AcceptedCourseInline(admin.TabularInline):
    model = AcceptedCourse
    extra = 1


class CriterionWeightInline(admin.StackedInline):
    model = CriterionWeight
    extra = 0
    max_num = 1


@admin.register(StudentExamProfile)
class StudentExamProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "exam_group",
        "exam_year",
        "province",
        "rank_in_quota",
        "final_score",
    )

    list_filter = (
        ExamGroupFilter,  # جایگزین "exam_group"
        "exam_year",
        "gender",
        "quota",
        "geographic_distance_is_important",
    )

    search_fields = (
        "full_name",
        "user__username",
        "province",
        "city",
    )

    inlines = [
        InterestedMajorInline,
        RejectedMajorInline,
        AcceptedCourseInline,
        CriterionWeightInline,
    ]
