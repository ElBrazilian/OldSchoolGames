
from .ParticlePool import ParticlePool
from .Particle import *

class Emitter:
    def __init__(self, system):
        self.system = system
    
    def update(self, system):
        pass

    def draw(self, fenetre):
        self.pool.draw(fenetre)

class LinearEmitter(Emitter):
    def __init__(self, system, emission_rate, position, direction, speed, lifespan, color, radius):
        super().__init__(system)

        self.pool = ParticlePool(RoundParticle)
        self._emission_rate = emission_rate

        # particle arguments
        self.position = position
        self.direction = direction
        self.speed = speed
        self.lifespan = lifespan
        self.radius = radius
        self.color = color

        self.time = 0
        if type(self._emission_rate) == types.FunctionType:
            self.time_between_emission = 1/emission_rate(self)
        else:
            self.time_between_emission = 1/emission_rate
        self.time_after_emission = self.time_between_emission

    def emission_rate(self):
        if type(self._emission_rate) == types.FunctionType:
            return self._emission_rate(self)
        else:
            return self._emission_rate
    def color(self):
        if type(self._color) == types.FunctionType:
            return self._color(self)
        else:
            return self._color

    def update(self, dt):
        self.time_after_emission += dt
        self.time += dt

        if type(self.speed) == types.FunctionType:
            speed = self.speed(self)
        else:
            speed = self.speed
        if type(self.direction) == types.FunctionType:
            direction = self.direction(self)
        else:
            direction = self.direction



        if self.time_after_emission >= self.time_between_emission:
            particles = int(self.time_after_emission // self.time_between_emission)
            self.time_after_emission -= particles * self.time_between_emission
            ddt = dt/particles
            for particle in range(particles):
                pos = self.position
                pos += direction * ddt * speed
                self.pool.spawn(pos, self.direction, self.speed, self.lifespan, self.color, self.radius)
        
            self.time_between_emission = 1/self.emission_rate()
        self.pool.update(dt)

