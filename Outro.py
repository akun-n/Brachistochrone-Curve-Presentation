from manim import *
import numpy as np
import random
import math

class Outro(Scene):
    def questions_section(self):
        """Dynamic Q&A loop with TRUE mathematically perfect physics races."""
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
        
        q_title = Text("Questions?", font_size=72, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(q_title))

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=5,
            axis_config={"color": DARK_GREY, "stroke_opacity": 0.5},
        ).shift(DOWN * 0.5)
        
        self.play(FadeIn(axes))

        # ==========================================
        # 1. THE MATH SOLVERS
        # ==========================================

        # Solves the transcendental equation for the true Cycloid parameter theta_f
        def solve_theta_f(dx, dy):
            K = dy / dx
            low, high = 0.001, 2 * PI
            for _ in range(50): 
                mid = (low + high) / 2
                val = (1 - np.cos(mid)) / (mid - np.sin(mid))
                if val > K:
                    low = mid
                else:
                    high = mid
            return (low + high) / 2

        # Universal Gravitational Integrator
        # Calculates the exact time and real velocity profile for ANY curve
        def get_physics_profile(path, start_y, g=5.0):
            num_samples = 250
            alphas = np.linspace(0, 1, num_samples)
            points = [path.point_from_proportion(a) for a in alphas]
            
            times = [0.0]
            total_time = 0.0
            
            # Numerically integrate time: dt = 2*ds / (v1 + v2)
            for i in range(1, num_samples):
                p1 = points[i-1]
                p2 = points[i]
                ds = np.linalg.norm(p2 - p1)
                
                # Calculate vertical drop from start (Manim +Y is up)
                drop1 = max(start_y - p1[1], 0.0)
                drop2 = max(start_y - p2[1], 0.0)
                
                # v = sqrt(2gy)
                v1 = np.sqrt(2 * g * drop1)
                v2 = np.sqrt(2 * g * drop2)
                
                if v1 + v2 == 0:
                    dt = 0.0
                else:
                    dt = 2 * ds / (v1 + v2)
                    
                total_time += dt
                times.append(total_time)
                
            normalized_times = np.array(times) / total_time
            
            def true_rate_func(t):
                # Maps linear time (0 to 1) to the actual physical position (alpha) on the curve
                return np.clip(np.interp(t, normalized_times, alphas), 0.0, 1.0)
                
            return total_time, true_rate_func

        # ==========================================
        # 2. THE RACE LOOP
        # ==========================================
        loop_count = 10 

        for i in range(loop_count):
            # Randomize points
            x_a = random.uniform(0.5, 3.0)
            y_a = random.uniform(4.0, 5.5)
            x_b = random.uniform(7.0, 9.5)
            y_b = random.uniform(0.5, 2.0)
            
            dx = x_b - x_a
            dy = y_a - y_b

            pA = axes.c2p(x_a, y_a)
            pB = axes.c2p(x_b, y_b)

            dot_A = Dot(pA, color=WHITE, radius=0.08)
            dot_B = Dot(pB, color=WHITE, radius=0.08)
            label_A = MathTex("A").scale(0.7).next_to(dot_A, UP, buff=0.1)
            label_B = MathTex("B").scale(0.7).next_to(dot_B, RIGHT, buff=0.1)

            # Generate the true Cycloid equations
            theta_f = solve_theta_f(dx, dy)
            R = dy / (1 - np.cos(theta_f))
            
            def true_cycloid(t):
                x = x_a + R * (t - np.sin(t))
                y = y_a - R * (1 - np.cos(t))
                return axes.c2p(x, y)

            # Define the 4 competitor paths
            path_straight = Line(pA, pB, color=BLUE, stroke_width=2, stroke_opacity=0.6)
            
            # The "Top Curve" (Shallow): Arcs strictly above the straight line
            path_shallow = ArcBetweenPoints(pA, pB, angle=PI/4, color=GREEN, stroke_width=2, stroke_opacity=0.6)
            
            # The "Steep Curve" (Bottom): Drops straight down, then cuts across
            p_corner = axes.c2p(x_a, y_b)
            path_steep = CubicBezier(pA, p_corner, p_corner, pB, color=RED, stroke_width=2, stroke_opacity=0.6)
            
            # The Mathematically Perfect Cycloid
            path_brach = ParametricFunction(true_cycloid, t_range=[0, theta_f], color=YELLOW, stroke_width=4)

            paths = VGroup(path_straight, path_shallow, path_steep, path_brach)
            
            self.play(FadeIn(dot_A), FadeIn(dot_B), FadeIn(label_A), FadeIn(label_B), run_time=0.5)
            self.play(*[Create(p) for p in paths], run_time=1.5, rate_func=rate_functions.ease_in_out_sine)

            # ==========================================
            # 3. APPLY TRUE PHYSICS
            # ==========================================
            # By passing all 4 paths through the exact same gravitational integration,
            # we guarantee the race is mathematically fair and accurate.
            start_y_screen = pA[1] 
            
            t_straight, rate_straight = get_physics_profile(path_straight, start_y_screen)
            t_shallow, rate_shallow = get_physics_profile(path_shallow, start_y_screen)
            t_steep, rate_steep = get_physics_profile(path_steep, start_y_screen)
            t_brach, rate_brach = get_physics_profile(path_brach, start_y_screen)

            balls = VGroup(*[Dot(pA, radius=0.1, color=WHITE) for _ in range(4)])
            self.add(balls)

            # Race using the true calculated times and true acceleration curves!
            self.play(
                MoveAlongPath(balls[0], path_straight, run_time=t_straight, rate_func=rate_straight),
                MoveAlongPath(balls[1], path_shallow, run_time=t_shallow, rate_func=rate_shallow),
                MoveAlongPath(balls[2], path_steep, run_time=t_steep, rate_func=rate_steep),
                MoveAlongPath(balls[3], path_brach, run_time=t_brach, rate_func=rate_brach),
            )
            
            flash = Flash(pB, color=YELLOW, line_length=0.2, num_lines=8)
            self.play(path_brach.animate.set_stroke(width=8, opacity=0.8), flash, run_time=0.5)
            self.play(path_brach.animate.set_stroke(width=4, opacity=1.0), run_time=0.5)
            
            self.wait(1.5)
            self.play(FadeOut(VGroup(dot_A, dot_B, label_A, label_B, paths, balls)), run_time=0.5)

        self.next_slide()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def resources_section(self):
        """Clean resource list with accurate MLA citations."""
        title = Text("Resources & Works Cited", color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Using font_size 18 to ensure all MLA citations fit beautifully on the screen
        resources = VGroup(
            Text("1. 3Blue1Brown. \"The Brachistochrone, with Steven Strogatz.\" YouTube, 1 Apr. 2016.", font_size=18),
            Text("2. 3Blue1Brown. \"Snell's law proof using springs.\" YouTube, 1 Apr. 2016.", font_size=18),
            Text("3. Physics Ninja. \"The Brachistochrone Problem - Curve of Fastest Time.\" YouTube, 28 Jul. 2023.", font_size=18),
            Text("4. \"Gemini.\" Gemini, Google, 30 May 2026.", font_size=18),
            Text("5. akun-n. \"Brachistochrone-Curve-Presentation.\" GitHub.", font_size=18),
            Text("6. Bernoulli, Johann. \"Problema Novum Ad Cujus Solutionem Mathematici Invitantur.\" Acta Eruditorum, 1696.", font_size=18),
            Text("7. Levi, Mark. The Mathematical Mechanic. Princeton University Press, 2009.", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.5).shift(RIGHT * 0.5)

        # Smaller radius for the bullets to match the refined text size
        bullets = VGroup(*[Dot(color=BLUE, radius=0.05).next_to(res, LEFT, buff=0.2) for res in resources])

        # Shift the entire block to center it nicely (without assigning to an unused variable)
        VGroup(bullets, resources).move_to(ORIGIN).shift(DOWN * 0.2)

        self.play(
            AnimationGroup(
                *[FadeIn(VGroup(b, r), shift=RIGHT * 0.5) for b, r in zip(bullets, resources)],
                lag_ratio=0.1
            )
        )

        footer = Text("Prepared by Aykun Nersesyan", font_size=20, color=GREY).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(footer))

        self.next_slide()
        self.play(*[FadeOut(mob) for mob in self.mobjects])