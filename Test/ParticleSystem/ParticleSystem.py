
class ParticleSystem:

    def __init__(self):
        """
        

        Variables:
            - emitters              [list(Emitters)]    : list of all emitters in 
        
        Functions:
            - remove_emitter        [Emitter]           : remove the emitter given as argument from the particle system
            - remove_all_emitters   []                  : remove all emitters from the particle system

        """
        self.emitters = []

    def remove_emitter(emitter):
        #emitter.remove()
        self.emitters.remove(emitter)
    def remove_all_emitters():
        #for emitter in self.emitters:
        #    emitter.remove()
        self.emitters = []


