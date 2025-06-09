"""
This module for visualizing the structure of Flet framework objects.
Allows viewing nested objects in a readable form.
"""

from typing import Any, Dict, List, Union
import json


class FletInspector:
    """Класс для инспекции и визуализации структуры объектов Flet"""
    
    def __init__(self, indent_size: int = 2, max_depth: int = 10):
        self.indent_size = indent_size
        self.max_depth = max_depth
        self.current_depth = 0
    
    def inspect(self, obj: Any, show_properties: bool = True) -> str:
        """
        Основной метод для инспекции объекта
        
        Args:
            obj: Объект для инспекции
            show_properties: Показывать ли свойства объектов
            
        Returns:
            Строковое представление структуры
        """
        self.current_depth = 0
        return self._inspect_recursive(obj, show_properties)
    
    def _inspect_recursive(self, obj: Any, show_properties: bool, depth: int = 0) -> str:
        """Рекурсивная инспекция объекта"""
        
        if depth > self.max_depth:
            return "... (max depth reached)"
        
        indent = " " * (depth * self.indent_size)
        
        # Если это Flet контрол
        if hasattr(obj, '__class__') and obj.__class__.__module__.startswith('flet'):
            return self._inspect_flet_control(obj, show_properties, depth, indent)
        
        # Если это список
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            
            result = "[\n"
            for i, item in enumerate(obj):
                result += f"{indent}  [{i}] {self._inspect_recursive(item, show_properties, depth + 1)}"
                if i < len(obj) - 1:
                    result += ","
                result += "\n"
            result += f"{indent}]"
            return result
        
        # Если это словарь
        elif isinstance(obj, dict):
            if not obj:
                return "{}"
            
            result = "{\n"
            items = list(obj.items())
            for i, (key, value) in enumerate(items):
                result += f"{indent}  '{key}': {self._inspect_recursive(value, show_properties, depth + 1)}"
                if i < len(items) - 1:
                    result += ","
                result += "\n"
            result += f"{indent}}}"
            return result
        
        # Для остальных типов
        else:
            return repr(obj)
    
    def _inspect_flet_control(self, obj: Any, show_properties: bool, depth: int, indent: str) -> str:
        """Инспекция Flet контрола"""
        
        class_name = obj.__class__.__name__
        result = f"{class_name}"
        
        # Получаем основные свойства
        if show_properties:
            props = self._get_control_properties(obj)
            if props:
                result += f" {props}"
        
        # Ищем дочерние элементы
        children = self._get_children(obj)
        special_children = self._get_special_children(obj)
        
        if children or special_children:
            result += " {\n"
            
            # Сначала отображаем специальные дочерние элементы (appbar, etc.)
            if special_children:
                for name, child in special_children.items():
                    child_repr = self._inspect_recursive(child, show_properties, depth + 1)
                    result += f"{indent}  {name}: {child_repr}\n"
            
            # Затем основные дочерние элементы
            if children:
                if isinstance(children, list):
                    for i, child in enumerate(children):
                        child_repr = self._inspect_recursive(child, show_properties, depth + 1)
                        result += f"{indent}  [{i}] {child_repr}"
                        if i < len(children) - 1:
                            result += ","
                        result += "\n"
                else:
                    child_repr = self._inspect_recursive(children, show_properties, depth + 1)
                    result += f"{indent}  {child_repr}\n"
            
            result += f"{indent}}}"
        
        return result
    
    def _get_control_properties(self, obj: Any) -> str:
        """Получение основных свойств контрола"""
        props = {}
        
        # Список основных свойств для отображения
        common_props = ['text', 'value', 'width', 'height', 'bgcolor', 'color', 
                       'visible', 'disabled', 'tooltip', 'key', 'data', 'route', 
                       'title', 'label', 'hint_text', 'padding', 'margin']
        
        for prop in common_props:
            if hasattr(obj, prop):
                value = getattr(obj, prop)
                if value is not None and value != "":
                    if isinstance(value, str) and len(value) > 30:
                        value = f"{value[:30]}..."
                    props[prop] = value
        
        if props:
            # Форматируем свойства
            prop_strs = []
            for key, value in props.items():
                if isinstance(value, str):
                    prop_strs.append(f"{key}='{value}'")
                else:
                    prop_strs.append(f"{key}={value}")
            return f"({', '.join(prop_strs)})"
        
        return ""
    
    def _get_special_children(self, obj: Any) -> Dict[str, Any]:
        """Получение специальных дочерних элементов (appbar, drawer, etc.)"""
        special_children = {}
        
        # Список специальных атрибутов, которые нужно показать отдельно
        special_attrs = ['appbar', 'drawer', 'end_drawer', 'floating_action_button', 
                        'bottom_navigation_bar', 'navigation_bar']
        
        for attr in special_attrs:
            if hasattr(obj, attr):
                value = getattr(obj, attr)
                if value is not None and hasattr(value, '__class__'):
                    if value.__class__.__module__.startswith('flet'):
                        special_children[attr] = value
        
        return special_children
    
    def _get_children(self, obj: Any) -> Union[List, Any, None]:
        """Получение дочерних элементов контрола"""
        
        # Проверяем различные атрибуты, которые могут содержать дочерние элементы
        # Исключаем специальные атрибуты, которые обрабатываются отдельно
        child_attrs = ['controls', 'content', 'actions', 'tabs', 'items', 
                      'leading', 'title', 'trailing', 'options']
        
        for attr in child_attrs:
            if hasattr(obj, attr):
                value = getattr(obj, attr)
                if value is not None:
                    if isinstance(value, list) and len(value) > 0:
                        return value
                    elif not isinstance(value, (str, int, float, bool)) and hasattr(value, '__class__'):
                        if value.__class__.__module__.startswith('flet'):
                            return value
        
        return None
    
    def to_dict(self, obj: Any) -> Dict:
        """Конвертация объекта в словарь для JSON-сериализации"""
        
        if hasattr(obj, '__class__') and obj.__class__.__module__.startswith('flet'):
            result = {
                'type': obj.__class__.__name__,
                'properties': {},
                'children': None
            }
            
            # Добавляем свойства
            common_props = ['text', 'value', 'width', 'height', 'bgcolor', 'color', 
                           'visible', 'disabled', 'tooltip', 'key', 'data', 'route',
                           'title', 'label', 'hint_text', 'padding', 'margin']
            
            for prop in common_props:
                if hasattr(obj, prop):
                    value = getattr(obj, prop)
                    if value is not None and value != "":
                        result['properties'][prop] = value
            
            # Добавляем дочерние элементы
            children = self._get_children(obj)
            if children:
                if isinstance(children, list):
                    result['children'] = [self.to_dict(child) for child in children]
                else:
                    result['children'] = self.to_dict(children)
            
            return result
        
        elif isinstance(obj, list):
            return [self.to_dict(item) for item in obj]
        
        elif isinstance(obj, dict):
            return {key: self.to_dict(value) for key, value in obj.items()}
        
        else:
            return obj


