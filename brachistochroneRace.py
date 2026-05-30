from manim import *

class BrachistochroneRace(Scene):
    def race(self):
        # 1. Setup Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=4,
            axis_config={"color": GREY},
        ).to_edge(LEFT, buff=0.5).shift(UP * 0.5)

        # 2. Points A and B 
        a_coords = [1, 5]
        b_coords = [9, 1]
        
        point_a = Dot(axes.c2p(*a_coords), color=YELLOW)
        point_b = Dot(axes.c2p(*b_coords), color=YELLOW)
        label_a = Tex("A").next_to(point_a, UP)
        label_b = Tex("B").next_to(point_b, RIGHT)

        # 3. Dynamic Timer Setup
        time_tracker = ValueTracker(0.0)
        timer_label = Text("Current Time:").scale(0.5)
        timer_val = DecimalNumber(0.00, num_decimal_places=2)
        timer_val.add_updater(lambda d: d.set_value(time_tracker.get_value()))
        timer_group = VGroup(timer_label, timer_val).arrange(RIGHT).to_edge(UP, buff=0.5)

        # 4. Fixed Table Setup 
        table_bg = RoundedRectangle(corner_radius=0.2, width=5.5, height=4.5, color=GREY_E, fill_opacity=0.3)
        table_bg.to_edge(RIGHT, buff=0.2).shift(DOWN * 0.5)
        
        header_y = table_bg.get_top()[1] - 0.5
        col1_x = table_bg.get_center()[0] - 1.2
        col2_x = table_bg.get_center()[0] + 1.2

        header_path = Text("Path", weight=BOLD).scale(0.5).move_to([col1_x, header_y, 0])
        header_time = Text("Time (s)", weight=BOLD).scale(0.5).move_to([col2_x, header_y, 0])
        table_header = VGroup(header_path, header_time)

        # --- NEW: Fade everything in smoothly at the start ---
        self.play(
            FadeIn(axes), FadeIn(point_a), FadeIn(point_b), 
            FadeIn(label_a), FadeIn(label_b), FadeIn(timer_group), 
            FadeIn(table_bg), FadeIn(table_header)
        )
        self.next_slide() 

        # 5. Define Curves 
        def line_func(x): return 5 - 0.5 * (x - 1)
        def shallow(x): return 0.05 * (x - 1) * (x - 9) + line_func(x)
        def parabola(x): return 0.2 * (x - 1) * (x - 9) + line_func(x) 
        def steep_drop(x): return 5 - 4 * ((x - 1) / 8)**0.3
        def cubic_slow(x): return 5 - 4 * ((x - 1) / 8)**3

        curve_configs = [
            {"func": line_func, "name": "Straight Line", "color": BLUE, "time": 3.00},
            {"func": shallow, "name": "Shallow Arc", "color": GREEN, "time": 2.45},
            {"func": parabola, "name": "Parabola", "color": GOLD, "time": 2.05},
            {"func": steep_drop, "name": "Steep Drop", "color": RED, "time": 2.15},
            {"func": cubic_slow, "name": "Slow Start", "color": PURPLE, "time": 3.80},
        ]

        # 6. Animation Loop
        ball = Dot(color=WHITE, radius=0.12)
        current_path_mobject = None
        current_name_label = None

        for i, config in enumerate(curve_configs):
            new_path = axes.plot(config["func"], x_range=[1, 9], color=config["color"])
            new_name_label = Text(config["name"], color=config["color"]).scale(0.6).next_to(axes, UP)

            if current_path_mobject is None:
                self.play(Create(new_path), Write(new_name_label))
            else:
                self.play(
                    ReplacementTransform(current_path_mobject, new_path),
                    ReplacementTransform(current_name_label, new_name_label)
                )
            
            current_path_mobject = new_path
            current_name_label = new_name_label

            ball.move_to(axes.c2p(1, 5))
            time_tracker.set_value(0.0)
            self.add(ball)
            
            # self.next_slide() 

            self.play(
                MoveAlongPath(ball, new_path, rate_func=rate_functions.ease_in_quad),
                time_tracker.animate(rate_func=linear).set_value(config["time"]),
                run_time=2.5 
            )

            row_y = header_y - 0.7 - (i * 0.6) 
            
            row_name = Text(config["name"], color=config["color"]).scale(0.4).move_to([col1_x, row_y, 0])
            row_time = Text(f"{config['time']:.2f}s").scale(0.4).move_to([col2_x, row_y, 0])
            new_row = VGroup(row_name, row_time)

            self.play(Write(new_row))
            self.play(FadeOut(ball))
            
            self.next_slide()

        self.wait(1)

        # --- NEW: Fade out every single object remaining on screen ---
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

    def balance(self):
        # 1. Setup Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=4,
            axis_config={"color": GREY},
        ).to_edge(DOWN, buff=1)

        # Points A and B
        point_a = Dot(axes.c2p(1, 5), color=YELLOW)
        point_b = Dot(axes.c2p(9, 1), color=YELLOW)
        label_a = Tex("A").next_to(point_a, UP)
        label_b = Tex("B").next_to(point_b, RIGHT)

        self.play(FadeIn(axes, point_a, point_b, label_a, label_b))
        self.next_slide()

        # 2. Mathematical Functions for the extremes
        def straight_func(x): return 5 - 0.5 * (x - 1)
        def steep_func(x): return 5 - 4 * ((x - 1) / 8)**0.15 

        path_straight = axes.plot(straight_func, x_range=[1, 9], color=BLUE)
        path_steep = axes.plot(steep_func, x_range=[1, 9], color=RED)

        # --- EXTREME 1: Straight Line ---
        title_straight = Text("Extreme 1: Straight Line", color=BLUE).to_edge(UP, buff=0.8)
        pro_straight = Text("+ Shortest Distance", color=GREEN).scale(0.6).next_to(title_straight, DOWN)
        con_straight = Text("- Slow Initial Acceleration", color=RED).scale(0.6).next_to(pro_straight, DOWN)
        
        self.play(Create(path_straight), Write(title_straight))
        self.play(FadeIn(pro_straight, shift=UP*0.2), FadeIn(con_straight, shift=UP*0.2))
        self.wait(1)
        self.next_slide()

        # --- EXTREME 2: Steep Drop ---
        title_steep = Text("Extreme 2: Steep Drop", color=RED).to_edge(UP, buff=0.8)
        pro_steep = Text("+ Fastest Initial Acceleration", color=GREEN).scale(0.6).next_to(title_steep, DOWN)
        con_steep = Text("- Longer Distance Covered", color=RED).scale(0.6).next_to(pro_steep, DOWN)

        self.play(
            ReplacementTransform(path_straight, path_steep),
            ReplacementTransform(title_straight, title_steep),
            ReplacementTransform(pro_straight, pro_steep),
            ReplacementTransform(con_straight, con_steep),
        )
        self.wait(1)
        self.next_slide()

        # --- THE CLIFFHANGER: Finding the Balance ---
        title_balance = Text("The Perfect Balance?", color=GOLD).to_edge(UP, buff=0.8)
        subtitle_balance = Text("We must balance distance and acceleration.", color=WHITE).scale(0.6).next_to(title_balance, DOWN)
        
        # We recreate the straight path to show it alongside the steep path
        ghost_straight = axes.plot(straight_func, x_range=[1, 9], color=BLUE).set_opacity(0.3)

        self.play(
            path_steep.animate.set_opacity(0.3),
            FadeIn(ghost_straight), 
            ReplacementTransform(title_steep, title_balance),
            ReplacementTransform(pro_steep, subtitle_balance),
            FadeOut(con_steep)
        )
        
        # Add a large question mark in the middle to emphasize the unknown solution
        question_mark = Text("?", font_size=120, color=GOLD).move_to(axes.c2p(4.5, 3))
        self.wait(1)
        self.play(Write(question_mark))

        self.next_slide()
        
        # Clean fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)
    

    def final_race(self):
        # 1. Clean slate
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

        # 3. Rebuild Axes with PERFECT 1:1 Aspect Ratio
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=4.2, 
            axis_config={"color": GREY},
        ).to_edge(LEFT, buff=0.5).shift(UP * 0.5)

        point_a = Dot(axes.c2p(1, 5), color=YELLOW)
        point_b = Dot(axes.c2p(9, 1), color=YELLOW)
        label_a = Tex("A").next_to(point_a, UP)
        label_b = Tex("B").next_to(point_b, RIGHT)

        # Rebuild Timer & Table
        time_tracker = ValueTracker(0.0)
        timer_label = Text("Current Time:").scale(0.5)
        timer_val = DecimalNumber(0.00, num_decimal_places=2)
        timer_val.add_updater(lambda d: d.set_value(time_tracker.get_value()))
        timer_group = VGroup(timer_label, timer_val).arrange(RIGHT).to_edge(UP, buff=0.5)

        table_bg = RoundedRectangle(corner_radius=0.2, width=5.5, height=4.5, color=GREY_E, fill_opacity=0.3)
        table_bg.to_edge(RIGHT, buff=0.2).shift(DOWN * 0.5)
        
        header_y = table_bg.get_top()[1] - 0.5
        col1_x = table_bg.get_center()[0] - 1.2
        col2_x = table_bg.get_center()[0] + 1.2

        table_header = VGroup(
            Text("Path", weight=BOLD).scale(0.5).move_to([col1_x, header_y, 0]),
            Text("Time (s)", weight=BOLD).scale(0.5).move_to([col2_x, header_y, 0])
        )

        previous_configs = [
            {"name": "Straight Line", "color": BLUE, "time": 3.00},
            {"name": "Shallow Arc", "color": GREEN, "time": 2.45},
            {"name": "Parabola", "color": GOLD, "time": 2.05},
            {"name": "Steep Drop", "color": RED, "time": 2.15},
            {"name": "Slow Start", "color": PURPLE, "time": 3.80},
        ]

        previous_rows = VGroup()
        for i, path_data in enumerate(previous_configs):
            row_y = header_y - 0.7 - (i * 0.6) 
            previous_rows.add(
                Text(path_data["name"], color=path_data["color"]).scale(0.4).move_to([col1_x, row_y, 0]),
                Text(f"{path_data['time']:.2f}s").scale(0.4).move_to([col2_x, row_y, 0])
            )

        self.play(
            FadeIn(axes, point_a, point_b, label_a, label_b, timer_group, table_bg, table_header, previous_rows),
            run_time=1
        )

        # 4. Draw the TRUE "Found Curve" (A pure, mathematical cycloid)
        R = 2.07
        theta_end = 3.51
        
        def cycloid_func(t):
            x = 1 + R * (t - np.sin(t))
            y = 5 - R * (1 - np.cos(t))
            return axes.c2p(x, y)

        found_path = ParametricFunction(cycloid_func, t_range=[0, theta_end], color=YELLOW, stroke_width=4)
        found_name_label = Text("Found Curve", color=YELLOW, weight=BOLD).scale(0.6).next_to(axes, UP)

        self.play(Create(found_path), Write(found_name_label))

        self.next_slide()
        # 5. Race the ball!
        optimal_time = 1.85
        ball = Dot(color=WHITE, radius=0.12).move_to(axes.c2p(1, 5))
        self.add(ball)

        self.play(
            MoveAlongPath(ball, found_path, rate_func=rate_functions.ease_in_out_sine),
            time_tracker.animate(rate_func=linear).set_value(optimal_time),
            run_time=2.5 
        )

        # 6. Update Table
        row_y = header_y - 0.7 - (5 * 0.6) 
        winner_row = VGroup(
            Text("Found Curve", color=YELLOW, weight=BOLD).scale(0.45).move_to([col1_x, row_y, 0]),
            Text(f"{optimal_time:.2f}s", color=YELLOW, weight=BOLD).scale(0.45).move_to([col2_x, row_y, 0])
        )

        w_box, h_box = SurroundingRectangle(winner_row, buff=0.1).get_width(), SurroundingRectangle(winner_row, buff=0.1).get_height()
        p_c = winner_row.get_center()
        winner_box = VGroup(
            Line(p_c + LEFT*(w_box/2) + UP*(h_box/2), p_c + RIGHT*(w_box/2) + UP*(h_box/2), color=YELLOW, stroke_width=2),
            Line(p_c + LEFT*(w_box/2) + DOWN*(h_box/2), p_c + RIGHT*(w_box/2) + DOWN*(h_box/2), color=YELLOW, stroke_width=2),
            Line(p_c + LEFT*(w_box/2) + UP*(h_box/2), p_c + LEFT*(w_box/2) + DOWN*(h_box/2), color=YELLOW, stroke_width=2),
            Line(p_c + RIGHT*(w_box/2) + UP*(h_box/2), p_c + RIGHT*(w_box/2) + DOWN*(h_box/2), color=YELLOW, stroke_width=2)
        )

        self.play(Write(winner_row))
        self.play(Create(winner_box))
        self.wait(1)

        # ==========================================
        # 7. THE TRUE CYCLOID REVEAL 
        # ==========================================
        
        self.next_slide()

        mobs_to_fade = [m for m in self.mobjects if m != found_path]
        self.play(*[FadeOut(mob) for mob in mobs_to_fade], run_time=1)

        question = Text("So what is this curve?", font_size=48).to_edge(UP, buff=1)
        
        start_pt = LEFT * 5 + UP * 1.5
        shift_vector = start_pt - found_path.get_start()
        
        self.play(
            found_path.animate.shift(shift_vector),
            Write(question)
        )
        self.wait(2)
        
        self.next_slide()
        self.play(FadeOut(question))

        R_manim = R * 0.7 
        ceiling_y = start_pt[1]
        start_x = start_pt[0]

        ceiling = Line(LEFT * 6 + UP * ceiling_y, RIGHT * 6 + UP * ceiling_y, color=GREY)
        circle = Circle(radius=R_manim, color=BLUE).move_to(np.array([start_x, ceiling_y - R_manim, 0]))
        dot = Dot(circle.point_at_angle(PI/2), color=WHITE, radius=0.08)

        self.play(
            FadeIn(ceiling), Create(circle), FadeIn(dot),
            found_path.animate.set_opacity(0.3)
        )

        # 8. Roll the circle perfectly!
        theta = ValueTracker(0)

        def update_circle(c):
            c.move_to(np.array([start_x + R_manim * theta.get_value(), ceiling_y - R_manim, 0]))

        def update_dot(d):
            center = np.array([start_x + R_manim * theta.get_value(), ceiling_y - R_manim, 0])
            angle = PI/2 + theta.get_value()
            d.move_to(center + np.array([R_manim * np.cos(angle), R_manim * np.sin(angle), 0]))

        circle.add_updater(update_circle)
        dot.add_updater(update_dot)

        trace = TracedPath(dot.get_center, stroke_width=5, stroke_color=YELLOW)
        self.add(trace)

        # Changed to rate_func=smooth for natural acceleration and deceleration!
        self.play(theta.animate.set_value(2 * PI), run_time=4, rate_func=smooth)

        # Removed the clear_updaters() calls so the TracedPath stays solidly on screen
        
        cycloid_text = Text("A Cycloid!", color=YELLOW, font_size=60).next_to(ceiling, UP, buff=1)
        
        self.next_slide()
        self.play(Write(cycloid_text))
        
        self.next_slide()

        # Finally, safely fade everything out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)