# derivations.py
from manim import *

class TimeDerivationAnimations:
    def setup_graph(self):
        self.axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 7, 1],
            tips=True,
            axis_config={"include_numbers": True}
        )
        
        self.x_A, self.y_A = 1.0, 5.0
        self.x_B, self.y_B = 6.0, 1.0
        
        self.point_A = Dot(self.axes.c2p(self.x_A, self.y_A), color=RED)
        self.point_B = Dot(self.axes.c2p(self.x_B, self.y_B), color=RED)
        
        self.label_A = MathTex("A(x_A, y_A)").next_to(self.point_A, UP+RIGHT, buff=0.1)
        self.label_B = MathTex("B(x_B, y_B)").next_to(self.point_B, DOWN+RIGHT, buff=0.1)
        
        # Function for a smooth path connecting A and B
        def curve_func(x):
            return (4/25) * (x - 6)**2 + 1
            
        self.curve = self.axes.plot(
            curve_func,
            x_range=[self.x_A, self.x_B],
            color=YELLOW
        )
        
        # Group everything so we can smoothly scale/move it later
        self.graph_group = VGroup(
            self.axes, self.curve, 
            self.point_A, self.point_B, 
            self.label_A, self.label_B
        )
        
        self.play(Create(self.axes))
        self.play(FadeIn(self.point_A, self.label_A), FadeIn(self.point_B, self.label_B))
        self.play(Create(self.curve))

    def animate_particle(self):
        self.particle = Dot(color=BLUE).move_to(self.point_A.get_center())
        # Add to graph_group so it moves when the graph moves
        self.graph_group.add(self.particle)
        
        self.play(FadeIn(self.particle))
        self.wait(0.5)
        self.play(MoveAlongPath(self.particle, self.curve), run_time=2, rate_func=smooth)
        
    def zoom_to_infinitesimal(self):
        def curve_func(x):
            return (4/25) * (x - 6)**2 + 1
            
        # Specific coordinate for the zoom
        zoom_x = 3.5
        zoom_y = curve_func(zoom_x)
        zoom_point = self.axes.c2p(zoom_x, zoom_y)
        
        # Move particle back to the zoom point
        self.play(self.particle.animate.move_to(zoom_point), run_time=1)
        
        # 2. Animate the zoom for the graph ONLY. 
        self.play(self.graph_group.animate.scale(3, about_point=zoom_point), run_time=1.5)
        self.wait(0.2)
        
        dx_val = 0.5
        y_next = curve_func(zoom_x + dx_val)
        
        p1 = self.axes.c2p(zoom_x, zoom_y)
        p2 = self.axes.c2p(zoom_x + dx_val, zoom_y)
        p3 = self.axes.c2p(zoom_x + dx_val, y_next)
        
        self.triangle = VGroup(
            Line(p1, p2, color=GREEN),  # dx
            Line(p2, p3, color=RED),    # dy
            Line(p1, p3, color=BLUE)    # ds (hypotenuse)
        )
        
        self.label_dx = MathTex("dx", color=GREEN).scale(1).next_to(self.triangle[0], UP, buff=0.2)
        self.label_dy = MathTex("dy", color=RED).scale(1).next_to(self.triangle[1], RIGHT, buff=0.25)
        self.label_ds = MathTex("ds", color=BLUE).scale(1).next_to(self.triangle[2], DOWN, buff=0.01)
        
        self.play(Create(self.triangle))
        self.play(Write(self.label_dx), Write(self.label_dy), Write(self.label_ds))
        self.wait(1)
        
        # 5. Smoothly Unzoom everything back to original size.
        zoomed_elements = VGroup(
            self.graph_group,
            self.triangle,
            self.label_dx,
            self.label_dy,
            self.label_ds
        )
        self.next_slide()
        self.play(zoomed_elements.animate.scale(1/3, about_point=zoom_point), run_time=1.5)
        self.graph_group.add(self.triangle, self.label_dx, self.label_dy, self.label_ds)

    def shrink_and_move_left(self):
        self.play(
            self.graph_group.animate.scale(0.45).to_edge(LEFT+DOWN, buff=0.3)
        )

    def _build_velocity_derivation(self):
        """Helper method that builds and animates the velocity derivation."""
        eq1 = MathTex("E_A", "=", "E_P", tex_to_color_map={"E_A": GREEN, "E_P": RED})
        eq2 = MathTex("K_A + U_A", "=", "K_P + U_P", tex_to_color_map={"K_A": GREEN, "U_A": GREEN, "K_P": RED, "U_P": RED})
        eq3 = MathTex("0 + ", "mg y_A", "=", "\\frac{1}{2}mv^2", " + ", "mg y")
        eq3[1].set_color(GREEN)  # mg y_A
        eq3[3].set_color(RED)    # 1/2 mv^2
        eq3[5].set_color(RED)    # mg y
        
        eq4 = MathTex("mg", "(y_A - y)", "=", "\\frac{1}{2}mv^2")
        eq4[0].set_color(GREEN)  # mg
        eq4[1].set_color(GREEN)  # (y_A - y)
        eq4[3].set_color(RED)    # 1/2 mv^2
        
        eq4_delta = MathTex("mg", "\\Delta y", "=", "\\frac{1}{2}mv^2")
        eq4_delta[0].set_color(GREEN)
        eq4_delta[1].set_color(GREEN)
        eq4_delta[3].set_color(RED)

        eq5 = MathTex(r"v = \sqrt{2g {{(y_A - y)}} }")
        eq5_delta = MathTex(r"v = \sqrt{2g {{\Delta y}} }")

        # Arrange the initial equations
        deriv_group = VGroup(eq1, eq3, eq4, eq5).arrange(DOWN, buff=0.4)
        deriv_group.move_to(LEFT * 3.2 + UP)
        
        # Snap the new delta equation exactly to the position of the originals
        eq4_delta.move_to(eq4)
        eq2.move_to(eq1)
        eq5_delta.move_to(eq5)
        
        # Animate the derivation
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(0.5)
        self.play(Write(eq3))
        self.wait(0.5)
        self.play(Write(eq4))
        self.wait(0.5)
        self.next_slide()
        self.play(TransformMatchingTex(eq4, eq4_delta))
        self.wait(0.5)
        self.play(Write(eq5_delta))
        self.wait(0.5)
        
        # Highlight final equation
        self.play(eq5_delta.animate.set_color(YELLOW))
        self.final_velocity_eq = eq5_delta
        
        # Return the final state of the equations so the caller can fade them out
        return VGroup(eq2, eq3, eq4_delta, eq5_delta)

    def derive_velocity(self):
        # Standard derivation, fades out immediately.
        self.deriv_v = self._build_velocity_derivation()
        self.play(FadeOut(self.deriv_v))
        
    def derive_velocity2(self):
        # Derivation that includes the graph group and waits for the next slide.
        self.deriv_v = self._build_velocity_derivation()
        self.deriv_v.add(self.graph_group) 
        self.next_slide()                  
        self.play(FadeOut(self.deriv_v))

    def derive_time_equation(self):
        # Fade out old derivations, slide the velocity equation up
        self.play(
            FadeOut(self.deriv_v[:-1]),
            self.final_velocity_eq.animate.move_to(LEFT * 3.2 + UP * 2.5)
        )
        
        t_eq1 = MathTex(r"v = \frac{ds}{dt} \implies dt = \frac{ds}{v}")
        t_eq1.set_color_by_tex_to_color_map({
            "ds": YELLOW,
        })
        t_eq1Changed = MathTex("v = \\frac{ds}{dt} \\implies dt = \\frac{ds}{\\sqrt{2g\Delta y}}", tex_to_color_map={"\\sqrt{2g\Delta y}": YELLOW, "v": YELLOW})
        t_eq2 = MathTex("ds = \\sqrt{dx^2 + dy^2} = \\sqrt{1 + (y')^2} dx")
        t_eq3 = MathTex("T = \\int_{x_A}^{x_B} \\frac{\\sqrt{1 + (y')^2}}{\\sqrt{2g\Delta y}} dx", tex_to_color_map={"\\sqrt{2g\Delta y}": YELLOW, "T": TEAL})
        
        # Arrange using the TALLER equation (t_eq1Changed) so the spacing stays safe
        self.deriv_t = VGroup(t_eq1Changed, t_eq2, t_eq3).arrange(DOWN, buff=0.8)
        self.deriv_t.move_to(RIGHT * 2.8 + UP * 0.8)
        
        t_eq1.move_to(t_eq1Changed)
        
        # Highlight the final integrand components
        t_eq3[0].set_color(BLUE)
        
        self.play(Write(t_eq1))
        self.wait(0.8)
        
        self.play(TransformMatchingShapes(t_eq1, t_eq1Changed))
        self.wait(0.8)
        
        # 3. Write the remaining equations sequentially
        for eq in [t_eq2, t_eq3]:
            self.play(Write(eq))
            self.wait(0.8)
