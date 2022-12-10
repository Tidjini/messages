import requests



def notify_users(event, message):
    response = requests.post("https://notification-ecru.vercel.app/notify", {
        'event': event,
        'message' : message
    })

    
    print('response', response.content)