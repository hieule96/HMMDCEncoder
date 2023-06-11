import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import re
import Lib.Transform as tf
import dataclasses
from typing import List


# utilities
def printI(img, title):
    fig = plt.figure(figsize=(20, 20))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb)
    plt.title(title)
    plt.show()


def printI2(i1, i2):
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(cv2.cvtColor(i1, cv2.COLOR_BGR2RGB))
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.imshow(cv2.cvtColor(i2, cv2.COLOR_BGR2RGB))
    plt.show()


@dataclasses.dataclass
class Node:
    x0: int
    y0: int
    width: int
    height: int
    r1: float = dataclasses.field(default=0.0)
    r2: float = dataclasses.field(default=0.0)
    Ci1: int = dataclasses.field(default=0)
    Ci2: int = dataclasses.field(default=0)
    children: list = dataclasses.field(default_factory=list)
    DRcoeff: np.ndarray = dataclasses.field(default=None)
    bound: list = dataclasses.field(default=None)
    aki: int = dataclasses.field(default=0)
    sigma: int = dataclasses.field(default=None)
    isSkip: bool = dataclasses.field(default=False)

    def get_points(self, img):
        return img[self.y0:self.y0 + self.height, self.x0:self.x0 + self.width]

    def DFS(self):
        yield self
        for child in self.children:
            yield from child.DFS()


@dataclasses.dataclass
class Image:
    img: np.ndarray
    block_size_w: int = 64
    block_size_h: int = 64
    frame: int = 0
    heigh: int = dataclasses.field(init=False)
    width: int = dataclasses.field(init=False)
    ctu_list: list = dataclasses.field(default_factory=list)
    nbCTU: int = dataclasses.field(init=False)
    step_h: int = dataclasses.field(init=False)
    step_w: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.heigh = self.img.shape[0]
        self.width = self.img.shape[1]
        self.step_h = int(self.heigh / self.block_size_h)
        self.step_w = int(self.width / self.block_size_w)
        self.nbCTU = self.step_h * self.step_w
        self.init_ctu()

    def init_ctu(self):
        for y in range(0, self.heigh, self.block_size_h):
            for x in range(0, self.width, self.block_size_w):
                # calculate the width and height for the CTU
                # if it's the last one in the row/column, it should be smaller
                width = min(self.block_size_w, self.width - x)
                height = min(self.block_size_h, self.heigh - y)
                qt = Node(x0=x, y0=y, width=width, height=height)
                self.ctu_list.append(qt)  # Add Node to list

    def get_ctu(self, rs_pos) -> Node:
        return self.ctu_list[rs_pos]

    def get_DRcoeff(self) -> np.ndarray:
        return np.array([ctu.DRcoeff for ctu in self.ctu_list])

    def get_aki(self) -> np.ndarray:
        return np.array([ctu.aki for ctu in self.ctu_list])

    def get_Ci(self, description: int) -> np.ndarray:
        if description == 1:
            return np.array([ctu.Ci1 for ctu in self.ctu_list])
        elif description == 2:
            return np.array([ctu.Ci2 for ctu in self.ctu_list])
        else:
            raise ValueError("description must be 1 or 2")

    def get_bound(self) -> np.ndarray:
        return np.array([ctu.bound for ctu in self.ctu_list])

    def get_r(self, description) -> np.ndarray:
        if description == 1:
            return np.array([ctu.r1 for ctu in self.ctu_list])
        elif description == 2:
            return np.array([ctu.r2 for ctu in self.ctu_list])
        else:
            raise ValueError("description must be 1 or 2")

    def set_r(self, r_new, description):
        for ctu, r in zip(self.ctu_list, r_new):
            if description==1:
                ctu.r1 = r
            elif description==2:
                ctu.r2 = r
            else:
                raise ValueError("description must be 1 or 2")

    def get_flat_nodes(self) -> List[Node]:
        flat_node = [i.DFS() for i in self.ctu_list]
        return flat_node

    def convert_tree_node_to_array(self):
        for i in self.ctu_list:
            if not i.children:
                i.children = None
            else:
                i.children = i.DFS()

    def update_weight(self, salience_map):
        for ctu in self.ctu_list:
            ctu.sigma = np.mean(ctu.get_points(salience_map) / 255)

    def init_aki(self):
        for ctu in self.ctu_list:
            ctu.aki = (ctu.height * ctu.width) / (self.heigh * self.width)


def import_subdivide(node: Node, subdivide_signal_array: List[str], i: int, ctursIndex: int) -> int:
    if i >= len(subdivide_signal_array):  # prevent index out of range error
        return i

    if subdivide_signal_array[i] == "99":
        w_1 = int(math.floor(node.width / 2))
        w_2 = int(math.ceil(node.width / 2))
        h_1 = int(math.floor(node.height / 2))
        h_2 = int(math.ceil(node.height / 2))
        x1 = Node(node.x0, node.y0, w_1, h_1, ctursIndex)  # top left
        x2 = Node(node.x0 + w_1, node.y0, w_2, h_1, ctursIndex)  # top right
        x3 = Node(node.x0, node.y0 + h_1, w_1, h_2, ctursIndex)  # bottom left
        x4 = Node(node.x0 + w_1, node.y0 + h_1, w_2, h_2, ctursIndex)  # bottom right
        i += 1
        if i < len(subdivide_signal_array) and subdivide_signal_array[i] == "99":
            i = import_subdivide(x1, subdivide_signal_array, i, ctursIndex)
        i += 1
        if i < len(subdivide_signal_array) and subdivide_signal_array[i] == "99":
            i = import_subdivide(x2, subdivide_signal_array, i, ctursIndex)
        i += 1
        if i < len(subdivide_signal_array) and subdivide_signal_array[i] == "99":
            i = import_subdivide(x3, subdivide_signal_array, i, ctursIndex)
        i += 1
        if i < len(subdivide_signal_array) and subdivide_signal_array[i] == "99":
            i = import_subdivide(x4, subdivide_signal_array, i, ctursIndex)
        node.children = [x1, x2, x3, x4]

    # If the signal is not 99, it means the node is a leaf, no further subdivision.
    # Nothing to do here, just return the current index.

    return i
