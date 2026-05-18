import pygame
import sys
from modules.data_structures.data_structures_visualiser import run as run_data_structures
from modules.sorting.sorting_visualiser import run as run_sorting
from modules.graphs.graphs_visualiser import run as run_graphs

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Explorer")

FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()


def draw_text(text, pos):
    txt_surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)


def main_menu():
    screen.fill((200, 200, 250))
    draw_text("DSA Explorer and Visualiser", (WIDTH // 3, 50))

    buttons = {
        'Data Structures': pygame.Rect(300, 150, 200, 50),
        'Sorting':         pygame.Rect(300, 230, 200, 50),
        'Graphs':          pygame.Rect(300, 310, 200, 50),
        'Exit':            pygame.Rect(300, 390, 200, 50),
    }

    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 20, rect.y + 10))

    pygame.display.flip()
    return buttons


def main():
    running = True
    current_module = None

    while running:
        if current_module is None:
            buttons = main_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for name, rect in buttons.items():
                        if rect.collidepoint(pos):
                            if name == "Exit":
                                running = False
                            else:
                                current_module = name
        else:
            try:
                if current_module == "Data Structures":
                    run_data_structures(screen)
                elif current_module == "Sorting":
                    run_sorting(screen)
                elif current_module == "Graphs":
                    run_graphs(screen)
            except SystemExit:
                running = False
                break
            finally:
                current_module = None

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()