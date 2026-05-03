"""
WaselX Express — Professional DSA Prototype
MAIB Final Project | Data Structures & Algorithms

AI-assisted cleanup/refactor note:
This file was cleaned and reorganized with ChatGPT assistance for debugging,
structure, and readability. The team must review, understand, and be able to
explain every section before submission.

Deployment:
    streamlit run final_cleaned.py

Self-test without Streamlit/Plotly installed:
    python final_cleaned.py --self-test
"""

from __future__ import annotations

import random
import sys
import time
from dataclasses import dataclass
from math import ceil, log2, isinf
from typing import Any, Dict, Iterable, List, Optional, Tuple

# =============================================================================
# BUSINESS DATA FROM THE FINAL PROJECT BRIEF
# =============================================================================

NODES: List[str] = [
    "H1", "H2", "H3", "H4", "H5", "H6", "H7",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
]

# id: name, type, emirate, daily_orders, latitude, longitude
NODE_INFO: Dict[str, Tuple[str, str, str, int, float, float]] = {
    "H1": ("Dubai Marina Hub", "Hub", "Dubai", 450, 25.0807, 55.1332),
    "H2": ("Business Bay Hub", "Hub", "Dubai", 520, 25.1851, 55.2795),
    "H3": ("Deira Hub", "Hub", "Dubai", 380, 25.2697, 55.3095),
    "H4": ("JLT Hub", "Hub", "Dubai", 290, 25.0657, 55.1453),
    "H5": ("Abu Dhabi Corniche Hub", "Hub", "Abu Dhabi", 410, 24.4667, 54.3667),
    "H6": ("Khalifa City Hub", "Hub", "Abu Dhabi", 310, 24.4215, 54.4860),
    "H7": ("Sharjah Al Nahda Hub", "Hub", "Sharjah", 340, 25.3283, 55.4119),
    "D1": ("Downtown Dubai", "Delivery Zone", "Dubai", 280, 25.1972, 55.2744),
    "D2": ("Al Quoz Industrial", "Delivery Zone", "Dubai", 150, 25.1380, 55.2220),
    "D3": ("Jumeirah", "Delivery Zone", "Dubai", 200, 25.1298, 55.1882),
    "D4": ("Silicon Oasis", "Delivery Zone", "Dubai", 180, 25.1190, 55.3796),
    "D5": ("Ajman City Centre", "Delivery Zone", "Ajman", 130, 25.4106, 55.4354),
    "D6": ("Yas Island", "Delivery Zone", "Abu Dhabi", 160, 24.4674, 54.6074),
    "D7": ("Al Reem Island", "Delivery Zone", "Abu Dhabi", 220, 24.4972, 54.4034),
    "D8": ("Muwaileh (University City)", "Delivery Zone", "Sharjah", 190, 25.3170, 55.5040),
}

# from, to, road, distance_km, time_min, cost_aed
EDGES: List[Tuple[str, str, str, float, float, float]] = [
    ("H1", "H4", "Sheikh Zayed Rd", 5, 10, 3.5),
    ("H1", "D3", "Jumeirah Beach Rd", 4, 12, 3.0),
    ("H1", "D1", "Al Khail Rd", 8, 15, 5.5),
    ("H4", "D2", "Hessa St", 6, 14, 4.0),
    ("H4", "H2", "Sheikh Zayed Rd", 7, 13, 5.0),
    ("H2", "D1", "Financial Centre Rd", 3, 8, 2.5),
    ("H2", "H3", "Al Maktoum Bridge", 9, 18, 6.0),
    ("H3", "D4", "Dubai-Al Ain Rd", 12, 22, 8.0),
    ("H3", "H7", "Emirates Rd", 15, 25, 10.0),
    ("H7", "D8", "University Rd", 4, 8, 3.0),
    ("H7", "D5", "Sheikh Mohammed Rd", 10, 18, 7.0),
    ("D1", "D3", "2nd December St", 5, 11, 3.5),
    ("D1", "D2", "Al Khail Rd", 6, 13, 4.0),
    ("D2", "D4", "Hatta Rd", 10, 20, 7.0),
    ("H5", "D7", "Corniche Rd", 6, 12, 4.0),
    ("H5", "H6", "Abu Dhabi Ring Rd", 14, 20, 9.0),
    ("H6", "D6", "Yas Connector", 8, 15, 5.5),
    ("D6", "D7", "Al Saadiyat Bridge", 7, 13, 5.0),
    ("H5", "D6", "Island Bypass", 12, 22, 8.0),
    ("D4", "D8", "Academic City Rd", 18, 30, 12.0),
    ("H3", "D2", "Al Asayel St", 8, 16, 5.5),
    ("H1", "H2", "Happiness St", 10, 18, 7.0),
    ("D5", "D8", "Sharjah Ring Rd", 8, 15, 5.5),
    ("H6", "D7", "Reem Bridge", 10, 18, 7.0),
]

POS: Dict[str, Tuple[float, float]] = {node: (NODE_INFO[node][5], NODE_INFO[node][4]) for node in NODES}
EMIRATE_COLORS = {
    "Dubai": "#2E75B6",
    "Abu Dhabi": "#C55A11",
    "Sharjah": "#375623",
    "Ajman": "#7030A0",
}

TEAM_MEMBERS = [
    "Anurag Devarakonda",
    "Anish Borkar",
    "Nandana Santhosh",
    "Neha Thapa",
    "Sarth Malankar",
]

WEIGHT_INDEX = {"distance": 3, "time": 4, "cost": 5}
WEIGHT_LABEL = {"distance": "km", "time": "min", "cost": "AED"}
INF = float("inf")


# =============================================================================
# FROM-SCRATCH DATA STRUCTURES
# =============================================================================

class MinHeap:
    """Binary min-heap implemented from scratch, with FIFO tie-breaking."""

    def __init__(self) -> None:
        self._heap: List[Tuple[Any, ...]] = []
        self._counter = 0

    def push(self, priority: float, value: Any, *extra: Any) -> Tuple[Any, ...]:
        item = (priority, self._counter, value, *extra)
        self._counter += 1
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)
        return item

    def pop(self) -> Tuple[Any, ...]:
        if not self._heap:
            raise IndexError("pop from empty MinHeap")
        root = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return root

    def peek(self) -> Optional[Tuple[Any, ...]]:
        return self._heap[0] if self._heap else None

    def display(self) -> List[Tuple[Any, ...]]:
        return sorted(self._heap)

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._heap[index] < self._heap[parent]:
                self._heap[index], self._heap[parent] = self._heap[parent], self._heap[index]
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        size = len(self._heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            if left < size and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < size and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest == index:
                break
            self._heap[index], self._heap[smallest] = self._heap[smallest], self._heap[index]
            index = smallest


class SimpleQueue:
    """FIFO queue implemented with a head pointer, avoiding collections.deque."""

    def __init__(self, initial: Optional[Iterable[Any]] = None) -> None:
        self._items = list(initial or [])
        self._head = 0

    def enqueue(self, item: Any) -> None:
        self._items.append(item)

    def dequeue(self) -> Any:
        if self._head >= len(self._items):
            raise IndexError("dequeue from empty queue")
        item = self._items[self._head]
        self._head += 1
        if self._head > 50 and self._head * 2 > len(self._items):
            self._items = self._items[self._head:]
            self._head = 0
        return item

    def display(self) -> List[Any]:
        return self._items[self._head:]

    def __bool__(self) -> bool:
        return self._head < len(self._items)


class Stack:
    """LIFO stack used for order lifecycle and DFS."""

    def __init__(self) -> None:
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Optional[Any]:
        return self._items[-1] if self._items else None

    def display_top_first(self) -> List[Any]:
        return list(reversed(self._items))

    def display_bottom_first(self) -> List[Any]:
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)


