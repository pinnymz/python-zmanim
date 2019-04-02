from typing import Optional, Callable, Any


class Unit:
    def __init__(self, *components):
        self.__components = components

    @property
    def components(self) -> tuple:
        return self.__components

    def __str__(self):
        return self.render(str)

    def render(self, rendering_method: Callable[[Any], str]) -> str:
        def component_wrapper(component):
            if isinstance(component, str) or not isinstance(component, list):
                return [component]
            else:
                return component

        primary, *tail = map(lambda c: list(map(rendering_method, component_wrapper(c))), self.__components)
        secondary = tail[0] if len(tail) > 0 else None
        return self._render_with_root(primary) + self._render_secondary(secondary, primary)

    def _render_with_root(self, component: list) -> str:
        if len(component) == 0:
            return ''
        root, *extension = component
        if len(extension) == 0:
            return str(root)
        else:
            return str(root) + ' ' + self._render_extension(extension)

    @staticmethod
    def _render_extension(extension: list) -> str:
        return ':'.join(map(str, extension))

    def _render_secondary(self, second_component: list, first_component: list) -> str:
        if second_component is None:
            return ''
        elif second_component[0] != first_component[0]:
            return ' - ' + self._render_with_root(second_component)
        diff = self._render_difference(second_component, first_component)
        if diff is not None:
            return '-' + diff
        else:
            return ''

    def _render_difference(self, rendering: list, comparing: list) -> Optional[str]:
        if len(rendering) == 0:
            return None
        elif rendering[0] != comparing[0]:
            return self._render_extension(rendering)
        else:
            return self._render_difference(rendering[1:], comparing[1:])
