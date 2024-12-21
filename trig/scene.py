from manim import *
from math import cos, radians

HYP_COLOR = GREEN
ADJ_COLOR = RED
ANGLE_COLOR = BLUE

class Trig(Scene):        
    def construct(self):
        # Construct Triangle
        vertices = [
            [-2.5, -2, 0], # down left
            [1.5, -2, 0],  # down right
            [1.5, 1.5, 0] # upper right
            
        ]

        triangle = Polygon(*vertices, color=WHITE).move_to(ORIGIN)
        vertices = triangle.get_vertices()

        base = Line(vertices[0], vertices[1])
        height = Line(vertices[1], vertices[2])
        hyp = Line(vertices[0], vertices[2])

        right_angle = RightAngle(base, height, quadrant=(-1, 1))

        angle = Angle(base, hyp, radius=0.7)
        theta = MathTex(r"\theta", color=ANGLE_COLOR).scale(0.8).move_to(
            Angle(
                base, hyp, radius=0.5 + 5 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )
        angle_value = DecimalNumber(
            angle.get_value(degrees=True), unit="^{\circ}"
        ).set_color(ANGLE_COLOR).scale(0.6).next_to(base, LEFT * 0.8 + UP * 2.5)

        arrow = CurvedArrow(
            angle_value.get_right(),
            angle.get_left(),
            tip_length=0.2,
            angle=-PI / 3
        )

        hyp_len = MathTex(
            "42\ cm", color=HYP_COLOR
        ).scale(0.7).move_to(hyp.get_center()).rotate(angle.get_value()).shift((LEFT + UP) * 0.2)

        base_len = MathTex("y", color=ADJ_COLOR).scale(0.7).next_to(base, DOWN)

        
        triangle_group = Group(triangle, right_angle, angle, theta, angle_value, arrow, hyp_len, base_len)
        Group(base, height, hyp).to_edge(UP)
        
    
        self.play(Write(triangle))
        self.play(Write(right_angle))
        self.play(Write(angle), Write(theta))
        self.play(Write(angle_value), Write(arrow))
        self.play(Write(hyp_len))
        self.play(Write(base_len))
        self.play(triangle_group.animate.to_edge(UP))


        # Trig Mnemonics
        soh = Tex("{{S}}{{O}}{{H}}", color=ANGLE_COLOR)
        cah = Tex("{{C}}{{A}}{{H}}", color=ANGLE_COLOR)
        toa = Tex("{{T}}{{O}}{{A}}", color=ANGLE_COLOR)

        trig_mnemonics = {
            "S": "Sin", 
            "C": "Cos",  
            "T": "Tan", 
            "O": "Opp",  
            "A": "Adj", 
            "H": "Hyp"  
        }

        mnemonics = VGroup(soh, cah, toa).scale(0.8).arrange(buff=2).to_edge(DOWN)

        def create_labels(mnemonic):                    
            labels = VGroup(
                *[
                    Tex(f"{trig_mnemonics[k.get_tex_string()]}")
                    for k in mnemonic
                ]
            ).scale(0.7).arrange(buff=0.1).next_to(mnemonic, UP * 3)
            
            for label in labels:
                label_text = label.get_tex_string()
                if label_text == "Hyp":
                    label.set_color(HYP_COLOR)
                elif label_text == "Adj":
                    label.set_color(ADJ_COLOR)
                    
            labels[1].shift(UP * 0.2)
            return labels

        def map_labels(mnemonic, meaning):
            return VGroup(
                *[
                    Arrow(mnemonic[i].get_center(), meaning[i].get_center())
                    for i in range(len(mnemonic))
                ]
            )


        labels = VGroup(*[create_labels(mnemonic) for mnemonic in [soh, cah, toa]])
        arrows = VGroup(
            *[
                map_labels(mnemonic, meaning)
                for mnemonic, meaning in zip([soh, cah, toa], labels)
            ]
        )

        mnemonics_group = VGroup(mnemonics, labels, arrows)
        # self.add(mnemonics, labels, arrows)
       
        self.play(Write(soh))
        self.play(Write(cah))
        self.play(Write(toa))

        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        *[
                            Write(VGroup(arrow, label))
                            for arrow, label in zip(arrows[i], labels[i])
                        ],
                        lag_ratio=1
                    )
                    for i in range(3)
                ],
                lag_ratio=1
            )
        )

        # Add labels to triangle
        hyp_label = Tex("Hyp").scale(0.6).set_color(HYP_COLOR)
        hyp_label.move_to(hyp.get_center()).rotate(angle.get_value()).shift((LEFT + UP) * 0.2)

        base_label = Tex("Adj").scale(0.6).set_color(ADJ_COLOR)

        self.play(
            hyp_len.animate.shift((LEFT + UP) * 0.3),
            FadeIn(hyp_label),
        )
        
        self.play(
            base_len.animate.shift(DOWN * 0.4),
            FadeIn(base_label.next_to(base, DOWN))
        )

        # Calculate y
        triangle_group.add(hyp_label, base_label)
        self.play(
            triangle_group.animate.shift(RIGHT * 3),
            mnemonics_group.animate.scale(0.6),
        )


        cos_value = cos(radians(angle.get_value(degrees=True)))
        y_value = 42 * cos_value
        terms = VGroup(
            *[
                MathTex(rf"{term}")[0] for term in [
                    r"\cos{\theta} = \frac{\text{Adj}}{\text{Hyp}}",
                    r"\cos{41.19^\circ} = \frac{y}{42}",
                    r"42 \times \cos{41.19^\circ} = y",
                    rf"y = 42 \times {cos_value:.8f}",
                    f"y = {y_value:.6f}",
                    f"y = {round(y_value, 2)}",
                ]
            ]
        ).scale(0.7).arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(LEFT * 3).to_edge(UP)

        # for term in terms:
        #     self.add(index_labels(term))
                     
        terms[0][5:8].set_color(ADJ_COLOR)
        terms[0][9:].set_color(HYP_COLOR)

        terms[1][3:9].set_color(ANGLE_COLOR)
        terms[1][10].set_color(ADJ_COLOR)
        terms[1][12:].set_color(HYP_COLOR)

        terms[2][:2].set_color(HYP_COLOR)
        terms[2][6:12].set_color(ANGLE_COLOR)
        terms[2][13].set_color(ADJ_COLOR)

        terms[3][0].set_color(ADJ_COLOR)
        terms[3][2:4].set_color(HYP_COLOR)

        terms[4][0].set_color(ADJ_COLOR)
        terms[5][0].set_color(ADJ_COLOR)
        
        self.play(Write(terms[0][:5]))
        self.play(Write(terms[0][8]))
        self.play(
            FadeIn(terms[0][5:8], target_position=base_label),
            FadeIn(terms[0][9:], target_position=hyp_label),
            run_time=2
        )

        self.play(Write(terms[1]))

        self.play(Write(terms[2][2]))
        self.play(
            FadeIn(terms[2][:2], target_position=terms[1][12:]),
            FadeIn(terms[2][3:12], target_position=terms[1][0:9]),
            FadeIn(terms[2][12], target_position=terms[1][9]),
            FadeIn(terms[2][13], target_position=terms[1][10]),
            run_time=2
        )

        self.play(Write(terms[3]))
        self.play(Write(terms[4]))
        self.play(Write(terms[5]))

        
        self.wait(2)