class DLLNode:
    def __init__(self, stop_name: str, order_id: str, eta: str) -> None:
        self.stop_name = stop_name
        self.order_id = order_id
        self.eta = eta
        self.prev: Optional[DLLNode] = None
        self.next: Optional[DLLNode] = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head: Optional[DLLNode] = None
        self.tail: Optional[DLLNode] = None
        self._size = 0

    def append(self, stop_name: str, order_id: str, eta: str) -> DLLNode:
        node = DLLNode(stop_name, order_id, eta)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node

    def insert_after(self, target_order_id: str, stop_name: str, order_id: str, eta: str) -> Optional[DLLNode]:
        cur = self.head
        while cur:
            if cur.order_id == target_order_id:
                new_node = DLLNode(stop_name, order_id, eta)
                new_node.prev = cur
                new_node.next = cur.next
                if cur.next:
                    cur.next.prev = new_node
                else:
                    self.tail = new_node
                cur.next = new_node
                self._size += 1
                return new_node
            cur = cur.next
        return None

    def delete_by_order_id(self, order_id: str) -> Optional[DLLNode]:
        cur = self.head
        while cur:
            if cur.order_id == order_id:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                cur.prev = cur.next = None
                self._size -= 1
                return cur
            cur = cur.next
        return None

    def display_forward(self) -> List[Tuple[str, str, str]]:
        out = []
        cur = self.head
        while cur:
            out.append((cur.stop_name, cur.order_id, cur.eta))
            cur = cur.next
        return out

    def display_reverse(self) -> List[Tuple[str, str, str]]:
        out = []
        cur = self.tail
        while cur:
            out.append((cur.stop_name, cur.order_id, cur.eta))
            cur = cur.prev
        return out

    def __len__(self) -> int:
        return self._size


class CLLNode:
    def __init__(self, rider_name: str) -> None:
        self.rider_name = rider_name
        self.next: Optional[CLLNode] = None


class CircularLinkedList:
    def __init__(self) -> None:
        self.tail: Optional[CLLNode] = None
        self.current: Optional[CLLNode] = None
        self._size = 0

    def add_rider(self, rider_name: str) -> None:
        node = CLLNode(rider_name)
        if self.tail is None:
            node.next = node
            self.tail = node
            self.current = node
        else:
            node.next = self.tail.next
            self.tail.next = node
            self.tail = node
        self._size += 1

    def remove_rider(self, rider_name: str) -> bool:
        if self.tail is None:
            return False
        prev = self.tail
        cur = self.tail.next
        for _ in range(self._size):
            if cur and cur.rider_name == rider_name:
                if self._size == 1:
                    self.tail = None
                    self.current = None
                else:
                    prev.next = cur.next
                    if cur == self.tail:
                        self.tail = prev
                    if cur == self.current:
                        self.current = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next if cur else None
        return False

    def assign_next_order(self) -> Optional[str]:
        if self.current is None:
            return None
        rider = self.current.rider_name
        self.current = self.current.next
        return rider

    def display_roster(self) -> List[str]:
        if self.tail is None:
            return []
        roster = []
        cur = self.tail.next
        for _ in range(self._size):
            if cur is None:
                break
            roster.append(cur.rider_name)
            cur = cur.next
        return roster


# =============================================================================
# GRAPH ALGORITHMS
# =============================================================================

@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    road: str
    distance: float
    time: float
    cost: float

    def weight(self, criterion: str) -> float:
        return {"distance": self.distance, "time": self.time, "cost": self.cost}[criterion]

    def key(self) -> Tuple[str, str]:
        return normalized_edge(self.source, self.target)


def normalized_edge(u: str, v: str) -> Tuple[str, str]:
    return tuple(sorted((u, v)))


