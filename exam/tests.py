from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import (
    CriterionWeightForm,
    InterestedMajorForm,
    RejectedMajorForm,
    StudentExamProfileForm,
)
from .models import (
    AcceptedCourse,
    CriterionWeight,
    InterestedMajor,
    RejectedMajor,
    StudentExamProfile,
)

User = get_user_model()


class StudentExamProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123",
            email="test@example.com",
        )

    def get_valid_data(self):
        return {
            "full_name": "علی رضایی",
            "gender": StudentExamProfile.Gender.MALE,
            "exam_group": StudentExamProfile.ExamGroup.MATHEMATICS,
            "exam_year": 1405,
            "province": "تهران",
            "city": "تهران",
            "quota": StudentExamProfile.Quota.REGION_1,
            "region": "منطقه ۱",
            "native_area": "تهران",
            "native_pole": "مرکز",
            "selection_type": StudentExamProfile.SelectionType.PROVINCE,
            "rank_in_quota": 100,
            "rank_in_region": 120,
            "national_rank": 500,
            "total_score": 9000,
            "exam_score": 8500,
            "academic_record_score": 8800,
            "final_score": 8700,
        }

    def test_student_exam_profile_creation(self):
        profile = StudentExamProfile.objects.create(
            user=self.user,
            **self.get_valid_data(),
        )

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.full_name, "علی رضایی")
        self.assertEqual(
            profile.exam_group,
            StudentExamProfile.ExamGroup.MATHEMATICS,
        )

    def test_one_exam_profile_per_user(self):
        StudentExamProfile.objects.create(
            user=self.user,
            **self.get_valid_data(),
        )

        with self.assertRaises(Exception):
            StudentExamProfile.objects.create(
                user=self.user,
                **self.get_valid_data(),
            )


class StudentExamProfileFormTest(TestCase):

    def get_valid_data(self):
        return {
            "full_name": "علی رضایی",
            "gender": StudentExamProfile.Gender.MALE,
            "exam_group": StudentExamProfile.ExamGroup.MATHEMATICS,
            "exam_year": 1405,
            "province": "تهران",
            "city": "تهران",
            "quota": StudentExamProfile.Quota.REGION_1,
            "region": "منطقه ۱",
            "native_area": "تهران",
            "native_pole": "مرکز",
            "selection_type": StudentExamProfile.SelectionType.PROVINCE,
            "rank_in_quota": 100,
            "rank_in_region": 120,
            "national_rank": 500,
            "total_score": 9000,
            "exam_score": 8500,
            "academic_record_score": 8800,
            "final_score": 8700,
            "allowed_daytime": StudentExamProfile.AllowedStatus.ALLOWED,
            "allowed_night": StudentExamProfile.AllowedStatus.ALLOWED,
            "allowed_campus": StudentExamProfile.AllowedStatus.UNKNOWN,
            "allowed_azad": StudentExamProfile.AllowedStatus.UNKNOWN,
            "allowed_payame_noor": StudentExamProfile.AllowedStatus.UNKNOWN,
            "allowed_non_profit": StudentExamProfile.AllowedStatus.UNKNOWN,
            "allowed_other": StudentExamProfile.AllowedStatus.UNKNOWN,
            "only_declared_majors": False,
            "max_annual_tuition": 100000000,
            "can_pay_night": True,
            "can_pay_campus": False,
            "can_pay_azad": True,
            "can_pay_payame_noor": True,
            "can_pay_non_profit": True,
            "max_distance_km": 300,
            "accepted_provinces": "تهران\nالبرز",
            "rejected_provinces": "سیستان و بلوچستان",
            "preferred_cities": "تهران\nکرج",
            "rejected_cities": "اهواز",
            "geographic_distance_is_important": True,
        }

    def test_valid_form(self):
        form = StudentExamProfileForm(
            data=self.get_valid_data()
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_exam_year(self):
        data = self.get_valid_data()
        data["exam_year"] = 1300

        form = StudentExamProfileForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("exam_year", form.errors)

    def test_regional_quota_requires_region(self):
        data = self.get_valid_data()
        data["region"] = ""

        form = StudentExamProfileForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("region", form.errors)


class InterestedMajorTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="majoruser",
            password="TestPassword123",
        )

        self.profile = StudentExamProfile.objects.create(
            user=self.user,
            full_name="علی رضایی",
            gender=StudentExamProfile.Gender.MALE,
            exam_group=StudentExamProfile.ExamGroup.MATHEMATICS,
            exam_year=1405,
            province="تهران",
            city="تهران",
            quota=StudentExamProfile.Quota.REGION_1,
            selection_type=StudentExamProfile.SelectionType.PROVINCE,
        )

    def test_interested_major_creation(self):
        major = InterestedMajor.objects.create(
            profile=self.profile,
            major_name="مهندسی کامپیوتر",
            interest_score=10,
        )

        self.assertEqual(
            major.major_name,
            "مهندسی کامپیوتر",
        )

    def test_interest_score_range(self):
        form = InterestedMajorForm(
            data={
                "major_name": "مهندسی کامپیوتر",
                "interest_score": 11,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("interest_score", form.errors)


class RejectedMajorTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="rejecteduser",
            password="TestPassword123",
        )

        self.profile = StudentExamProfile.objects.create(
            user=self.user,
            full_name="علی رضایی",
            gender=StudentExamProfile.Gender.MALE,
            exam_group=StudentExamProfile.ExamGroup.MATHEMATICS,
            exam_year=1405,
            province="تهران",
            city="تهران",
            quota=StudentExamProfile.Quota.REGION_1,
            selection_type=StudentExamProfile.SelectionType.PROVINCE,
        )

    def test_rejected_major_creation(self):
        major = RejectedMajor.objects.create(
            profile=self.profile,
            major_name="رشته‌ای که نمی‌خواهم",
        )

        self.assertEqual(
            major.profile,
            self.profile,
        )


class CriterionWeightTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="weightuser",
            password="TestPassword123",
        )

        self.profile = StudentExamProfile.objects.create(
            user=self.user,
            full_name="علی رضایی",
            gender=StudentExamProfile.Gender.MALE,
            exam_group=StudentExamProfile.ExamGroup.MATHEMATICS,
            exam_year=1405,
            province="تهران",
            city="تهران",
            quota=StudentExamProfile.Quota.REGION_1,
            selection_type=StudentExamProfile.SelectionType.PROVINCE,
        )

    def test_criterion_weight_creation(self):
        weights = CriterionWeight.objects.create(
            profile=self.profile,
            interest=10,
            university_reputation=8,
            faculty_quality=9,
            job_market=8,
            income_potential=7,
            immigration_potential=6,
            academic_career=5,
        )

        self.assertEqual(weights.interest, 10)
        self.assertEqual(weights.profile, self.profile)

    def test_criterion_weight_form_range(self):
        form = CriterionWeightForm(
            data={
                "interest": 11,
                "university_reputation": 5,
                "faculty_quality": 5,
                "job_market": 5,
                "income_potential": 5,
                "immigration_potential": 5,
                "academic_career": 5,
            }
        )

        self.assertFalse(form.is_valid())


class AcceptedCourseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="courseuser",
            password="TestPassword123",
        )

        self.profile = StudentExamProfile.objects.create(
            user=self.user,
            full_name="علی رضایی",
            gender=StudentExamProfile.Gender.MALE,
            exam_group=StudentExamProfile.ExamGroup.MATHEMATICS,
            exam_year=1405,
            province="تهران",
            city="تهران",
            quota=StudentExamProfile.Quota.REGION_1,
            selection_type=StudentExamProfile.SelectionType.PROVINCE,
        )

    def test_accepted_course_creation(self):
        course = AcceptedCourse.objects.create(
            profile=self.profile,
            course=StudentExamProfile.Course.DAYTIME,
        )

        self.assertEqual(
            course.course,
            StudentExamProfile.Course.DAYTIME,
        )

    def test_duplicate_course_is_not_allowed(self):
        AcceptedCourse.objects.create(
            profile=self.profile,
            course=StudentExamProfile.Course.DAYTIME,
        )

        with self.assertRaises(Exception):
            AcceptedCourse.objects.create(
                profile=self.profile,
                course=StudentExamProfile.Course.DAYTIME,
            )


class ExamViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="viewuser",
            password="TestPassword123",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123",
        )

        self.profile = StudentExamProfile.objects.create(
            user=self.user,
            full_name="علی رضایی",
            gender=StudentExamProfile.Gender.MALE,
            exam_group=StudentExamProfile.ExamGroup.MATHEMATICS,
            exam_year=1405,
            province="تهران",
            city="تهران",
            quota=StudentExamProfile.Quota.REGION_1,
            selection_type=StudentExamProfile.SelectionType.PROVINCE,
        )

    def test_exam_profile_requires_login(self):
        response = self.client.get(
            reverse("exam:exam_profile")
        )

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_open_exam_profile(self):
        self.client.login(
            username="viewuser",
            password="TestPassword123",
        )

        response = self.client.get(
            reverse("exam:exam_profile")
        )

        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_create_exam_profile(self):
        self.client.login(
            username="otheruser",
            password="TestPassword123",
        )

        response = self.client.post(
            reverse("exam:exam_profile"),
            data={
                "full_name": "محمد احمدی",
                "gender": StudentExamProfile.Gender.MALE,
                "exam_group": StudentExamProfile.ExamGroup.MATHEMATICS,
                "exam_year": 1405,
                "province": "تهران",
                "city": "تهران",
                "quota": StudentExamProfile.Quota.REGION_1,
                "region": "منطقه ۱",
                "native_area": "تهران",
                "native_pole": "مرکز",
                "selection_type": StudentExamProfile.SelectionType.PROVINCE,
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            StudentExamProfile.objects.filter(
                user=self.other_user
            ).exists()
        )

    def test_user_cannot_access_other_users_profile(self):
        self.client.login(
            username="otheruser",
            password="TestPassword123",
        )

        response = self.client.get(
            reverse("exam:summary")
        )

        self.assertEqual(response.status_code, 404)

    def test_summary_requires_own_exam_profile(self):
        self.client.login(
            username="viewuser",
            password="TestPassword123",
        )

        response = self.client.get(
            reverse("exam:summary")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["exam_profile"],
            self.profile,
        )