import flet as ft
from flet_object_inspector_v2 import inspect_flet, flet_to_json

# Создаем структуру
view = ft.View(
    controls=[
        ft.AppBar(title=ft.Text("App")),
        ft.Container(
            content=ft.Row([
                ft.IconButton(ft.Icons.HOME),
                ft.IconButton(ft.Icons.MENU)
            ])
        )
    ]
)

view2 = ft.View(
        route="/",
        appbar=ft.AppBar(
            title=ft.Text("My App"),
            bgcolor=ft.Colors.BLUE
        ),
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.IconButton(ft.Icons.HOME, tooltip="Home"),
                    ft.IconButton(ft.Icons.SETTINGS, tooltip="Settings"),
                    ft.ElevatedButton("Click me", width=200)
                ]),
                padding=20,
                bgcolor=ft.Colors.GREY_100
            ),
            ft.Text("Hello, World!", size=20),
            ft.Column([
                ft.TextField(label="Name", width=300),
                ft.TextField(label="Email", width=300),
            ])
        ]
    )

# Просматриваем структуру
inspect_flet(view2)

# Или в JSON формате
# print(flet_to_json(view))