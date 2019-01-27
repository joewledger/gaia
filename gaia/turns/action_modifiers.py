class HasHexagonLocation:
    def __init__(self, hexagon):
        self.hexagon = hexagon


class NavigationModifiable:
    def __init__(self):
        self._base_navigation = 0

    @property
    def base_navigation(self):
        return self._base_navigation

    @base_navigation.setter
    def base_navigation(self, navigation):
        self._base_navigation = navigation


class GaiaformingRequirementsModifiable:
    def __init__(self):
        self._base_free_gaiaforming = 0

    @property
    def base_free_gaiaforming(self):
        return self._base_free_gaiaforming

    @base_free_gaiaforming.setter
    def base_free_gaiaforming(self, free_gaiaforming):
        self._base_free_gaiaforming = free_gaiaforming
