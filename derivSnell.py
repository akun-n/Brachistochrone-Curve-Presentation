from manim import *

class DerivationSnellsLaw(Scene):
    def define_variables_and_functions(self):
        # 1. Colors & Variables
        self.color_m1 = BLUE_B
        self.color_m2 = PURPLE_B
        self.color_path = ORANGE
        self.color_labels = GREY_B
        
        # 2. Key Geometric Coordinates
        self.y_interface = 0 
        self.x_a = -3
        self.y_a = 2
        self.x_b = 3
        self.y_b = -3
        
        # 3. Path generator
        def get_refracted_path_points(xo_val):
            return [
                axes.c2p(self.x_a, self.y_a), 
                axes.c2p(xo_val, self.y_interface), 
                axes.c2p(self.x_b, self.y_b)  
            ]
        self.get_refracted_path_points = get_refracted_path_points

    def snells_law_scene_1(self):
        # 1. Title
        title = Tex("How to find the fastest path?").to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.next_slide()
        title2 = Tex("Deriving Snell's Law").to_edge(UP+LEFT, buff=0.5).shift(LEFT*0.7).scale(0.7)
        
        # 2. Geometric Setup & The Principle
        quote = Tex(
            "Fermat's principle:",
            " If a beam of light travels from \\\\",
            "point $A$ to $B$, it does so along the fastest path \\\\",
            "possible.",
            tex_environment="flushleft",
            font_size=48
        )
        
        quote[0].set_color("#5BC2E7") 
        
        self.play(Write(quote))

        self.next_slide()

        self.play(FadeOut(quote))

        global axes 
        # --- SHIFTED UP HERE ---
        # Changed buff from 0.5 to 2.5 to lift the entire grid
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 3, 1],
            axis_config={"color": GREY},
        ).to_edge(DOWN, buff=1.5).to_edge(RIGHT, buff=0.5)
        
        interface = Line(axes.c2p(-5, 0), axes.c2p(5, 0), color=self.color_labels)
        label_m1 = Tex("$n_1, v_1$", color=self.color_m1).move_to(axes.c2p(4.2, 2.4))
        label_m2 = Tex("$n_2, v_2$", color=self.color_m2).move_to(axes.c2p(4.2, -2.4))

        self.play(Create(axes), Create(interface), Write(label_m1), Write(label_m2), title.animate.shift(LEFT*5).scale(0.7), Transform(title, title2))
        # self.next_slide()
        
        point_a_fixed = Dot(axes.c2p(self.x_a, self.y_a), color=YELLOW)
        label_point_a = Tex("A").next_to(point_a_fixed, UP, buff=0.15)
        
        point_b_fixed = Dot(axes.c2p(self.x_b, self.y_b), color=YELLOW)
        label_point_b = Tex("B").next_to(point_b_fixed, DOWN, buff=0.15)
        
        self.play(FadeIn(point_a_fixed, label_point_a), FadeIn(point_b_fixed, label_point_b))
        self.next_slide()
        
        straight_points = [axes.c2p(self.x_a, self.y_a), axes.c2p(self.x_b, self.y_b)]
        straight_path = VMobject().set_points_as_corners(straight_points).set_color(self.color_path).set_opacity(0.3)
        straight_label = Tex("Shortest Distance", color=self.color_path).scale(0.6).next_to(straight_path.get_top(), UP)

        self.play(Create(straight_path), Write(straight_label))
        self.next_slide()
        
        xo_optimal = 1.2 
        refracted_points = self.get_refracted_path_points(xo_optimal)
        
        refracted_path = VMobject().set_points_as_corners(refracted_points).set_color(self.color_path)
        
        point_o = Dot(axes.c2p(xo_optimal, 0), color=YELLOW)
        label_point_o = Tex("O").next_to(point_o, UP, buff=0.15)

        point_d = Dot(axes.c2p(3, 0), color=WHITE).scale(0.7)
        label_point_d = Tex("d").next_to(point_d, UP+RIGHT, buff=0.15)
        
        dash_a = DashedLine(axes.c2p(self.x_a, self.y_a), axes.c2p(self.x_a, 0), color=GREY)
        dash_b = DashedLine(axes.c2p(self.x_b, self.y_b), axes.c2p(self.x_b, 0), color=GREY)

        brace_a = BraceBetweenPoints(axes.c2p(self.x_a, 0), axes.c2p(self.x_a, self.y_a), direction=LEFT)
        label_a = brace_a.get_tex("a")
        
        brace_x = BraceBetweenPoints(axes.c2p(self.x_a, 0), axes.c2p(xo_optimal, 0), direction=DOWN)
        label_x = brace_x.get_tex("x")

        brace_b = BraceBetweenPoints(axes.c2p(self.x_b, self.y_b), axes.c2p(self.x_b, 0), direction=RIGHT)
        label_b = brace_b.get_tex("b")
        
        brace_dx = BraceBetweenPoints(axes.c2p(xo_optimal, 0), axes.c2p(self.x_b, 0), direction=UP)
        label_dx = brace_dx.get_tex("d-x")
        
        self.play(
            ReplacementTransform(straight_path, refracted_path), 
            FadeOut(straight_label), 
            FadeIn(point_o, label_point_o)
        )

        self.play(
            Create(dash_a),
            GrowFromCenter(brace_a), Write(label_a),
            GrowFromCenter(brace_x), Write(label_x),
            GrowFromCenter(point_d), Write(label_point_d)
        )
        # self.next_slide()
        
        self.play(
            Create(dash_b),
            GrowFromCenter(brace_b), Write(label_b),
            GrowFromCenter(brace_dx), Write(label_dx)
        )
        self.next_slide()
        
        path_ao = MathTex(r"AO = \sqrt{a^2 + x^2}", color=self.color_m1).scale(0.75).move_to(axes.c2p(-1.5, 2.3))
        path_ob = MathTex(r"OB = \sqrt{b^2 + (d-x)^2}", color=self.color_m2).scale(0.64).move_to(axes.c2p(1.1, -2.4))
        
        self.play(Write(path_ao))
        self.play(Write(path_ob))
        self.next_slide()
        
        time_eq = MathTex(r"t_{\text{Total}}(x) = \frac{\sqrt{a^2+x^2}}{v_1} + \frac{\sqrt{b^2+(d-x)^2}}{v_2}").scale(0.8).move_to(axes.c2p(-3.3, -2))
        self.play(Write(time_eq))
        
        self.next_slide()
        goal_text = Tex(r"Minimize $t \implies \frac{dt}{dx} = 0$").scale(0.8).next_to(time_eq, DOWN, buff=0.5)
        derivative_full = MathTex(r"\frac{dt}{dx} = \frac{1}{v_1} \frac{2x}{2\sqrt{a^2+x^2}} + \frac{1}{v_2} \frac{-2(d-x)}{2\sqrt{b^2+(d-x)^2}} = 0").scale(0.7).next_to(time_eq, DOWN, buff=0.5)
        self.play(Write(goal_text))
        
        self.next_slide()
        self.play(ReplacementTransform(goal_text, derivative_full))
        
        self.next_slide()
        
        derivative_simple = MathTex(r"\frac{x}{v_1 \sqrt{a^2+x^2}} - \frac{(d-x)}{v_2 \sqrt{b^2+(d-x)^2}} = 0").scale(0.75).next_to(time_eq, DOWN, buff=0.5)
        self.play(ReplacementTransform(derivative_full, derivative_simple))
        
        self.next_slide()
        self.play(*[FadeOut(m) for m in self.mobjects])

    def snells_law_scene_2(self):
        self.define_variables_and_functions()
        
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 3, 1],
            axis_config={"color": GREY},
        ).to_edge(DOWN, buff=1.5).to_edge(RIGHT, buff=0.5)
        
        interface = Line(axes.c2p(-5, 0), axes.c2p(5, 0), color=self.color_labels)
        xo_optimal = 1.2
        refracted_points = self.get_refracted_path_points(xo_optimal)
        refracted_path = VMobject().set_points_as_corners(refracted_points).set_color(self.color_path)
        
        point_a_fixed = Dot(axes.c2p(self.x_a, self.y_a), color=YELLOW)
        label_point_a = Tex("A").next_to(point_a_fixed, UP, buff=0.15)
        
        point_o = Dot(axes.c2p(xo_optimal, 0), color=YELLOW)
        label_point_o = Tex("O").next_to(point_o, UP+RIGHT, buff=0.05)
        
        point_b_fixed = Dot(axes.c2p(self.x_b, self.y_b), color=YELLOW)
        label_point_b = Tex("B").next_to(point_b_fixed, DOWN, buff=0.15)
        
        self.play(FadeIn(
            axes, interface, refracted_path, 
            point_a_fixed, label_point_a, 
            point_b_fixed, label_point_b, 
            point_o, label_point_o
        ))

        derivative_simple = MathTex(r"\frac{x}{v_1 \sqrt{a^2+x^2}} - \frac{(d-x)}{v_2 \sqrt{b^2+(d-x)^2}} = 0").scale(0.7).to_edge(UP, buff=1).to_edge(RIGHT, buff=0.5)
        self.play(Write(derivative_simple))

        path_ao = MathTex(r"AO = \sqrt{a^2 + x^2}", color=self.color_m1).scale(0.75).move_to(axes.c2p(-5, 2.3))
        path_ob = MathTex(r"OB = \sqrt{b^2 + (d-x)^2}", color=self.color_m2).scale(0.75).move_to(axes.c2p(-4.6, 1.6))
        
        self.next_slide()
        
        self.play(Write(path_ao), Write(path_ob))
        
        normal = DashedLine(axes.c2p(xo_optimal, -3), axes.c2p(xo_optimal, 3), color=self.color_labels)
        angle_i = Tex(r"$\theta_i$").scale(0.6).move_to(axes.c2p(xo_optimal-0.2, 0.5))
        angle_t = Tex(r"$\theta_t$").scale(0.6).move_to(axes.c2p(xo_optimal+0.2, -0.6))
        
        triangle_m1_points = [axes.c2p(xo_optimal, 0), axes.c2p(self.x_a, 0), axes.c2p(self.x_a, self.y_a), axes.c2p(xo_optimal, 0)]
        triangle_m1 = VMobject().set_points_as_corners(triangle_m1_points).set_color(self.color_m1)
        label_tri_m1 = Tex("AO", color=self.color_m1).scale(0.8).next_to(triangle_m1, UP, buff=0.01)
        
        triangle_m2_points = [axes.c2p(xo_optimal, 0), axes.c2p(self.x_b, 0), axes.c2p(self.x_b, self.y_b), axes.c2p(xo_optimal, 0)]
        triangle_m2 = VMobject().set_points_as_corners(triangle_m2_points).set_color(self.color_m2)
        label_tri_m2 = Tex("OB", color=self.color_m2).scale(0.8).next_to(triangle_m2, DOWN, buff=0.1)
        self.next_slide()
        self.play(FadeIn(normal))
        self.play(FadeIn(triangle_m1, label_tri_m1, angle_i))
        self.next_slide()
        self.play(FadeIn(triangle_m2, label_tri_m2, angle_t))
        self.next_slide()
        
        sin_definitions_group = VGroup()
        sin_i_def = MathTex(r"\sin\theta_i = \frac{x}{\sqrt{a^2+x^2}}", color=self.color_m1).scale(0.8)
        sin_t_def = MathTex(r"\sin\theta_t = \frac{d-x}{\sqrt{b^2+(d-x)^2}}", color=self.color_m2).scale(0.8)
        
        sin_definitions_group.add(sin_i_def, sin_t_def).arrange(DOWN, buff=0.3).move_to(axes.c2p(-2.5, -2))
        
        self.play(Write(sin_definitions_group))
        self.next_slide()
        
        # --- COMBINING ANIMATION ---
        connection_intermediate = MathTex(r"\frac{\sin\theta_i}{v_1} - \frac{\sin\theta_t}{v_2} = 0").scale(0.8).move_to(derivative_simple)
        connection_result = MathTex(r"\frac{\sin\theta_i}{v_1} - \frac{\sin\theta_t}{v_2} = 0").scale(0.8).move_to(connection_intermediate)
        
        self.play(TransformMatchingShapes(derivative_simple, connection_result))
        self.next_slide()
        
        connection_result2 = MathTex(r"\frac{\sin\theta_i}{v_1} = \frac{\sin\theta_t}{v_2}", color=YELLOW).scale(0.8).move_to(connection_intermediate)
        self.play(TransformMatchingShapes(connection_result, connection_result2))
        
        self.next_slide()
        # --- NEW STEP-BY-STEP ALGEBRA BREAKDOWN ---
        # Explicitly show v1 and v2 substitution to make it clear for the audience
        ref_definition = MathTex(r"n = \frac{c}{v} \implies v_1 = \frac{c}{n_1}, \ v_2 = \frac{c}{n_2}").scale(0.8).move_to(axes.c2p(-3,-2))
        self.play(Write(ref_definition), FadeOut(sin_definitions_group))
        self.next_slide()
        
        # Step A: Substitute c/n into the denominators
        sub_eq_1 = MathTex(r"\frac{\sin\theta_i}{c/n_1} = \frac{\sin\theta_t}{c/n_2}").scale(0.8).move_to(connection_result2)
        self.play(TransformMatchingShapes(connection_result2, sub_eq_1))
        self.next_slide()

        # Step B: Flip the denominators up
        sub_eq_2 = MathTex(r"\frac{n_1 \sin\theta_i}{c} = \frac{n_2 \sin\theta_t}{c}").scale(0.8).move_to(sub_eq_1)
        self.play(TransformMatchingShapes(sub_eq_1, sub_eq_2))
        self.next_slide()
        
        # Step C: Cancel 'c' for the Final Equation
        final_eq = MathTex(r"n_1 \sin\theta_i = n_2 \sin\theta_t", color=YELLOW).scale(1.1).next_to(ref_definition, DOWN, buff=0.6)
        self.play(ReplacementTransform(sub_eq_2, final_eq))
        self.next_slide()

        # --- FADE OUT EVERYTHING ---
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)