from django.contrib.auth import get_user_model


User = get_user_model()


def notification_cleanser(user_id: int, body: str) -> str:

    """
        function that deletes existing notifications to avoid duplication, putting the latest of such notification first
        mitigates users' getting spammed with actions that trigger notifications
        deletes notification if it exists within the user's last 8 notifications
    """

    user = User.objects.get(id= user_id)
    for alert in user.notifications.all()[:8]:
        if body == alert.body:
            alert.delete()
            print('deleted')
            print(body)
            return body
    return body
