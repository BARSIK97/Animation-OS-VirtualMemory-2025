from manimlib import *
import numpy as np
from manimlib import ReplacementTransform

class VirtualMemoryAnimation(Scene):
    def construct(self):
        
        CODE_BG = "#2d2d2d"
        MEMORY_BG = "#1a1a2e"
        OS_BG = "#16213e"
        HIGHLIGHT_COLOR = YELLOW
        ARROW_COLOR = GREEN
        HEAP_COLOR = BLUE
        STACK_COLOR = RED
        FREE_MEM_COLOR = "#555555"
        ALLOCATED_COLOR = "#00ff00"
        DELETE_COLOR = "#ff4444"
        BUDDY_SELECTED_COLOR = "#00ff00"  
        
        
        code_col = Rectangle(
            height=6, width=4,
            fill_color=CODE_BG,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        
        virt_mem_col = Rectangle(
            height=6, width=4,
            fill_color=MEMORY_BG,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        
        os_col = Rectangle(
            height=6, width=4,
            fill_color=OS_BG,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        
        
        code_col.to_edge(LEFT, buff=0.5)
        virt_mem_col.to_edge(LEFT, buff=5)
        os_col.to_edge(LEFT, buff=9.5)
        
        
        code_title = Text("C++ Код программы", font_size=24).next_to(code_col, UP, buff=0.2)
        virt_mem_title = Text("Виртуальная память", font_size=24).next_to(virt_mem_col, UP, buff=0.2)
        os_title = Text("Операционная система", font_size=24).next_to(os_col, UP, buff=0.2)
        
        
        self.add(code_col, virt_mem_col, os_col, code_title, virt_mem_title, os_title)
        
        
        code_lines = VGroup(
            Text("int main() {", font="Consolas", font_size=18, color=WHITE),
            Text("  int* arr = new int[250];", font="Consolas", font_size=18, color=WHITE),
            Text("  // использование массива", font="Consolas", font_size=18, color=WHITE),
            Text("  delete[] arr;", font="Consolas", font_size=18, color=WHITE),
            Text("  return 0;", font="Consolas", font_size=18, color=WHITE),
            Text("}", font="Consolas", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code_lines.move_to(code_col.get_center())
        
        self.play(Write(code_lines))
        self.wait(1)
        
        
        stack_label = Text("Стек", font_size=20, color=STACK_COLOR)
        stack_rect = Rectangle(
            height=1.5, width=3,
            fill_color=STACK_COLOR,
            fill_opacity=0.3,
            stroke_color=STACK_COLOR,
            stroke_width=1
        )
        stack_group = VGroup(stack_label, stack_rect).arrange(DOWN, buff=0.1)
        stack_group.move_to(virt_mem_col.get_center() + UP * 1.5)
        
        heap_label = Text("Куча", font_size=20, color=HEAP_COLOR)
        heap_rect = Rectangle(
            height=2, width=3,
            fill_color=HEAP_COLOR,
            fill_opacity=0.3,
            stroke_color=HEAP_COLOR,
            stroke_width=1
        )
        heap_group = VGroup(heap_label, heap_rect).arrange(DOWN, buff=0.1)
        heap_group.move_to(virt_mem_col.get_center() + DOWN * 1)
        
        self.play(
            Write(stack_group),
            Write(heap_group)
        )
        self.wait(1)
        
        
        free_mem_label = Text("Нераспределенная\nпамять", font_size=18, color=FREE_MEM_COLOR)
        free_mem_blocks = VGroup(*[
            Rectangle(
                height=0.8, width=2.5,
                fill_color=FREE_MEM_COLOR,
                fill_opacity=0.5,
                stroke_color=WHITE,
                stroke_width=0.5
            ) for _ in range(5)
        ]).arrange(DOWN, buff=0.1)
        
        free_mem_group = VGroup(free_mem_label, free_mem_blocks).arrange(DOWN, buff=0.2)
        free_mem_group.move_to(os_col.get_center())
        
        self.play(Write(free_mem_group))
        self.wait(1)
        
        
        new_line = code_lines[1]
        highlight_rect = SurroundingRectangle(new_line, color=HIGHLIGHT_COLOR, buff=0.1)
        
        self.play(ShowCreation(highlight_rect))
        self.wait(1)
        
        
        malloc_text = Text("malloc()", font_size=16, color=ARROW_COLOR)
        malloc_text.move_to(virt_mem_col.get_center() + LEFT * 1.2 + UP * 0.3)
        
        os_call_text = Text("VirtualAlloc()", font_size=16, color=ARROW_COLOR)
        os_call_text.move_to(virt_mem_col.get_center() + RIGHT * 1.2 + UP * 0.3)
        
        arrow = Arrow(
            malloc_text.get_right(),
            os_call_text.get_left(),
            color=ARROW_COLOR,
            buff=0.1
        )
        
        arrow_from_code = Arrow(
            code_col.get_right() + RIGHT * 0.1,
            virt_mem_col.get_left() + LEFT * 0.1,
            color=ARROW_COLOR,
            buff=0.1
        )
        
        self.play(
            GrowArrow(arrow_from_code),
            Write(malloc_text),
            GrowArrow(arrow),
            Write(os_call_text)
        )
        self.wait(1)
        
        
        malloc_arrows_group = VGroup(arrow_from_code, arrow, malloc_text, os_call_text)
        
        
        self.wait(3)
        self.play(FadeOut(malloc_arrows_group))
        
        
        buddy_text = Text("Buddy System", font_size=18, color=YELLOW)
        buddy_text.move_to(os_col.get_center() + UP * 2)
        
        
        big_block = Rectangle(
            height=1.5, width=3,
            fill_color=FREE_MEM_COLOR,
            fill_opacity=0.7,
            stroke_color=WHITE
        )
        big_block.move_to(os_col.get_center())
        big_block_label = Text("Большой блок", font_size=12)
        big_block_label.next_to(big_block, UP, buff=0.1)
        
        self.play(
            Transform(free_mem_blocks, big_block),
            Write(big_block_label),
            Write(buddy_text)
        )
        self.wait(1)
        
        
        self.play(
            FadeOut(big_block),
            FadeOut(big_block_label)
        )
        
        medium_block1 = Rectangle(
            height=1.5, width=1.4,
            fill_color=FREE_MEM_COLOR,
            fill_opacity=0.7,
            stroke_color=WHITE
        )
        medium_block2 = Rectangle(
            height=1.5, width=1.4,
            fill_color=FREE_MEM_COLOR,
            fill_opacity=0.7,
            stroke_color=WHITE
        )
        medium_block1.move_to(os_col.get_center() + LEFT * 0.8)
        medium_block2.move_to(os_col.get_center() + RIGHT * 0.8)
        
        medium_label = Text("Делим пополам", font_size=12)
        medium_label.next_to(medium_block1, UP, buff=0.1)
        
        self.play(
            Write(medium_block1),
            Write(medium_block2),
            Write(medium_label)
        )
        self.wait(1)
        
        
        self.play(
            FadeOut(medium_block1),
            FadeOut(medium_block2),
            FadeOut(medium_label)
        )
        
        small_block1 = Rectangle(
            height=1.5, width=0.6,
            fill_color=FREE_MEM_COLOR,
            fill_opacity=0.7,
            stroke_color=WHITE
        )
        small_block2 = Rectangle(
            height=1.5, width=0.6,
            fill_color=FREE_MEM_COLOR,
            fill_opacity=0.7,
            stroke_color=WHITE
        )
        small_block3 = Rectangle(
            height=1.5, width=0.6,
            fill_color=FREE_MEM_COLOR,
            fill_opacity=0.7,
            stroke_color=WHITE
        )
        small_block4 = Rectangle(
            height=1.5, width=0.6,
            fill_color=FREE_MEM_COLOR,
            fill_opacity=0.7,
            stroke_color=WHITE
        )
        
        small_block1.move_to(os_col.get_center() + LEFT * 1.2 + UP * 0)
        small_block2.move_to(os_col.get_center() + LEFT * 0.4 + UP * 0)
        small_block3.move_to(os_col.get_center() + RIGHT * 0.4 + UP * 0)
        small_block4.move_to(os_col.get_center() + RIGHT * 1.2 + UP * 0)
        
        small_label = Text("Делим еще раз", font_size=12)
        small_label.next_to(small_block1, UP, buff=0.1)
        
        self.play(
            Write(small_block1),
            Write(small_block2),
            Write(small_block3),
            Write(small_block4),
            Write(small_label)
        )
        self.wait(1)
        
        
        selected_block1 = small_block1.copy()
        selected_block1.set_fill(BUDDY_SELECTED_COLOR, opacity=0.9)
        selected_block1.set_stroke(GREEN, width=3)
        
        
        self.play(
            Transform(small_block1, selected_block1),
        )
        self.wait(1)
        
        
        clock = Circle(radius=0.3, color=WHITE)
        clock_hand = Line(clock.get_center(), clock.get_top(), color=WHITE)
        clock_group = VGroup(clock, clock_hand)
        clock_group.move_to(os_col.get_center() + UP * 1.5)
        clock_text = Text("Ожидание...", font_size=12)
        clock_text.next_to(clock_group, DOWN, buff=0.1)
        
        self.play(
            Write(clock_group),
            Write(clock_text)
        )
        
        
        for _ in range(3):
            self.play(Rotate(clock_hand, -PI, about_point=clock.get_center()), run_time=0.5)
        
        self.play(
            FadeOut(clock_group),
            FadeOut(clock_text),
            FadeOut(small_block2),
            FadeOut(small_block3),
            FadeOut(small_block4),
            FadeOut(small_label)
        )
        self.wait(1)
        
        
        pointer_text = Text("Указатель: 0x7FFA1234", font_size=14, color=GREEN)
        pointer_text.move_to(os_col.get_center() + DOWN * 2)
        
        return_arrow = Arrow(
            selected_block1.get_bottom(),
            pointer_text.get_top(),
            color=GREEN,
            buff=0.1
        )
        
        self.play(
            Write(pointer_text),
            GrowArrow(return_arrow)
        )
        self.wait(1)
        
        
        heap_allocated = Rectangle(
            height=0.8, width=2,
            fill_color=ALLOCATED_COLOR,
            fill_opacity=0.7,
            stroke_color=GREEN
        )
        heap_allocated.move_to(heap_rect.get_center())
        heap_addr = Text("0x7FFA1234", font_size=12, color=WHITE)
        heap_addr.next_to(heap_allocated, UP, buff=0.05)
        
        final_arrow = Arrow(
            pointer_text.get_left(),
            heap_allocated.get_right(),
            color=GREEN,
            buff=0.1
        )
        
        self.play(
            Transform(heap_rect, heap_allocated),
            Write(heap_addr),
            GrowArrow(final_arrow)
        )
        self.wait(2)
        
        
        stack_pointer_label = Text("arr = 0x7FFA1234", font_size=14, color=YELLOW)
        stack_pointer_label.move_to(stack_rect.get_center())
        
        self.play(Write(stack_pointer_label))
        self.wait(1)
        
        
        delete_line = code_lines[3]
        delete_highlight = SurroundingRectangle(delete_line, color=DELETE_COLOR, buff=0.1)
        
        self.play(
            FadeOut(highlight_rect),
            ShowCreation(delete_highlight)
        )
        self.wait(1)

if __name__ == "__main__":
    VirtualMemoryAnimation().render()