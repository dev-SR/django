d# Django Channels + HTMX

- [What is Django Channels?](#what-is-django-channels)
- [Sync vs Async](#sync-vs-async)
- [Install and setup channels](#install-and-setup-channels)
- [WebSocket consumer](#websocket-consumer)
  - [Adding Routers for WebSocket connections](#adding-routers-for-websocket-connections)
  - [Setting up ASGI Application](#setting-up-asgi-application)
- [Implementing the WebSocket Client](#implementing-the-websocket-client)
  - [Sending Messages with HTMX](#sending-messages-with-htmx)
  - [Receiving Messages from WebSocket](#receiving-messages-from-websocket)


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

Consumers are the equivalent of Django views for asynchronous applications. As mentioned, they handle WebSockets in a very similar way to how traditional views handle HTTP requests. Consumers are ASGI applications that can handle messages, notifications, and other things. Unlike Django views, consumers are built for longrunning communication. URLs are mapped to consumers through routing classes that allow you to combine and stack consumers.

Create a new file inside the `chat` application directory and name it `consumers.py`.
Add the following code to it:


```python
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.template.loader import render_to_string

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # accept connection
        await self.accept()
        print("*" * 50)
        print("You are connected to websocket")

    # receive messages
    async def receive_json(self, data):
        print("*" * 50)
        print("WebSocket received data:")
        print(data)
        try:
            chat_message = data.get('chat_message')
            print(chat_message)
            if not chat_message:
                # Handle case where chat message is not present in data
                return

            # Render template with message and time
            html = render_to_string("chat/partials/ws_response.html",
                                    {'message': chat_message})

            # Send HTML response via WebSocket
            await self.send(text_data=html)

        except Exception as e:
            # Log any errors for debugging
            print(f"Error occurred: {e}")
```

### Adding Routers for WebSocket connections

Next, add the following code to a new file named `example_channels/routing.py` to configure routes, which function almost identically to Django URL configuration:

```python
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat', consumers.ChatConsumer.as_asgi()),
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


## Implementing the WebSocket Client

In the provided code snippet, a WebSocket client is implemented using JavaScript. Let's break down the implementation:

```html
<script>
    var url = 'ws://' + window.location.host +'/ws/chat';
    var chatSocket = new WebSocket(url);
</script>
```

Here's what's happening:

- `url` variable: It is set to the WebSocket URL. The URL is composed of the current host (`window.location.host`) and the WebSocket endpoint (`/ws/chat`). This endpoint should match the URL pattern defined in the `routing.py` file on the server side.

- `chatSocket` variable: It initializes a new WebSocket object connecting to the specified URL. This establishes the WebSocket connection to the server.

### Sending Messages with HTMX

To integrate HTMX with WebSocket for sending and receiving messages, you can utilize HTMX's WebSocket extension.

```html
<div id="content"></div>
<div hx-ext="ws" ws-connect="/ws/chat">
    <form id="form" ws-send>
        <input type="text" name="chat_message" id="chat_message" placeholder="Type a message...">
    </form>
</div>
```

Here's how it works:

- `hx-ext="ws"` attribute: Enables the WebSocket extension for HTMX.

- `ws-connect="/ws/chat"` attribute: Specifies the WebSocket URL to connect to. This URL should match the WebSocket URL pattern defined in the server-side routing.

- `ws-send` attribute: Indicates that when the form is submitted, the form values will be sent to the nearest enclosing WebSocket connection. In this case, it will send the data to the `/ws/chat` endpoint.

### Receiving Messages from WebSocket

On the server-side, when a message is received from the WebSocket, the `ChatConsumer` class handles it. After processing the message, it sends back HTML response via the WebSocket.

```python
async def receive_json(self, data):
        # Process received data

        # Render HTML response
        html = render_to_string("chat/partials/ws_response.html",{'message': chat_message})

        # Send HTML response via WebSocket
        await self.send(text_data=html)
```

The `ws_response.html` template contains the structure for displaying the received message content.

```html
<div hx-swap-oob="beforeend:#content">
    <div>
        {{ message }}
    </div>
</div>
```

This template is used to format the message content received from the WebSocket. The `hx-swap-oob` attribute specifies where to insert the content. In this case, it's appending the message to the `#content` element.