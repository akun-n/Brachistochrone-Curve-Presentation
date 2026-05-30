from manim import *

class StratifiedMedium(Scene):
    def continuous_limit(self):
        """Method 1: The transition to the continuum limit"""
        total_height = 6.0 
        num_layers_start = 6
        
        def get_layers(num):
            group = VGroup()
            colors = color_gradient(["#1E5974", "#A2CFDE"], num)
            h = total_height / num
            for i in range(num):
                rect = Rectangle(
                    width=config.frame_width, height=h, 
                    fill_color=colors[i], fill_opacity=1, stroke_width=0
                )
                group.add(rect)
            group.arrange(DOWN, buff=0)
            return group
        # Discrete Setup
        layers_discrete = get_layers(num_layers_start)
        self.play(FadeIn(layers_discrete, run_time=1.5))
        
        eqs = VGroup()
        for i in range(3):
            eq = MathTex(rf"v_{i+1} = \sqrt{{y_{i+1}}}")
            eq.move_to(np.array([-2, layers_discrete[i].get_center()[1], 0]))
            eqs.add(eq)
        self.play(Write(eqs, lag_ratio=0.3))
        
        braces = VGroup()
        brace_labels = VGroup()
        top_y = layers_discrete[0].get_top()[1]
        start_x_pos = 1.5
        x_step = 1.2
        
        for i in range(3):
            bottom_y = layers_discrete[i].get_bottom()[1]
            current_x = start_x_pos + (i * x_step)
            brace = BraceBetweenPoints(np.array([current_x, top_y, 0]), np.array([current_x, bottom_y, 0]), direction=RIGHT)
            label = brace.get_tex(f"y_{i+1}")
            braces.add(brace)
            brace_labels.add(label)

        for i in range(3):
            self.play(GrowFromCenter(braces[i]), Write(brace_labels[i]), run_time=0.6)
        
        self.next_slide() 
        
        # Transition to Continuum
        self.play(FadeOut(eqs), FadeOut(braces), FadeOut(brace_labels))
        
        layers_12 = get_layers(12)
        layers_24 = get_layers(24)
        layers_100 = get_layers(100) 
        
        self.play(ReplacementTransform(layers_discrete, layers_12), run_time=0.8)
        self.play(ReplacementTransform(layers_12, layers_24), run_time=0.8)
        self.play(ReplacementTransform(layers_24, layers_100), run_time=1.5)
        
        cont_eq = MathTex(r"v(y) = \sqrt{y}", font_size=72, color=WHITE)
        
        self.play(FadeIn(cont_eq, shift=UP*0.5))
        self.next_slide()
        
        # --- SMOOTH TRANSITION OUT ---
        # Fade everything out cleanly before the next scene
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)


    def zoomed_snells_law(self):
        total_height = 6.0 
        num_layers = 6
        layer_height = total_height / num_layers
        colors = ["#1E5974", "#307490", "#518CA3", "#6FAABF", "#8CBCCC", "#A2CFDE"]
        
        layers = VGroup()
        for i in range(num_layers):
            rect = Rectangle(
                width=config.frame_width, height=layer_height, 
                fill_color=colors[i], fill_opacity=1, stroke_width=0
            )
            layers.add(rect)
        layers.arrange(DOWN, buff=0)
        
        self.play(FadeIn(layers))

        eqs = VGroup()
        for i in range(3):
            eq = MathTex(rf"v_{i+1} = \sqrt{{y_{i+1}}}")
            eq.move_to(np.array([-2, layers[i].get_center()[1], 0]))
            eqs.add(eq)
        self.play(FadeIn(eqs))

        # 1. Helper function: Hollow box made of Lines
        def get_hollow_box(w, h, color, sw):
            hw, hh = w / 2, h / 2
            top = Line(LEFT*hw + UP*hh, RIGHT*hw + UP*hh, color=color, stroke_width=sw)
            bot = Line(LEFT*hw + DOWN*hh, RIGHT*hw + DOWN*hh, color=color, stroke_width=sw)
            left = Line(LEFT*hw + UP*hh, LEFT*hw + DOWN*hh, color=color, stroke_width=sw)
            right = Line(RIGHT*hw + UP*hh, RIGHT*hw + DOWN*hh, color=color, stroke_width=sw)
            return VGroup(top, bot, left, right)

        # 2. Draw the path
        def axes_pt(x, y): return RIGHT * x + UP * y
        p0 = axes_pt(-5.5, 3)
        p1 = axes_pt(-4.5, 2)  
        p2 = axes_pt(-3.2, 1)  
        p3 = axes_pt(-1.6, 0)  
        p4 = axes_pt(0.3, -1)
        p5 = axes_pt(2.5, -2)
        p6 = axes_pt(5.0, -3)
        
        path = VMobject().set_points_as_corners([p0, p1, p2, p3, p4, p5, p6]).set_color(YELLOW).set_stroke(width=3)
        self.play(Create(path), run_time=2)

        self.next_slide()

        # 3. Create the Highlight Box at p1
        box_size = 0.8
        highlight_box = get_hollow_box(box_size, box_size, GREEN_B, 3).move_to(p1)
        self.play(Create(highlight_box))

        # 4. Helper functions to generate the Inset Panel dynamically
        inset_center = RIGHT * 3.5 + UP * 0.5
        inset_w, inset_h = 4.5, 4.5

        def build_inset_base(color_top, color_bot, dx_in, dx_out, label_1, label_2):
            """Builds everything in the inset EXCEPT the equation."""
            bg_top = Rectangle(width=inset_w, height=inset_h/2, fill_color=color_top, fill_opacity=1, stroke_width=0)
            bg_bot = Rectangle(width=inset_w, height=inset_h/2, fill_color=color_bot, fill_opacity=1, stroke_width=0)
            bg = VGroup(bg_top, bg_bot).arrange(DOWN, buff=0).move_to(inset_center)
            
            border = get_hollow_box(inset_w, inset_h, GREEN_B, 4).move_to(inset_center)
            normal_line = DashedLine(inset_center + UP*inset_h/2, inset_center + DOWN*inset_h/2, color=WHITE)
            
            # Rays
            ray_in = Line(inset_center + UP*(inset_h/2) + LEFT*dx_in, inset_center, color=YELLOW, stroke_width=3)
            ray_out = Line(inset_center, inset_center + DOWN*(inset_h/2) + RIGHT*dx_out, color=YELLOW, stroke_width=3)
            
            # Angles
            line_up = Line(inset_center, inset_center + UP)
            line_in_rev = Line(inset_center, inset_center + UP*(inset_h/2) + LEFT*dx_in)
            angle_i = Angle(line_up, line_in_rev, radius=0.8, color=WHITE, stroke_width=2, fill_opacity=0)
            
            line_down = Line(inset_center, inset_center + DOWN)
            line_out = Line(inset_center, inset_center + DOWN*(inset_h/2) + RIGHT*dx_out)
            angle_t = Angle(line_down, line_out, radius=0.9, color=WHITE, stroke_width=2, fill_opacity=0)
            
            # Perfect relative label positioning
            tex_i = MathTex(label_1).scale(0.8).next_to(angle_i, LEFT, buff=0.1)
            tex_t = MathTex(label_2).scale(0.8).next_to(angle_t, RIGHT, buff=0.1)

            return VGroup(bg, normal_line, ray_in, ray_out, angle_i, tex_i, angle_t, tex_t, border)

        def get_snells_eq(l_1, l_2, denom_1, denom_2):
            
            eq_str = rf"\frac{{\sin({l_1})}}{{{denom_1}}} = \frac{{\sin({l_2})}}{{{denom_2}}}"
            return MathTex(eq_str).scale(0.55).move_to(inset_center + RIGHT*1.2 + UP*1.4)

        # 5. Build the First Zoom (Boundary 1 -> 2)
        base_1 = build_inset_base(colors[0], colors[1], 0.8, 1.3, r"\theta_1", r"\theta_2")
        eq_1_v = get_snells_eq(r"\theta_1", r"\theta_2", "v_1", "v_2")
        
        inset_1 = VGroup(base_1, eq_1_v)
        
        # Animate the pop-out
        inset_1.scale(box_size / inset_w).move_to(p1).set_opacity(0)
        self.play(
            inset_1.animate.scale(inset_w / box_size).move_to(inset_center).set_opacity(1),
            run_time=1.5
        )
        self.next_slide()
        
        # Transition v to sqrt(y)
        eq_1_y = get_snells_eq(r"\theta_1", r"\theta_2", r"\sqrt{y_1}", r"\sqrt{y_2}")
        self.play(ReplacementTransform(eq_1_v, eq_1_y))
        self.next_slide()
        
        # 6. Move Box to Second Zoom (Boundary 2 -> 3)
        self.play(highlight_box.animate.move_to(p2), run_time=1)
        
        base_2 = build_inset_base(colors[1], colors[2], 1.3, 1.8, r"\theta_2", r"\theta_3")
        eq_2_v = get_snells_eq(r"\theta_2", r"\theta_3", "v_2", "v_3")
        
        # Smoothly morph the old inset into the new one
        self.play(
            ReplacementTransform(base_1, base_2),
            ReplacementTransform(eq_1_y, eq_2_v),
            run_time=1.5
        )
        self.next_slide()

        # Transition v to sqrt(y) for the second boundary
        eq_2_y = get_snells_eq(r"\theta_2", r"\theta_3", r"\sqrt{y_2}", r"\sqrt{y_3}")
        self.play(ReplacementTransform(eq_2_v, eq_2_y))
        self.next_slide()


    def snells_law_everywhere(self):
        """Method 3: The complete sequence - simple tracker, equation transform, and detailed geometry slide"""
        
        # 1. Clean slate
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
        
        # 2. Generate the cinematic gradient background (height = 6.0)
        total_height = 6.0
        def get_gradient(num):
            group = VGroup()
            colors = color_gradient(["#1E5974", "#A2CFDE"], num)
            h = total_height / num
            for i in range(num):
                rect = Rectangle(
                    width=config.frame_width, height=h, 
                    fill_color=colors[i], fill_opacity=1, stroke_width=0
                )
                group.add(rect)
            group.arrange(DOWN, buff=0)
            return group

        bg_gradient = get_gradient(100)
        self.play(FadeIn(bg_gradient, run_time=1.5))

        # 3. Draw the smooth continuous curve
        p0 = LEFT * 6 + UP * 3        
        p1 = LEFT * 3 + DOWN * 1      
        p2 = RIGHT * 1 + DOWN * 2     
        p3 = RIGHT * 5 + DOWN * 2.5   
        
        curve = CubicBezier(p0, p1, p2, p3).set_color(YELLOW).set_stroke(width=3)
        self.play(Create(curve), run_time=2)

        # 4. PHASE 1: The Simple Sliding Box
        square = Square(side_length=0.35, color=WHITE, stroke_width=2, fill_opacity=0)
        intro_text = Tex("Snell's law everywhere").scale(0.9)
        
        # We use a separate tracker for the first slide
        tracker1 = ValueTracker(0.15) 
        
        square.add_updater(lambda s: s.move_to(curve.point_from_proportion(tracker1.get_value())))
        intro_text.add_updater(lambda t: t.next_to(square, RIGHT, buff=0.3))

        self.play(FadeIn(square, intro_text))
        
        # Slide the box and text along the curve
        self.play(tracker1.animate.set_value(0.85), run_time=4, rate_func=linear)
        self.next_slide()
        # Stop the updaters so we can safely animate them independently
        square.clear_updaters()
        intro_text.clear_updaters()

        # 5. PHASE 2: Text Transitions to Math at the Top Right
        self.play(FadeOut(square)) # The box disappears
        
        final_eq = MathTex(r"\text{Snell's law : } \frac{\sin(\theta)}{\sqrt{y}} = \text{constant}").scale(0.9)
        final_eq.to_edge(UP, buff=2.5).to_edge(RIGHT, buff=0.5)
        
        # Smoothly fly the text to the corner and turn it into the equation
        self.play(ReplacementTransform(intro_text, final_eq), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # 6. PHASE 3: Step-by-Step Geometry Buildup
        # We start back at 15% of the curve for the detailed breakdown
        start_val = 0.15 
        p = curve.point_from_proportion(start_val)
        
        dot = Dot(p, color=WHITE)
        top_p = np.array([p[0], 3.0, 0])
        bot_p = np.array([p[0], p[1] - 1.5, 0])
        
        normal = Line(top_p, bot_p, color=WHITE, stroke_width=2)
        tan = TangentLine(curve, alpha=start_val, length=5, color=WHITE, stroke_width=2)
        
        brace = BraceBetweenPoints(top_p, p, direction=RIGHT)
        y_lab = brace.get_tex("y")
        
        line_up = Line(p, top_p)
        vec1 = tan.get_start() - p
        vec2 = tan.get_end() - p
        tan_up = Line(p, p + vec1) if vec1[1] > 0 else Line(p, p + vec2)
        
        angle = Angle(line_up, tan_up, radius=0.8, color=WHITE, stroke_width=2, fill_opacity=0)
        
        arc_center = angle.point_from_proportion(0.5)
        direction = (arc_center - p) / np.linalg.norm(arc_center - p)
        theta_lab = MathTex(r"\theta").scale(0.8).move_to(p + direction * 1.2)

        # Animate the geometry popping in
        self.play(FadeIn(dot))
        self.play(Create(normal))
        self.play(GrowFromCenter(brace), Write(y_lab))
        self.play(Create(tan))
        self.play(Create(angle), Write(theta_lab))
        self.wait(0.5)

        # 7. PHASE 4: The Detailed Geometry Slide
        static_group = VGroup(normal, tan, dot, brace, y_lab, angle, theta_lab)
        tracker2 = ValueTracker(start_val) # New tracker for the geometry
        dynamic_group = VGroup()
        
        # Updater builds a fresh geometry group every frame and Replaces it
        def update_geom(group):
            v = tracker2.get_value()
            pt = curve.point_from_proportion(v)
            
            d = Dot(pt, color=WHITE)
            t_p = np.array([pt[0], 3.0, 0])
            b_p = np.array([pt[0], pt[1] - 1.5, 0])
            n = Line(t_p, b_p, color=WHITE, stroke_width=2)
            
            t = TangentLine(curve, alpha=v, length=5, color=WHITE, stroke_width=2)
            
            br = BraceBetweenPoints(t_p, pt, direction=RIGHT)
            y_l = br.get_tex("y")
            
            l_up = Line(pt, t_p)
            v1 = t.get_start() - pt
            v2 = t.get_end() - pt
            t_up = Line(pt, pt + v1) if v1[1] > 0 else Line(pt, pt + v2)
            
            ang = Angle(l_up, t_up, radius=0.8, color=WHITE, stroke_width=2, fill_opacity=0)
            
            arc_c = ang.point_from_proportion(0.5)
            direc = (arc_c - pt) / np.linalg.norm(arc_c - pt)
            th_l = MathTex(r"\theta").scale(0.8).move_to(pt + direc * 1.2)
            
            new_group = VGroup(n, t, d, br, y_l, ang, th_l)
            group.become(new_group)

        # Swap the static group for the dynamically updating one
        dynamic_group.add_updater(update_geom)
        self.add(dynamic_group)
        self.remove(static_group)
        
        # Slide the detailed geometry
        self.play(tracker2.animate.set_value(0.85), run_time=6, rate_func=linear)
        
        # Clean up and conclude
        self.next_slide()
        dynamic_group.clear_updaters()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)