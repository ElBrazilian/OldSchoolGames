from .Particle import Particle

class ParticlePool:
    """

    Variables:
        - particles [list(Particle)]                : the current "alive" particles
        - unused    [list(Particle)]                : list of unused particles, ready to be used again
        - size      [int]                           : the current size of the pool
        - max_size  [int]                           : the maximum size of the pool
    
    Methods:
        - spawn     [*Particle args -> Particle]    : spawns a particle in the pool given the arguments used, and returns this particle
        - remove    [Particle]                      : removes the particle given as argument from the pool
    """
    def __init__(self, ParticleClass):
        self.particles      = []
        self.unused         = []
        self.size           = 0
        self.max_size       = 0
        self.ParticleClass  = ParticleClass

    def spawn(self, *args, **kwargs):
        if self.size < self.max_size:
            # we can use an unused particle
            part = self.unused.pop()
            part.reset(*args, **kwargs)
            self.particles.append(part)
            self.size += 1
            return part
        else:
            part = self.ParticleClass(*args, **kwargs)
            self.particles.append(part)
            self.max_size += 1
            self.size += 1
            return part

    def remove(self, particle):
        self.particles.remove(particle)
        self.unused.append(particle)
        self.size -= 1

    def update(self, dt):
        dead = []
        for particle in self.particles:
            particle.update(dt)
            if particle.life <= 0:
                dead.append(particle)

        for particle in dead:
            self.particles.remove(particle)
            self.unused.append(particle)
            self.size -= 1

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

