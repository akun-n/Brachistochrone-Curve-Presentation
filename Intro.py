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

        title = Tex("For the next 13 minutes:")
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

        timeline_group = VGroup(timeline, tick1, tick2, tick3, tick4, tick5, tick6)

        # 3. First Brace and Text (Bottom)
        brace_history = BraceBetweenPoints(tick1.get_bottom(), tick2.get_bottom(), direction=DOWN)   
        text_history = VGroup(
            Tex("Problem statement"),
            Tex("History"),
        ).arrange(DOWN, buff=0.15).next_to(brace_history, DOWN)

        brace_curve = BraceBetweenPoints(tick2.get_top(), tick3.get_top(), direction=UP)
        text_curve = Tex("Curve analysis", color=WHITE).next_to(brace_curve, UP)

        brace_derivation1 = BraceBetweenPoints(tick3.get_bottom(), tick4.get_bottom(), direction=DOWN)
        text_derivation1 = Tex("1st Derivation", color=WHITE).next_to(brace_derivation1, DOWN)


        brace_derivation2 = BraceBetweenPoints(tick4.get_top(), tick5.get_top(), direction=UP)
        text_derivation2 = VGroup(Tex("A Brief look to"),
                                  Tex("the 2nd Derivation")
                                  ).arrange(DOWN, buff=0.15).next_to(brace_derivation2, UP)

        brace_questions = BraceBetweenPoints(tick5.get_bottom(), tick6.get_bottom(), direction=DOWN)
        text_questions = Tex("Questions", color=WHITE).next_to(brace_questions, DOWN)


        # --- Animations Sequence ---
        self.play(Write(title))
        
        self.play(Create(timeline_group))
        
        self.play(GrowFromCenter(brace_history), Write(text_history))

        self.play(GrowFromCenter(brace_curve), Write(text_curve))

        self.play(GrowFromCenter(brace_derivation1), Write(text_derivation1))
        
        self.play(GrowFromCenter(brace_derivation2), Write(text_derivation2))
        
        self.play(GrowFromCenter(brace_questions), Write(text_questions))

        groupEverything = VGroup(title, timeline_group, brace_history, text_history, brace_curve, text_curve, brace_derivation1, text_derivation1, brace_derivation2, text_derivation2, brace_questions, text_questions)
        
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