# Удобные функции для быстрого использования
def inspect_flet(obj: Any, show_properties: bool = True, indent_size: int = 2, max_depth: int = 10) -> None:
    """
    Печать структуры Flet объекта
    
    Args:
        obj: Объект для инспекции
        show_properties: Показывать ли свойства объектов
        indent_size: Размер отступа
        max_depth: Максимальная глубина рекурсии
    """
    inspector = FletInspector(indent_size, max_depth)
    print(inspector.inspect(obj, show_properties))


def flet_to_dict(obj: Any) -> Dict:
    """
    Конвертация Flet объекта в словарь
    
    Args:
        obj: Объект для конвертации
        
    Returns:
        Словарное представление объекта
    """
    inspector = FletInspector()
    return inspector.to_dict(obj)


def flet_to_json(obj: Any, indent: int = 2) -> str:
    """
    Конвертация Flet объекта в JSON строку
    
    Args:
        obj: Объект для конвертации
        indent: Отступ для JSON
        
    Returns:
        JSON строка
    """
    inspector = FletInspector()
    data = inspector.to_dict(obj)
    
    # ИСПРАВЛЕНИЕ: Добавляем отладочную информацию
    def debug_object(o, path="root"):
        if hasattr(o, '__class__'):
            print(f"DEBUG: {path} -> {o.__class__.__name__} from module {getattr(o.__class__, '__module__', 'None')}")
        if isinstance(o, dict):
            for k, v in o.items():
                debug_object(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                debug_object(v, f"{path}[{i}]")
    
    # Раскомментируйте для отладки:
    # debug_object(data)
    
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


