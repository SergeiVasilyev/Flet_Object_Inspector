"""
Модуль для красивого отображения структуры объектов Flet framework
"""

import flet as ft
from typing import Any, List, Dict, Optional, Union
import json


class FletInspector:
    """Класс для инспекции и отображения структуры объектов Flet"""
    
    def __init__(self, show_properties: bool = True, max_depth: int = 10, 
                 indent: str = "  ", show_private: bool = False):
        """
        Инициализация инспектора
        
        Args:
            show_properties: Показывать ли свойства объектов
            max_depth: Максимальная глубина вложенности
            indent: Строка для отступов
            show_private: Показывать ли приватные атрибуты (начинающиеся с _)
        """
        self.show_properties = show_properties
        self.max_depth = max_depth
        self.indent = indent
        self.show_private = show_private
    
    def inspect(self, obj: Any, depth: int = 0) -> str:
        """
        Основной метод для инспекции объекта
        
        Args:
            obj: Объект для инспекции
            depth: Текущая глубина вложенности
            
        Returns:
            Строковое представление структуры объекта
        """
        if depth > self.max_depth:
            return f"{self.indent * depth}... (max depth reached)"
        
        if self._is_flet_control(obj):
            return self._inspect_flet_control(obj, depth)
        elif isinstance(obj, list):
            return self._inspect_list(obj, depth)
        elif isinstance(obj, dict):
            return self._inspect_dict(obj, depth)
        else:
            return self._inspect_primitive(obj, depth)
    
    def _is_flet_control(self, obj: Any) -> bool:
        """Проверяет, является ли объект контролом Flet"""
        return hasattr(obj, '__class__') and hasattr(obj.__class__, '__module__') and \
               (obj.__class__.__module__.startswith('flet') or 
                isinstance(obj, ft.Control) if hasattr(ft, 'Control') else False)
    
    def _inspect_flet_control(self, obj: Any, depth: int) -> str:
        """Инспекция Flet контрола"""
        class_name = obj.__class__.__name__
        result = f"{self.indent * depth}{class_name}"
        
        # Получаем основные свойства
        properties = self._get_object_properties(obj)
        
        if properties and self.show_properties:
            result += " {"
            for key, value in properties.items():
                if value is not None and (self.show_private or not key.startswith('_')):
                    result += f"\n{self.indent * (depth + 1)}{key}: "
                    if key == 'controls' or key == 'content':
                        # Особая обработка для вложенных контролов
                        if isinstance(value, list):
                            result += "["
                            for i, item in enumerate(value):
                                result += f"\n{self.inspect(item, depth + 2)}"
                                if i < len(value) - 1:
                                    result += ","
                            result += f"\n{self.indent * (depth + 1)}]"
                        else:
                            result += f"\n{self.inspect(value, depth + 2)}"
                    else:
                        result += self._format_value(value)
            result += f"\n{self.indent * depth}}}"
        
        # Проверяем наличие дочерних контролов
        children = self._get_children(obj)
        if children:
            result += f"\n{self.indent * depth}└─ children: ["
            for i, child in enumerate(children):
                result += f"\n{self.inspect(child, depth + 1)}"
                if i < len(children) - 1:
                    result += ","
            result += f"\n{self.indent * depth}]"
        
        return result
    
    def _inspect_list(self, obj: List, depth: int) -> str:
        """Инспекция списка"""
        if not obj:
            return f"{self.indent * depth}[]"
        
        result = f"{self.indent * depth}["
        for i, item in enumerate(obj):
            result += f"\n{self.inspect(item, depth + 1)}"
            if i < len(obj) - 1:
                result += ","
        result += f"\n{self.indent * depth}]"
        return result
    
    def _inspect_dict(self, obj: Dict, depth: int) -> str:
        """Инспекция словаря"""
        if not obj:
            return f"{self.indent * depth}{{}}"
        
        result = f"{self.indent * depth}{{"
        items = list(obj.items())
        for i, (key, value) in enumerate(items):
            result += f"\n{self.indent * (depth + 1)}{key}: "
            result += self.inspect(value, depth + 1).lstrip()
            if i < len(items) - 1:
                result += ","
        result += f"\n{self.indent * depth}}}"
        return result
    
    def _inspect_primitive(self, obj: Any, depth: int) -> str:
        """Инспекция примитивных типов"""
        return f"{self.indent * depth}{self._format_value(obj)}"
    
    def _get_object_properties(self, obj: Any) -> Dict[str, Any]:
        """Получает свойства объекта"""
        properties = {}
        
        # Список важных атрибутов для Flet контролов
        important_attrs = [
            'text', 'value', 'width', 'height', 'padding', 'margin',
            'alignment', 'bgcolor', 'color', 'visible', 'disabled',
            'tooltip', 'data', 'key', 'expand', 'opacity', 'rotate',
            'scale', 'offset', 'aspect_ratio', 'col', 'title', 'leading',
            'actions', 'automatically_imply_leading', 'center_title'
        ]
        
        for attr in important_attrs:
            if hasattr(obj, attr):
                value = getattr(obj, attr, None)
                if value is not None:
                    properties[attr] = value
        
        return properties
    
    def _get_children(self, obj: Any) -> List[Any]:
        """Получает дочерние элементы объекта"""
        children = []
        
        # Проверяем различные атрибуты, которые могут содержать дочерние элементы
        child_attrs = ['controls', 'content', 'tabs', 'sections', 'actions', 'leading']
        
        for attr in child_attrs:
            if hasattr(obj, attr):
                value = getattr(obj, attr, None)
                if value is not None:
                    if isinstance(value, list):
                        children.extend(value)
                    elif self._is_flet_control(value):
                        children.append(value)
        
        return children
    
    def _format_value(self, value: Any) -> str:
        """Форматирует значение для отображения"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (int, float, bool)):
            return str(value)
        elif value is None:
            return "None"
        elif hasattr(value, '__class__'):
            return f"<{value.__class__.__name__}>"
        else:
            return str(value)
    
    def to_dict(self, obj: Any, depth: int = 0) -> Union[Dict, List, Any]:
        """
        Преобразует объект в словарь для JSON-сериализации
        
        Args:
            obj: Объект для преобразования
            depth: Текущая глубина вложенности
            
        Returns:
            Словарь, список или примитивное значение
        """
        if depth > self.max_depth:
            return f"... (max depth {self.max_depth} reached)"
        
        if self._is_flet_control(obj):
            result = {
                '_type': obj.__class__.__name__,
                '_module': obj.__class__.__module__
            }
            
            # Добавляем свойства
            properties = self._get_object_properties(obj)
            for key, value in properties.items():
                if value is not None and (self.show_private or not key.startswith('_')):
                    if isinstance(value, (str, int, float, bool)) or value is None:
                        result[key] = value
                    else:
                        result[key] = self.to_dict(value, depth + 1)
            
            # Добавляем дочерние элементы
            children = self._get_children(obj)
            if children:
                result['_children'] = [self.to_dict(child, depth + 1) for child in children]
            
            return result
        
        elif isinstance(obj, list):
            return [self.to_dict(item, depth + 1) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.to_dict(value, depth + 1) for key, value in obj.items()}
        else:
            return obj


# Удобные функции для быстрого использования
def inspect_flet(obj: Any, show_properties: bool = True, max_depth: int = 10) -> None:
    """
    Быстрая функция для инспекции объекта Flet
    
    Args:
        obj: Объект для инспекции
        show_properties: Показывать ли свойства
        max_depth: Максимальная глубина вложенности
    """
    inspector = FletInspector(show_properties=show_properties, max_depth=max_depth)
    print(inspector.inspect(obj))


def flet_to_dict(obj: Any, show_properties: bool = True, max_depth: int = 10) -> Dict:
    """
    Преобразует объект Flet в словарь
    
    Args:
        obj: Объект для преобразования
        show_properties: Показывать ли свойства
        max_depth: Максимальная глубина вложенности
        
    Returns:
        Словарь с структурой объекта
    """
    inspector = FletInspector(show_properties=show_properties, max_depth=max_depth)
    return inspector.to_dict(obj)


def flet_to_json(obj: Any, show_properties: bool = True, max_depth: int = 10, 
                 indent: int = 2) -> str:
    """
    Преобразует объект Flet в JSON строку
    
    Args:
        obj: Объект для преобразования
        show_properties: Показывать ли свойства
        max_depth: Максимальная глубина вложенности
        indent: Отступы для JSON
        
    Returns:
        JSON строка
    """
    data = flet_to_dict(obj, show_properties, max_depth)
    return json.dumps(data, indent=indent, ensure_ascii=False)


# Пример использования
if __name__ == "__main__":
    # Создаем пример структуры Flet
    app_bar = ft.AppBar(
        title=ft.Text("My App"),
        center_title=True,
        actions=[
            ft.IconButton(ft.icons.SEARCH),
            ft.IconButton(ft.icons.MENU)
        ]
    )
    
    container = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.icons.HOME),
            ft.IconButton(ft.icons.FAVORITE),
            ft.Text("Hello World")
        ]),
        padding=10,
        bgcolor=ft.colors.BLUE_100
    )
    
    view = ft.View(
        route="/",
        controls=[app_bar, container],
        appbar=app_bar
    )
    
    print("=== Инспекция View ===")
    inspect_flet(view)
    
    print("\n=== В виде JSON ===")
    print(flet_to_json(view))