import unittest
from datetime import datetime, timedelta

# Все импорты
from exceptions import *
from enums import UserRole, CourseStatus

from User import User
from UserRepository import UserRepository
from AuthenticationService import AuthenticationService
from Student import Student
from Teacher import Teacher
from Admin import Admin
from ContentCreator import ContentCreator

from Course import Course
from CourseManager import CourseManager
from CourseCatalog import CourseCatalog
from CourseBundle import CourseBundle
from LearningPath import LearningPath
from CourseSchedule import CourseSchedule

from LearningContent import LearningContent
from Lesson import Lesson
from Module import Module
from ContentManagementSystem import ContentManagementSystem
from ContentVersion import ContentVersion
from ResourceLibrary import ResourceLibrary
from LearningResource import LearningResource

from Assignment import Assignment
from AssignmentSubmission import AssignmentSubmission
from Quiz import Quiz
from QuizQuestion import QuizQuestion
from QuizAttempt import QuizAttempt
from Certificate import Certificate

from DiscussionForum import DiscussionForum
from ForumThread import ForumThread
from ForumPost import ForumPost
from StudyGroup import StudyGroup
from StudySession import StudySession
from Poll import Poll

from RatingSystem import RatingSystem
from ProgressTracker import ProgressTracker
from StudentPerformanceAnalytics import StudentPerformanceAnalytics
from InstructorDashboard import InstructorDashboard
from CourseRecommender import CourseRecommender

from AchievementSystem import AchievementSystem
from Achievement import Achievement
from UserAchievement import UserAchievement
from GamificationEngine import GamificationEngine

from NotificationService import NotificationService
from Notification import Notification
from CourseAnnouncement import CourseAnnouncement
from StudyReminder import StudyReminder

from TimeTracker import TimeTracker
from StudySessionRecord import StudySessionRecord
from LiveSession import LiveSession
from ChatMessage import ChatMessage
from CourseReview import CourseReview