class WaselGraph:
    def __init__(self, blocked_edges: Optional[Iterable[Tuple[str, str]]] = None,
                 extra_edges: Optional[Iterable[Edge]] = None) -> None:
        self.nodes = list(NODES)
        self.index = {node: i for i, node in enumerate(self.nodes)}
        self.blocked = {normalized_edge(u, v) for u, v in (blocked_edges or [])}
        self.edges: List[Edge] = [Edge(*edge) for edge in EDGES]
        if extra_edges:
            self.edges.extend(extra_edges)
        self.adj: Dict[str, List[Edge]] = {node: [] for node in self.nodes}
        for edge in self.edges:
            if edge.key() in self.blocked:
                continue
            self.adj[edge.source].append(edge)
            self.adj[edge.target].append(Edge(edge.target, edge.source, edge.road, edge.distance, edge.time, edge.cost))

    def neighbors(self, node: str) -> List[Edge]:
        return self.adj[node]

    def edge_between(self, u: str, v: str) -> Optional[Edge]:
        for edge in self.adj.get(u, []):
            if edge.target == v:
                return edge
        return None

    def adjacency_list_rows(self) -> List[Dict[str, str]]:
        rows = []
        for node in self.nodes:
            rows.append({
                "Node": node,
                "Neighbors": ", ".join(
                    f"{e.target}(d={e.distance:g}, t={e.time:g}, c={e.cost:g})" for e in self.adj[node]
                ) or "None",
            })
        return rows

    def adjacency_matrix(self, criterion: str = "distance") -> List[List[float]]:
        size = len(self.nodes)
        matrix = [[INF for _ in range(size)] for _ in range(size)]
        for i in range(size):
            matrix[i][i] = 0
        for edge in self.edges:
            if edge.key() in self.blocked:
                continue
            i, j = self.index[edge.source], self.index[edge.target]
            w = edge.weight(criterion)
            if w < matrix[i][j]:
                matrix[i][j] = w
                matrix[j][i] = w
        return matrix

    def dijkstra(self, source: str, destination: str, criterion: str = "distance") -> Dict[str, Any]:
        dist = {node: INF for node in self.nodes}
        prev: Dict[str, Optional[str]] = {node: None for node in self.nodes}
        visited = set()
        trace = []
        heap = MinHeap()
        dist[source] = 0
        heap.push(0, source)
        trace.append({
            "step": 0,
            "action": f"Initialize source {source}",
            "current": source,
            "visited": [],
            "distances": dict(dist),
            "previous": dict(prev),
        })
        step = 1
        while heap:
            current_distance, _, current = heap.pop()[:3]
            if current in visited:
                continue
            visited.add(current)
            trace.append({
                "step": step,
                "action": f"Visit {current} at {current_distance:g}",
                "current": current,
                "visited": sorted(visited),
                "distances": dict(dist),
                "previous": dict(prev),
            })
            step += 1
            if current == destination:
                break
            for edge in self.neighbors(current):
                if edge.target in visited:
                    continue
                candidate = dist[current] + edge.weight(criterion)
                if candidate < dist[edge.target]:
                    old = dist[edge.target]
                    dist[edge.target] = candidate
                    prev[edge.target] = current
                    heap.push(candidate, edge.target)
                    trace.append({
                        "step": step,
                        "action": f"Relax {current}->{edge.target} via {edge.road}: {format_number(old)} -> {candidate:g}",
                        "current": current,
                        "relaxed_edge": (current, edge.target),
                        "visited": sorted(visited),
                        "distances": dict(dist),
                        "previous": dict(prev),
                    })
                    step += 1
        path = reconstruct_path(prev, source, destination)
        return {
            "path": path,
            "best": dist[destination],
            "distances": dist,
            "previous": prev,
            "trace": trace,
            "metrics": self.path_metrics(path),
        }

    def path_metrics(self, path: List[str]) -> Dict[str, float]:
        if not path or len(path) == 1:
            return {"distance": 0.0, "time": 0.0, "cost": 0.0} if path else {"distance": INF, "time": INF, "cost": INF}
        totals = {"distance": 0.0, "time": 0.0, "cost": 0.0}
        for u, v in zip(path, path[1:]):
            edge = self.edge_between(u, v)
            if edge is None:
                return {"distance": INF, "time": INF, "cost": INF}
            totals["distance"] += edge.distance
            totals["time"] += edge.time
            totals["cost"] += edge.cost
        return totals

    def bfs(self, start: str) -> Dict[str, Any]:
        q = SimpleQueue([start])
        seen = {start}
        parent: Dict[str, Optional[str]] = {start: None}
        order: List[str] = []
        trace = []
        while q:
            node = q.dequeue()
            order.append(node)
            added = []
            for edge in self.neighbors(node):
                if edge.target not in seen:
                    seen.add(edge.target)
                    parent[edge.target] = node
                    q.enqueue(edge.target)
                    added.append(edge.target)
            trace.append({"current": node, "visited": list(order), "queue": q.display(), "added": added})
        return {"order": order, "parent": parent, "trace": trace, "reachable_all": len(order) == len(self.nodes)}

    def dfs(self, start: str) -> Dict[str, Any]:
        stack = Stack()
        stack.push((start, None))
        seen = set()
        parent: Dict[str, Optional[str]] = {start: None}
        order: List[str] = []
        while len(stack) > 0:
            node, par = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            parent.setdefault(node, par)
            order.append(node)
            # reversed preserves visible adjacency-list order in iterative DFS
            for edge in reversed(self.neighbors(node)):
                if edge.target not in seen:
                    parent.setdefault(edge.target, node)
                    stack.push((edge.target, node))
        return {"order": order, "parent": parent, "reachable_all": len(order) == len(self.nodes)}

    def connected_components(self) -> List[List[str]]:
        unseen = set(self.nodes)
        components = []
        while unseen:
            start = sorted(unseen)[0]
            result = self.bfs(start)
            comp = sorted(result["order"])
            components.append(comp)
            unseen -= set(comp)
        return components

    def floyd_warshall(self, nodes: Optional[List[str]] = None, criterion: str = "time") -> Dict[str, Any]:
        selected = list(nodes or self.nodes)
        idx = {node: i for i, node in enumerate(selected)}
        n = len(selected)
        dist = [[INF for _ in range(n)] for _ in range(n)]
        nxt: List[List[Optional[str]]] = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for edge in self.edges:
            if edge.key() in self.blocked:
                continue
            if edge.source in idx and edge.target in idx:
                i, j = idx[edge.source], idx[edge.target]
                w = edge.weight(criterion)
                if w < dist[i][j]:
                    dist[i][j] = dist[j][i] = w
                    nxt[i][j] = edge.target
                    nxt[j][i] = edge.source
        initial = [row[:] for row in dist]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]
        return {"nodes": selected, "initial": initial, "final": dist, "next": nxt}

    def kruskal_mst(self) -> Dict[str, Any]:
        parent = {node: node for node in self.nodes}
        rank = {node: 0 for node in self.nodes}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: str, b: str) -> bool:
            root_a, root_b = find(a), find(b)
            if root_a == root_b:
                return False
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
            return True

        chosen: List[Edge] = []
        rejected: List[Edge] = []
        trace = []
        for edge in sorted(self.edges, key=lambda e: (e.cost, e.distance, e.source, e.target)):
            if edge.key() in self.blocked:
                continue
            if union(edge.source, edge.target):
                chosen.append(edge)
                action = "ADDED"
                reason = "No cycle"
            else:
                rejected.append(edge)
                action = "REJECTED"
                reason = "Cycle would be formed"
            trace.append({
                "edge": f"{edge.source}-{edge.target}",
                "road": edge.road,
                "cost": edge.cost,
                "action": action,
                "reason": reason,
                "running_total": sum(e.cost for e in chosen),
            })
        return {
            "edges": chosen,
            "rejected": rejected,
            "trace": trace,
            "total": sum(e.cost for e in chosen),
            "components": self.connected_components(),
            "is_spanning_tree": len(chosen) == len(self.nodes) - 1 and len(self.connected_components()) == 1,
        }

    def prim_mst(self, start: str = "H2") -> Dict[str, Any]:
        visited = {start}
        heap = MinHeap()
        chosen: List[Edge] = []
        trace = []

        def add_edges(node: str) -> None:
            for edge in self.neighbors(node):
                if edge.target not in visited:
                    heap.push(edge.cost, edge)

        add_edges(start)
        while heap and len(visited) < len(self.nodes):
            _, _, edge = heap.pop()[:3]
            if edge.target in visited:
                continue
            visited.add(edge.target)
            chosen.append(edge)
            trace.append({
                "edge": f"{edge.source}-{edge.target}",
                "road": edge.road,
                "cost": edge.cost,
                "running_total": sum(e.cost for e in chosen),
            })
            add_edges(edge.target)
        return {
            "edges": chosen,
            "trace": trace,
            "total": sum(e.cost for e in chosen),
            "visited": sorted(visited),
            "is_complete": len(visited) == len(self.nodes),
        }


def reconstruct_path(prev: Dict[str, Optional[str]], source: str, destination: str) -> List[str]:
    if source == destination:
        return [source]
    if prev[destination] is None:
        return []
    path = []
    cur: Optional[str] = destination
    while cur is not None:
        path.append(cur)
        if cur == source:
            break
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == source else []


def format_number(value: float, decimals: int = 1) -> str:
    if isinf(value):
        return "INF"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.{decimals}f}"


def path_to_string(path: List[str]) -> str:
    return " -> ".join(path) if path else "No route available"


