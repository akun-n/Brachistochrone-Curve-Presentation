from manim import *
import numpy as np

# Note: Ensure your class inherits from Slide (manim-slides) if you are using self.next_slide()
class MathematicalDerivation(Scene):
    def cycloid_derivation(self):
        # ==========================================
        # TITLE ANIMATION
        # ==========================================
        title = Text("Snell's Law to Cycloid", color=ORANGE)
        
        self.play(Write(title))
        self.next_slide()
        
        self.play(title.animate.scale(0.65).to_edge(UP, buff=0.3))

        # ==========================================
        # ACT 1: THE INFINITESIMAL TRIANGLE
        # ==========================================
        
        # Center of the triangle geometry shifted right to avoid the border
        col1_x = -3.8
        C = np.array([col1_x, 1, 0])
        
        dy_line = Line(C, C + DOWN * 3, color=BLUE)
        dx_line = Line(C + DOWN * 3, C + DOWN * 3 + RIGHT * 4, color=GREEN)
        ds_line = Line(C, C + DOWN * 3 + RIGHT * 4, color=YELLOW)
        
        normal_up = DashedLine(C, C + UP * 2, color=WHITE)
        
        # Explicit visible dashed line extending backwards from ds to anchor theta
        ext_dir = np.array([-4, 3, 0]) / 5.0 # Normalized direction going up-left
        ds_extension = DashedLine(C, C + ext_dir * 2.0, color=WHITE)
        
        angle_arc = Angle(normal_up, ds_extension, radius=1.0, color=WHITE)
        theta_lab = MathTex(r"\theta").next_to(angle_arc, UP, buff=0.04)

        dy_lab = MathTex("dy", color=BLUE).next_to(dy_line, LEFT, buff=0.2)
        dx_lab = MathTex("dx", color=GREEN).next_to(dx_line, DOWN, buff=0.2)
        ds_lab = MathTex("ds", color=YELLOW).move_to(ds_line.get_center() + UP * 0.4 + RIGHT * 0.4)

        triangle_group = VGroup(
            dy_line, dx_line, ds_line, normal_up, 
            ds_extension, angle_arc, theta_lab, dy_lab, dx_lab, ds_lab
        )
        
        self.play(
            Create(normal_up), Create(ds_line), Create(ds_extension), 
            Create(angle_arc), Write(theta_lab), Write(ds_lab)
        )
        self.play(Create(dy_line), Write(dy_lab), Create(dx_line), Write(dx_lab))
        self.next_slide()

        # Right Column for Act 1 Equations
        col2_x = 2.0
        eq1 = MathTex(r"\sin(\theta) = \frac{dx}{ds}").move_to(np.array([col2_x, 1.5, 0]))
        self.play(Write(eq1))
        self.next_slide()

        eq2 = MathTex(r"\sin(\theta) = \frac{dx}{\sqrt{dx^2 + dy^2}}").next_to(eq1, DOWN, buff=0.8).align_to(eq1, LEFT)
        self.play(TransformFromCopy(eq1, eq2))
        self.next_slide()

        # In-place simplification
        eq3 = MathTex(r"\sin(\theta) = \frac{1}{\sqrt{1 + (y')^2}}").move_to(eq2).align_to(eq1, LEFT)
        div_text = Text("Divide by dx", font_size=24, color=GREY).next_to(eq2, DOWN, buff=0.5)
        
        self.play(FadeIn(div_text, shift=LEFT * 0.2))
        self.play(ReplacementTransform(eq2, eq3), FadeOut(div_text))
        self.next_slide()

        # ==========================================
        # ACT 2: SNELL'S LAW (TWO-COLUMN LAYOUT)
        # ==========================================
        
        # Clear geometry, move eq3 to act as the header of the Left Column
        self.play(
            FadeOut(triangle_group), FadeOut(eq1),
            eq3.animate.move_to(np.array([col1_x, 2.0, 0]))
        )

        # Left Column progression
        snell = MathTex(r"\frac{\sin(\theta)}{\sqrt{y}} = C").next_to(eq3, DOWN, buff=1.0).align_to(eq3, LEFT)
        self.play(Write(snell))
        self.next_slide()
        
        step1 = MathTex(r"\frac{1}{\sqrt{y} \sqrt{1 + (y')^2}} = C").next_to(snell, DOWN, buff=1.0).align_to(eq3, LEFT)
        self.play(TransformFromCopy(VGroup(eq3, snell), step1))
        self.next_slide()
        
        # Move to Right Column progression
        step2 = MathTex(r"\frac{1}{y(1 + (y')^2)} = C^2").move_to(np.array([col2_x, 2.0, 0]))
        self.play(TransformFromCopy(step1, step2))
        self.next_slide()
        
        step3 = MathTex(r"y(1 + (y')^2) = \frac{1}{C^2}").next_to(step2, DOWN, buff=0.8).align_to(step2, LEFT)
        self.play(TransformFromCopy(step2, step3))
        self.next_slide()
        
        # In-place swap for 2a
        step4 = MathTex(r"y(1 + (y')^2) = 2a").move_to(step3).align_to(step2, LEFT)
        note_2a = Text("Let 1/C² = 2a", font_size=24, color=YELLOW).next_to(step4, UP, buff=0.2).align_to(step2, LEFT)
        
        self.play(FadeIn(note_2a))
        self.play(ReplacementTransform(step3, step4))
        self.next_slide()
        
        step5 = MathTex(r"\frac{dy}{dx} = \sqrt{\frac{2a - y}{y}}").next_to(step4, DOWN, buff=0.8).align_to(step2, LEFT)
        self.play(TransformFromCopy(step4, step5))
        self.next_slide()

        # ==========================================
        # ACT 3: PARAMETRIC SOLUTION
        # ==========================================
        
        # Keep only the final slope equation, move it to Left Column Top
        self.play(
            FadeOut(eq3), FadeOut(snell), FadeOut(step1), 
            FadeOut(step2), FadeOut(note_2a), FadeOut(step4),
            step5.animate.move_to(np.array([col1_x, 2.0, 0]))
        )
        
        # Left Column
        eq_y = MathTex(r"y = a(1 - \cos\phi)").next_to(step5, DOWN, buff=1.0).align_to(step5, LEFT)
        sub_text = Text("Substitute y:", font_size=24, color=BLUE).next_to(eq_y, UP, buff=0.2).align_to(step5, LEFT)
        self.play(Write(sub_text), Write(eq_y))
        self.next_slide()
        
        slope_phi = MathTex(r"\frac{dy}{dx} = \frac{\sin\phi}{1 - \cos\phi}").next_to(eq_y, DOWN, buff=1.0).align_to(step5, LEFT)
        self.play(TransformFromCopy(VGroup(step5, eq_y), slope_phi))
        self.next_slide()
        
        # Right Column
        eq_dy = MathTex(r"dy = a\sin\phi \, d\phi").move_to(np.array([col2_x, 2.0, 0]))
        self.play(TransformFromCopy(eq_y, eq_dy))
        self.next_slide()
        
        eq_dx1 = MathTex(r"dx = \frac{dy}{dy/dx} = \frac{a\sin\phi \, d\phi}{\frac{\sin\phi}{1 - \cos\phi}}").next_to(eq_dy, DOWN, buff=0.8).align_to(eq_dy, LEFT)
        self.play(TransformFromCopy(VGroup(slope_phi, eq_dy), eq_dx1))
        self.next_slide()
        
        eq_dx2 = MathTex(r"dx = a(1 - \cos\phi) \, d\phi").move_to(eq_dx1).align_to(eq_dy, LEFT)
        self.play(ReplacementTransform(eq_dx1, eq_dx2))
        self.next_slide()
        
        eq_x = MathTex(r"x = a(\phi - \sin\phi)").next_to(eq_dx2, DOWN, buff=1.0).align_to(eq_dy, LEFT)
        int_text = Text("Integrate dx:", font_size=24, color=GREEN).next_to(eq_x, UP, buff=0.2).align_to(eq_dy, LEFT)
        
        self.play(FadeIn(int_text))
        self.play(TransformFromCopy(eq_dx2, eq_x))
        self.next_slide()

        # ==========================================
        # THE GRAND FINALE
        # ==========================================
        
        # Wipe away everything except the final x and y
        mobs_to_keep = [title, eq_x, eq_y]
        self.play(*[FadeOut(m) for m in self.mobjects if m not in mobs_to_keep])

        # Anchor them neatly at the center of the screen
        self.play(
            eq_x.animate.move_to(np.array([-2.5, 0, 0])).scale(1.2),
            eq_y.animate.move_to(np.array([2.5, 0, 0])).scale(1.2)
        )

        box = SurroundingRectangle(VGroup(eq_x, eq_y), color=YELLOW, buff=0.5)
        cycloid_label = Text("The Cycloid Equations!", color=YELLOW, font_size=40).next_to(box, DOWN, buff=0.8)
        
        self.play(Create(box))
        self.play(Write(cycloid_label))
        self.next_slide()

        # Final absolute wipe of all screen components
        

        # ==========================================
        # THE GRAND FINALE
        # ==========================================

        # ==========================================
        # ACT 4: GRAPHING THE MATH
        # ==========================================
        
        # Smooth transition: Fade out titles/boxes and move equations to act as a legend
        self.play(FadeOut(box), FadeOut(cycloid_label))
        eq_temp = Tex("temp").to_corner(UR, buff=1.5)
        self.play(eq_x.animate.scale(0.7).move_to(eq_temp),
                  eq_y.animate.scale(0.7).next_to(eq_temp, DOWN, buff=0.3))
        # Build Axes (Strict 1:1 Aspect  so the rolling circle doesn't distort!)
        # x span = 15. If x_length = 10, scale factor is 10/15 = 2/3.
        # y span = 4.  y_length MUST be 4 * (2/3) = 8/3 (approx 2.66) to keep 1:1 ratio.
        axes = Axes(
            x_range=[-1, 14, 2],
            y_range=[-1, 3, 1],
            x_length=10,
            y_length=8/3,
            axis_config={"color": GREY},
        ).to_edge(DOWN, buff=1.0).shift(LEFT * 1)
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axes_labels))
        self.next_slide()

        # The math logic (setting a = 1.0 for the graph)
        a = 1.0
        def parametric_cycloid(phi):
            x = a * (phi - np.sin(phi))
            y = a * (1 - np.cos(phi))
            return axes.c2p(x, y)

        # Plot 2 full arches (4 * PI)
        cycloid_curve = ParametricFunction(
            parametric_cycloid, 
            t_range=[0, 4 * PI], 
            color=YELLOW, 
            stroke_width=4
        )
        
        trace_dot = Dot(color=WHITE).move_to(parametric_cycloid(0))
        phi_tracker = ValueTracker(0)
        
        trace_dot.add_updater(
            lambda d: d.move_to(parametric_cycloid(phi_tracker.get_value()))
        )

        # Trace the mathematical curve forward
        self.play(FadeIn(trace_dot))
        self.play(
            Create(cycloid_curve),
            phi_tracker.animate.set_value(4 * PI),
            run_time=4,
            rate_func=linear
        )
        self.next_slide()

        # THE ULTIMATE PROOF: 
        # Spawn a physical circle to roll backward along the math curve!
        
        # Calculate physical radius length on screen
        r_screen = axes.c2p(a, 0)[0] - axes.c2p(0, 0)[0]
        circle = Circle(radius=r_screen, color=BLUE, stroke_width=2)
        radius_line = Line(color=WHITE, stroke_width=2)
        
        def update_circle(c):
            phi = phi_tracker.get_value()
            # c2p already returns an [x, y, z] array, so we pass it directly!
            c.move_to(axes.c2p(a * phi, a))
            
        def update_radius_line(l):
            phi = phi_tracker.get_value()
            center = axes.c2p(a * phi, a)
            edge_pt = parametric_cycloid(phi)
            l.put_start_and_end_on(center, edge_pt)
            
        circle.add_updater(update_circle)
        radius_line.add_updater(update_radius_line)
        
        self.play(FadeIn(circle), FadeIn(radius_line))
        self.next_slide()
        
        # Roll it backward to 0 to show the math exactly equals a rolling wheel
        self.play(
            phi_tracker.animate.set_value(0),
            run_time=4,
            rate_func=smooth
        )
        self.next_slide()

        # Final absolute wipe of all screen components
        circle.clear_updaters()
        radius_line.clear_updaters()
        trace_dot.clear_updaters()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)