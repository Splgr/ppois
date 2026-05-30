from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Set
from enum import Enum

class StudyGroupFullException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class CourseFullException(Exception):
    pass

class DuplicateEnrollmentException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class CourseNotFoundException(Exception):
    pass

class ContentNotApprovedException(Exception):
    pass

class InsufficientPermissionsException(Exception):
    pass

class AssignmentDeadlinePassedException(Exception):
    pass

class QuizAttemptsExceededException(Exception):
    pass

class InvalidRatingException(Exception):
    pass

class StudyGroupNotFoundException(Exception):
    pass

class ContentNotFoundException(Exception):
    pass

class AchievementAlreadyAwardedException(Exception):
    pass

class CourseNotPublishedException(Exception):
    pass

class PaymentRequiredException(Exception):
    pass

class UserRole(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    CONTENT_CREATOR = "content_creator"

class CourseStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class User(ABC):
    def __init__(self, user_id: str, username: str, email: str):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._registration_date = datetime.now()
        self._is_active = True
        
    @abstractmethod
    def get_role(self) -> UserRole:
        pass
    
    def get_profile_info(self) -> dict:
        return {
            "user_id": self._user_id,
            "username": self._username,
            "email": self._email,
            "role": self.get_role().value
        }
    
    def deactivate_account(self) -> None:
        self._is_active = False
    
    def reactivate_account(self) -> None:
        self._is_active = True
    
    @property
    def user_id(self) -> str:
        return self._user_id

class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._user_credentials: Dict[str, str] = {}
    
    def add_user(self, user: User, password: str) -> None:
        self._users[user.user_id] = user
        self._user_credentials[user.username] = password
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        user = self._users.get(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return user
    
    def find_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        raise UserNotFoundException(f"User with username {username} not found")
    
    def verify_credentials(self, username: str, password: str) -> bool:
        stored_password = self._user_credentials.get(username)
        return stored_password == password
    
    def get_total_users_count(self) -> int:
        return len(self._users)

class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self._active_sessions: Dict[str, User] = {}
    
    def login(self, username: str, password: str) -> User:
        if not self._user_repository.verify_credentials(username, password):
            raise InvalidCredentialsException("Invalid credentials")
        
        user = self._user_repository.find_by_username(username)
        self._active_sessions[user.user_id] = user
        return user
    
    def logout(self, user_id: str) -> None:
        if user_id in self._active_sessions:
            del self._active_sessions[user_id]
    
    def get_current_user(self, user_id: str) -> Optional[User]:
        return self._active_sessions.get(user_id)

class Student(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
        self._enrolled_courses: List['Course'] = []
        self._completed_courses: List['Course'] = []
        self._favorite_courses: Set[str] = set()
    
    def get_role(self) -> UserRole:
        return UserRole.STUDENT
    
    def enroll_in_course(self, course: 'Course') -> None:
        if course._status != CourseStatus.PUBLISHED:
            raise CourseNotPublishedException("Cannot enroll in unpublished course")
        
        if course in self._enrolled_courses:
            raise DuplicateEnrollmentException("Already enrolled in this course")
        
        course.add_student(self)
        self._enrolled_courses.append(course)
    
    def complete_course(self, course: 'Course') -> None:
        if course not in self._enrolled_courses:
            raise CourseNotFoundException("Course not found in enrolled courses")
        
        self._enrolled_courses.remove(course)
        self._completed_courses.append(course)
    
    def add_to_favorites(self, course: 'Course') -> None:
        if course not in self._enrolled_courses:
            raise CourseNotFoundException("Cannot favorite a course you're not enrolled in")
        self._favorite_courses.add(course.course_id)
    
    def remove_from_favorites(self, course: 'Course') -> None:
        self._favorite_courses.discard(course.course_id)
    
    def get_enrollment_count(self) -> int:
        return len(self._enrolled_courses)
    
    def get_completion_count(self) -> int:
        return len(self._completed_courses)

class Teacher(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
        self._taught_courses: List['Course'] = []
        self._specializations: List[str] = []
    
    def get_role(self) -> UserRole:
        return UserRole.TEACHER
    
    def create_course(self, course_manager: 'CourseManager', course_data: dict) -> 'Course':
        course = course_manager.create_course(self, course_data)
        self._taught_courses.append(course)
        return course
    
    def add_specialization(self, specialization: str) -> None:
        if specialization not in self._specializations:
            self._specializations.append(specialization)
    
    def get_specializations(self) -> List[str]:
        return self._specializations.copy()
    
    def get_total_students_taught(self) -> int:
        return sum(len(course._current_students) for course in self._taught_courses)

class Admin(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
    
    def get_role(self) -> UserRole:
        return UserRole.ADMIN
    
    def suspend_user(self, user_repository: UserRepository, user_id: str) -> None:
        user = user_repository.find_by_id(user_id)
        user.deactivate_account()
    
    def unsuspend_user(self, user_repository: UserRepository, user_id: str) -> None:
        user = user_repository.find_by_id(user_id)
        user.reactivate_account()

class Course:
    def __init__(self, course_id: str, title: str, instructor: Teacher, max_students: int = 100):
        self._course_id = course_id
        self._title = title
        self._instructor = instructor
        self._current_students: List[Student] = []
        self._status = CourseStatus.DRAFT
        self._tags: List[str] = []
        self._difficulty_level: str = "beginner"
        self._max_students = max_students
    
    def add_student(self, student: Student) -> None:
        if len(self._current_students) >= self._max_students:
            raise CourseFullException("Course is full")
        
        if student in self._current_students:
            raise DuplicateEnrollmentException("Student already enrolled")
        
        if self._status != CourseStatus.PUBLISHED:
            raise CourseNotPublishedException("Cannot enroll in unpublished course")
        
        self._current_students.append(student)
    
    def remove_student(self, student: Student) -> None:
        if student in self._current_students:
            self._current_students.remove(student)
    
    def publish(self) -> None:
        self._status = CourseStatus.PUBLISHED
    
    def archive(self) -> None:
        self._status = CourseStatus.ARCHIVED
    
    def add_tag(self, tag: str) -> None:
        if tag not in self._tags:
            self._tags.append(tag)
    
    def get_enrollment_count(self) -> int:
        return len(self._current_students)
    
    def get_course_info(self) -> dict:
        return {
            "course_id": self._course_id,
            "title": self._title,
            "instructor": self._instructor.get_profile_info(),
            "students_count": len(self._current_students),
            "status": self._status.value
        }
    
    @property
    def course_id(self) -> str:
        return self._course_id
    
    @property
    def title(self) -> str:
        return self._title

class CourseManager:
    def __init__(self):
        self._courses: List[Course] = []
        self._course_categories: Dict[str, List[Course]] = {}
    
    def create_course(self, teacher: Teacher, course_data: dict) -> Course:
        course = Course(course_data['course_id'], course_data['title'], teacher)
        self._courses.append(course)
        return course
    
    def get_course_by_id(self, course_id: str) -> Course:
        for course in self._courses:
            if course.course_id == course_id:
                return course
        raise CourseNotFoundException(f"Course with ID {course_id} not found")
    
    def get_courses_by_instructor(self, instructor: Teacher) -> List[Course]:
        return [course for course in self._courses if course._instructor == instructor]
    
    def add_course_to_category(self, course: Course, category: str) -> None:
        if category not in self._course_categories:
            self._course_categories[category] = []
        if course not in self._course_categories[category]:
            self._course_categories[category].append(course)
    
    def search_courses(self, query: str) -> List[Course]:
        results = []
        for course in self._courses:
            if (query.lower() in course._title.lower() or 
                any(query.lower() in tag.lower() for tag in course._tags)):
                results.append(course)
        return results

class ContentCreator(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
        self._created_content: List['LearningContent'] = []
        self._specialization: str = ""
    
    def get_role(self) -> UserRole:
        return UserRole.CONTENT_CREATOR
    
    def create_learning_content(self, content_data: dict) -> 'LearningContent':
        content = LearningContent(content_data['content_id'], content_data['title'], self)
        self._created_content.append(content)
        return content
    
    def set_specialization(self, specialization: str) -> None:
        self._specialization = specialization
    
    def get_content_count(self) -> int:
        return len(self._created_content)

class LearningContent:
    def __init__(self, content_id: str, title: str, creator: ContentCreator):
        self._content_id = content_id
        self._title = title
        self._creator = creator
        self._creation_date = datetime.now()
        self._ratings: List[float] = []
        self._download_count: int = 0
        self._is_approved: bool = False
    
    def add_rating(self, rating: float) -> None:
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        self._ratings.append(rating)
    
    def get_average_rating(self) -> float:
        return sum(self._ratings) / len(self._ratings) if self._ratings else 0.0
    
    def increment_download_count(self) -> None:
        if not self._is_approved:
            raise ContentNotApprovedException("Cannot download unapproved content")
        self._download_count += 1
    
    def approve_content(self) -> None:
        self._is_approved = True
    
    def get_popularity_score(self) -> float:
        return (self._download_count * 0.6) + (len(self._ratings) * 0.4)

class Lesson:
    def __init__(self, lesson_id: str, title: str):
        self._lesson_id = lesson_id
        self._title = title
        self._materials: List[LearningContent] = []
        self._duration_minutes: int = 0
        self._learning_objectives: List[str] = []
    
    def add_material(self, material: LearningContent) -> None:
        if not material._is_approved:
            raise ContentNotApprovedException("Cannot add unapproved content to lesson")
        self._materials.append(material)
    
    def set_duration(self, minutes: int) -> None:
        self._duration_minutes = minutes
    
    def add_learning_objective(self, objective: str) -> None:
        self._learning_objectives.append(objective)
    
    def calculate_total_duration(self) -> int:
        material_duration = len(self._materials) * 30
        return self._duration_minutes + material_duration

class Module:
    def __init__(self, module_id: str, title: str):
        self._module_id = module_id
        self._title = title
        self._lessons: List[Lesson] = []
        self._description: str = ""
    
    def add_lesson(self, lesson: Lesson) -> None:
        self._lessons.append(lesson)
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def get_total_duration(self) -> int:
        return sum(lesson.calculate_total_duration() for lesson in self._lessons)
    
    def get_lesson_count(self) -> int:
        return len(self._lessons)

class Assignment:
    def __init__(self, assignment_id: str, title: str):
        self._assignment_id = assignment_id
        self._title = title
        self._submissions: Dict[str, 'AssignmentSubmission'] = {}
        self._max_score: float = 100.0
        self._due_date: Optional[datetime] = None
    
    def submit_assignment(self, student: Student, submission_data: str) -> 'AssignmentSubmission':
        if self._due_date and datetime.now() > self._due_date:
            raise AssignmentDeadlinePassedException("Assignment deadline has passed")
        
        submission = AssignmentSubmission(student, self, submission_data)
        self._submissions[student.user_id] = submission
        return submission
    
    def set_due_date(self, due_date: datetime) -> None:
        self._due_date = due_date
    
    def is_overdue(self) -> bool:
        return self._due_date and datetime.now() > self._due_date
    
    def get_submission_count(self) -> int:
        return len(self._submissions)
    
    def grade_submission(self, student_id: str, grade: float) -> bool:
        if student_id in self._submissions:
            self._submissions[student_id].grade(grade)
            return True
        return False

class AssignmentSubmission:
    def __init__(self, student: Student, assignment: Assignment, content: str):
        self._student = student
        self._assignment = assignment
        self._content = content
        self._submission_date = datetime.now()
        self._grade: Optional[float] = None
        self._is_graded: bool = False
    
    def grade(self, grade: float) -> None:
        if grade <= self._assignment._max_score:
            self._grade = grade
            self._is_graded = True
    
    def get_grade(self) -> Optional[float]:
        return self._grade
    
    def is_late(self) -> bool:
        return self._assignment._due_date and self._submission_date > self._assignment._due_date

class Quiz:
    def __init__(self, quiz_id: str, title: str):
        self._quiz_id = quiz_id
        self._title = title
        self._questions: List['QuizQuestion'] = []
        self._time_limit_minutes: int = 30
        self._max_attempts: int = 3
        self._attempts: Dict[str, int] = {}
    
    def add_question(self, question: 'QuizQuestion') -> None:
        self._questions.append(question)
    
    def set_time_limit(self, minutes: int) -> None:
        self._time_limit_minutes = minutes
    
    def get_question_count(self) -> int:
        return len(self._questions)
    
    def get_total_points(self) -> float:
        return sum(question._points for question in self._questions)
    
    def can_attempt(self, student: Student) -> bool:
        attempts = self._attempts.get(student.user_id, 0)
        return attempts < self._max_attempts
    
    def record_attempt(self, student: Student) -> None:
        attempts = self._attempts.get(student.user_id, 0)
        if attempts >= self._max_attempts:
            raise QuizAttemptsExceededException("Maximum quiz attempts exceeded")
        self._attempts[student.user_id] = attempts + 1

class QuizQuestion:
    def __init__(self, question_text: str, correct_answer: str):
        self._question_text = question_text
        self._correct_answer = correct_answer
        self._options: List[str] = []
        self._points: float = 1.0
    
    def add_option(self, option: str) -> None:
        self._options.append(option)
    
    def set_points(self, points: float) -> None:
        self._points = points
    
    def validate_answer(self, answer: str) -> bool:
        return answer == self._correct_answer

class QuizAttempt:
    def __init__(self, student: Student, quiz: Quiz):
        if not quiz.can_attempt(student):
            raise QuizAttemptsExceededException("Maximum quiz attempts exceeded")
        
        quiz.record_attempt(student)
        self._student = student
        self._quiz = quiz
        self._start_time = datetime.now()
        self._score: Optional[float] = None
        self._answers: Dict[str, str] = {}
    
    def submit_answer(self, question_id: str, answer: str) -> None:
        self._answers[question_id] = answer
    
    def calculate_score(self) -> float:
        total_points = 0
        earned_points = 0
        
        for question in self._quiz._questions:
            total_points += question._points
            student_answer = self._answers.get(question._question_text)
            if student_answer and question.validate_answer(student_answer):
                earned_points += question._points
        
        self._score = (earned_points / total_points * 100) if total_points > 0 else 0
        return self._score

class DiscussionForum:
    def __init__(self, course: Course):
        self._course = course
        self._threads: List['ForumThread'] = []
    
    def create_thread(self, author: User, title: str) -> 'ForumThread':
        if author not in self._course._current_students and author != self._course._instructor:
            raise InsufficientPermissionsException("Only enrolled students and instructors can create threads")
        
        thread = ForumThread(author, title)
        self._threads.append(thread)
        return thread
    
    def get_thread_count(self) -> int:
        return len(self._threads)
    
    def search_threads(self, query: str) -> List['ForumThread']:
        return [thread for thread in self._threads 
                if query.lower() in thread._title.lower()]

class ForumThread:
    def __init__(self, author: User, title: str):
        self._author = author
        self._title = title
        self._creation_date = datetime.now()
        self._posts: List['ForumPost'] = []
        self._is_locked: bool = False
        self._view_count: int = 0
    
    def add_post(self, author: User, content: str) -> 'ForumPost':
        if not self._is_locked:
            post = ForumPost(author, content)
            self._posts.append(post)
            return post
        return None
    
    def lock_thread(self) -> None:
        self._is_locked = True
    
    def unlock_thread(self) -> None:
        self._is_locked = False
    
    def increment_view_count(self) -> None:
        self._view_count += 1
    
    def get_post_count(self) -> int:
        return len(self._posts)

class ForumPost:
    def __init__(self, author: User, content: str):
        self._author = author
        self._content = content
        self._post_date = datetime.now()
        self._likes: Set[str] = set()
    
    def like(self, user: User) -> None:
        self._likes.add(user.user_id)
    
    def unlike(self, user: User) -> None:
        self._likes.discard(user.user_id)
    
    def get_like_count(self) -> int:
        return len(self._likes)

class Certificate:
    def __init__(self, student: Student, course: Course):
        if course not in student._completed_courses:
            raise InsufficientPermissionsException("Student must complete course to receive certificate")
        
        self._student = student
        self._course = course
        self._issue_date = datetime.now()
        self._grade: Optional[float] = None
    
    def set_grade(self, grade: float) -> None:
        self._grade = grade
    
    def verify_certificate(self) -> bool:
        return (self._student is not None and 
                self._course is not None and 
                self._grade is not None)
    
    def get_certificate_info(self) -> dict:
        return {
            "student": self._student.get_profile_info(),
            "course": self._course.get_course_info(),
            "issue_date": self._issue_date,
            "grade": self._grade
        }

class NotificationService:
    def __init__(self):
        self._notifications: List['Notification'] = []
    
    def send_notification(self, user: User, title: str) -> 'Notification':
        notification = Notification(user, title)
        self._notifications.append(notification)
        return notification
    
    def get_user_notifications(self, user: User) -> List['Notification']:
        return [n for n in self._notifications if n._user.user_id == user.user_id]
    
    def mark_all_as_read(self, user: User) -> None:
        for notification in self.get_user_notifications(user):
            notification.mark_as_read()

class Notification:
    def __init__(self, user: User, title: str):
        self._user = user
        self._title = title
        self._sent_date = datetime.now()
        self._is_read: bool = False
    
    def mark_as_read(self) -> None:
        self._is_read = True
    
    def mark_as_unread(self) -> None:
        self._is_read = False

class ProgressTracker:
    def __init__(self, student: Student, course: Course):
        if course not in student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        
        self._student = student
        self._course = course
        self._completed_lessons: Set[str] = set()
        self._time_spent_minutes: int = 0
    
    def mark_lesson_completed(self, lesson: Lesson) -> None:
        self._completed_lessons.add(lesson._lesson_id)
    
    def add_study_time(self, minutes: int) -> None:
        self._time_spent_minutes += minutes
    
    def get_completion_percentage(self, total_lessons: int) -> float:
        return (len(self._completed_lessons) / total_lessons * 100) if total_lessons > 0 else 0
    
    def get_time_spent(self) -> int:
        return self._time_spent_minutes

class CourseCatalog:
    def __init__(self):
        self._courses: List[Course] = []
        self._categories: Dict[str, List[Course]] = {}
    
    def add_course(self, course: Course) -> None:
        self._courses.append(course)
    
    def search_courses(self, query: str) -> List[Course]:
        results = []
        for course in self._courses:
            if query.lower() in course._title.lower():
                results.append(course)
        return results
    
    def add_course_to_category(self, course: Course, category: str) -> None:
        if category not in self._categories:
            self._categories[category] = []
        if course not in self._categories[category]:
            self._categories[category].append(course)
    
    def get_courses_by_category(self, category: str) -> List[Course]:
        return self._categories.get(category, [])

class RatingSystem:
    def __init__(self):
        self._course_ratings: Dict[str, List[float]] = {}
        self._instructor_ratings: Dict[str, List[float]] = {}
    
    def rate_course(self, course: Course, rating: float) -> None:
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        
        if course.course_id not in self._course_ratings:
            self._course_ratings[course.course_id] = []
        self._course_ratings[course.course_id].append(rating)
    
    def rate_instructor(self, instructor: Teacher, rating: float) -> None:
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        
        if instructor.user_id not in self._instructor_ratings:
            self._instructor_ratings[instructor.user_id] = []
        self._instructor_ratings[instructor.user_id].append(rating)
    
    def get_course_rating(self, course: Course) -> float:
        ratings = self._course_ratings.get(course.course_id, [])
        return sum(ratings) / len(ratings) if ratings else 0.0
    
    def get_instructor_rating(self, instructor: Teacher) -> float:
        ratings = self._instructor_ratings.get(instructor.user_id, [])
        return sum(ratings) / len(ratings) if ratings else 0.0

class LiveSession:
    def __init__(self, session_id: str, title: str, instructor: Teacher):
        self._session_id = session_id
        self._title = title
        self._instructor = instructor
        self._participants: List[Student] = []
        self._scheduled_time: datetime = datetime.now()
        self._is_active: bool = False
    
    def start_session(self) -> None:
        self._is_active = True
    
    def end_session(self) -> None:
        self._is_active = False
    
    def join_session(self, student: Student) -> None:
        if student not in self._participants:
            self._participants.append(student)
    
    def get_participant_count(self) -> int:
        return len(self._participants)
    
    def is_ongoing(self) -> bool:
        return self._is_active

class ChatMessage:
    def __init__(self, author: User, content: str):
        self._author = author
        self._content = content
        self._timestamp = datetime.now()
    
    def get_message_info(self) -> dict:
        return {
            "author": self._author.username,
            "content": self._content,
            "timestamp": self._timestamp
        }

class CourseBundle:
    def __init__(self, bundle_id: str, name: str):
        self._bundle_id = bundle_id
        self._name = name
        self._courses: List[Course] = []
        self._price: float = 0.0
    
    def add_course(self, course: Course) -> None:
        if course not in self._courses:
            self._courses.append(course)
    
    def set_price(self, price: float) -> None:
        self._price = price
    
    def calculate_savings(self) -> float:
        individual_price = sum(100 for _ in self._courses)
        return individual_price - self._price
    
    def get_course_count(self) -> int:
        return len(self._courses)
    
    def purchase_bundle(self, student: Student) -> None:
        if self._price > 0:
            raise PaymentRequiredException("Payment required to purchase this bundle")
        
        for course in self._courses:
            student.enroll_in_course(course)

class AchievementSystem:
    def __init__(self):
        self._achievements: List['Achievement'] = []
        self._user_achievements: Dict[str, List['UserAchievement']] = {}
    
    def create_achievement(self, name: str) -> 'Achievement':
        achievement = Achievement(name)
        self._achievements.append(achievement)
        return achievement
    
    def award_achievement(self, user: User, achievement: 'Achievement') -> 'UserAchievement':
        user_achievements = self._user_achievements.get(user.user_id, [])
        for ua in user_achievements:
            if ua._achievement._name == achievement._name:
                raise AchievementAlreadyAwardedException("Achievement already awarded to user")
        
        user_achievement = UserAchievement(user, achievement)
        
        if user.user_id not in self._user_achievements:
            self._user_achievements[user.user_id] = []
        self._user_achievements[user.user_id].append(user_achievement)
        
        return user_achievement
    
    def get_user_achievements(self, user: User) -> List['UserAchievement']:
        return self._user_achievements.get(user.user_id, [])

class Achievement:
    def __init__(self, name: str):
        self._name = name
        self._description: str = ""
        self._points: int = 0
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def set_points(self, points: int) -> None:
        self._points = points
    
    def get_achievement_info(self) -> dict:
        return {
            "name": self._name,
            "description": self._description,
            "points": self._points
        }

class UserAchievement:
    def __init__(self, user: User, achievement: Achievement):
        self._user = user
        self._achievement = achievement
        self._awarded_date = datetime.now()
    
    def get_days_since_awarded(self) -> int:
        return (datetime.now() - self._awarded_date).days

class StudyGroup:
    def __init__(self, group_id: str, name: str, course: Course):
        self._group_id = group_id
        self._name = name
        self._course = course
        self._members: List[Student] = []
        self._max_members: int = 10
    
    def add_member(self, student: Student) -> bool:
        if len(self._members) >= self._max_members:
            raise StudyGroupFullException("Study group is full")
        
        if student not in self._course._current_students:
            raise CourseNotFoundException("Student not enrolled in the course")
        
        if student in self._members:
            raise DuplicateEnrollmentException("Student already in study group")
        
        self._members.append(student)
        return True
    
    def remove_member(self, student: Student) -> bool:
        if student in self._members:
            self._members.remove(student)
            return True
        return False
    
    def get_member_count(self) -> int:
        return len(self._members)
    
    def is_full(self) -> bool:
        return len(self._members) >= self._max_members

class StudySession:
    def __init__(self, study_group: StudyGroup, title: str):
        self._study_group = study_group
        self._title = title
        self._attendees: List[Student] = []
        self._scheduled_time: datetime = datetime.now()
    
    def mark_attendance(self, student: Student) -> None:
        if student not in self._study_group._members:
            raise StudyGroupNotFoundException("Student not in study group")
        
        if student not in self._attendees:
            self._attendees.append(student)
    
    def get_attendance_count(self) -> int:
        return len(self._attendees)
    
    def get_attendance_rate(self) -> float:
        total_members = len(self._study_group._members)
        return (len(self._attendees) / total_members * 100) if total_members > 0 else 0

class ResourceLibrary:
    def __init__(self):
        self._resources: List['LearningResource'] = []
    
    def add_resource(self, resource: 'LearningResource') -> None:
        self._resources.append(resource)
    
    def search_resources(self, query: str) -> List['LearningResource']:
        results = []
        for resource in self._resources:
            if (query.lower() in resource._title.lower() or 
                query.lower() in resource._description.lower()):
                results.append(resource)
        return results
    
    def get_resource_count(self) -> int:
        return len(self._resources)
    
    def get_resource_by_title(self, title: str) -> 'LearningResource':
        for resource in self._resources:
            if resource._title == title:
                return resource
        raise ContentNotFoundException(f"Resource with title '{title}' not found")

class LearningResource:
    def __init__(self, title: str, resource_type: str):
        self._title = title
        self._resource_type = resource_type
        self._description: str = ""
        self._uploader: Optional[User] = None
        self._download_count: int = 0
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def set_uploader(self, uploader: User) -> None:
        self._uploader = uploader
    
    def increment_download_count(self) -> None:
        self._download_count += 1
    
    def get_resource_info(self) -> dict:
        return {
            "title": self._title,
            "type": self._resource_type,
            "uploader": self._uploader.username if self._uploader else "Unknown",
            "downloads": self._download_count
        }

class TimeTracker:
    def __init__(self, student: Student):
        self._student = student
        self._study_sessions: List['StudySessionRecord'] = []
        self._daily_goals: Dict[str, int] = {}
    
    def start_study_session(self, course: Course) -> None:
        if course not in self._student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        
        session = StudySessionRecord(course)
        self._study_sessions.append(session)
    
    def set_daily_goal(self, minutes: int) -> None:
        today_str = datetime.now().strftime("%Y-%m-%d")
        self._daily_goals[today_str] = minutes
    
    def get_todays_study_time(self) -> int:
        today = datetime.now().date()
        todays_sessions = [s for s in self._study_sessions if s._end_time and s._end_time.date() == today]
        return sum(session.get_duration_minutes() for session in todays_sessions)
    
    def is_goal_achieved(self) -> bool:
        return self.get_todays_study_time() >= self._daily_goals.get(datetime.now().strftime("%Y-%m-%d"), 0)

class StudySessionRecord:
    def __init__(self, course: Course):
        self._course = course
        self._start_time = datetime.now()
        self._end_time: Optional[datetime] = None
    
    def end_session(self) -> None:
        self._end_time = datetime.now()
    
    def get_duration_minutes(self) -> int:
        if self._end_time:
            return int((self._end_time - self._start_time).total_seconds() / 60)
        return int((datetime.now() - self._start_time).total_seconds() / 60)

class CourseRecommender:
    def __init__(self, course_catalog: CourseCatalog):
        self._course_catalog = course_catalog
    
    def recommend_courses(self, user: User) -> List[Course]:
        published_courses = [course for course in self._course_catalog._courses 
                           if course._status == CourseStatus.PUBLISHED]
        return published_courses[:3]
    
    def calculate_recommendation_confidence(self, course: Course, user: User) -> float:
        if course._status != CourseStatus.PUBLISHED:
            raise CourseNotPublishedException("Cannot recommend unpublished course")
        return 0.7

class CourseSchedule:
    def __init__(self, course: Course):
        self._course = course
        self._lessons_schedule: Dict[Lesson, datetime] = {}
        self._assignments_deadlines: Dict[Assignment, datetime] = {}
    
    def schedule_lesson(self, lesson: Lesson, date_time: datetime) -> None:
        self._lessons_schedule[lesson] = date_time
    
    def add_assignment_deadline(self, assignment: Assignment, deadline: datetime) -> None:
        self._assignments_deadlines[assignment] = deadline
    
    def get_upcoming_events(self, days: int = 7) -> List[dict]:
        upcoming = []
        now = datetime.now()
        
        for lesson, lesson_time in self._lessons_schedule.items():
            if 0 <= (lesson_time - now).days <= days:
                upcoming.append({"type": "lesson", "title": lesson._title, "time": lesson_time})
        
        for assignment, deadline in self._assignments_deadlines.items():
            if 0 <= (deadline - now).days <= days:
                upcoming.append({"type": "assignment", "title": assignment._title, "deadline": deadline})
        
        return sorted(upcoming, key=lambda x: x['time'] if 'time' in x else x['deadline'])

class StudentPerformanceAnalytics:
    def __init__(self, student: Student):
        self._student = student
        self._course_performance: Dict[str, Dict[str, float]] = {}
    
    def analyze_course_performance(self, course: Course) -> Dict[str, float]:
        if course not in self._student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        
        performance = {
            "assignments_avg": 85.0,
            "quizzes_avg": 78.0,
            "overall_score": 81.5
        }
        self._course_performance[course.course_id] = performance
        return performance
    
    def predict_final_grade(self, course: Course) -> float:
        performance = self._course_performance.get(course.course_id, {})
        return performance.get("overall_score", 70)

class InstructorDashboard:
    def __init__(self, instructor: Teacher):
        self._instructor = instructor
        self._course_metrics: Dict[str, Dict] = {}
    
    def update_course_metrics(self, course: Course) -> None:
        if course._instructor != self._instructor:
            raise InsufficientPermissionsException("Instructor can only access their own courses")
        
        metrics = {
            "total_students": len(course._current_students),
            "completion_rate": 75.0,
            "avg_grade": 82.5
        }
        self._course_metrics[course.course_id] = metrics
    
    def get_teaching_insights(self) -> Dict[str, any]:
        return {
            "most_popular_course": "Python Basics",
            "total_students": self._instructor.get_total_students_taught()
        }

class ContentManagementSystem:
    def __init__(self):
        self._content_versions: Dict[str, List['ContentVersion']] = {}
        self._approval_queue: List[LearningContent] = []
    
    def create_content_version(self, content: LearningContent, author: User) -> 'ContentVersion':
        if author.get_role() not in [UserRole.TEACHER, UserRole.CONTENT_CREATOR, UserRole.ADMIN]:
            raise InsufficientPermissionsException("Only teachers, content creators and admins can create content")
        
        version = ContentVersion(content, author)
        
        if content._content_id not in self._content_versions:
            self._content_versions[content._content_id] = []
        self._content_versions[content._content_id].append(version)
        
        self._approval_queue.append(content)
        return version
    
    def approve_content(self, content: LearningContent) -> None:
        if content in self._approval_queue:
            self._approval_queue.remove(content)
            content.approve_content()
    
    def get_pending_approvals(self) -> List[LearningContent]:
        return self._approval_queue.copy()

class ContentVersion:
    def __init__(self, content: LearningContent, author: User):
        self._content = content
        self._author = author
        self._created_date = datetime.now()
        self._is_current: bool = False
    
    def make_current(self) -> None:
        self._is_current = True
    
    def get_version_info(self) -> dict:
        return {
            "author": self._author.get_profile_info(),
            "created_date": self._created_date,
            "is_current": self._is_current
        }

class GamificationEngine:
    def __init__(self):
        self._points_system: Dict[str, int] = {
            "complete_lesson": 10,
            "complete_assignment": 25
        }
        self._student_points: Dict[str, int] = {}
    
    def award_points(self, student: Student, action: str) -> int:
        points = self._points_system.get(action, 0)
        if student.user_id not in self._student_points:
            self._student_points[student.user_id] = 0
        self._student_points[student.user_id] += points
        return points
    
    def get_student_points(self, student: Student) -> int:
        return self._student_points.get(student.user_id, 0)
    
    def calculate_student_level(self, student: Student) -> int:
        points = self.get_student_points(student)
        return points // 100 + 1

class LearningPath:
    def __init__(self, path_id: str, title: str):
        self._path_id = path_id
        self._title = title
        self._courses: List[Course] = []
        self._description: str = ""
    
    def add_course(self, course: Course) -> None:
        self._courses.append(course)
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def enroll_student(self, student: Student) -> bool:
        if not self._courses:
            raise CourseNotFoundException("No courses in learning path")
        
        student.enroll_in_course(self._courses[0])
        return True
    
    def calculate_progress(self, student: Student) -> float:
        completed = sum(1 for course in self._courses if course in student._completed_courses)
        return (completed / len(self._courses)) * 100 if self._courses else 0

class Poll:
    def __init__(self, question: str):
        self._question = question
        self._options: List[str] = []
        self._votes: Dict[str, int] = {}
        self._is_active: bool = True
    
    def add_option(self, option: str) -> None:
        if option not in self._options:
            self._options.append(option)
            self._votes[option] = 0
    
    def vote(self, user: User, option: str) -> bool:
        if not self._is_active:
            raise InsufficientPermissionsException("Poll is no longer active")
        
        if option not in self._options:
            raise ContentNotFoundException("Option not found in poll")
        
        self._votes[option] += 1
        return True
    
    def get_results(self) -> Dict[str, int]:
        return self._votes.copy()
    
    def get_winner(self) -> Optional[str]:
        if not self._votes:
            return None
        return max(self._votes.items(), key=lambda x: x[1])[0]
    
class CourseAnnouncement:
    def __init__(self, announcement_id: str, course: Course, author: User, title: str, content: str):
        if author.get_role() not in [UserRole.TEACHER, UserRole.ADMIN]:
            raise InsufficientPermissionsException("Only teachers and admins can create announcements")
        
        self._announcement_id = announcement_id
        self._course = course
        self._author = author
        self._title = title
        self._content = content
        self._created_date = datetime.now()
        self._is_pinned = False
        self._view_count = 0
    
    def pin_announcement(self) -> None:
        self._is_pinned = True
    
    def unpin_announcement(self) -> None:
        self._is_pinned = False
    
    def increment_view_count(self) -> None:
        self._view_count += 1
    
    def get_announcement_info(self) -> dict:
        return {
            "announcement_id": self._announcement_id,
            "course": self._course.title,
            "author": self._author.username,
            "title": self._title,
            "created_date": self._created_date,
            "is_pinned": self._is_pinned,
            "view_count": self._view_count
        }
    
    def is_recent(self, hours: int = 24) -> bool:
        return (datetime.now() - self._created_date).total_seconds() < hours * 3600


class StudyReminder:
    def __init__(self, reminder_id: str, student: Student, title: str, reminder_time: datetime):
        self._reminder_id = reminder_id
        self._student = student
        self._title = title
        self._reminder_time = reminder_time
        self._is_completed = False
        self._course: Optional[Course] = None
    
    def set_course(self, course: Course) -> None:
        if course not in self._student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        self._course = course
    
    def mark_completed(self) -> None:
        self._is_completed = True
    
    def mark_incomplete(self) -> None:
        self._is_completed = False
    
    def is_due(self) -> bool:
        return datetime.now() >= self._reminder_time and not self._is_completed
    
    def get_reminder_info(self) -> dict:
        return {
            "reminder_id": self._reminder_id,
            "title": self._title,
            "reminder_time": self._reminder_time,
            "is_completed": self._is_completed,
            "course": self._course.title if self._course else None,
            "is_due": self.is_due()
        }
    
    def reschedule(self, new_time: datetime) -> None:
        self._reminder_time = new_time


class CourseReview:
    def __init__(self, review_id: str, course: Course, student: Student, rating: float, comment: str):
        if course not in student._completed_courses:
            raise InsufficientPermissionsException("Student must complete course to review it")
        
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        
        self._review_id = review_id
        self._course = course
        self._student = student
        self._rating = rating
        self._comment = comment
        self._created_date = datetime.now()
        self._is_verified = False
        self._helpful_count = 0
    
    def verify_review(self) -> None:
        self._is_verified = True
    
    def mark_helpful(self) -> None:
        self._helpful_count += 1
    
    def update_rating(self, new_rating: float) -> None:
        if not (1 <= new_rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        self._rating = new_rating
    
    def update_comment(self, new_comment: str) -> None:
        self._comment = new_comment
    
    def get_review_info(self) -> dict:
        return {
            "review_id": self._review_id,
            "course": self._course.title,
            "student": self._student.username,
            "rating": self._rating,
            "comment": self._comment,
            "created_date": self._created_date,
            "is_verified": self._is_verified,
            "helpful_count": self._helpful_count
        }
    
    def is_positive(self) -> bool:
        return self._rating >= 4.0
    
    def is_recent(self, days: int = 30) -> bool:
        return (datetime.now() - self._created_date).days <= days