# =============================================================================
# TREE ALGORITHMS
# =============================================================================

class TreeNode:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        self.height = 1


def bst_insert(root: Optional[TreeNode], key: int) -> TreeNode:
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    elif key > root.key:
        root.right = bst_insert(root.right, key)
    return root


def build_bst(keys: Iterable[int]) -> Optional[TreeNode]:
    root: Optional[TreeNode] = None
    for key in keys:
        root = bst_insert(root, key)
    return root


def tree_height(node: Optional[TreeNode]) -> int:
    return node.height if node else 0


def update_height(node: TreeNode) -> None:
    node.height = 1 + max(tree_height(node.left), tree_height(node.right))


def balance_factor(node: Optional[TreeNode]) -> int:
    return tree_height(node.left) - tree_height(node.right) if node else 0


def rotate_right(y: TreeNode) -> TreeNode:
    x = y.left
    assert x is not None
    t2 = x.right
    x.right = y
    y.left = t2
    update_height(y)
    update_height(x)
    return x


def rotate_left(x: TreeNode) -> TreeNode:
    y = x.right
    assert y is not None
    t2 = y.left
    y.left = x
    x.right = t2
    update_height(x)
    update_height(y)
    return y


def avl_insert(root: Optional[TreeNode], key: int, rotations: List[str]) -> TreeNode:
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = avl_insert(root.left, key, rotations)
    elif key > root.key:
        root.right = avl_insert(root.right, key, rotations)
    else:
        return root
    update_height(root)
    bf = balance_factor(root)
    if bf > 1 and root.left and key < root.left.key:
        rotations.append(f"LL imbalance at {root.key}; right rotation")
        return rotate_right(root)
    if bf < -1 and root.right and key > root.right.key:
        rotations.append(f"RR imbalance at {root.key}; left rotation")
        return rotate_left(root)
    if bf > 1 and root.left and key > root.left.key:
        rotations.append(f"LR imbalance at {root.key}; left rotation at {root.left.key}, then right rotation")
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if bf < -1 and root.right and key < root.right.key:
        rotations.append(f"RL imbalance at {root.key}; right rotation at {root.right.key}, then left rotation")
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root


def build_avl(keys: Iterable[int]) -> Tuple[Optional[TreeNode], List[str]]:
    root: Optional[TreeNode] = None
    rotations: List[str] = []
    for key in keys:
        root = avl_insert(root, key, rotations)
    return root, rotations


def inorder(root: Optional[TreeNode]) -> List[int]:
    return inorder(root.left) + [root.key] + inorder(root.right) if root else []


def preorder(root: Optional[TreeNode]) -> List[int]:
    return [root.key] + preorder(root.left) + preorder(root.right) if root else []


def postorder(root: Optional[TreeNode]) -> List[int]:
    return postorder(root.left) + postorder(root.right) + [root.key] if root else []


def search_bst(root: Optional[TreeNode], target: int) -> Tuple[bool, List[int]]:
    path = []
    cur = root
    while cur:
        path.append(cur.key)
        if target == cur.key:
            return True, path
        cur = cur.left if target < cur.key else cur.right
    return False, path


