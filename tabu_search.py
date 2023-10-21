import math
import random
from collections import deque
from heapq import heappush, heappop

cities = [
    "FORTALEZA",
    "CAUCAIA",
    "JUAZEIRO DO NORTE",
    "MARACANAÚ",
    "SOBRAL",
    "CRATO",
    "ITAPIPOCA",
    "MARANGUAPE",
    "IGUATU",
    "QUIXADÁ",
    "PACATUBA",
    "QUIXERAMOBIM",
    "AQUIRAZ",
    "CANINDÉ",
    "CRATEÚS",
    "ARACATI",
    "PACAJUS",
    "RUSSAS",
    "ICÓ",
    "TIANGUÁ",
]

costs = [
    [0, 20, 500, 30, 220, 400, 90, 40, 320, 220, 10, 180, 25, 130, 260, 110, 35, 280, 170, 410],
    [20, 0, 480, 28, 240, 420, 110, 60, 300, 200, 8, 160, 15, 140, 270, 100, 25, 260, 150, 400],
    [500, 480, 0, 510, 180, 560, 410, 470, 260, 360, 490, 320, 475, 375, 190, 410, 485, 170, 295, 60],
    [30, 28, 510, 0, 280, 460, 50, 75, 320, 220, 22, 190, 20, 140, 270, 100, 25, 260, 150, 400],
    [220, 240, 180, 280, 0, 360, 190, 260, 330, 240, 235, 70, 220, 45, 260, 220, 245, 30, 155, 200],
    [400, 420, 560, 460, 360, 0, 510, 500, 160, 60, 410, 190, 390, 440, 540, 300, 420, 400, 390, 520],
    [90, 110, 410, 50, 190, 510, 0, 50, 270, 170, 85, 140, 35, 70, 180, 65, 100, 160, 90, 350],
    [40, 60, 470, 75, 260, 500, 50, 0, 310, 210, 35, 150, 25, 95, 220, 55, 80, 210, 100, 360],
    [320, 300, 260, 320, 330, 160, 270, 310, 0, 100, 310, 140, 295, 195, 110, 230, 260, 140, 30, 250],
    [220, 200, 360, 220, 240, 60, 170, 210, 100, 0, 220, 100, 195, 170, 300, 60, 120, 70, 165, 180],
    [10, 8, 490, 22, 235, 410, 85, 35, 310, 220, 0, 150, 15, 120, 250, 80, 15, 250, 140, 380],
    [180, 160, 320, 190, 70, 190, 140, 150, 140, 100, 150, 0, 155, 30, 230, 90, 115, 90, 15, 200],
    [25, 15, 475, 20, 220, 390, 35, 25, 295, 195, 15, 155, 0, 115, 245, 75, 10, 245, 135, 375],
    [130, 140, 375, 140, 45, 440, 70, 95, 195, 170, 120, 30, 115, 0, 290, 100, 125, 45, 90, 225],
    [260, 270, 190, 270, 260, 540, 180, 220, 110, 300, 250, 230, 245, 290, 0, 320, 350, 220, 170, 80],
    [110, 100, 410, 100, 220, 300, 65, 55, 230, 60, 80, 90, 75, 100, 320, 0, 65, 160, 100, 300],
    [35, 25, 485, 25, 245, 420, 100, 80, 260, 120, 15, 115, 10, 125, 350, 65, 0, 235, 125, 365],
    [280, 260, 170, 260, 30, 400, 160, 210, 140, 70, 250, 90, 245, 45, 220, 160, 235, 0, 125, 170],
    [170, 150, 295, 150, 155, 390, 90, 100, 30, 165, 140, 15, 135, 90, 170, 100, 125, 125, 0, 240],
    [410, 400, 60, 400, 200, 520, 350, 360, 250, 180, 380, 200, 375, 225, 80, 300, 365, 170, 240, 0]
]

# The 'S' state will be an Array of Indexes

# TODO; Maybe generate a class and a unique hashcode for each array
CostAndState = tuple[float, list[int]]

NGB_SIZE: int
BEST_S: CostAndState = math.inf, []


def tabu_search(iterations: int = 10_000, neighborhood_size: int = 10, threshold=1, queue_len=10):
    global NGB_SIZE, BEST_S
    NGB_SIZE = neighborhood_size

    curr_s: CostAndState = gen_fisrt()  # Current is allways the best in the neighborhood
    tabu_queue: deque[CostAndState] = deque(maxlen=queue_len)

    repetead = 0
    i = 0
    while i <= iterations and repetead <= 20:
        i += 1
        tabu_queue.append(curr_s)

        # The neighborhood is already in a heap.
        neighborhood: list[CostAndState] = get_neighborhood(curr_s)

        c = heappop(neighborhood)
        while is_tabu(c, tabu_queue) and len(neighborhood) > 0:
            c = heappop(neighborhood)

        if len(neighborhood) > 0:
            curr_s = c

        if test_threshold(curr_s[0], BEST_S[0], threshold):
            repetead += 1

        if curr_s[0] < BEST_S[0]:
            BEST_S = curr_s


def test_threshold(c1: float, c2: float, threshold: float):
    return c1 - c2 <= threshold


def is_tabu(state: CostAndState, tabu_queue: deque[CostAndState]):
    return (state in tabu_queue) and (not aceptance_of_s(state))


def aceptance_of_s(state: CostAndState):
    return BEST_S[0] > state[0]


def gen_fisrt() -> CostAndState:
    amount = len(cities) - 1
    sample = random_gen.sample([i + 1 for i in range(amount)], amount)
    return fitness(sample), sample


# The state list will be acounted without first state
def fitness(state: list[int], invert=False) -> float:
    global costs
    prev = 0
    cost = 0
    for index in state:
        cost += costs[prev][index]
        prev = index

    total_cost = cost + costs[state[len(state) - 1]][0]
    return total_cost if invert is False else -total_cost


def get_neighborhood(state) -> list[CostAndState]:
    global NGB_SIZE
    heap = []

    for i in range(NGB_SIZE):
        node1 = 0
        node2 = 0

        while node1 == node2:
            amount = len(state[1]) - 1
            node1 = random_gen.randint(1, amount)
            node2 = random_gen.randint(1, amount)

        if node1 > node2:
            swap = node1
            node1 = node2
            node2 = swap

        tmp = state[1][node1:node2]
        tmp_state = state[1][0:node1] + tmp[::-1] + state[1][node2:]  # Without fisrt city

        heappush(heap, (fitness(tmp_state), tmp_state))

    return heap


def pretty_print(path: list[int]):
    print('Path:\n\t', end='')
    for index in path:
        print(cities[index] + ' -> ', end='')

    print(cities[0])


if __name__ == '__main__':
    random_gen = random.Random(1)
    tabu_search()
    pretty_print(BEST_S[1])
