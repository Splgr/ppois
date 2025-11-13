# Анализ кода платформы онлайн-обучения

## Полная статистика системы

| Категория | Количество |
|-----------|------------|
| **Основные классы** | 50 |
| **Исключения** | 16 |
| **Поля** | 179 |
| **Методы** | 193 |
| **Ассоциации** | 87 |

## Детализация классов

### Основные классы (50)

| Класс | Поля | Методы | Ассоциации |
|-------|------|--------|------------|
| Achievement | 3 | 3 |  |
| AchievementSystem | 2 | 3 | Achievement, UserAchievement, User |
| Admin | 0 | 3 | User, UserRepository |
| Assignment | 5 | 5 |  |
| AssignmentSubmission | 6 | 4 | Assignment, Student |
| AuthenticationService | 2 | 3 | UserRepository, User |
| Certificate | 4 | 3 | Student, Course |
| ChatMessage | 3 | 1 | User |
| ContentCreator | 2 | 4 | User, LearningContent |
| ContentManagementSystem | 2 | 3 | LearningContent, ContentVersion, User |
| ContentVersion | 4 | 2 | LearningContent, User |
| Course | 8 | 6 | Student |
| CourseAnnouncement | 7 | 6 | Course, User |
| CourseBundle | 4 | 5 | Course, Student |
| CourseCatalog | 2 | 4 | Course |
| CourseManager | 2 | 4 | Course, Teacher |
| CourseRecommender | 1 | 2 | CourseCatalog |
| CourseReview | 8 | 7 | Course, Student |
| CourseSchedule | 2 | 3 |  |
| DiscussionForum | 2 | 3 | Course, ForumThread, User |
| ForumPost | 4 | 3 | ForumThread, User |
| ForumThread | 6 | 6 | User, ForumPost |
| GamificationEngine | 2 | 3 | Student |
| InstructorDashboard | 1 | 3 | Teacher, Course |
| LearningContent | 7 | 5 | ContentCreator, Lesson |
| LearningPath | 4 | 4 | Course, Student |
| LearningResource | 5 | 4 | ResourceLibrary, User |
| Lesson | 5 | 4 | Module, LearningContent |
| LiveSession | 6 | 5 | Teacher, Student |
| Module | 4 | 3 | Lesson |
| Notification | 4 | 3 | User, NotificationService |
| NotificationService | 1 | 3 | User, Notification |
| Poll | 4 | 5 |  |
| ProgressTracker | 3 | 4 | Student, Course, Lesson |
| Quiz | 6 | 6 | QuizQuestion, Student |
| QuizAttempt | 5 | 3 | Quiz, Student |
| QuizQuestion | 4 | 3 | Quiz |
| RatingSystem | 2 | 4 | Course, Teacher |
| ResourceLibrary | 1 | 3 | LearningResource |
| Student | 3 | 7 | User, Course |
| StudentPerformanceAnalytics | 2 | 3 | Student, Course |
| StudyGroup | 5 | 5 | Course, Student |
| StudyReminder | 6 | 6 | Student, Course |
| StudySession | 4 | 3 | StudyGroup, Student |
| StudySessionRecord | 3 | 3 | Course |
| Teacher | 2 | 5 | User, Course, Student |
| TimeTracker | 2 | 4 | Student, Course, StudySessionRecord |
| User | 5 | 3 |  |
| UserAchievement | 3 | 2 | User, Achievement |
| UserRepository | 2 | 4 | User |

### Исключения (16)

| Исключение | Назначение |
|------------|------------|
| AchievementAlreadyAwardedException | Достижение уже получено |
| AssignmentDeadlinePassedException | Срок сдачи задания истек |
| ContentNotApprovedException | Контент не утвержден |
| ContentNotFoundException | Контент не найден |
| CourseFullException | Курс переполнен |
| CourseNotFoundException | Курс не найден |
| CourseNotPublishedException | Курс не опубликован |
| DuplicateEnrollmentException | Дублирующая запись |
| InsufficientPermissionsException | Недостаточно прав |
| InvalidCredentialsException | Неверные учетные данные |
| InvalidRatingException | Неверная оценка |
| PaymentRequiredException | Требуется оплата |
| QuizAttemptsExceededException | Превышены попытки теста |
| StudyGroupFullException | Группа обучения переполнена |
| StudyGroupNotFoundException | Группа обучения не найдена |
| UserNotFoundException | Пользователь не найден |
