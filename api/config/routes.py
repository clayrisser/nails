from nails import Route

routes = [
    Route(
        path='/',
        handler='default_controller.Root'
    ),
    Route(
        path='/info/',
        handler='default_controller.Info'
    )
]
