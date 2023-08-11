from datetime import datetime

from django.utils import timezone


def context_processor(request):
    context={}
    if request.user:
        last_seen=timezone.timedelta(seconds=timezone.now() - request.user.last_activity)
        print(last_seen)
        if last_seen.hour:
            if last_seen.hour <= 4:
                last_seen=last_seen.hour
                context['type']='hour'
        elif last_seen.minute:
            last_seen=last_seen.minute
            context['type'] = 'minute'
        elif last_seen.second:
            last_seen=last_seen.second
            context['type'] = 'second'
        context['last_seen']=last_seen
        print(context)
    return context
