from manim import *

class Intro:

    def show_title(self):

        title = Tex("Brachistochrone Curve", color=BLUE_C).scale(2)
        sub_title = Tex("by Aykun Nersesyan", color=WHITE,).next_to(title, DOWN, buff=0.4).scale(0.8)
        self.play(Write(title))
        self.play(Write(sub_title))
        self.all= VGroup(title, sub_title)
    
    def show_timeline(self):
        # 1. Title
        self.play(FadeOut(self.all))

        title = Tex("For the next 12 minutes:")
        title.to_edge(UP, buff=1)

        # Adjust start, end, and split points to change the line's proportions
        start_point = LEFT * 5
        history = LEFT * 3.5
        curveAnalysis = LEFT * 1.5
        derivation1 = RIGHT * 3
        derivation2 = RIGHT * 4
        end_point = RIGHT * 5

        timeline = Line(start_point, end_point, color=BLUE_C)
        
        # Create the vertical tick marks
        tick_height = 0.4
        tick1 = Line(UP * (tick_height/2), DOWN * (tick_height/2), color=BLUE_C).move_to(start_point)
        tick2 = Line(UP * (tick_height/2), DOWN * (tick_height/2), color=BLUE_C).move_to(history)
        tick3 = Line(UP * (tick_height/2), DOWN * (tick_height/2), color=BLUE_C).move_to(curveAnalysis)
        tick4 = Line(UP * (tick_height/2), DOWN * (tick_height/2), color=BLUE_C).move_to(derivation1)
        tick5 = Line(UP * (tick_height/2), DOWN * (tick_height/2), color=BLUE_C).move_to(derivation2)
        tick6 = Line(UP * (tick_height/2), DOWN * (tick_height/2), color=BLUE_C).move_to(end_point)

        timeline_group = VGroup(timeline, tick1, tick2, tick3, tick5, tick6)

        # 3. First Brace and Text (Bottom)
        brace_history = BraceBetweenPoints(tick1.get_bottom(), tick2.get_bottom(), direction=DOWN)   
        text_history = VGroup(
            Tex("Problem statement"),
            Tex("History"),
        ).arrange(DOWN, buff=0.15).next_to(brace_history, DOWN)

        brace_curve = BraceBetweenPoints(tick2.get_top(), tick3.get_top(), direction=UP)
        text_curve = Tex("Curve analysis", color=WHITE).next_to(brace_curve, UP)

        brace_derivation1 = BraceBetweenPoints(tick3.get_bottom(), tick5.get_bottom(), direction=DOWN)
        text_derivation1 = Tex("Finding brachistochrone", color=WHITE).next_to(brace_derivation1, DOWN)


        """brace_derivation2 = BraceBetweenPoints(tick4.get_top(), tick5.get_top(), direction=UP)
        text_derivation2 = VGroup(Tex("A Brief look to"),
                                  Tex("the 2nd Derivation")
                                  ).arrange(DOWN, buff=0.15).next_to(brace_derivation2, UP)"""

        brace_questions = BraceBetweenPoints(tick5.get_top(), tick6.get_top(), direction=UP)
        text_questions = Tex("Questions", color=WHITE).next_to(brace_questions, UP)


        # --- Animations Sequence ---
        self.play(Write(title))
        
        self.play(Create(timeline_group))
        
        self.play(GrowFromCenter(brace_history), Write(text_history))

        self.play(GrowFromCenter(brace_curve), Write(text_curve))

        self.play(GrowFromCenter(brace_derivation1), Write(text_derivation1))
        
        """self.play(GrowFromCenter(brace_derivation2), Write(text_derivation2))"""
        
        self.play(GrowFromCenter(brace_questions), Write(text_questions))

        groupEverything = VGroup(title, timeline_group, brace_history, text_history, brace_curve, text_curve, brace_derivation1, text_derivation1, brace_questions, text_questions)
        
        self.next_slide()
        
        self.play(FadeOut(groupEverything))


    def show_brachistochroneWord(self):

        intro_part1 = Tex("So what is ")
        intro_part2 = Tex("Brachistochrone")
        intro_part3 = Tex("?")
        
        # Group them and arrange them side-by-side
        intro_group = VGroup(intro_part1, intro_part2, intro_part3).arrange(RIGHT)
        
        self.play(Write(intro_group))
        
        self.next_slide()

        self.play(FadeOut(intro_part1, intro_part3))
        
        self.play(intro_part2.animate.move_to(ORIGIN))
        
        dotted_word = Tex("Bra", "$\\cdot$", "chis", "$\\cdot$", "to", "$\\cdot$", "chrone")
        
        self.play(TransformMatchingShapes(intro_part2, dotted_word))
        
        left_syllables = dotted_word[0:5] 
        right_syllables = dotted_word[6]
        
        brace_shortest = Brace(left_syllables, direction=UP)
        text_shortest = Tex("Shortest", color=YELLOW).next_to(brace_shortest, UP)
        
        brace_time = Brace(right_syllables, direction=UP)
        text_time = Tex("Time", color=YELLOW).next_to(brace_time, UP)
        
        # We use Text() instead of Tex() to safely handle the unicode ə and ō characters
        phonetic_text = Text("/brəkistəkrōn/", font="serif").scale(0.8).next_to(dotted_word, DOWN, buff=0.5)
        greek = Tex("Greek:", color=YELLOW).next_to(text_shortest, LEFT, buff=1)

        self.play(Write(phonetic_text))
        
        self.next_slide()
        
        self.play(
            Write(greek),
            GrowFromCenter(brace_shortest), 
            Write(text_shortest),
            GrowFromCenter(brace_time), 
            Write(text_time)
        )

        everything = VGroup(greek, phonetic_text, brace_shortest, brace_time, dotted_word, text_shortest, text_time)
        self.next_slide()
        self.play(FadeOut(everything))

    def challenge_statement(self):
        # 1. Clean slate just in case
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)

        # 2. Setup a clean xy-plane (No numbers to keep the visual pure)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=4.8,
            axis_config={"color": GREY},
        ).shift(DOWN * 0.2)

        # 3. Plot Points A and B (clearly visible, off the axes)
        pA = axes.c2p(1, 5)
        pB = axes.c2p(9, 1)

        dot_A = Dot(pA, color=WHITE, radius=0.1)
        dot_B = Dot(pB, color=WHITE, radius=0.1)

        # Minimalist labels
        label_A = MathTex("A", font_size=48).next_to(dot_A, UP, buff=0.2)
        label_B = MathTex("B", font_size=48).next_to(dot_B, RIGHT, buff=0.2)

        # Fade in the environment
        self.play(Create(axes))
        self.play(
            FadeIn(dot_A, shift=DOWN*0.5), Write(label_A),
            FadeIn(dot_B, shift=UP*0.5), Write(label_B)
        )
        
        # ---> Pause here to start explaining the setup: "Imagine two points, A and B..."
        self.next_slide()

        # 4. Generate 11 Crazy Paths
        paths = VGroup()

        # Path 1: The Intuitive Straight Line
        paths.add(Line(pA, pB, color=BLUE, stroke_width=3))
        
        # Path 2: Shallow Arc
        paths.add(ArcBetweenPoints(pA, pB, angle=-PI/6, color=GREEN, stroke_width=3))
        
        # Path 3: Upward Arc (Against gravity, but still a geometric path!)
        paths.add(ArcBetweenPoints(pA, pB, angle=PI/4, color=RED, stroke_width=3))
        
        # Path 4: The 'L' Drop (Max acceleration, then flat)
        paths.add(VMobject(color=TEAL, stroke_width=3).set_points_as_corners([pA, axes.c2p(1, 1), pB]))
        
        # Path 5: The 'L' Slide (Zero acceleration initially)
        paths.add(VMobject(color=ORANGE, stroke_width=3).set_points_as_corners([pA, axes.c2p(9, 5), pB]))
        
        # Path 6: Wavy Sine-like path
        paths.add(VMobject(color=PINK, stroke_width=3).set_points_smoothly([pA, axes.c2p(3, 4), axes.c2p(5, 6), axes.c2p(7, 3), pB]))
        
        # Path 7: Bouncing Path
        paths.add(VMobject(color=LIGHT_BROWN, stroke_width=3).set_points_smoothly([pA, axes.c2p(2.5, 1), axes.c2p(4, 3.5), axes.c2p(6.5, 0.5), pB]))
        
        # Path 8: The Loop-de-loop
        paths.add(VMobject(color=MAROON, stroke_width=3).set_points_smoothly([pA, axes.c2p(6, 5), axes.c2p(7.5, 2.5), axes.c2p(4.5, 2.5), axes.c2p(6, 0.5), pB]))
        
        # Path 9: Staircase
        paths.add(VMobject(color=LIGHT_GRAY, stroke_width=3).set_points_as_corners([pA, axes.c2p(3, 5), axes.c2p(3, 3), axes.c2p(6, 3), axes.c2p(6, 1), pB]))
        
        # Path 10: Late Drop Curve
        paths.add(CubicBezier(pA, pA + RIGHT*6, pB + UP*4, pB, color=PURPLE, stroke_width=3))
        
        # Path 11: Deep Drop (The foreshadowing shape!)
        paths.add(ArcBetweenPoints(pA, pB, angle=PI/1.1, color=YELLOW, stroke_width=4))

        # 5. Animate drawing all paths like a brainstorm!
        # lag_ratio=0.3 makes them trace sequentially, but overlapping, creating a beautiful chaotic build-up.
        self.play(
            AnimationGroup(
                *[Create(path) for path in paths], 
                lag_ratio=0.3
            ),
            run_time=6,
            rate_func=linear
        )
        
        # ---> Pause here to ask the ultimate question: "Out of all these infinite possibilities... which is the fastest?"
        self.next_slide()

        # 6. Clean fade out before moving to the historical drama
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

    def history_of_the_challenge(self):
        
        # 1. UPDATED Portrait Builder
        def get_portrait(name, image_path, width1, height1, imageHeight):
            # The outer frame
            frame = RoundedRectangle(width=width1, height=height1, corner_radius=0.1, color=WHITE, fill_color=BLACK, fill_opacity=1)
            
            # Load the actual image file
            pic_area = ImageMobject(image_path)
            
            # Resize the image to fit perfectly inside our frame
            pic_area.set_height(imageHeight)
            pic_area.next_to(frame.get_top(), DOWN, buff=0.1)
            
            # The name label at the bottom
            label = Text(name, font_size=20, weight=BOLD).next_to(pic_area, DOWN, buff=0.2)
            
            # --- FIX: We must use Group() instead of VGroup() because pic_area is an ImageMobject ---
            return Group(frame, pic_area, label)

        # 2. The Envelope Builder 
        def get_envelope():
            body = Rectangle(width=0.6, height=0.4, color=WHITE, fill_color=LIGHT_GREY, fill_opacity=1)
            flap_left = Line(body.get_corner(UL), body.get_center() + UP * 0.05, color=BLACK, stroke_width=2)
            flap_right = Line(body.get_corner(UR), body.get_center() + UP * 0.05, color=BLACK, stroke_width=2)
            return VGroup(body, flap_left, flap_right)

        # ==========================================
        # ACT 1: INTRODUCING JOHANN BERNOULLI
        # ==========================================
        
        title = Text("History of The Challenge (1696)", color=YELLOW)
        self.play(Write(title))
        self.wait(0.5)
        johann = get_portrait("Johann Bernoulli", "assets/johann.jpg", 4, 4, 3.4)
        
        self.next_slide()
        
        self.play(FadeIn(johann, shift=UP * 0.5), title.animate.to_edge(UP, buff=0.2).scale(0.7))
        self.wait(1.5)
        
        self.next_slide()

        self.play(johann.animate.to_edge(LEFT, buff=1.0))

        # ==========================================
        # ACT 2: THE RIVALS
        # ==========================================
        
        newton = get_portrait("Isaac Newton", "assets/newton.jpg", 2.2, 2.8, 2)
        jakob = get_portrait("Jakob Bernoulli", "assets/jakob.jpg", 2.2, 2.8, 2)
        leibniz = get_portrait("Gottfried Leibniz", "assets/leibniz.jpg", 2.2, 2.8, 2)
        lhopital = get_portrait("L'Hôpital", "assets/lhopital.jpg", 2.2, 2.8, 2)

        # --- FIX: rivals must also be a standard Group because it contains ImageMobjects ---
        rivals = Group(newton, jakob, leibniz, lhopital)
        rivals.arrange_in_grid(rows=2, cols=2, buff=0.5).to_edge(RIGHT, buff=1.0)
        
        # ==========================================
        # ACT 3: SENDING THE LETTERS
        # ==========================================
        
        # --- FIX: Standard Group used here as well for consistency ---
        envelopes = Group(*[get_envelope().move_to(johann.get_center()) for _ in rivals])
        self.add(envelopes, johann)
        
        self.play(
            *[env.animate.move_to(rival.get_center()) for env, rival in zip(envelopes, rivals)],
            run_time=2, rate_func=smooth, lag_ratio=0.1 
        )
        self.wait(0.2)

        # We use a crossfade with a scale effect instead of a mathematical transform
        # so Manim doesn't try to bend vector shapes into raster .jpg images!
        self.play(
            *[FadeOut(env, scale=0.5) for env in envelopes],
            *[FadeIn(rival, scale=0.5) for rival in rivals],
            run_time=1.5
        )
        self.next_slide()

        bigger_than = Text(">", weight=SEMIBOLD, color=BLUE).scale(1.5).shift(LEFT*0.2)
        smaller_than = Text("<", weight=SEMIBOLD, color=RED).scale(1.5).shift(LEFT*0.3)
        question = Text("?", color=ORANGE).scale(1.5).shift(LEFT*0.18)
        self.play(Write(bigger_than))

        self.next_slide()

        newton_note = Text("Solved in 1 night!", font_size=16, color=YELLOW).next_to(newton, DOWN, buff=0.1)
        self.play(Write(newton_note))
        self.play(Write(question), question.animate.shift(DOWN*0.7))

        self.next_slide()

        self.play(Transform(bigger_than, smaller_than), FadeOut(question))
        self.wait(1)
        self.next_slide()

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)