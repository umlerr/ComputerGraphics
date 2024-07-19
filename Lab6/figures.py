import numpy as np

class Sphere:
    def __init__(self, _center=[0, 0, 0], _radius=1, _color=[0, 0, 0],
                    _specular=500, _reflective=0, _camera=[0, 0, 0]):

        self.center = _center
        self.radius = _radius
        self.color = _color
        self.specular = _specular
        self.reflective = _reflective
        self.OC = []
        self.OCOC = []
        self.rr = 0
        self.count_oc(_camera)
        self.count_r()

    def get_elements(self):
        return {'center': self.center, 'radius': self.radius, 'color': self.color, 'specular': self.specular,
                'reflective': self.reflective}

    def get_oc(self):
        return self.OC

    def get_ococ(self):
        return self.OCOC

    def get_rr(self):
        return self.rr

    def count_r(self):
        self.rr = self.radius*self.radius

    def count_oc(self, _camera):
        self.OC = (_camera - self.center).copy()
        self.OCOC = np.dot(self.OC, self.OC)


Lights_type = ['ambient', 'point', 'directional']


class Light:
    global Lights_type

    def __init__(self, _type, _intensity, _position=None, _direction=None):
        self.type = Lights_type[_type]
        self.intensity = _intensity
        self.position = _position
        self.direction = _direction

    def get_elements(self):
        return {'type': self.type, 'intensity': self.intensity, 'position': self.position, 'direction': self.direction}