def delete_bst(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if root is None:
        return None
    if key < root.key:
        root.left = delete_bst(root.left, key)
    elif key > root.key:
        root.right = delete_bst(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = root.right
        while successor.left:
            successor = successor.left
        root.key = successor.key
        root.right = delete_bst(root.right, successor.key)
    return root


def tree_positions(root: Optional[TreeNode]) -> List[Tuple[int, float, float, Optional[int]]]:
    if root is None:
        return []
    q = SimpleQueue([(root, 0.0, 0.0, None, 1.0)])
    positions: List[Tuple[int, float, float, Optional[int]]] = []
    while q:
        node, x, y, parent, spread = q.dequeue()
        positions.append((node.key, x, y, parent))
        if node.left:
            q.enqueue((node.left, x - spread, y - 1.0, node.key, spread / 2.0))
        if node.right:
            q.enqueue((node.right, x + spread, y - 1.0, node.key, spread / 2.0))
    return positions


# =============================================================================
# SORTING, SEARCHING, AND PEAK HOUR ALGORITHMS
# =============================================================================

OrderTuple = Tuple[str, int]

def order_key(order: OrderTuple) -> Tuple[str, int]:
    return order[0], order[1]


def merge_sort(items: List[OrderTuple]) -> Tuple[List[OrderTuple], int, List[str]]:
    steps: List[str] = []

    def sort(arr: List[OrderTuple], level: int = 0) -> Tuple[List[OrderTuple], int]:
        if len(arr) <= 1:
            return arr[:], 0
        mid = len(arr) // 2
        if level < 3:
            steps.append(f"Level {level}: split {arr} into {arr[:mid]} and {arr[mid:]}")
        left, c_left = sort(arr[:mid], level + 1)
        right, c_right = sort(arr[mid:], level + 1)
        merged: List[OrderTuple] = []
        i = j = comparisons = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if order_key(left[i]) <= order_key(right[j]):
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged.extend(left[i:]); merged.extend(right[j:])
        if level < 3:
            steps.append(f"Level {level}: merge -> {merged}")
        return merged, c_left + c_right + comparisons

    sorted_items, count = sort(items)
    return sorted_items, count, steps


def quick_sort(items: List[OrderTuple]) -> Tuple[List[OrderTuple], int, List[str]]:
    arr = items[:]
    steps: List[str] = []

    def partition(low: int, high: int, level: int) -> Tuple[int, int]:
        pivot = arr[high]
        i = low - 1
        comparisons = 0
        for j in range(low, high):
            comparisons += 1
            if order_key(arr[j]) <= order_key(pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if level < 2:
            steps.append(f"Level {level}: pivot {pivot}, partition -> {arr[low:high+1]}")
        return i + 1, comparisons

    def sort(low: int, high: int, level: int = 0) -> int:
        if low >= high:
            return 0
        p, c = partition(low, high, level)
        return c + sort(low, p - 1, level + 1) + sort(p + 1, high, level + 1)

    count = sort(0, len(arr) - 1)
    return arr, count, steps


def binary_search(values: List[int], target: int) -> Tuple[int, int, List[Tuple[int, int, int, int]]]:
    low, high = 0, len(values) - 1
    comparisons = 0
    trace = []
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        trace.append((low, mid, high, values[mid]))
        if values[mid] == target:
            return mid, comparisons, trace
        if target < values[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons, trace


def linear_search(values: List[int], target: int) -> Tuple[int, int]:
    for i, value in enumerate(values):
        if value == target:
            return i, i + 1
    return -1, len(values)


def peak_hour_divide_conquer(hourly_orders: List[int], top_k: int = 1) -> List[Tuple[int, int]]:
    candidates: List[Tuple[int, int]] = []

    def collect(start: int, end: int) -> None:
        if end - start == 1:
            candidates.append((start, hourly_orders[start]))
            return
        mid = (start + end) // 2
        left_total = sum(hourly_orders[start:mid])
        right_total = sum(hourly_orders[mid:end])
        if left_total >= right_total:
            collect(start, mid)
            if top_k > 1:
                collect(mid, end)
        else:
            collect(mid, end)
            if top_k > 1:
                collect(start, mid)

    collect(0, len(hourly_orders))
    return sorted(candidates, key=lambda x: x[1], reverse=True)[:top_k]


# =============================================================================
# STREAMLIT UI HELPERS
# =============================================================================

def require_ui_libraries() -> Tuple[Any, Any, Any, Any]:
    try:
        import streamlit as st
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
    except ModuleNotFoundError as exc:
        missing = str(exc).split("No module named ")[-1].strip("'")
        raise SystemExit(
            f"Missing dependency: {missing}. Install dependencies with: pip install -r requirements.txt"
        )
    return st, go, px, pd


def matrix_to_dataframe(pd: Any, labels: List[str], matrix: List[List[float]]) -> Any:
    data = []
    for label, row in zip(labels, matrix):
        data.append([label] + [format_number(v) for v in row])
    return pd.DataFrame(data, columns=["Node"] + labels).set_index("Node")


def network_figure(go: Any, graph: WaselGraph, title: str = "WaselX Delivery Network",
                   highlight_path: Optional[List[str]] = None,
                   mst_edges: Optional[List[Edge]] = None,
                   blocked_edges: Optional[Iterable[Tuple[str, str]]] = None,
                   visited: Optional[Iterable[str]] = None,
                   current: Optional[str] = None) -> Any:
    highlight_path = highlight_path or []
    mst_edges = mst_edges or []
    blocked = {normalized_edge(u, v) for u, v in (blocked_edges or [])}
    visited_set = set(visited or [])
    path_edges = {normalized_edge(a, b) for a, b in zip(highlight_path, highlight_path[1:])}
    mst_set = {edge.key() for edge in mst_edges}
    fig = go.Figure()

    for edge in graph.edges:
        x0, y0 = POS[edge.source]
        x1, y1 = POS[edge.target]
        key = edge.key()
        if key in blocked:
            color, width, dash = "#CC0000", 3, "dot"
        elif key in path_edges:
            color, width, dash = "#FF6B00", 5, "solid"
        elif key in mst_set:
            color, width, dash = "#00A651", 4, "solid"
        else:
            color, width, dash = "#C8CDD2", 1.2, "solid"
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line={"color": color, "width": width, "dash": dash},
            text=f"{edge.source}-{edge.target} | {edge.road}<br>{edge.distance:g} km | {edge.time:g} min | AED {edge.cost:g}",
            hoverinfo="text", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[(x0 + x1) / 2], y=[(y0 + y1) / 2], mode="text",
            text=[f"{edge.distance:g}km"], textfont={"size": 9, "color": "#4D5663"},
            hoverinfo="skip", showlegend=False,
        ))

    x_vals, y_vals, labels, colors, sizes, hover = [], [], [], [], [], []
    for node in graph.nodes:
        x, y = POS[node]
        name, kind, emirate, orders, *_ = NODE_INFO[node]
        x_vals.append(x); y_vals.append(y); labels.append(node)
        hover.append(f"<b>{node}: {name}</b><br>{kind} | {emirate}<br>Daily orders: {orders}")
        if node == current:
            colors.append("#FF6B00"); sizes.append(25)
        elif node in highlight_path:
            colors.append("#FF6B00"); sizes.append(22)
        elif node in visited_set:
            colors.append("#00A651"); sizes.append(19)
        else:
            colors.append(EMIRATE_COLORS.get(emirate, "#777")); sizes.append(18 if kind == "Hub" else 14)

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals, mode="markers+text", text=labels,
        textposition="top center", hovertext=hover, hoverinfo="text",
        marker={"size": sizes, "color": colors, "line": {"width": 2, "color": "white"}},
        textfont={"size": 11, "color": "#111"}, showlegend=False,
    ))
    fig.update_layout(
        title={"text": title, "x": 0.5, "font": {"size": 17, "color": "#12395B"}},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        height=520,
        plot_bgcolor="#F8FAFD",
        paper_bgcolor="white",
        margin={"l": 5, "r": 5, "t": 45, "b": 5},
    )
    return fig


def tree_figure(go: Any, positions: List[Tuple[int, float, float, Optional[int]]], title: str,
                highlight: Optional[int] = None) -> Any:
    fig = go.Figure()
    pos = {key: (x, y) for key, x, y, _ in positions}
    for key, x, y, parent in positions:
        if parent is not None:
            px, py = pos[parent]
            fig.add_trace(go.Scatter(x=[px, x], y=[py, y], mode="lines",
                                     line={"color": "#A9B0B8", "width": 2}, showlegend=False))
    for key, x, y, _ in positions:
        color = "#FF6B00" if key == highlight else "#2E75B6"
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[str(key)],
                                 textposition="middle center",
                                 marker={"size": 38, "color": color, "line": {"width": 2, "color": "white"}},
                                 textfont={"color": "white", "size": 11}, showlegend=False))
    fig.update_layout(title=title, height=410, plot_bgcolor="#F8FAFD", paper_bgcolor="white",
                      xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
                      yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
                      margin={"l": 5, "r": 5, "t": 45, "b": 5})
    return fig


