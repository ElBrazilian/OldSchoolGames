import pygame
from pygame.locals import *

import time

from lib.Options import Options
from lib.Events import Events

class BaseScene:
    def __init__(self, app, options):
        self.app            = app
        self.window         = app.window
        self.options        = options
        self.loaded         = False
        self.continuer      = True

        self.events         = Events(self,  options.keys)
        self.return_value   = None

        self.last_update_timestamp = time.time()
        self.frame_dt       = 0
        self.last_fps       = []

    def _load(self):
        self.load()

    def run(self):
        if not self.loaded:
            self.load()

        self.continuer      = True
        frame_length        = 1/self.options.fps_target
        physicsframe_length = frame_length / self.options.physics_frame

        last_physics_dt     = 0
        last_frame_dt       = 0

        while self.continuer:
            try:
                frame_dt = 0
                for i in range(self.options.physics_frame):
                    start_physics_frame = time.time()
                    self._physics_update(last_physics_dt)
                    # Update last variables
                    
                    if i == self.options.physics_frame - 1:
                        self._update(last_frame_dt)
                        self._draw()

                        if pygame.event.peek(QUIT):
                            self.continuer = False
                        pygame.event.pump()

                    
                    now = time.time()
                    if now - start_physics_frame <= physicsframe_length:
                        time.sleep(physicsframe_length + start_physics_frame - now)
                    
                    re_now = time.time()
                    last_physics_dt = re_now - start_physics_frame
                    frame_dt += last_physics_dt
                
                last_frame_dt = frame_dt
            except Exception as e:
                self.continuer = False
                raise e

        return self.return_value

    def swap_scene(self, scene):
        """
        Used to quit the current scene and go to "scene"
        """
        self.continuer = False
        self.return_value = scene
            
            

    def _update(self, dt):
        # Handle time
        now = time.time()
        self.frame_dt = now - self.last_update_timestamp
        self.last_update_timestamp = now
        try:
            self.last_fps.append(1/self.frame_dt)
            
            if len(self.last_fps) > self.options.fps_count_average:
                self.last_fps = self.last_fps[-self.options.fps_count_average:]
        except Exception as e:
            pass
        
        
        # handle title
        if self.options.display_fps_count:
            try:
                fps = str(round(sum(self.last_fps)/len(self.last_fps), self.options.fps_rounding))
            except Exception as e:
                fps = 'inf'
            title = f'{self.app.title} [FPS : {fps}]'
            pygame.display.set_caption(title)
            self.app._last_title = self.app.title
        
        elif self.app.title != self.app._last_title:
            pygame.display.set_caption(self.app.title)
            self.app._last_title = self.app.title

        # handle events
        self.events.check()
        if self.events.quitter:
            self.continuer = False

        self.update(dt, self.events)

    def _physics_update(self, dt):
        self.physics_update(dt)

    def _draw(self):
        # self.window
        self.window.fill(self.options.background_color)
        self.draw(self.window)
        
        pygame.display.flip()

