# Django Channels + HTMX

## What is Django Channels?

Django Channels, often referred to as just Channels, enhances Django's capabilities by enabling the handling of not only HTTP but also protocols requiring long-lived connections like WebSockets, MQTT for IoT applications, chatbots, real-time notifications, and more. It seamlessly integrates with Django's core features such as authentication and sessions.

A typical Channels setup involves:

<p align="center">
<img src="img/django-channels-generic-architecture-overview.jpg" alt="django-channels-generic-architecture-overview.jpg" width="700px"/>
</p>
## Sync vs Async
Channels necessitates frequent transitions between synchronous and asynchronous code execution due to the differences between Channels and Django. For instance, while accessing the Django database, synchronous code is required, whereas interaction with the Channels channel layer mandates asynchronous code.

To facilitate this transition, Django provides built-in asgiref functions:

- `sync_to_async`: Converts a synchronous function into an asynchronous one.
- `async_to_sync`: Converts an asynchronous function into a synchronous one.

These utilities streamline the integration of synchronous and asynchronous code within a Channels-powered Django application.


## Install and setup channels

To integrate WebSocket functionality into our Django project, we'll utilize Django Channels, a package that extends Django's capabilities to handle long-running connections and asynchronous protocols like WebSockets.

Begin by installing Django Channels along with Daphne, which serves as the web server gateway interface for asynchronous web applications:

```bash
pip install -U channels["daphne"]
```

This command installs the latest versions of both Django Channels and Daphne.


Additionally, ensure that both `channels` and `daphne` are added to the `INSTALLED_APPS` configuration of your Django project. It's essential to prioritize the `daphne` app by placing it at the top of the list of applications.
Also add `ASGI_APPLICATION` to the settings file.


```python
INSTALLED_APPS = [
    "daphne",
    # ...
    # ...
    "channels",
]

ASGI_APPLICATION = "config.asgi.application"
```


Since we'll be using WebSockets instead of HTTP to communicate from the client to the server, we need to wrap our ASGI config with `ProtocolTypeRouter` in `config/asgi.py`:


```python
import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = ProtocolTypeRouter({
'http': get_asgi_application(),
})
```

## WebSocket consumer

Although Django Channels is based on a simple low-level specification called ASGI, it is more suited for interoperability than developing sophisticated applications. To make ASGI applications quickly, Channels offers your `Consumers` a rich abstraction.

`Consumers` (the equivalent of Django views) are ASGI applications. Consumers do a couple of things in particular:

- Structure your code as functions that are called whenever an event happens (as opposed to forcing you to write event loops).
- Allow you to write both sync, as well as async code.

Here’s a basic example of a sync consumer which accepts incoming WebSocket connections and then sends a message:

### Adding Routers for WebSocket connections

Next, add the following code to a new file named `example_channels/routing.py` to configure routes, which function almost identically to Django URL configuration:

```python
from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path('chat/<str:room_slug>/', consumers.ChatConsumer.as_asgi()),
]
```

### Setting up ASGI Application


Register the `routing.py` file inside `config/asgi.py`:

```python
from chat import routing
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})

```

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("*" * 50)
        print("You are connected to websocket")



<!--

With Channels now in our project, we proceed to configure the `CHANNEL_LAYERS` setting to specify the backend, which can be Redis, In-Memory, or others.


With these steps completed, Django Channels is now integrated into your project, ready to handle WebSocket connections efficiently. -->