class TestFinalCoverage(unittest.TestCase):
    """Финальная версия тестов с исправленными ошибками"""
    
    def setUp(self):
        self.student1 = Student("s1", "student1", "s1@test.com")
        self.student2 = Student("s2", "student2", "s2@test.com") 
        self.student3 = Student("s3", "student3", "s3@test.com")
        self.teacher = Teacher("t1", "teacher1", "t1@test.com")
        self.admin = Admin("a1", "admin1", "a1@test.com")
        self.creator = ContentCreator("c1", "creator1", "c1@test.com")

        self.course = Course("c1", "Python Programming", self.teacher, max_students=3)
        self.course.publish()

        self.course.add_student(self.student1)
        self.course.add_student(self.student2)
        
        self.student1._completed_courses.append(self.course)
        self.student2._completed_courses.append(self.course)

    def test_01_user_management_robust(self):
        """Надежное тестирование управления пользователями"""
        repo = UserRepository()

        repo.add_user(self.student1, "pass1")
        repo.add_user(self.teacher, "pass2")
        
        self.assertEqual(repo.get_total_users_count(), 2)

        self.assertEqual(repo.find_by_id("s1").username, "student1")
        self.assertEqual(repo.find_by_username("teacher1").user_id, "t1")

        self.assertTrue(repo.verify_credentials("student1", "pass1"))
        self.assertFalse(repo.verify_credentials("student1", "wrong"))

        auth = AuthenticationService(repo)
        user = auth.login("student1", "pass1")
        self.assertEqual(user.user_id, "s1")

        current_user = auth.get_current_user("s1")
        self.assertEqual(current_user.user_id, "s1")
 
        auth.logout("s1")
        self.assertIsNone(auth.get_current_user("s1"))

    def test_02_user_roles_and_profiles(self):
        """Тестирование ролей и профилей пользователей"""
        self.assertEqual(self.student1.get_role(), UserRole.STUDENT)
        profile = self.student1.get_profile_info()
        self.assertEqual(profile["username"], "student1")
        self.assertEqual(profile["role"], "student")

        self.assertEqual(self.student1.get_enrollment_count(), 0)
        self.assertEqual(self.student1.get_completion_count(), 1)
        
        self.teacher.add_specialization("Python")
        self.teacher.add_specialization("Data Science")
        specializations = self.teacher.get_specializations()
        self.assertEqual(len(specializations), 2)
        self.assertIn("Python", specializations)

        repo = UserRepository()
        temp_student = Student("temp", "temp", "temp@test.com")
        repo.add_user(temp_student, "temp")
        
        self.admin.suspend_user(repo, "temp")
        self.assertFalse(temp_student._is_active)
        
        self.admin.unsuspend_user(repo, "temp")
        self.assertTrue(temp_student._is_active)

        content = self.creator.create_learning_content({
            'content_id': 'test_cont',
            'title': 'Test Content'
        })
        self.assertEqual(self.creator.get_content_count(), 1)
        self.creator.set_specialization("Programming")
        self.assertEqual(self.creator._specialization, "Programming")

    def test_03_course_operations_complete(self):
        """Полное тестирование операций с курсами"""
        self.assertEqual(self.course.course_id, "c1")
        self.assertEqual(self.course.title, "Python Programming")
        self.assertEqual(self.course._status, CourseStatus.PUBLISHED)
        
        self.course.add_tag("programming")
        self.course.add_tag("python")
        self.course.add_tag("beginner")
        self.assertEqual(len(self.course._tags), 3)

        info = self.course.get_course_info()
        self.assertEqual(info["course_id"], "c1")
        self.assertEqual(info["title"], "Python Programming")
        self.assertEqual(info["status"], "published")
        self.assertEqual(info["students_count"], 2)

        self.course.archive()
        self.assertEqual(self.course._status, CourseStatus.ARCHIVED)
        
        self.course.publish()
        self.assertEqual(self.course._status, CourseStatus.PUBLISHED)

        self.course.remove_student(self.student2)
        self.assertEqual(self.course.get_enrollment_count(), 1)

        self.course.add_student(self.student2)

    def test_04_course_management_system(self):
        """Тестирование системы управления курсами"""
        manager = CourseManager()

        new_course = manager.create_course(self.teacher, {
            'course_id': 'new_course',
            'title': 'Advanced Python'
        })
        self.assertEqual(new_course.title, "Advanced Python")
        
        found_course = manager.get_course_by_id("new_course")
        self.assertEqual(found_course.course_id, "new_course")
  
        teacher_courses = manager.get_courses_by_instructor(self.teacher)
        self.assertGreaterEqual(len(teacher_courses), 1)
   
        manager.add_course_to_category(new_course, "Advanced")
        manager.add_course_to_category(new_course, "Programming")

        results = manager.search_courses("Advanced")
        self.assertGreaterEqual(len(results), 1)
        
        catalog = CourseCatalog()
        catalog.add_course(self.course)
        catalog.add_course(new_course)
        
        search_results = catalog.search_courses("Python")
        self.assertGreaterEqual(len(search_results), 1)
        
        catalog.add_course_to_category(self.course, "Programming")
        programming_courses = catalog.get_courses_by_category("Programming")
        self.assertGreaterEqual(len(programming_courses), 1)

    def test_05_course_bundles_and_paths(self):
        """Тестирование бандлов и путей обучения"""
        bundle = CourseBundle("b1", "Python Developer Bundle")
        bundle.add_course(self.course)
        
        second_course = Course("c2", "Python Advanced", self.teacher)
        bundle.add_course(second_course)
        
        self.assertEqual(bundle.get_course_count(), 2)
        
        bundle.set_price(180.0)
        savings = bundle.calculate_savings()
        self.assertEqual(savings, 20.0)
        
        # LearningPath
        path = LearningPath("p1", "Python Learning Path")
        path.add_course(self.course)
        path.add_course(second_course)
        path.set_description("Become a Python developer")
        
        self.assertEqual(path.calculate_progress(self.student1), 50.0)
 
        new_student = Student("new_s", "new_student", "new@test.com")
        result = path.enroll_student(new_student)
        self.assertTrue(result)

    def test_06_content_creation_full(self):
        """Полное тестирование создания контента"""
        content = LearningContent("cont1", "Python Tutorial", self.creator)
  
        content.add_rating(4.0)
        content.add_rating(5.0)
        content.add_rating(3.0)
        self.assertAlmostEqual(content.get_average_rating(), 4.0, places=1)
        
        with self.assertRaises(InvalidRatingException):
            content.add_rating(6.0)
  
        content.approve_content()
        self.assertTrue(content._is_approved)

        content.increment_download_count()
        content.increment_download_count()
        self.assertEqual(content._download_count, 2)

        popularity = content.get_popularity_score()
        expected_popularity = (2 * 0.6) + (3 * 0.4)
        self.assertAlmostEqual(popularity, expected_popularity, places=1)
 
        lesson = Lesson("l1", "Python Basics")
        lesson.set_duration(60)
        lesson.add_learning_objective("Understand Python syntax")
        lesson.add_learning_objective("Write first program")
        
        lesson.add_material(content)
        self.assertEqual(len(lesson._materials), 1)
 
        total_duration = lesson.calculate_total_duration()
        self.assertEqual(total_duration, 90)

        module = Module("m1", "Python Fundamentals")
        module.add_lesson(lesson)
        module.set_description("Learn Python basics")
        
        self.assertEqual(module.get_lesson_count(), 1)
        self.assertEqual(module.get_total_duration(), 90)

    def test_07_content_management_complete(self):
        """Полное тестирование управления контентом"""
        content = LearningContent("cms_cont", "CMS Test Content", self.creator)
        cms = ContentManagementSystem()

        version1 = cms.create_content_version(content, self.creator)
        self.assertEqual(len(cms.get_pending_approvals()), 1)

        version_info = version1.get_version_info()
        self.assertEqual(version_info["author"]["username"], "creator1")
        self.assertFalse(version_info["is_current"])

        version1.make_current()
        self.assertTrue(version1._is_current)

        cms.approve_content(content)
        self.assertEqual(len(cms.get_pending_approvals()), 0)
        self.assertTrue(content._is_approved)

        version2 = cms.create_content_version(content, self.creator)
        self.assertEqual(len(cms.get_pending_approvals()), 1)

    def test_08_resource_management_system(self):
        """Тестирование системы управления ресурсами"""
        resource1 = LearningResource("Python Cheat Sheet", "PDF")
        resource1.set_description("Quick reference for Python syntax")
        resource1.set_uploader(self.teacher)
        resource1.increment_download_count()
        
        resource2 = LearningResource("Python Exercises", "ZIP")
        resource2.set_description("Practice exercises")
        resource2.set_uploader(self.teacher)

        resource_info = resource1.get_resource_info()
        self.assertEqual(resource_info["title"], "Python Cheat Sheet")
        self.assertEqual(resource_info["type"], "PDF")
        self.assertEqual(resource_info["uploader"], "teacher1")
        self.assertEqual(resource_info["downloads"], 1)

        library = ResourceLibrary()
        library.add_resource(resource1)
        library.add_resource(resource2)
        
        self.assertEqual(library.get_resource_count(), 2)

        results = library.search_resources("Python")
        self.assertEqual(len(results), 2)
        
        results = library.search_resources("Cheat")
        self.assertEqual(len(results), 1)
        
        results = library.search_resources("Nonexistent")
        self.assertEqual(len(results), 0)

        found_resource = library.get_resource_by_title("Python Cheat Sheet")
        self.assertEqual(found_resource._title, "Python Cheat Sheet")
        
        with self.assertRaises(ContentNotFoundException):
            library.get_resource_by_title("Nonexistent Resource")

    def test_09_assessment_system_robust(self):
        """Надежное тестирование системы оценки"""
        assignment = Assignment("a1", "Python Fundamentals Assignment")

        future_due = datetime.now() + timedelta(days=7)
        assignment.set_due_date(future_due)
        self.assertFalse(assignment.is_overdue())
        
        # Сдача задания
        submission = assignment.submit_assignment(self.student1, "print('Hello World')")
        self.assertEqual(assignment.get_submission_count(), 1)
        

        self.assertFalse(submission.is_late())
        self.assertIsNone(submission.get_grade())
        self.assertFalse(submission._is_graded)
 
        assignment.grade_submission("s1", 88.5)
        self.assertEqual(submission.get_grade(), 88.5)
        self.assertTrue(submission._is_graded)

        submission2 = assignment.submit_assignment(self.student2, "print('Hi')")
        assignment.grade_submission("s2", 92.0)
        
        self.assertEqual(assignment.get_submission_count(), 2)

        past_due = datetime.now() - timedelta(hours=1)
        late_assignment = Assignment("a2", "Late Assignment")
        late_assignment.set_due_date(past_due)
        
        with self.assertRaises(AssignmentDeadlinePassedException):
            late_assignment.submit_assignment(self.student1, "Late submission")

    def test_10_quiz_system_comprehensive(self):
        """Комплексное тестирование системы тестов"""
        quiz = Quiz("q1", "Python Knowledge Test")

        quiz.set_time_limit(45)
        self.assertEqual(quiz._time_limit_minutes, 45)
        
        question1 = QuizQuestion("What is Python primarily used for?", "Programming")
        question1.add_option("Cooking")
        question1.add_option("Programming")
        question1.add_option("Drawing")
        question1.set_points(2.0)
        
        question2 = QuizQuestion("What does 'print' do in Python?", "Outputs text")
        question2.add_option("Inputs text")
        question2.add_option("Outputs text")
        question2.add_option("Deletes text")
        question2.set_points(1.0)
        
        quiz.add_question(question1)
        quiz.add_question(question2)
        
        self.assertEqual(quiz.get_question_count(), 2)
        self.assertEqual(quiz.get_total_points(), 3.0)

        self.assertTrue(question1.validate_answer("Programming"))
        self.assertFalse(question1.validate_answer("Cooking"))
        
        self.assertTrue(question2.validate_answer("Outputs text"))
        self.assertFalse(question2.validate_answer("Inputs text"))

        for attempt_num in range(3):
            attempt = QuizAttempt(self.student1, quiz)
            attempt.submit_answer("What is Python primarily used for?", "Programming")
            attempt.submit_answer("What does 'print' do in Python?", "Outputs text")
            score = attempt.calculate_score()
            self.assertEqual(score, 100.0)
            self.assertEqual(attempt._score, 100.0)
 
        with self.assertRaises(QuizAttemptsExceededException):
            QuizAttempt(self.student1, quiz)
 
        quiz2 = Quiz("q2", "Simple Test")
        simple_question = QuizQuestion("2+2=?", "4")
        simple_question.set_points(1.0)
        quiz2.add_question(simple_question)
        
        attempt = QuizAttempt(self.student2, quiz2)
        attempt.submit_answer("2+2=?", "5")
        score = attempt.calculate_score()
        self.assertEqual(score, 0.0)

    def test_11_certificate_system_validation(self):
        """Тестирование системы сертификатов с валидацией"""
        certificate = Certificate(self.student1, self.course)
        certificate.set_grade(95.5)

        self.assertTrue(certificate.verify_certificate())

        cert_info = certificate.get_certificate_info()
        self.assertEqual(cert_info["student"]["username"], "student1")
        self.assertEqual(cert_info["course"]["title"], "Python Programming")
        self.assertEqual(cert_info["grade"], 95.5)
        self.assertIn("issue_date", cert_info)
 
        cert_no_grade = Certificate(self.student2, self.course)
        self.assertFalse(cert_no_grade.verify_certificate())

    def test_12_social_features_engagement(self):
        """Тестирование социальных функций и вовлечения"""
        forum = DiscussionForum(self.course)

        thread1 = forum.create_thread(self.student1, "Need help with functions")
        self.assertEqual(forum.get_thread_count(), 1)

        thread2 = forum.create_thread(self.teacher, "Important announcement")
        self.assertEqual(forum.get_thread_count(), 2)

        help_threads = forum.search_threads("help")
        self.assertEqual(len(help_threads), 1)
        
        announcement_threads = forum.search_threads("announcement")
        self.assertEqual(len(announcement_threads), 1)
        
        thread1.increment_view_count()
        thread1.increment_view_count()
        self.assertEqual(thread1._view_count, 2)

        post1 = thread1.add_post(self.student1, "I'm stuck on lambda functions")
        post2 = thread1.add_post(self.teacher, "Lambda functions are anonymous functions...")
        post3 = thread1.add_post(self.student2, "Thanks for the explanation!")
        
        self.assertEqual(thread1.get_post_count(), 3)

        post1.like(self.student2)
        post1.like(self.teacher)
        self.assertEqual(post1.get_like_count(), 2)
        
        post1.unlike(self.student2)
        self.assertEqual(post1.get_like_count(), 1)

        thread1.lock_thread()
        locked_post = thread1.add_post(self.student1, "Can I still post?")
        self.assertIsNone(locked_post)
        
        thread1.unlock_thread()
        unlocked_post = thread1.add_post(self.student1, "Now I can post!")
        self.assertIsNotNone(unlocked_post)

    def test_13_study_groups_collaboration(self):
        """Тестирование учебных групп и коллаборации"""
        study_group = StudyGroup("g1", "Python Study Group", self.course)

        self.assertTrue(study_group.add_member(self.student1))
        self.assertTrue(study_group.add_member(self.student2))
        
        self.assertEqual(study_group.get_member_count(), 2)
        self.assertFalse(study_group.is_full())

        with self.assertRaises(DuplicateEnrollmentException):
            study_group.add_member(self.student1)
 
        outsider = Student("outsider", "outsider", "out@test.com")
        with self.assertRaises(CourseNotFoundException):
            study_group.add_member(outsider)

        self.assertTrue(study_group.remove_member(self.student1))
        self.assertEqual(study_group.get_member_count(), 1)

        study_group.add_member(self.student1)

        session = StudySession(study_group, "Weekly Python Practice")

        session.mark_attendance(self.student1)
        session.mark_attendance(self.student2)
        
        self.assertEqual(session.get_attendance_count(), 2)
        self.assertEqual(session.get_attendance_rate(), 100.0)

        partial_session = StudySession(study_group, "Extra Session")
        partial_session.mark_attendance(self.student1)
        
        self.assertEqual(partial_session.get_attendance_count(), 1)
        self.assertEqual(partial_session.get_attendance_rate(), 50.0)

    def test_14_poll_system_interaction(self):
        """Тестирование системы опросов и взаимодействия"""
        poll = Poll("What's your favorite Python framework?")
        poll.add_option("Django")
        poll.add_option("Flask")
        poll.add_option("FastAPI")
        poll.add_option("Other")
 
        self.assertTrue(poll.vote("Django"))
        self.assertTrue(poll.vote("Flask"))
        self.assertTrue(poll.vote("FastAPI"))
        self.assertTrue(poll.vote("Django"))

        results = poll.get_results()
        self.assertEqual(results["Django"], 2)
        self.assertEqual(results["Flask"], 1)
        self.assertEqual(results["FastAPI"], 1)
        self.assertEqual(results["Other"], 0)

        winner = poll.get_winner()
        self.assertEqual(winner, "Django")

        poll._is_active = False
        with self.assertRaises(InsufficientPermissionsException):
            poll.vote("Flask")

        poll._is_active = True
        with self.assertRaises(ContentNotFoundException):
            poll.vote("Nonexistent")

    def test_15_analytics_and_insights(self):
        """Тестирование аналитики и инсайтов"""
        self.student1._enrolled_courses.append(self.course)

        rating_system = RatingSystem()
        
        rating_system.rate_course(self.course, 4.5)
        rating_system.rate_course(self.course, 5.0)
        rating_system.rate_course(self.course, 4.0)
        
        course_rating = rating_system.get_course_rating(self.course)
        self.assertAlmostEqual(course_rating, 4.5, places=1)

        rating_system.rate_instructor(self.teacher, 5.0)
        rating_system.rate_instructor(self.teacher, 4.5)
        
        instructor_rating = rating_system.get_instructor_rating(self.teacher)
        self.assertAlmostEqual(instructor_rating, 4.75, places=2)
 
        with self.assertRaises(InvalidRatingException):
            rating_system.rate_course(self.course, 6.0)

        progress = ProgressTracker(self.student1, self.course)
        
        lesson1 = Lesson("l1", "Lesson 1")
        lesson2 = Lesson("l2", "Lesson 2")
        lesson3 = Lesson("l3", "Lesson 3")
        
        progress.mark_lesson_completed(lesson1)
        progress.mark_lesson_completed(lesson2)
        progress.add_study_time(120)  # 2 часа
        
        self.assertEqual(progress.get_completion_percentage(5), 40.0)  # 2 из 5 уроков
        self.assertEqual(progress.get_time_spent(), 120)

        analytics = StudentPerformanceAnalytics(self.student1)
        performance = analytics.analyze_course_performance(self.course)
        
        self.assertIn("assignments_avg", performance)
        self.assertIn("quizzes_avg", performance)
        self.assertIn("overall_score", performance)
        
        predicted_grade = analytics.predict_final_grade(self.course)
        self.assertGreater(predicted_grade, 0)
 
        dashboard = InstructorDashboard(self.teacher)
        dashboard.update_course_metrics(self.course)
        
        insights = dashboard.get_teaching_insights()
        self.assertIn("total_students", insights)
        self.assertIn("most_popular_course", insights)

        catalog = CourseCatalog()
        catalog.add_course(self.course)
        
        second_course = Course("c2", "Data Science", self.teacher)
        second_course.publish()
        catalog.add_course(second_course)
        
        recommender = CourseRecommender(catalog)
        recommendations = recommender.recommend_courses()
        self.assertLessEqual(len(recommendations), 3)
        
        confidence = recommender.calculate_recommendation_confidence(self.course)
        self.assertGreater(confidence, 0)

    def test_16_gamification_engagement(self):
        """Тестирование геймификации и вовлечения"""
        achievement_system = AchievementSystem()
        gamification = GamificationEngine()
  
        achievement1 = achievement_system.create_achievement("First Steps")
        achievement1.set_description("Complete your first lesson")
        achievement1.set_points(50)
        
        achievement2 = achievement_system.create_achievement("Quick Learner")
        achievement2.set_description("Complete 5 lessons quickly")
        achievement2.set_points(100)
        
        achievement3 = achievement_system.create_achievement("Course Master")
        achievement3.set_description("Complete a full course")
        achievement3.set_points(200)
        

        achievement_info = achievement1.get_achievement_info()
        self.assertEqual(achievement_info["name"], "First Steps")
        self.assertEqual(achievement_info["description"], "Complete your first lesson")
        self.assertEqual(achievement_info["points"], 50)
        
        user_achievement1 = achievement_system.award_achievement(self.student1, achievement1)
        user_achievement2 = achievement_system.award_achievement(self.student1, achievement2)
        
        user_achievements = achievement_system.get_user_achievements(self.student1)
        self.assertEqual(len(user_achievements), 2)
        
        days_since = user_achievement1.get_days_since_awarded()
        self.assertGreaterEqual(days_since, 0)

        with self.assertRaises(AchievementAlreadyAwardedException):
            achievement_system.award_achievement(self.student1, achievement1)

        points1 = gamification.award_points(self.student1, "complete_lesson")
        points2 = gamification.award_points(self.student1, "complete_assignment")
        points3 = gamification.award_points(self.student1, "complete_lesson")
        
        self.assertEqual(points1, 10)
        self.assertEqual(points2, 25)
        self.assertEqual(points3, 10)
        
        total_points = gamification.get_student_points(self.student1)
        self.assertEqual(total_points, 45)
        
        level1 = gamification.calculate_student_level(self.student1)
        self.assertEqual(level1, 1) 
 
        gamification.award_points(self.student1, "complete_assignment")
        gamification.award_points(self.student1, "complete_assignment")
        gamification.award_points(self.student1, "complete_lesson")
        
        total_points = gamification.get_student_points(self.student1)
        self.assertEqual(total_points, 105)
        
        level2 = gamification.calculate_student_level(self.student1)
        self.assertEqual(level2, 2)

    def test_17_notification_management(self):
        """Тестирование управления уведомлениями"""
        notification_service = NotificationService()
     
        test_student = Student("test_notif_student", "Test Student", "test_notif@test.com")
        test_teacher = Teacher("test_notif_teacher", "Test Teacher", "test_notif_teacher@test.com")
        test_course = Course("test_notif_course", "Test Notification Course", test_teacher)
 
        test_course.publish()
        test_course.add_student(test_student)
 
        if not hasattr(test_student, '_enrolled_courses'):
            test_student._enrolled_courses = []

        if test_course not in test_student._enrolled_courses:
            test_student._enrolled_courses.append(test_course)
    
        notifications = []
        for i in range(3):
            notification = notification_service.send_notification(
                test_student, f"Student notification {i+1}"
            )
            notifications.append(notification)
        
        for i in range(2):
            notification = notification_service.send_notification(
                test_teacher, f"Teacher notification {i+1}"
            )
        
        student_notifications = notification_service.get_user_notifications(test_student)
        teacher_notifications = notification_service.get_user_notifications(test_teacher)
        
        self.assertEqual(len(student_notifications), 3)
        self.assertEqual(len(teacher_notifications), 2)

        if student_notifications:
            first_notification = student_notifications[0]
            self.assertFalse(first_notification._is_read)
            
            first_notification.mark_as_read()
            self.assertTrue(first_notification._is_read)
            
            first_notification.mark_as_unread()
            self.assertFalse(first_notification._is_read)

        notification_service.mark_all_as_read(test_student)
        for notification in student_notifications:
            self.assertTrue(notification._is_read)

        announcement = CourseAnnouncement("ann1", test_course, test_teacher, "Important Update", "Course schedule changed")
        
        announcement.increment_view_count()
        announcement.increment_view_count()
        self.assertEqual(announcement._view_count, 2)
        
        announcement.pin_announcement()
        self.assertTrue(announcement._is_pinned)
        
        announcement.unpin_announcement()
        self.assertFalse(announcement._is_pinned)
 
        announcement_info = announcement.get_announcement_info()
        self.assertEqual(announcement_info["title"], "Important Update")
        self.assertEqual(announcement_info["author"], "Test Teacher") 
        self.assertEqual(announcement_info["course"], "Test Notification Course")
        self.assertFalse(announcement_info["is_pinned"])
  
        self.assertTrue(announcement.is_recent())
        self.assertTrue(announcement.is_recent(48))

        future_time = datetime.now() + timedelta(hours=2)
        reminder = StudyReminder("rem1", test_student, "Study for exam", future_time)
      
        reminder.set_course(test_course)
        self.assertEqual(reminder._course, test_course)
        
        self.assertFalse(reminder.is_due())
        self.assertFalse(reminder._is_completed)
        
        reminder.mark_completed()
        self.assertTrue(reminder._is_completed)
        
        reminder.mark_incomplete()
        self.assertFalse(reminder._is_completed)
        
        reminder_info = reminder.get_reminder_info()
        self.assertEqual(reminder_info["title"], "Study for exam")
        self.assertEqual(reminder_info["course"], "Test Notification Course")
        self.assertFalse(reminder_info["is_completed"])
        self.assertFalse(reminder_info["is_due"])
        
        new_time = datetime.now() + timedelta(days=1)
        reminder.reschedule(new_time)
        self.assertEqual(reminder._reminder_time, new_time)

 
    def test_18_utility_classes_functionality(self):
        """Тестирование функциональности утилитных классов"""
        self.student1._enrolled_courses.append(self.course)
        
        tracker = TimeTracker(self.student1)
        tracker.start_study_session(self.course)
        
        tracker.set_daily_goal(120)
        today_goal = tracker._daily_goals.get(datetime.now().strftime("%Y-%m-%d"))
        self.assertEqual(today_goal, 120)
     
        record = StudySessionRecord(self.course)
        self.assertIsNone(record._end_time)
  
        initial_duration = record.get_duration_minutes()
        self.assertGreaterEqual(initial_duration, 0)
        
        record.end_session()
        self.assertIsNotNone(record._end_time)
        
        final_duration = record.get_duration_minutes()
        self.assertGreaterEqual(final_duration, 0)
        
        session = LiveSession("live1", "Python Workshop", self.teacher)
        
        self.assertFalse(session.is_ongoing())
        session.start_session()
        self.assertTrue(session.is_ongoing())
        
        session.join_session(self.student1)
        session.join_session(self.student2)
        self.assertEqual(session.get_participant_count(), 2)
        
        session.end_session()
        self.assertFalse(session.is_ongoing())

        message = ChatMessage(self.student1, "Hello, can anyone help with this?")
        message_info = message.get_message_info()
        
        self.assertEqual(message_info["author"], "student1")
        self.assertEqual(message_info["content"], "Hello, can anyone help with this?")
        self.assertIn("timestamp", message_info)

        review = CourseReview("rev1", self.course, self.student1, 4.5, "Great course overall!")
        
        self.assertTrue(review.is_positive())
        self.assertTrue(review.is_recent())
        self.assertFalse(review._is_verified)
        self.assertEqual(review._helpful_count, 0)
    
        review.verify_review()
        self.assertTrue(review._is_verified)
        
        review.mark_helpful()
        review.mark_helpful()
        self.assertEqual(review._helpful_count, 2)
    
        review.update_rating(5.0)
        review.update_comment("Excellent course! Highly recommended.")
        
        self.assertEqual(review._rating, 5.0)
        self.assertEqual(review._comment, "Excellent course! Highly recommended.")
   
        with self.assertRaises(InvalidRatingException):
            review.update_rating(6.0)

        review_info = review.get_review_info()
        self.assertEqual(review_info["rating"], 5.0)
        self.assertEqual(review_info["comment"], "Excellent course! Highly recommended.")
        self.assertTrue(review_info["is_verified"])
        self.assertEqual(review_info["helpful_count"], 2)

    def test_19_course_scheduling_system(self):
        """Тестирование системы расписания курсов"""
        schedule = CourseSchedule(self.course)

        lesson1 = Lesson("l1", "Python Introduction")
        lesson2 = Lesson("l2", "Data Types")
        lesson3 = Lesson("l3", "Functions")

        assignment1 = Assignment("a1", "First Program")
        assignment2 = Assignment("a2", "Function Practice")

        lesson1_time = datetime.now() + timedelta(days=1, hours=10)
        lesson2_time = datetime.now() + timedelta(days=3, hours=14)
        lesson3_time = datetime.now() + timedelta(days=5, hours=16) 
        
        schedule.schedule_lesson(lesson1, lesson1_time)
        schedule.schedule_lesson(lesson2, lesson2_time)
        schedule.schedule_lesson(lesson3, lesson3_time)
        
        assignment1_deadline = datetime.now() + timedelta(days=2, hours=23, minutes=59)
        assignment2_deadline = datetime.now() + timedelta(days=6, hours=23, minutes=59)
        
        schedule.add_assignment_deadline(assignment1, assignment1_deadline)
        schedule.add_assignment_deadline(assignment2, assignment2_deadline)
        
        upcoming_week = schedule.get_upcoming_events(days=7)
        self.assertEqual(len(upcoming_week), 5)
        
        upcoming_today = schedule.get_upcoming_events(days=0)
        self.assertEqual(len(upcoming_today), 0)
        
        events = schedule.get_upcoming_events(days=7)
        self.assertEqual(len(events), 5)
        
        for i in range(len(events) - 1):
            current_time = events[i]['time'] if 'time' in events[i] else events[i]['deadline']
            next_time = events[i+1]['time'] if 'time' in events[i+1] else events[i+1]['deadline']
            self.assertLessEqual(current_time, next_time)

    def test_20_complete_integration_scenario(self):
        """Полный интеграционный сценарий обучения"""
        integration_student = Student("int_s1", "integration_student", "int@test.com")
        integration_teacher = Teacher("int_t1", "integration_teacher", "teacher@test.com")
        integration_creator = ContentCreator("int_c1", "integration_creator", "creator@test.com")
        
        repo = UserRepository()
        repo.add_user(integration_student, "student123")
        repo.add_user(integration_teacher, "teacher123")
        repo.add_user(integration_creator, "creator123")
        
        auth = AuthenticationService(repo)
        auth.login("integration_student", "student123")
 
        course_manager = CourseManager()
        integration_course = course_manager.create_course(integration_teacher, {
            'course_id': 'int_course',
            'title': 'Integration Test Course'
        })
        integration_course.publish()

        integration_student.enroll_in_course(integration_course)

        integration_content = integration_creator.create_learning_content({
            'content_id': 'int_content',
            'title': 'Integration Test Content'
        })

        cms = ContentManagementSystem()
        cms.create_content_version(integration_content, integration_creator)
        cms.approve_content(integration_content)

        integration_lesson = Lesson("int_lesson", "Integration Test Lesson")
        integration_lesson.add_material(integration_content)
        integration_lesson.set_duration(45)
        integration_lesson.add_learning_objective("Understand integration testing")
        
        integration_module = Module("int_module", "Integration Module")
        integration_module.add_lesson(integration_lesson)

        integration_progress = ProgressTracker(integration_student, integration_course)
        integration_progress.mark_lesson_completed(integration_lesson)
        integration_progress.add_study_time(60)
        
        integration_assignment = Assignment("int_assign", "Integration Assignment")
        integration_assignment.set_due_date(datetime.now() + timedelta(days=7))
        integration_submission = integration_assignment.submit_assignment(integration_student, "Integration test solution")
        integration_assignment.grade_submission("int_s1", 92.0)

        integration_quiz = Quiz("int_quiz", "Integration Quiz")
        integration_question = QuizQuestion("What is integration testing?", "Testing components together")
        integration_question.add_option("Unit testing")
        integration_question.add_option("Integration testing")
        integration_question.add_option("System testing")
        integration_question.set_points(2.0)
        
        integration_quiz.add_question(integration_question)
        integration_attempt = QuizAttempt(integration_student, integration_quiz)
        integration_attempt.submit_answer("What is integration testing?", "Integration testing")
        integration_score = integration_attempt.calculate_score()

        integration_forum = DiscussionForum(integration_course)
        integration_thread = integration_forum.create_thread(integration_student, "Integration question")
        integration_post = integration_thread.add_post(integration_teacher, "Integration answer")
        
        integration_study_group = StudyGroup("int_group", "Integration Study Group", integration_course)
        integration_study_group.add_member(integration_student)

        integration_student.complete_course(integration_course)

        integration_certificate = Certificate(integration_student, integration_course)
        integration_certificate.set_grade(94.5)

        integration_achievement_system = AchievementSystem()
        integration_achievement = integration_achievement_system.create_achievement("Integration Master")
        integration_achievement_system.award_achievement(integration_student, integration_achievement)
        
        integration_gamification = GamificationEngine()
        integration_gamification.award_points(integration_student, "complete_lesson")
        integration_gamification.award_points(integration_student, "complete_assignment")
        integration_gamification.award_points(integration_student, "complete_course")

        integration_review = CourseReview("int_review", integration_course, integration_student, 5.0, "Excellent integration test course!")

        self.assertEqual(integration_student.get_completion_count(), 1)
        self.assertTrue(integration_certificate.verify_certificate())
        self.assertEqual(integration_progress.get_completion_percentage(1), 100.0)
        self.assertEqual(integration_submission.get_grade(), 92.0)
        self.assertGreaterEqual(integration_score, 0.0)
        self.assertLessEqual(integration_score, 100.0)
        self.assertEqual(integration_gamification.get_student_points(integration_student), 35)
        self.assertTrue(integration_review.is_positive())
        self.assertEqual(len(integration_achievement_system.get_user_achievements(integration_student)), 1)
        self.assertEqual(integration_forum.get_thread_count(), 1)
        self.assertEqual(integration_study_group.get_member_count(), 1)

    def test_21_error_handling_comprehensive(self):
        """Комплексное тестирование обработки ошибок для существующих компонентов"""
        repo = UserRepository()
        with self.assertRaises(UserNotFoundException):
            repo.find_by_id("nonexistent_user")
        
        with self.assertRaises(UserNotFoundException):
            repo.find_by_username("nonexistent_user")

        repo.add_user(self.student1, "password")
        auth = AuthenticationService(repo)
        with self.assertRaises(InvalidCredentialsException):
            auth.login("student1", "wrong_password")

        manager = CourseManager()
        with self.assertRaises(CourseNotFoundException):
            manager.get_course_by_id("nonexistent_course")
 
        draft_course = Course("draft", "Draft Course", self.teacher)
        with self.assertRaises(CourseNotPublishedException):
            draft_course.add_student(self.student1)

        small_course = Course("small", "Small Course", self.teacher, max_students=1)
        small_course.publish()
        small_course.add_student(self.student1)
        
        with self.assertRaises(CourseFullException):
            small_course.add_student(self.student2)
            
        duplicate_course = Course("duplicate", "Duplicate Course", self.teacher, max_students=2)
        duplicate_course.publish()
        duplicate_course.add_student(self.student1)
 
        with self.assertRaises(DuplicateEnrollmentException):
            duplicate_course.add_student(self.student1)

        unapproved_content = LearningContent("unapproved", "Unapproved", self.creator)
        with self.assertRaises(ContentNotApprovedException):
            unapproved_content.increment_download_count()
        
        with self.assertRaises(InvalidRatingException):
            unapproved_content.add_rating(6.0)
        
        with self.assertRaises(InvalidRatingException):
            unapproved_content.add_rating(0.5)
        
        from datetime import timedelta
        expired_assignment = Assignment("expired", "Expired")
        past_due = datetime.now() - timedelta(minutes=1)
        expired_assignment.set_due_date(past_due)
        
        with self.assertRaises(AssignmentDeadlinePassedException):
            expired_assignment.submit_assignment(self.student1, "Too late")
  
        simple_quiz = Quiz("simple", "Simple")
        question = QuizQuestion("Q?", "A")
        simple_quiz.add_question(question)
        
        for _ in range(3):
            QuizAttempt(self.student1, simple_quiz)
        
        with self.assertRaises(QuizAttemptsExceededException):
            QuizAttempt(self.student1, simple_quiz)


if __name__ == '__main__':

    unittest.main(verbosity=2, failfast=False)
