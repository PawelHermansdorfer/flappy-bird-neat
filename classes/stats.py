import pygame
import numpy as np
from .entity import Entity
import src.constants as const
from src.colors import *


def draw_line_dashed(surface, color, start_pos, end_pos, width=1, dash_length=10, exclude_corners=True):
    start_pos = np.array(start_pos)
    end_pos = np.array(end_pos)

    length = np.linalg.norm(end_pos - start_pos)

    dash_amount = int(length / dash_length)

    dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

    return [pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n+1]), width)
            for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]


class Stats(Entity):
    display_center = (const.WIDTH_CENTER, const.HEIGHT * 0.95)
    display_size = (const.WIDTH*0.9, const.HEIGHT*0.5)

    def __init__(self, *args):
        if len(args) == 0:
            raise ValueError('No stats passed')

        super().__init__(
            pos=(self.display_center[0]-self.display_size[0]//2,
                 self.display_center[1]-self.display_size[1]),
            image=pygame.Surface(self.display_size),
            bg_color=TRANSPARENT
        )
        self.hidden = True
        self.font_size = min(round(self.display_size[1] / len(args)),
                            18)
        self.font_line_width = self.font_size
        self.stats_font = pygame.font.Font(const.FONT_VICTOR_MONO, self.font_size)

        self.text_lines = {key: self.stats_font.render(key + ': NAN', True, WHITE_SMOKE) for key in args}
        self.graph = pygame.Surface((0, 0))

    def update_stats(self, key, text):
        text = self.stats_font.render(key + ': ' + text, True, WHITE_SMOKE)
        self.text_lines[key] = text
        self.update_image()

    def draw_nn(self, genome, config):
        """
        Function used to display nodes and connetwions between them of best bird in current generation
        """
        graph_width, grapth_height = self.display_size[0], self.display_size[1]*0.5
        graph = pygame.Surface((graph_width, grapth_height))
        graph = graph.convert_alpha()
        graph.fill(self.bg_color)

        font = pygame.font.Font(const.FONT_VICTOR_MONO, 14)
        input_names = {
                '-1': 'bird y',
                '-2': 'vel y',
                '-3': 'pipe dist',
                '-4': 'Upper pipe x',
                '-5': 'Lower pipe x',
                }

        inputs = config.genome_config.input_keys
        outputs = config.genome_config.output_keys
        nodes = list(genome.nodes.keys())
        connections = genome.connections.values()

        node_radius = 10
        nodes_positions = {}

        gap_between_inputs = (grapth_height-((node_radius*2)*len(inputs)))//(len(inputs)+1)
        x = 140
        for i, node in enumerate(inputs):
            y = (gap_between_inputs+node_radius)*(i+1) + node_radius*i
            nodes_positions[str(node)] = (x, y)
            text = font.render(input_names[str(node)], True, WHITE_SMOKE)
            graph.blit(text, (x-text.get_rect().width-20, y-node_radius))
            if node in nodes:
                nodes.remove(node)

        gap_between_outputs = (grapth_height-((node_radius*2)*len(outputs)))//(len(outputs)+1)
        x = graph_width - 80
        for i, node in enumerate(outputs):
            y = (gap_between_outputs+node_radius)*(i+1) + node_radius*i
            nodes_positions[str(node)] = (x, y)
            if node in nodes:
                nodes.remove(node)

        # NOTE(Aa_Pawelek): When there are more then 1 hidden layer they are all displaied in on column
        gap_between_nodes = (grapth_height-((node_radius*2)*len(nodes)))//(len(nodes)+1)
        x = graph_width//2
        for i, node in enumerate(nodes):
            y = (gap_between_nodes+node_radius)*(i+1) + node_radius*i
            nodes_positions[str(node)] = (x, y)

        for position in nodes_positions.values():
            pygame.draw.circle(graph, WHITE, position, node_radius)

        for con in connections:
            input, output = con.key
            width = 1 if abs(con.weight) <= 1 else 3
            color = LIGHT_BLUE_2 if con.weight > 0 else RED_2
            if con.enabled:
                pygame.draw.line(graph,
                                 color,
                                 nodes_positions[str(input)],
                                 nodes_positions[str(output)],
                                 width
                                 )
            else:
                draw_line_dashed(graph,
                                 color,
                                 nodes_positions[str(input)],
                                 nodes_positions[str(output)],
                                 dash_length=5,
                                 width=width
                                 )

        self.graph = graph
        self.update_image()


    def clear_text(self):
        self.text_lines.clear()
        self.update_image()


    def update_image(self):
        if not self.hidden:
            pygame.draw.rect(
                self.image,
                TRANSPARENT_GREY,
                self.image.get_rect(),
            )
            pygame.draw.rect(
                self.image,
                DARK_BROWN,
                self.image.get_rect(),
                4
            )
            for i, text in enumerate(self.text_lines.values()):
                self.image.blit(text, text.get_rect(left=self.display_size[0]//2-text.get_rect().width//2,
                                                    top=(self.font_line_width*i)+10))
            self.image.blit(self.graph, (0, self.display_size[1]*0.5))
        else:
            self.image.fill(TRANSPARENT)


    def toggle(self):
        """
        Turns of and on visibility of panel
        """
        self.hidden = not self.hidden
        self.update_image()
