import instapush

def push_notify(settings, amount, goal):
    # Requires creating an app in Instapush and putting its credentials in secrets.yml
    app = instapush.App(
        appid = settings.id,
        secret = settings.secret
    )

    events = app.list_event()

    if 'transfer' not in [event['title'] for event in events]:
        # transfer doesn't exist yet, we have to create it
        app.add_event(
            event_name = 'transfer',
            trackers   = ['amount', 'goal'],
            message    = '${amount} transferred to {goal}.'
        )

    app.notify(event_name = 'transfer', trackers = {
        'amount': amount,
        'goal': goal
    })
