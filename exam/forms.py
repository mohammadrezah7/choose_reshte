from django import forms

from .models import (
    CriterionWeight,
    InterestedMajor,
    RejectedMajor,
    StudentExamProfile,
)


class StudentExamProfileForm(forms.ModelForm):
    class Meta:
        model = StudentExamProfile
        exclude = [
            "user",
            "created_at",
            "updated_at",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام و نام خانوادگی",
                }
            ),
            "gender": forms.Select(
                attrs={"class": "form-select"}
            ),
            "exam_group": forms.Select(
                attrs={"class": "form-select"}
            ),
            "exam_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1400",
                    "max": "1500",
                }
            ),
            "province": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "استان محل سکونت",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شهر محل سکونت",
                }
            ),
            "quota": forms.Select(
                attrs={"class": "form-select"}
            ),
            "region": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "منطقه",
                }
            ),
            "native_area": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ناحیه بومی",
                }
            ),
            "native_pole": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "قطب بومی",
                }
            ),
            "selection_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "rank_in_quota": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),
            "rank_in_region": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),
            "national_rank": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),
            "total_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "exam_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "academic_record_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "final_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "allowed_daytime": forms.Select(
                attrs={"class": "form-select"}
            ),
            "allowed_night": forms.Select(
                attrs={"class": "form-select"}
            ),
            "allowed_campus": forms.Select(
                attrs={"class": "form-select"}
            ),
            "allowed_azad": forms.Select(
                attrs={"class": "form-select"}
            ),
            "allowed_payame_noor": forms.Select(
                attrs={"class": "form-select"}
            ),
            "allowed_non_profit": forms.Select(
                attrs={"class": "form-select"}
            ),
            "allowed_other": forms.Select(
                attrs={"class": "form-select"}
            ),
            "only_declared_majors": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "max_annual_tuition": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),
            "can_pay_night": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "can_pay_campus": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "can_pay_azad": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "can_pay_payame_noor": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "can_pay_non_profit": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "max_distance_km": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),
            "accepted_provinces": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "استان‌های مورد قبول را وارد کنید",
                }
            ),
            "rejected_provinces": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "استان‌های غیرقابل قبول را وارد کنید",
                }
            ),
            "preferred_cities": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "شهرهای مورد علاقه را وارد کنید",
                }
            ),
            "rejected_cities": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "شهرهای غیرقابل قبول را وارد کنید",
                }
            ),
            "geographic_distance_is_important": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_exam_year(self):
        exam_year = self.cleaned_data["exam_year"]

        if not 1400 <= exam_year <= 1500:
            raise forms.ValidationError(
                "سال کنکور واردشده معتبر نیست."
            )

        return exam_year

    def clean(self):
        cleaned_data = super().clean()

        quota = cleaned_data.get("quota")
        region = cleaned_data.get("region")

        regional_quotas = {
            StudentExamProfile.Quota.REGION_1,
            StudentExamProfile.Quota.REGION_2,
            StudentExamProfile.Quota.REGION_3,
        }

        if quota in regional_quotas and not region:
            self.add_error(
                "region",
                "برای سهمیه منطقه‌ای باید منطقه مشخص شود.",
            )

        return cleaned_data


class InterestedMajorForm(forms.ModelForm):
    class Meta:
        model = InterestedMajor
        fields = [
            "major_name",
            "interest_score",
        ]

        widgets = {
            "major_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام رشته",
                }
            ),
            "interest_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
        }


class RejectedMajorForm(forms.ModelForm):
    class Meta:
        model = RejectedMajor
        fields = [
            "major_name",
        ]

        widgets = {
            "major_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام رشته",
                }
            ),
        }


class CriterionWeightForm(forms.ModelForm):
    class Meta:
        model = CriterionWeight
        fields = [
            "interest",
            "university_reputation",
            "faculty_quality",
            "job_market",
            "income_potential",
            "immigration_potential",
            "academic_career",
        ]

        widgets = {
            "interest": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
            "university_reputation": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
            "faculty_quality": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
            "job_market": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
            "income_potential": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
            "immigration_potential": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
            "academic_career": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "max": "10",
                }
            ),
        }