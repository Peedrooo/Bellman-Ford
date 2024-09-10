import pygame
import sys
from src.front.colors import *
from src.front.node import Node
from src.front.edge import Edge
from src.back.main import Graph

pygame.init()

WIDTH, HEIGHT = 800, 600
font = pygame.font.Font(None, 32)

# Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bellman-Ford")

# Graph
nodes = []
edges = []
lis_edges = []

connecting = False
start_node = None

node_color = BLUE

def draw_graph():
    screen.fill(BLACK) 
    for edge in edges:
        edge.draw(screen)
    for node in nodes:
        node.draw(screen)


def find_clicked_node(pos):
    for node in nodes:
        dist = ((pos[0] - node.pos[0])**2 + (pos[1] - node.pos[1])**2)**0.5
        if dist < 20:
            return node
    return None

# Main loop
class Interface:
    def __init__(self) -> None:
        self.running = True
        self.clock = pygame.time.Clock()
        self.dragging = False
        self.selected_node = None
    
    def pop_up_cost(self):
        input_box = pygame.Rect(300, 250, 200, 32)
        active = True
        input_text = ''
        error_message = ''

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            if input_text[0] == '-':
                                cost = float(input_text[1::]) * -1
                            else:
                                cost = float(input_text)
                            return cost
                        except ValueError:
                            error_message = "Por favor, insira um número inteiro válido."
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            screen.fill(BLACK)
            
            question_surface = font.render("Insira o custo da aresta:", True, WHITE)
            screen.blit(question_surface, (input_box.x, input_box.y - 40))
            
            pygame.draw.rect(screen, WHITE, input_box, 2)
            text_surface = font.render(input_text, True, WHITE)
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(200, text_surface.get_width() + 10)

            if error_message:
                error_surface = font.render(error_message, True, RED)
                screen.blit(error_surface, (input_box.x, input_box.y + 40))

            pygame.display.flip()
            self.clock.tick(30)
    
    def pop_up_negative_cycle(self):
        input_box = pygame.Rect(200, 250, 500, 100)
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        active = False
                        self.reset_graph()

            screen.fill(BLACK)
            
            message_surface = font.render("Ciclo negativo detectado!", True, RED)
            instruction_surface = font.render("Pressione Enter ou Esc para continuar", True, WHITE)
            screen.blit(message_surface, (input_box.x + 20, input_box.y + 20))
            screen.blit(instruction_surface, (input_box.x + 20, input_box.y + 60))

            pygame.draw.rect(screen, WHITE, input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

    def pop_up_no_path(self):
        input_box = pygame.Rect(200, 250, 500, 100)
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        active = False

            screen.fill(BLACK)
            
            message_surface = font.render("Não existe caminho possível!", True, RED)
            instruction_surface = font.render("Pressione Enter ou Esc para continuar", True, WHITE)
            screen.blit(message_surface, (input_box.x + 20, input_box.y + 20))
            screen.blit(instruction_surface, (input_box.x + 20, input_box.y + 60))

            pygame.draw.rect(screen, WHITE, input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

    def reset_graph(self):
        global nodes, edges, lis_edges, connecting, start_node
        nodes = []
        edges = []
        lis_edges = []
        connecting = False
        start_node = None

    def reset_edge_colors(self):
        for edge in edges:
            edge.color = WHITE

    def run(self):
        global connecting, start_node
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        self.selected_node = find_clicked_node(pos)
                        if self.selected_node is None:
                            new_node = Node(len(nodes)+1, pos)
                            nodes.append(new_node)
                        else:
                            self.dragging = True
                    elif event.button == 3:
                        global start_node
                        if connecting:
                            pos = pygame.mouse.get_pos()
                            end_node = find_clicked_node(pos)
                            if end_node is not None and end_node != start_node:
                                cost = self.pop_up_cost()
                                edge = Edge(start_node, end_node, cost)
                                lis_edges.append([nodes.index(start_node)+1, nodes.index(end_node)+1, cost])
                                edges.append(edge)
                            connecting = False
                        else:
                            pos = pygame.mouse.get_pos()
                            start_node = find_clicked_node(pos)
                            if start_node is not None:
                                connecting = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False
                        self.selected_node = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if len(nodes) >= 2:
                            grph = Graph(nodes, [(nodes.index(e.start)+1, nodes.index(e.end)+1, e.cost) for e in edges])
                            distances, path, has_negative_cycle = grph.run()

                            if has_negative_cycle:
                                self.pop_up_negative_cycle()
                            elif not path or path[0] != 1 or path[-1] != len(nodes):
                                self.pop_up_no_path()
                            else:
                                self.reset_edge_colors()
                                for i in range(len(path) - 1):
                                    for edge in edges:
                                        if (nodes.index(edge.start)+1 == path[i] and nodes.index(edge.end)+1 == path[i+1]) or \
                                           (nodes.index(edge.end)+1 == path[i] and nodes.index(edge.start)+1 == path[i+1]):
                                            edge.color = BLUE
            if self.dragging and self.selected_node is not None:
                pos = pygame.mouse.get_pos()
                self.selected_node.pos = pos

            draw_graph()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    Interface().run()
