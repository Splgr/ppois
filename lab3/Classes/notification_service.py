from user import User
from notification import Notification

class NotificationService:
    def __init__(self):
        self._notifications: list[Notification] = []
    
    def send_notification(self, user: User, title: str) -> Notification:
        notification = Notification(user, title)
        self._notifications.append(notification)
        return notification
    
    def get_user_notifications(self, user: User) -> list[Notification]:
        return [n for n in self._notifications if n._user.user_id == user.user_id]
    
    def mark_all_as_read(self, user: User) -> None:
        for notification in self.get_user_notifications(user):
            notification.mark_as_read()