
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
        self.time_between_emission = 1/emission_rate
        self.time_after_emission = self.time_between_emission

        # particle arguments
        self.position = position
        self.direction = direction
        self.speed = speed
        self.lifespan = lifespan
        self.radius = radius
        self.color = color

    def update(self, dt):
        self.time_after_emission += dt
        if self.time_after_emission >= self.time_between_emission:
            particles = int(self.time_after_emission // self.time_between_emission)
            self.time_after_emission -= particles * self.time_between_emission
            ddt = dt/particles
            for particle in range(particles):
                pos = self.position
                pos += self.direction * ddt * self.speed
                self.pool.spawn(self.position, self.direction, self.speed, self.lifespan, self.color, self.radius)
        self.pool.update(dt)