import pygame
import sys
import random

from modules.shared import clock, draw_test_overlay
from modules.sorting.bubble_sort import BubbleSort
from tests.sorting.test_bubble_sort import TestBubbleSort
from modules.sorting.selection_sort import SelectionSort
from tests.sorting.test_selection_sort import TestSelectionSort
from modules.sorting.merge_sort import MergeSort
from tests.sorting.test_merge_sort import TestMergeSort


def _sorting_visualisation(screen, font, algo_fn, test_class, label):
    WIDTH, HEIGHT = screen.get_size()
    ARRAY_SIZE    = 30
    bar_width     = WIDTH // ARRAY_SIZE
    running       = True

    def fresh_array():
        return [random.randint(10, HEIGHT - 60) for _ in range(ARRAY_SIZE)]

    array = fresh_array()

    def draw_array(arr, compare=None, swap=None, sorted_up_to=None):
        screen.fill((30, 32, 40))
        for i, val in enumerate(arr):
            if swap and i in swap:
                color = (100, 255, 150)
            elif compare and i in compare:
                color = (255, 120, 100)
            elif sorted_up_to is not None and i >= sorted_up_to:
                color = (100, 220, 180)
            else:
                color = (100, 160, 250)
            pygame.draw.rect(screen, color,
                             (i * bar_width, HEIGHT - val - 30, bar_width - 2, val))
        info = font.render(
            f"{label}  |  SPACE: Sort  |  R: Reset  |  T: Tests  |  ESC: Menu",
            True, (180, 180, 200)
        )
        screen.blit(info, (10, 10))
        pygame.display.flip()

    def check_sorting_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    draw_array(array)

    while running:
        pygame.time.wait(16)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    array = fresh_array()
                    draw_array(array)
                    pygame.time.wait(600)
                    algo_fn(array, draw_array, pygame.time.wait, check_sorting_events)

                    holding = True
                    while holding and running:
                        draw_array(array, sorted_up_to=0)
                        pygame.time.wait(16)
                        for event2 in pygame.event.get():
                            if event2.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event2.type == pygame.KEYDOWN:
                                if event2.key == pygame.K_ESCAPE:
                                    running = False
                                elif event2.key == pygame.K_r:
                                    array = fresh_array()
                                    draw_array(array)
                                elif event2.key == pygame.K_t:
                                    draw_test_overlay(screen, font, test_class, label)
                                holding = False

                elif event.key == pygame.K_r:
                    array = fresh_array()
                    draw_array(array)

                elif event.key == pygame.K_t:
                    draw_test_overlay(screen, font, test_class, label)

        draw_array(array)


def bubble_sort_visualisation(screen, font):
    _sorting_visualisation(screen, font, BubbleSort, TestBubbleSort, "Bubble Sort")


def selection_sort_visualisation(screen, font):
    _sorting_visualisation(screen, font, SelectionSort, TestSelectionSort, "Selection Sort")


def merge_sort_visualisation(screen, font):
    _sorting_visualisation(screen, font, MergeSort, TestMergeSort, "Merge Sort")


def run(screen):
    font = pygame.font.SysFont(None, 28)
    menu_items = [
        "Bubble Sort Visualisation",
        "Selection Sort Visualisation",
        "Merge Sort Visualisation",
        "Back",
    ]
    selected = 0
    running = True

    while running:
        screen.fill((220, 220, 220))
        for i, item in enumerate(menu_items):
            color = (255, 0, 0) if i == selected else (0, 0, 0)
            text = font.render(item, True, color)
            screen.blit(text, (100, 100 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    choice = menu_items[selected]
                    if choice == "Bubble Sort Visualisation":
                        bubble_sort_visualisation(screen, font)
                    elif choice == "Selection Sort Visualisation":
                        selection_sort_visualisation(screen, font)
                    elif choice == "Merge Sort Visualisation":
                        merge_sort_visualisation(screen, font)
                    elif choice == "Back":
                        running = False
        clock.tick(30)