

def unread_alerts_counter(request):
    if request.user.is_authenticated:
        alerts = request.user.notifications.filter(viewed_status__gt= 0)
        unread_notifications = len(alerts)
        return {"unread_notifications": unread_notifications}
    else:
        return {"unread_notifications": 0}