def style_app(st: Any) -> None:
    st.set_page_config(page_title="WaselX Express — DSA Prototype", page_icon="🚚", layout="wide")
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {background:#0F1C2E;}
    [data-testid="stSidebar"] * {color:#E8F1FF !important;}
    .hero {background:linear-gradient(135deg,#12395B,#2E75B6); padding:24px; border-radius:18px; color:white; text-align:center; margin-bottom:18px;}
    .metric-card {background:white; border:1px solid #E1E6EF; border-radius:14px; padding:16px; box-shadow:0 3px 12px rgba(0,0,0,.04);}
    .note {background:#F2F7FF; border-left:5px solid #2E75B6; padding:12px 14px; border-radius:8px;}
    .warn {background:#FFF8E1; border-left:5px solid #FFB000; padding:12px 14px; border-radius:8px;}
    .success {background:#ECF8EF; border-left:5px solid #00A651; padding:12px 14px; border-radius:8px;}
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# STREAMLIT PAGES
# =============================================================================

def page_overview(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.markdown("""
    <div class="hero">
      <h1>🚚 WaselX Express</h1>
      <p>Professional Data Structures & Algorithms Prototype for UAE Last-Mile Delivery Optimization</p>
    </div>
    """, unsafe_allow_html=True)
    cols = st.columns(4)
    metrics = [("15", "Network Nodes"), ("24", "Road Edges"), ("3,500", "Daily Orders"), ("5", "Task Areas")]
    for col, (value, label) in zip(cols, metrics):
        col.markdown(f"<div class='metric-card'><h2>{value}</h2><p>{label}</p></div>", unsafe_allow_html=True)
    st.plotly_chart(network_figure(go, graph, "WaselX UAE Operating Network", blocked_edges=blocked), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Business Problems")
        st.table(pd.DataFrame([
            ["Inefficient routes", "23% extra rider distance", "Dijkstra + path simulator"],
            ["Slow dispatch", "8-minute manual sorting delay", "From-scratch min-heap priority queue"],
            ["Poor lookup", "45-second support lookup", "AVL tree order index"],
        ], columns=["Challenge", "Impact", "DSA Solution"]))
    with c2:
        st.subheader("Readiness Notes")
        comps = graph.connected_components()
        if len(comps) > 1:
            st.markdown(f"<div class='warn'><b>Important:</b> The supplied network is disconnected into {len(comps)} components. Routing from Dubai/Sharjah/Ajman to Abu Dhabi is impossible unless a new inter-emirate edge is added.</div>", unsafe_allow_html=True)
        st.markdown("<div class='success'>The cleaned prototype removes unused dependencies, fixes path simulator errors, uses custom heap/queue structures, and handles road closures safely.</div>", unsafe_allow_html=True)


def page_network(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.title("Network Explorer")
    tab1, tab2, tab3, tab4 = st.tabs(["Map", "Adjacency List", "Adjacency Matrix", "Connectivity"])
    with tab1:
        node = st.selectbox("Highlight node", ["None"] + graph.nodes)
        path = [node] if node != "None" else []
        st.plotly_chart(network_figure(go, graph, "Network Map", highlight_path=path, blocked_edges=blocked), use_container_width=True)
    with tab2:
        st.dataframe(pd.DataFrame(graph.adjacency_list_rows()), use_container_width=True, hide_index=True)
    with tab3:
        criterion = st.selectbox("Weight", ["distance", "time", "cost"], key="matrix_weight")
        st.dataframe(matrix_to_dataframe(pd, graph.nodes, graph.adjacency_matrix(criterion)), use_container_width=True)
        st.caption("INF means no direct road segment exists between the two locations.")
    with tab4:
        comps = graph.connected_components()
        st.write(f"Connected components: {len(comps)}")
        for i, comp in enumerate(comps, start=1):
            st.markdown(f"**Component {i}:** {', '.join(comp)}")
        if len(comps) > 1:
            st.warning("This matters for Q6/Q7/Q4: H5/H6/D6/D7 are isolated from the Dubai-Sharjah-Ajman component in the given edge table.")


def page_pathfinder(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.title("Dijkstra Path Simulator")
    c1, c2, c3 = st.columns(3)
    with c1:
        source = st.selectbox("Source", graph.nodes, index=0)
    with c2:
        destination = st.selectbox("Destination", graph.nodes, index=graph.nodes.index("D1"))
    with c3:
        criterion = st.selectbox("Optimize for", ["distance", "time", "cost"])

    result = graph.dijkstra(source, destination, criterion)
    metrics = result["metrics"]
    st.plotly_chart(network_figure(go, graph, f"Optimal path by {criterion}: {path_to_string(result['path'])}", result["path"], blocked_edges=blocked), use_container_width=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Path", path_to_string(result["path"]))
    m2.metric("Distance", f"{format_number(metrics['distance'])} km")
    m3.metric("Time", f"{format_number(metrics['time'])} min")
    m4.metric("Cost", f"AED {format_number(metrics['cost'])}")

    tabs = st.tabs(["Step Trace", "All Criteria", "Road Closure Comparison"])
    with tabs[0]:
        trace_rows = []
        for row in result["trace"]:
            trace_rows.append({
                "Step": row["step"],
                "Action": row["action"],
                "Visited": ", ".join(row.get("visited", [])),
            })
        st.dataframe(pd.DataFrame(trace_rows), use_container_width=True, hide_index=True)
    with tabs[1]:
        rows = []
        for crit in ["distance", "time", "cost"]:
            r = graph.dijkstra(source, destination, crit)
            met = r["metrics"]
            rows.append({"Criterion": crit, "Path": path_to_string(r["path"]), "Distance": met["distance"], "Time": met["time"], "Cost": met["cost"]})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    with tabs[2]:
        edge_labels = {f"{u}-{v} ({road})": (u, v) for u, v, road, *_ in EDGES}
        selected = st.selectbox("Temporarily block one road", ["None"] + list(edge_labels.keys()))
        if selected == "None":
            st.info("Select a road to compare original vs rerouted results.")
        else:
            closure = [edge_labels[selected]]
            closure_graph = WaselGraph(blocked_edges=list(blocked) + closure)
            original = graph.dijkstra(source, destination, criterion)
            rerouted = closure_graph.dijkstra(source, destination, criterion)
            left, right = st.columns(2)
            with left:
                st.plotly_chart(network_figure(go, graph, "Original", original["path"], blocked_edges=blocked), use_container_width=True)
                st.write(path_to_string(original["path"]))
            with right:
                st.plotly_chart(network_figure(go, closure_graph, "Rerouted", rerouted["path"], blocked_edges=list(blocked)+closure), use_container_width=True)
                st.write(path_to_string(rerouted["path"]))
            o, r = original["metrics"], rerouted["metrics"]
            comparison = pd.DataFrame([
                ["Original", path_to_string(original["path"]), o["distance"], o["time"], o["cost"]],
                ["Rerouted", path_to_string(rerouted["path"]), r["distance"], r["time"], r["cost"]],
                ["Delta", "", r["distance"]-o["distance"] if not isinf(r["distance"]) else INF, r["time"]-o["time"] if not isinf(r["time"]) else INF, r["cost"]-o["cost"] if not isinf(r["cost"]) else INF],
            ], columns=["Case", "Path", "Distance", "Time", "Cost"])
            st.dataframe(comparison, use_container_width=True, hide_index=True)


def page_floyd(st: Any, go: Any, pd: Any, graph: WaselGraph) -> None:
    st.title("Floyd-Warshall All-Pairs Shortest Paths")
    criterion = st.selectbox("Weight", ["time", "distance", "cost"], key="fw_weight")
    scope = st.radio("Scope", ["Hubs only (H1-H7)", "All nodes"], horizontal=True)
    nodes = [n for n in graph.nodes if n.startswith("H")] if scope.startswith("Hubs") else graph.nodes
    result = graph.floyd_warshall(nodes, criterion)
    tab1, tab2, tab3 = st.tabs(["Initial Matrix", "Final Matrix", "New Edge Scenario"])
    with tab1:
        st.dataframe(matrix_to_dataframe(pd, nodes, result["initial"]), use_container_width=True)
    with tab2:
        st.dataframe(matrix_to_dataframe(pd, nodes, result["final"]), use_container_width=True)
        final = result["final"]
        finite_pairs = [(nodes[i], nodes[j], final[i][j]) for i in range(len(nodes)) for j in range(i+1, len(nodes)) if not isinf(final[i][j])]
        if finite_pairs:
            farthest = max(finite_pairs, key=lambda x: x[2])
            st.metric("Farthest reachable pair", f"{farthest[0]}-{farthest[1]}", f"{farthest[2]:g} {WEIGHT_LABEL[criterion]}")
        averages = []
        for i, n in enumerate(nodes):
            vals = [final[i][j] for j in range(len(nodes)) if i != j and not isinf(final[i][j])]
            if vals:
                averages.append((n, sum(vals) / len(vals)))
        if averages:
            best = min(averages, key=lambda x: x[1])
            st.metric("Best average connectivity", best[0], f"{best[1]:.1f} {WEIGHT_LABEL[criterion]}")
    with tab3:
        st.markdown("Default scenario: add a direct H3-H5 express corridor to bridge the disconnected Dubai/Sharjah/Ajman and Abu Dhabi components.")
        c1, c2, c3 = st.columns(3)
        with c1:
            u = st.selectbox("New edge from", [n for n in graph.nodes if n.startswith("H")], index=2)
        with c2:
            v = st.selectbox("New edge to", [n for n in graph.nodes if n.startswith("H")], index=4)
        with c3:
            new_weight = st.number_input(f"Assumed {criterion}", min_value=1.0, value=65.0 if criterion == "time" else 60.0, step=1.0)
        if u != v:
            if criterion == "time":
                extra = Edge(u, v, "Proposed express corridor", 60, new_weight, 18)
            elif criterion == "distance":
                extra = Edge(u, v, "Proposed express corridor", new_weight, 65, 18)
            else:
                extra = Edge(u, v, "Proposed express corridor", 60, 65, new_weight)
            g2 = WaselGraph(extra_edges=[extra])
            updated = g2.floyd_warshall(nodes, criterion)
            st.dataframe(matrix_to_dataframe(pd, nodes, updated["final"]), use_container_width=True)


def page_traversal(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.title("BFS and DFS Traversal")
    start = st.selectbox("Start node", graph.nodes, index=graph.nodes.index("H3"))
    bfs_result = graph.bfs(start)
    dfs_result = graph.dfs(start)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("BFS")
        st.plotly_chart(network_figure(go, graph, "BFS Reachability", visited=bfs_result["order"], current=start, blocked_edges=blocked), use_container_width=True)
        st.write(" -> ".join(bfs_result["order"]))
        st.dataframe(pd.DataFrame([{"Node": k, "Parent": v or "-"} for k, v in bfs_result["parent"].items()]), hide_index=True)
    with c2:
        st.subheader("DFS")
        st.write(" -> ".join(dfs_result["order"]))
        st.dataframe(pd.DataFrame([{"Node": k, "Parent": v or "-"} for k, v in dfs_result["parent"].items()]), hide_index=True)
    if not bfs_result["reachable_all"]:
        st.warning(f"Starting from {start}, only {len(bfs_result['order'])} of {len(graph.nodes)} nodes are reachable. This is a key finding for Q7.")


def page_mst(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.title("Minimum Spanning Tree / Forest")
    result = graph.kruskal_mst()
    st.plotly_chart(network_figure(go, graph, "Kruskal Minimum Spanning Forest", mst_edges=result["edges"], blocked_edges=blocked), use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Selected edges", len(result["edges"]))
    c2.metric("Total cost", f"AED {result['total']:.1f}K")
    c3.metric("Components", len(result["components"]))
    if not result["is_spanning_tree"]:
        st.warning("Because the provided graph is disconnected, the mathematically correct output is a Minimum Spanning Forest. A true MST over all 15 nodes would require at least one new bridge edge between components.")
    tab1, tab2 = st.tabs(["Kruskal Trace", "Prim from H2"])
    with tab1:
        st.dataframe(pd.DataFrame(result["trace"]), use_container_width=True, hide_index=True)
    with tab2:
        start = st.selectbox("Start", graph.nodes, index=graph.nodes.index("H2"), key="prim_start")
        prim = graph.prim_mst(start)
        st.dataframe(pd.DataFrame(prim["trace"]), use_container_width=True, hide_index=True)
        if not prim["is_complete"]:
            st.info(f"Prim starting at {start} covers {len(prim['visited'])} nodes in its connected component. Run Kruskal for the full spanning forest across disconnected components.")


def page_trees(st: Any, go: Any, pd: Any) -> None:
    st.title("BST and AVL Tree Indexing")
    order_ids = [1045, 1023, 1078, 1012, 1034, 1056, 1089, 1005, 1020, 1067, 1050, 1098]
    root = build_bst(order_ids)
    avl_root, rotations = build_avl(order_ids)
    tab1, tab2, tab3 = st.tabs(["BST", "AVL", "Search / Delete"])
    with tab1:
        st.plotly_chart(tree_figure(go, tree_positions(root), "BST from Morning Shift Orders"), use_container_width=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Height", tree_height(root))
        c2.metric("In-order", str(inorder(root)))
        c3.metric("Worst-case", "O(h)")
        st.write("Pre-order:", preorder(root))
        st.write("Post-order:", postorder(root))
    with tab2:
        st.plotly_chart(tree_figure(go, tree_positions(avl_root), "AVL Tree from Same Orders"), use_container_width=True)
        st.metric("AVL height", tree_height(avl_root))
        if rotations:
            st.write("Rotations triggered:")
            for r in rotations:
                st.write("-", r)
        else:
            st.info("This exact sequence remains balanced enough that no AVL rotations are triggered. The assignment still asks for rotation diagrams, so use the examples below in the report.")
        st.table(pd.DataFrame([
            ["LL", "Insert 1003 after 1005", "Right rotation"],
            ["RL", "Insert 1070 under 1067/1078", "Right rotation then left rotation"],
        ], columns=["Case", "Example", "Fix"]))
    with tab3:
        target = st.number_input("Search Order ID", min_value=1000, max_value=9999, value=1067)
        found, path = search_bst(root, int(target))
        st.plotly_chart(tree_figure(go, tree_positions(root), f"Search path for {target}", highlight=path[-1] if path else None), use_container_width=True)
        st.write(f"Found: {found}; Path: {' -> '.join(map(str, path))}; Comparisons: {len(path)}")
        delete_id = st.selectbox("Delete example", order_ids, index=order_ids.index(1078))
        if st.button("Show deletion"):
            new_root = delete_bst(build_bst(order_ids), delete_id)
            st.plotly_chart(tree_figure(go, tree_positions(new_root), f"BST after deleting {delete_id}"), use_container_width=True)
            st.write("After deletion in-order:", inorder(new_root))


def page_pipeline(st: Any, pd: Any) -> None:
    st.title("Linked Lists, Priority Queue, and Stack")
    tab1, tab2, tab3, tab4 = st.tabs(["Doubly Linked List", "Circular Linked List", "Priority Queue", "Stack"])
    with tab1:
        route = DoublyLinkedList()
        for stop in [("Dubai Marina Hub", "ORD001", "10:15"), ("JLT", "ORD002", "10:30"), ("Downtown Dubai", "ORD003", "10:50"), ("Business Bay", "ORD004", "11:05"), ("Deira", "ORD005", "11:25"), ("Silicon Oasis", "ORD006", "11:50")]:
            route.append(*stop)
        before = route.display_forward()
        route.insert_after("ORD003", "Al Quoz (Urgent)", "ORD_URGENT", "10:55")
        after_insert = route.display_forward()
        route.delete_by_order_id("ORD005")
        after_delete = route.display_forward()
        st.write("Before:", before)
        st.write("After urgent insertion:", after_insert)
        st.write("After cancellation:", after_delete)
    with tab2:
        riders = CircularLinkedList()
        for i in range(1, 9):
            riders.add_rider(f"Rider {i}")
        assignments = []
        for order in range(1, 12):
            assignments.append((order, riders.assign_next_order()))
        riders.remove_rider("Rider 4")
        for order in range(12, 21):
            assignments.append((order, riders.assign_next_order()))
        st.dataframe(pd.DataFrame(assignments, columns=["Order", "Assigned Rider"]), hide_index=True)
        st.write("Current roster:", riders.display_roster())
    with tab3:
        orders = [("Order A", 3), ("Order B", 1), ("Order C", 4), ("Order D", 2), ("Order E", 1), ("Order F", 5), ("Order G", 2), ("Order H", 3), ("Order I", 1), ("Order J", 4)]
        pq = MinHeap()
        for name, priority in orders:
            pq.push(priority, name)
        dequeued = []
        while pq:
            priority, _, name = pq.pop()[:3]
            dequeued.append((name, priority))
        st.dataframe(pd.DataFrame(dequeued, columns=["Order", "Priority"]), hide_index=True)
        st.caption("FIFO tie-breaking is preserved by an internal arrival counter.")
    with tab4:
        lifecycle = Stack()
        for status in ["Received", "Confirmed", "Preparing", "Dispatched", "In Transit", "Delivered"]:
            lifecycle.push(status)
        st.write("Delivered order stack (top first):", lifecycle.display_top_first())
        error_demo = Stack()
        for status in ["Received", "Confirmed", "Preparing", "Dispatched"]:
            error_demo.push(status)
        before = error_demo.display_top_first()
        error_demo.pop()
        after = error_demo.display_top_first()
        st.write("Undo demo before:", before)
        st.write("Undo demo after:", after)


def page_sorting(st: Any, go: Any, px: Any, pd: Any) -> None:
    st.title("Sorting, Searching, and Divide-and-Conquer")
    tab1, tab2, tab3 = st.tabs(["Sort manifest", "Search order ID", "Peak hour"])
    sample = [("JLT",3), ("Deira",1), ("Marina",4), ("JLT",1), ("Deira",2), ("Marina",2), ("Silicon",5), ("Deira",3), ("JLT",2), ("Marina",1), ("Silicon",1), ("Deira",4), ("Silicon",3), ("JLT",5), ("Marina",3)]
    with tab1:
        ms_sorted, ms_count, ms_steps = merge_sort(sample)
        qs_sorted, qs_count, qs_steps = quick_sort(sample)
        st.dataframe(pd.DataFrame(ms_sorted, columns=["Zone", "Priority"]), hide_index=True)
        st.metric("Merge comparisons", ms_count)
        st.metric("Quick comparisons", qs_count)
        with st.expander("Merge first 3 recursion levels"):
            st.write("\n".join(ms_steps))
        with st.expander("Quick first 2 partition levels"):
            st.write("\n".join(qs_steps))
    with tab2:
        ids = list(range(10001, 11001))
        target = st.number_input("Order ID", min_value=10001, max_value=11000, value=10667)
        b_idx, b_comp, b_trace = binary_search(ids, int(target))
        l_idx, l_comp = linear_search(ids, int(target))
        st.table(pd.DataFrame([["Binary", b_idx, b_comp], ["Linear", l_idx, l_comp]], columns=["Method", "Index", "Comparisons"]))
        st.dataframe(pd.DataFrame(b_trace, columns=["Low", "Mid", "High", "Mid Value"]), hide_index=True)
    with tab3:
        default_orders = [80, 55, 40, 30, 25, 20, 35, 60, 120, 210, 280, 330, 300, 260, 240, 290, 410, 520, 610, 480, 360, 250, 180, 120]
        top = peak_hour_divide_conquer(default_orders, 3)
        st.line_chart(pd.DataFrame({"Hour": list(range(24)), "Orders": default_orders}).set_index("Hour"))
        st.write("Top peak hours:", top)


def main() -> None:
    st, go, px, pd = require_ui_libraries()
    style_app(st)
    with st.sidebar:
        st.markdown("## 🚚 WaselX DSA")
        st.caption("Professional cleaned prototype")
        section = st.radio("Navigate", [
            "Overview", "Network", "Pathfinder", "Floyd-Warshall", "BFS/DFS", "MST", "BST/AVL", "Pipeline DS", "Sorting/Search/Peak"
        ])
        edge_labels = {f"{u}-{v} ({road})": (u, v) for u, v, road, *_ in EDGES}
        selected = st.multiselect("Global road closures", list(edge_labels.keys()))
        blocked = [edge_labels[label] for label in selected]
        st.markdown("---")
        st.caption("Team: " + " · ".join(TEAM_MEMBERS))
    graph = WaselGraph(blocked_edges=blocked)
    if section == "Overview":
        page_overview(st, go, pd, graph, blocked)
    elif section == "Network":
        page_network(st, go, pd, graph, blocked)
    elif section == "Pathfinder":
        page_pathfinder(st, go, pd, graph, blocked)
    elif section == "Floyd-Warshall":
        page_floyd(st, go, pd, graph)
    elif section == "BFS/DFS":
        page_traversal(st, go, pd, graph, blocked)
    elif section == "MST":
        page_mst(st, go, pd, graph, blocked)
    elif section == "BST/AVL":
        page_trees(st, go, pd)
    elif section == "Pipeline DS":
        page_pipeline(st, pd)
    else:
        page_sorting(st, go, px, pd)


# =============================================================================
# TESTS / VALIDATION
# =============================================================================

def run_self_test() -> None:
    graph = WaselGraph()
    h1_d1 = graph.dijkstra("H1", "D1", "distance")
    assert h1_d1["path"] == ["H1", "D1"], h1_d1
    assert h1_d1["best"] == 8, h1_d1
    h1_d4 = graph.dijkstra("H1", "D4", "distance")
    assert h1_d4["metrics"]["distance"] == 21, h1_d4
    h5_d5 = graph.dijkstra("H5", "D5", "distance")
    assert h5_d5["path"] == [], h5_d5
    bfs_h3 = graph.bfs("H3")
    assert len(bfs_h3["order"]) == 11, bfs_h3
    mst = graph.kruskal_mst()
    assert round(mst["total"], 1) == 62.0, mst
    assert len(mst["edges"]) == 13, mst
    pq = MinHeap()
    for name, priority in [("A", 3), ("B", 1), ("C", 1)]:
        pq.push(priority, name)
    assert [pq.pop()[2], pq.pop()[2], pq.pop()[2]] == ["B", "C", "A"]
    print("Self-test passed: core graph, heap, BFS, MST, and disconnection checks are valid.")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        run_self_test()
    else:
        main()
