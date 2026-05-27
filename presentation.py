from manim import *
from manim_slides import Slide
from timeDeriv import TimeDerivationAnimations
from Intro import Intro
from brachistochroneRace import BrachistochroneRace
from derivSnell import DerivationSnellsLaw
from usingSnell import StratifiedMedium
from cycloidDeriv import MathematicalDerivation
class BrachistochronePresentation(Slide,
                                  Intro,
                                  BrachistochroneRace,
                                  TimeDerivationAnimations,
                                  DerivationSnellsLaw,
                                  StratifiedMedium,
                                  MathematicalDerivation):
    def construct(self):
        
       # GİRİŞ --> Bütün insanlar, tarihçe
        """
        self.show_title()
        self.next_slide()

        self.show_timeline()
        self.next_slide()

        self.show_brachistochroneWord()
        self.next_slide()
        # Top bırakma animasyonu

        self.race()
        self.next_slide()

        self.balance()
        self.next_slide()
 
        # İlk derivation snell falan
        """
        self.define_variables_and_functions()
        self.next_slide()
        
        self.snells_law_scene_1()
        self.next_slide()

        self.snells_law_scene_2()
        self.next_slide()
        """
        self.setup_graph()
        self.next_slide()
        
        # 2. Animate the particle sliding down"
        self.animate_particle()
        self.next_slide()
        
        # 3. Zoom into the curve to explicitly show ds, dx, dy
        self.zoom_to_infinitesimal()
        self.next_slide()
        
        # 4. Shrink and move the graph to the left
        self.shrink_and_move_left()
        
        # 5. Derive velocity step-by-step using Energy Conservation
        self.derive_velocity2()
        self.next_slide()

        self.continuous_limit()
        self.next_slide()
        
        self.zoomed_snells_law()
        self.next_slide()
        
        self.snells_law_everywhere()
        self.next_slide()

        self.final_race()
        self.next_slide()
        
        self.cycloid_derivation()
        self.next_slide()
        
        # 1. Setup the initial full-screen graph and points
        self.setup_graph()
        self.next_slide()
        
        # 2. Animate the particle sliding down"
        self.animate_particle()
        self.next_slide()
        
        # 3. Zoom into the curve to explicitly show ds, dx, dy
        self.zoom_to_infinitesimal()
        self.next_slide()
        
        # 4. Shrink and move the graph to the left
        self.shrink_and_move_left()
        
        # 5. Derive velocity step-by-step using Energy Conservation
        self.derive_velocity()
        self.next_slide()
        
        # 6. Derive the final time equation step-by-step
        self.derive_time_equation()
        """


