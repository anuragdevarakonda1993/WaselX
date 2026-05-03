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

# Manual presentation layout used by Plotly to produce clearer, presenter-grade
# network visuals than raw latitude/longitude coordinates.
DISPLAY_POS: Dict[str, Tuple[float, float]] = {
    "H5": (-5.8, -2.5), "D7": (-5.1, -2.1), "H6": (-4.2, -2.9), "D6": (-3.2, -2.4),
    "H4": (0.0, 0.2), "H1": (0.8, -0.35), "D3": (1.55, 0.42), "D2": (2.2, 0.52),
    "D1": (2.95, 1.08), "H2": (3.55, 1.14), "H3": (5.2, 2.0), "D4": (6.35, 0.72),
    "H7": (7.4, 2.72), "D5": (8.45, 3.62), "D8": (9.45, 2.62),
}

TEXT_POSITIONS: Dict[str, str] = {
    "H5": "top center", "D7": "top center", "H6": "bottom center", "D6": "top center",
    "H4": "top center", "H1": "bottom center", "D3": "top center", "D2": "top center",
    "D1": "top center", "H2": "bottom center", "H3": "top center", "D4": "bottom center",
    "H7": "top center", "D5": "top center", "D8": "middle right",
}
EMIRATE_COLORS = {
    "Dubai": "#2563EB",
    "Abu Dhabi": "#C2410C",
    "Sharjah": "#15803D",
    "Ajman": "#7C3AED",
}

THEME = {
    "ink": "#0F172A",
    "muted": "#64748B",
    "panel": "#FFFFFF",
    "line": "#D9E2EC",
    "surface": "#F8FAFC",
    "primary": "#0F766E",
    "primary_dark": "#134E4A",
    "accent": "#F97316",
    "accent_alt": "#7C3AED",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger": "#DC2626",
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



def metric_card_html(value: str, label: str, detail: str = "", icon: str = "", tone: str = "primary") -> str:
    """Small reusable HTML card used to keep Streamlit pages visually consistent."""
    return f"""
    <div class="metric-card metric-{tone}">
      <div class="metric-icon">{icon}</div>
      <div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {f'<div class="metric-detail">{detail}</div>' if detail else ''}
      </div>
    </div>
    """


def section_header_html(title: str, subtitle: str = "", kicker: str = "") -> str:
    return f"""
    <div class="section-header">
      {f'<div class="section-kicker">{kicker}</div>' if kicker else ''}
      <h2>{title}</h2>
      {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """


def route_card_html(title: str, path: List[str], metrics: Dict[str, float], tone: str = "primary") -> str:
    path_text = path_to_string(path)
    distance = format_number(metrics.get("distance", INF))
    minutes = format_number(metrics.get("time", INF))
    cost = format_number(metrics.get("cost", INF))
    return f"""
    <div class="route-card route-{tone}">
      <div class="route-card-title">{title}</div>
      <div class="route-path">{path_text}</div>
      <div class="route-metrics">
        <span>{distance} km</span><span>{minutes} min</span><span>AED {cost}</span>
      </div>
    </div>
    """


def format_delta(after: float, before: float, suffix: str = "") -> str:
    if isinf(after) or isinf(before):
        return "No feasible route"
    delta = after - before
    sign = "+" if delta > 0 else ""
    return f"{sign}{format_number(delta)}{suffix}"


def route_to_dataframe(pd: Any, route_rows: List[Tuple[str, str, str]]) -> Any:
    return pd.DataFrame(route_rows, columns=["Stop", "Order ID", "ETA"])

def network_figure(go: Any, graph: WaselGraph, title: str,
                   highlight_path: Optional[List[str]] = None,
                   blocked_edges: Optional[List[Tuple[str, str]]] = None,
                   secondary_path: Optional[List[str]] = None,
                   mst_edges: Optional[List[Edge]] = None,
                   visited: Optional[List[str]] = None,
                   current: Optional[str] = None,
                   primary_label: str = "Primary route",
                   secondary_label: str = "Secondary route",
                   show_edge_labels: bool = False,
                   temporary_edge: Optional[Tuple[str, str]] = None) -> Any:
    """Presenter-grade Plotly network visualization for the WaselX graph.

    Uses a manual display layout for readability, stronger visual hierarchy for
    highlighted routes, and selective edge labels to avoid clutter.
    """
    highlight_path = highlight_path or []
    secondary_path = secondary_path or []
    mst_edges = mst_edges or []
    blocked = {normalized_edge(u, v) for u, v in (blocked_edges or [])}
    visited_set = set(visited or [])
    mst_set = {edge.key() for edge in mst_edges}
    highlight_edges = {normalized_edge(u, v) for u, v in zip(highlight_path, highlight_path[1:])}
    secondary_edges = {normalized_edge(u, v) for u, v in zip(secondary_path, secondary_path[1:])}
    temp_edge = normalized_edge(*temporary_edge) if temporary_edge else None

    fig = go.Figure()

    # Legend anchors.
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name="Hubs",
                             marker={"symbol": "diamond", "size": 17, "color": "#94A3B8",
                                     "line": {"width": 1.5, "color": "white"}}))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name="Delivery zones",
                             marker={"symbol": "circle", "size": 14, "color": "#94A3B8",
                                     "line": {"width": 1.5, "color": "white"}}))

    # Draw base road network with white halo under each edge.
    for edge in graph.edges:
        x0, y0 = DISPLAY_POS[edge.source]
        x1, y1 = DISPLAY_POS[edge.target]
        key = edge.key()
        if key == temp_edge:
            color, width, dash, opacity = THEME["warning"], 4.6, "dash", 0.98
        elif key in blocked:
            color, width, dash, opacity = THEME["danger"], 4.0, "dot", 0.95
        elif key in mst_set:
            color, width, dash, opacity = THEME["success"], 4.2, "solid", 0.96
        elif key in highlight_edges:
            color, width, dash, opacity = THEME["accent"], 5.2, "solid", 0.98
        elif key in secondary_edges:
            color, width, dash, opacity = THEME["accent_alt"], 4.7, "dash", 0.96
        else:
            color, width, dash, opacity = "#B8C5D6", 2.0, "solid", 0.72

        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line={"color": "rgba(255,255,255,0.96)", "width": width + 3.0},
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line={"color": color, "width": width, "dash": dash}, opacity=opacity,
            text=f"<b>{edge.source} ↔ {edge.target}</b><br>{edge.road}<br>{edge.distance:g} km · {edge.time:g} min · AED {edge.cost:g}",
            hoverinfo="text", showlegend=False,
        ))

        label_needed = show_edge_labels or key in highlight_edges or key in secondary_edges or key in mst_set or key in blocked or key == temp_edge
        if label_needed:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            fig.add_annotation(
                x=mx, y=my, text=f"{edge.distance:g} km", showarrow=False,
                font={"size": 10, "color": "#334155", "family": "Inter, Arial"},
                bgcolor="rgba(255,255,255,0.92)", bordercolor="#D9E2EC", borderwidth=1,
                borderpad=2,
            )

    def add_route(path: List[str], color: str, label: str, dash: str = "solid", width: float = 6.0) -> None:
        if len(path) < 2:
            return
        x, y = [], []
        for u, v in zip(path, path[1:]):
            if graph.edge_between(u, v) is None:
                continue
            x.extend([DISPLAY_POS[u][0], DISPLAY_POS[v][0], None])
            y.extend([DISPLAY_POS[u][1], DISPLAY_POS[v][1], None])
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="lines", name=label,
            line={"color": "rgba(255,255,255,0.96)", "width": width + 3},
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="lines", name=label,
            line={"color": color, "width": width, "dash": dash},
            opacity=0.98, hoverinfo="skip", showlegend=True,
        ))

    add_route(secondary_path, THEME["accent_alt"], secondary_label, "dash", 5.2)
    add_route(highlight_path, THEME["accent"], primary_label, "solid", 6.2)

    # Node traces, one per node for per-node label positioning.
    for node in graph.nodes:
        x, y = DISPLAY_POS[node]
        name, kind, emirate, orders, *_ = NODE_INFO[node]
        is_hub = kind == "Hub"
        base_color = EMIRATE_COLORS.get(emirate, "#64748B")
        node_color = base_color
        if node in secondary_path:
            node_color = THEME["accent_alt"]
        if node in highlight_path:
            node_color = THEME["accent"]
        if node in visited_set and node not in highlight_path and node not in secondary_path:
            node_color = THEME["success"]
        if node == current:
            node_color = THEME["warning"]
        size = 26 if is_hub else 20
        if node in highlight_path or node in secondary_path:
            size += 6
        if node == current:
            size += 6
        hover = f"<b>{node}: {name}</b><br>{kind} · {emirate}<br>Daily orders: {orders}"

        # white halo then main marker
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers", showlegend=False, hoverinfo="skip",
            marker={"symbol": "diamond" if is_hub else "circle", "size": size + 8, "color": "rgba(255,255,255,0.92)"},
        ))
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers+text", showlegend=False,
            text=[node], textposition=TEXT_POSITIONS.get(node, "top center"),
            hovertext=hover, hoverinfo="text",
            marker={"symbol": "diamond" if is_hub else "circle", "size": size, "color": node_color,
                    "line": {"width": 2.0, "color": "white"}},
            textfont={"size": 12, "color": THEME["ink"], "family": "Inter, Arial"},
        ))

    if blocked:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="Blocked road",
                                 line={"color": THEME["danger"], "width": 4, "dash": "dot"}))
    if mst_edges:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="Forest edge",
                                 line={"color": THEME["success"], "width": 4}))
    if temp_edge:
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="Current step",
                                 line={"color": THEME["warning"], "width": 4, "dash": "dash"}))

    xs = [x for x, _ in DISPLAY_POS.values()]
    ys = [y for _, y in DISPLAY_POS.values()]
    x_pad, y_pad = 0.8, 0.75
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left", "font": {"size": 20, "color": THEME["ink"], "family": "Inter, Arial"}},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "fixedrange": True, "range": [min(xs)-x_pad, max(xs)+x_pad]},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "fixedrange": True, "range": [min(ys)-y_pad, max(ys)+y_pad], "scaleanchor": "x", "scaleratio": 1},
        height=620,
        plot_bgcolor="#F8FAFC",
        paper_bgcolor="rgba(0,0,0,0)",
        margin={"l": 10, "r": 10, "t": 62, "b": 10},
        hovermode="closest",
        font={"family": "Inter, Arial", "color": THEME["ink"]},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0,
                "bgcolor": "rgba(255,255,255,0.82)", "bordercolor": "#E2E8F0", "borderwidth": 1},
    )
    fig.add_annotation(x=-4.6, y=-1.55, text="<b>Abu Dhabi cluster</b>", showarrow=False,
                       font={"size": 12, "color": "#7C2D12"}, bgcolor="rgba(255,255,255,0.80)",
                       bordercolor="#FED7AA", borderwidth=1)
    fig.add_annotation(x=4.8, y=4.0, text="<b>Dubai · Sharjah · Ajman cluster</b>", showarrow=False,
                       font={"size": 12, "color": "#1E3A8A"}, bgcolor="rgba(255,255,255,0.80)",
                       bordercolor="#BFDBFE", borderwidth=1)
    return fig

def tree_figure(go: Any, positions: List[Tuple[int, float, float, Optional[int]]], title: str,
                highlight: Optional[int] = None) -> Any:
    fig = go.Figure()
    pos = {key: (x, y) for key, x, y, _ in positions}
    for key, x, y, parent in positions:
        if parent is not None:
            px, py = pos[parent]
            edge_color = THEME["accent"] if key == highlight or parent == highlight else "#CBD5E1"
            fig.add_trace(go.Scatter(x=[px, x], y=[py, y], mode="lines",
                                     line={"color": edge_color, "width": 2.3}, showlegend=False, hoverinfo="skip"))
    for key, x, y, _ in positions:
        is_highlight = key == highlight
        color = THEME["accent"] if is_highlight else "#2563EB"
        size = 44 if is_highlight else 38
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[str(key)],
                                 textposition="middle center",
                                 marker={"size": size, "color": color, "line": {"width": 2.5, "color": "white"}},
                                 textfont={"color": "white", "size": 11, "family": "Inter, Arial"},
                                 hovertext=f"Order ID {key}", hoverinfo="text", showlegend=False))
    fig.update_layout(title={"text": title, "x": 0.02, "font": {"size": 18, "color": THEME["ink"]}}, height=430,
                      plot_bgcolor="#F8FAFC", paper_bgcolor="rgba(0,0,0,0)",
                      xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "fixedrange": True},
                      yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "fixedrange": True},
                      font={"family": "Inter, Arial", "color": THEME["ink"]},
                      margin={"l": 8, "r": 8, "t": 52, "b": 8})
    return fig


def style_app(st: Any) -> None:
    st.set_page_config(page_title="WaselX Express — Professional DSA Prototype", page_icon="🚚", layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root {
      --ink:#0F172A; --muted:#64748B; --line:#D9E2EC; --surface:#F8FAFC; --panel:#FFFFFF;
      --primary:#0F766E; --primary-dark:#134E4A; --accent:#F97316; --violet:#7C3AED;
      --success:#16A34A; --warning:#D97706; --danger:#DC2626;
    }
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    .stApp { background: radial-gradient(circle at top left, rgba(15,118,110,.08), transparent 35%), linear-gradient(180deg,#F8FAFC 0%,#EEF2F7 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg,#0B1220 0%,#102A43 56%,#134E4A 100%); border-right:1px solid rgba(255,255,255,.08); }
    [data-testid="stSidebar"] * { color:#E8F1FF !important; }
    [data-testid="stSidebar"] .stRadio label { padding:.24rem 0; }
    [data-testid="stSidebar"] .stCaption { color:#B9C6D6 !important; }
    .block-container { padding-top: 1.2rem; max-width: 1360px; }
    h1, h2, h3 { letter-spacing: -.02em; color: var(--ink); }
    div[data-testid="stTabs"] button { font-weight: 700; letter-spacing: -.01em; }
    div[data-testid="stDataFrame"], div[data-testid="stTable"] { border-radius: 14px; overflow: hidden; box-shadow: 0 10px 28px rgba(15,23,42,.05); }
    .hero {
      position: relative; overflow: hidden; color:white; padding: 34px 38px; border-radius: 26px; margin-bottom: 22px;
      background: radial-gradient(circle at 15% 10%, rgba(255,255,255,.28), transparent 24%), linear-gradient(135deg,#0F766E 0%,#0B2F52 55%,#1E1B4B 100%);
      box-shadow: 0 22px 55px rgba(15,23,42,.22); border:1px solid rgba(255,255,255,.16);
    }
    .hero h1 { color:white; font-size: 2.55rem; margin:0; font-weight:800; }
    .hero p { margin:.5rem 0 0; color:#D7F7EF; font-size:1.05rem; max-width: 900px; }
    .section-header { margin: 1.3rem 0 .85rem; padding: 0 0 .25rem; }
    .section-kicker { color: var(--primary); font-size:.78rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; margin-bottom:.22rem; }
    .section-header h2 { margin:0; font-size:1.45rem; font-weight:800; }
    .section-header p { margin:.35rem 0 0; color:var(--muted); }
    .metric-card {
      min-height: 112px; display:flex; align-items:center; gap:14px; background: rgba(255,255,255,.9); border:1px solid rgba(217,226,236,.95);
      border-radius: 20px; padding:18px; box-shadow: 0 14px 35px rgba(15,23,42,.075); backdrop-filter: blur(8px); transition: transform .18s ease, box-shadow .18s ease;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 18px 42px rgba(15,23,42,.11); }
    .metric-icon { width:46px; height:46px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:1.35rem; background:linear-gradient(135deg,#CCFBF1,#DBEAFE); }
    .metric-value { font-size:1.72rem; line-height:1.05; color:var(--ink); font-weight:800; }
    .metric-label { color:#334155; font-weight:700; font-size:.95rem; }
    .metric-detail { color:var(--muted); font-size:.78rem; margin-top:.18rem; }
    .metric-warn .metric-icon { background:linear-gradient(135deg,#FEF3C7,#FED7AA); }
    .metric-danger .metric-icon { background:linear-gradient(135deg,#FEE2E2,#FFE4E6); }
    .metric-ok .metric-icon { background:linear-gradient(135deg,#DCFCE7,#CCFBF1); }
    .panel, .note, .warn, .success {
      border-radius:18px; padding:16px 18px; margin:.4rem 0; border:1px solid var(--line); box-shadow:0 10px 28px rgba(15,23,42,.05); background:white;
    }
    .note { border-left:6px solid #2563EB; background:#EFF6FF; }
    .warn { border-left:6px solid var(--warning); background:#FFFBEB; }
    .success { border-left:6px solid var(--success); background:#F0FDF4; }
    .route-card { background:white; border:1px solid var(--line); border-radius:18px; padding:16px; box-shadow: 0 10px 30px rgba(15,23,42,.06); margin:.35rem 0; }
    .route-card-title { font-weight:800; color:var(--ink); font-size:1rem; margin-bottom:.45rem; }
    .route-path { color:#0F766E; font-weight:800; line-height:1.45; word-break:break-word; }
    .route-metrics { display:flex; gap:10px; flex-wrap:wrap; margin-top:.75rem; }
    .route-metrics span, .status-chip { display:inline-flex; align-items:center; padding:.35rem .62rem; border-radius:999px; font-weight:700; font-size:.78rem; border:1px solid transparent; }
    .route-metrics span { background:#F1F5F9; color:#334155; }
    .route-primary { border-top:4px solid var(--accent); }
    .route-secondary { border-top:4px solid var(--violet); }
    .chip-ok { background:#DCFCE7; color:#166534; border-color:#BBF7D0; }
    .chip-warn { background:#FEF3C7; color:#92400E; border-color:#FDE68A; }
    .chip-danger { background:#FEE2E2; color:#991B1B; border-color:#FECACA; }
    .chip-info { background:#DBEAFE; color:#1E40AF; border-color:#BFDBFE; }
    .footer { color:#64748B; font-size:.82rem; border-top:1px solid #E2E8F0; margin-top:2rem; padding-top:1rem; }
    .stButton > button { border-radius: 12px; border:1px solid #CBD5E1; font-weight:700; }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# STREAMLIT PAGES
# =============================================================================

def page_overview(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.markdown("""
    <div class="hero">
      <h1>🚚 WaselX Express</h1>
      <p>Professional-grade Data Structures & Algorithms prototype for UAE last-mile delivery optimization. The app connects each implementation to a measurable business problem: route waste, dispatch latency, and support lookup delay.</p>
    </div>
    """, unsafe_allow_html=True)
    cols = st.columns(4)
    metrics = [
        ("15", "Network nodes", "7 hubs + 8 zones", "🗺️", "primary"),
        ("24", "Road edges", "Weighted by distance/time/cost", "🛣️", "primary"),
        ("3,500", "Daily orders", "Scales to 15,000 in analysis", "📦", "ok"),
        ("10+", "Interactive simulations", "Animated walkthroughs now included", "🎬", "ok"),
    ]
    for col, (value, label, detail, icon, tone) in zip(cols, metrics):
        col.markdown(metric_card_html(value, label, detail, icon, tone), unsafe_allow_html=True)

    st.markdown(section_header_html("Operating network", "All visualizations use the assignment's exact 15-node, 24-edge UAE network."), unsafe_allow_html=True)
    st.plotly_chart(network_figure(go, graph, "WaselX UAE Operating Network", blocked_edges=blocked), use_container_width=True)

    st.markdown(section_header_html("Implementation coverage", "Aligned with the implementation plan and task tracker. Phase 3 adds professional UI polish without reintroducing redundant code."), unsafe_allow_html=True)
    coverage = pd.DataFrame([
        ["A", "Graphs, shortest paths, MST/forest", "Adjacency list/matrix, Dijkstra, Floyd-Warshall, BFS/DFS, Kruskal, Prim", "Complete"],
        ["B", "Tree-based order lookup", "BST, traversals, search, deletion, AVL build + rotation cases", "Complete"],
        ["C", "Order pipeline structures", "DLL, circular list, custom min-heap priority queue, stack undo", "Complete"],
        ["D", "Sorting/search/divide-and-conquer", "Merge sort, quick sort, binary/linear search, peak-hour D&C", "Complete"],
        ["E", "Management/leadership alignment", "Business impact and adoption narrative preserved for final report", "Report-linked"],
    ], columns=["Area", "Scope", "Implemented in dashboard", "Status"])
    st.dataframe(coverage, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(section_header_html("Business problem → DSA solution", kicker="Consulting narrative"), unsafe_allow_html=True)
        st.table(pd.DataFrame([
            ["Inefficient routes", "23% extra rider distance", "Dijkstra + road-closure simulator"],
            ["Slow dispatch", "8-minute manual sorting delay", "From-scratch min-heap priority queue"],
            ["Poor lookup", "45-second support lookup", "AVL tree order index"],
        ], columns=["Challenge", "Impact", "Prototype response"]))
    with c2:
        st.markdown(section_header_html("Readiness notes", kicker="Submission quality"), unsafe_allow_html=True)
        comps = graph.connected_components()
        if len(comps) > 1:
            st.markdown(f"<div class='warn'><b>Network finding:</b> The supplied graph has {len(comps)} disconnected components. The dashboard now handles unreachable routes and labels Q4 as a Minimum Spanning Forest unless a bridge edge is proposed.</div>", unsafe_allow_html=True)
        st.markdown("<div class='success'><b>Code hygiene:</b> The cleaned app removes duplicate files, removes unused dependencies, avoids <code>heapq</code>/<code>deque</code> as primary structures, and validates core algorithms through <code>--self-test</code>.</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>WaselX Express MAIB DSA prototype — final_cleaned.py is the single source of truth for the dashboard.</div>", unsafe_allow_html=True)


def page_network(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.markdown(section_header_html("Network Explorer", "Graph representation, weighted adjacency structures, and connectivity diagnostics for the WaselX road network.", "Task Area A / Q1 + Q7"), unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Executive map", "📋 Adjacency list", "🧮 Adjacency matrix", "🔌 Connectivity"])
    with tab1:
        left, right = st.columns([3, 1])
        with right:
            node = st.selectbox("Highlight node", ["None"] + graph.nodes)
            show_labels = st.toggle("Show all road labels", value=False)
            if node != "None":
                name, kind, emirate, orders, lat, lon = NODE_INFO[node]
                st.markdown(metric_card_html(str(orders), "Daily orders", f"{name} · {kind} · {emirate}", "📍", "primary"), unsafe_allow_html=True)
                st.write("Connected roads:")
                st.dataframe(pd.DataFrame([
                    {"To": e.target, "Road": e.road, "Km": e.distance, "Min": e.time, "AED": e.cost}
                    for e in graph.neighbors(node)
                ]), use_container_width=True, hide_index=True)
        with left:
            path = [node] if node != "None" else []
            st.plotly_chart(network_figure(go, graph, "Professional network map", highlight_path=path, blocked_edges=blocked, show_edge_labels=show_labels), use_container_width=True)
    with tab2:
        st.markdown("<div class='note'><b>Why this matters:</b> The adjacency list is preferred for sparse routing because algorithms scan actual neighbors instead of mostly empty matrix cells.</div>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(graph.adjacency_list_rows()), use_container_width=True, hide_index=True)
    with tab3:
        criterion = st.selectbox("Weight", ["distance", "time", "cost"], key="matrix_weight")
        st.dataframe(matrix_to_dataframe(pd, graph.nodes, graph.adjacency_matrix(criterion)), use_container_width=True)
        st.caption("INF means no direct road segment exists between the two locations. The matrix shown is the full 15-node representation required for Q1.")
    with tab4:
        comps = graph.connected_components()
        cols = st.columns(3)
        cols[0].markdown(metric_card_html(str(len(comps)), "Connected components", "Supplied graph structure", "🔌", "warn" if len(comps) > 1 else "ok"), unsafe_allow_html=True)
        cols[1].markdown(metric_card_html(str(len(comps[0]) if comps else 0), "Largest component", "Dubai/Sharjah/Ajman cluster", "🏙️", "primary"), unsafe_allow_html=True)
        cols[2].markdown(metric_card_html(str(len(graph.nodes)), "Total nodes", "All hubs and zones", "📍", "primary"), unsafe_allow_html=True)
        for i, comp in enumerate(comps, start=1):
            st.markdown(f"**Component {i}:** {', '.join(comp)}")
        if len(comps) > 1:
            st.warning("This is a material project finding: H5/H6/D6/D7 are isolated from the Dubai-Sharjah-Ajman component in the supplied edge table. The app now treats such routes as unreachable instead of forcing fake paths.")

def page_pathfinder(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.markdown(section_header_html("Dijkstra Path Simulator", "Interactive route optimization with animated step trace, multi-criteria comparison, dual path overlay, and road-closure rerouting.", "Task Area A / Q2 + Q6 + Q27"), unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        source = st.selectbox("Source", graph.nodes, index=0)
    with c2:
        destination = st.selectbox("Destination", graph.nodes, index=graph.nodes.index("D1"))
    with c3:
        criterion = st.selectbox("Optimize for", ["distance", "time", "cost"])

    result = graph.dijkstra(source, destination, criterion)
    metrics = result["metrics"]
    st.plotly_chart(network_figure(go, graph, f"Optimal path by {criterion}: {path_to_string(result['path'])}", result["path"], blocked_edges=blocked, primary_label=f"Optimal by {criterion}", show_edge_labels=True), use_container_width=True)
    cols = st.columns(4)
    cols[0].markdown(metric_card_html(path_to_string(result["path"]), "Optimal path", "Unreachable if no connected route exists", "🧭", "primary"), unsafe_allow_html=True)
    cols[1].markdown(metric_card_html(f"{format_number(metrics['distance'])} km", "Distance", "Total route length", "📏", "primary"), unsafe_allow_html=True)
    cols[2].markdown(metric_card_html(f"{format_number(metrics['time'])} min", "Travel time", "Weighted by minutes", "⏱️", "primary"), unsafe_allow_html=True)
    cols[3].markdown(metric_card_html(f"AED {format_number(metrics['cost'])}", "Segment cost", "Fuel + wear proxy", "💰", "ok"), unsafe_allow_html=True)

    tabs = st.tabs(["🎬 Step animation", "⚖️ All criteria", "🛣️ Dual path overlay", "🚧 Road closure comparison"])
    with tabs[0]:
        trace_rows = [{
            "Step": row["step"], "Action": row["action"], "Current": row.get("current", "-"), "Visited": ", ".join(row.get("visited", []))
        } for row in result["trace"]]
        col_left, col_right = st.columns([2, 1])
        with col_right:
            step_idx = st.slider("Review Dijkstra step", 0, len(result["trace"]) - 1, len(result["trace"]) - 1)
            autoplay = st.button("▶ Play Dijkstra animation")
            st.dataframe(pd.DataFrame(trace_rows), use_container_width=True, hide_index=True)
        fig_slot = col_left.empty()
        note_slot = col_left.empty()
        def draw_dijkstra_step(i: int) -> None:
            row = result["trace"][i]
            fig_slot.plotly_chart(network_figure(
                go, graph, f"Dijkstra step {row['step']}: {row['action']}",
                highlight_path=result["path"] if i == len(result["trace"]) - 1 else [],
                blocked_edges=blocked, visited=row.get("visited", []), current=row.get("current"),
                temporary_edge=row.get("relaxed_edge"), show_edge_labels=True,
                primary_label="Final optimal path",
            ), use_container_width=True)
            current = row.get("current", "-")
            note_slot.markdown(f"<div class='route-card route-primary'><div class='route-card-title'>Current step</div><div><b>Node:</b> {current}<br><b>Action:</b> {row['action']}<br><b>Visited:</b> {', '.join(row.get('visited', [])) or '-'}</div></div>", unsafe_allow_html=True)
        if autoplay:
            for i in range(len(result["trace"])):
                draw_dijkstra_step(i)
                time.sleep(st.session_state.get("anim_speed", 0.55))
        else:
            draw_dijkstra_step(step_idx)
    with tabs[1]:
        rows = []
        for crit in ["distance", "time", "cost"]:
            r = graph.dijkstra(source, destination, crit)
            met = r["metrics"]
            rows.append({"Criterion": crit, "Path": path_to_string(r["path"]), "Distance": met["distance"], "Time": met["time"], "Cost": met["cost"]})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.info("This view supports the consulting recommendation: Dijkstra can be rerun quickly for different business priorities without recomputing all pairs.")
    with tabs[2]:
        st.markdown("Compare two source-destination pairs on the same professional network map, as required by Q6(d).")
        a, b, c, d = st.columns(4)
        with a:
            s1 = st.selectbox("Pair 1 source", graph.nodes, index=0, key="dual_s1")
        with b:
            t1 = st.selectbox("Pair 1 destination", graph.nodes, index=graph.nodes.index("D4"), key="dual_t1")
        with c:
            s2 = st.selectbox("Pair 2 source", graph.nodes, index=graph.nodes.index("H7"), key="dual_s2")
        with d:
            t2 = st.selectbox("Pair 2 destination", graph.nodes, index=graph.nodes.index("D3"), key="dual_t2")
        r1 = graph.dijkstra(s1, t1, criterion)
        r2 = graph.dijkstra(s2, t2, criterion)
        st.plotly_chart(network_figure(go, graph, "Dual route overlay", r1["path"], blocked_edges=blocked, secondary_path=r2["path"], primary_label=f"{s1}→{t1}", secondary_label=f"{s2}→{t2}", show_edge_labels=True), use_container_width=True)
        left, right = st.columns(2)
        left.markdown(route_card_html(f"Pair 1: {s1} → {t1}", r1["path"], r1["metrics"], "primary"), unsafe_allow_html=True)
        right.markdown(route_card_html(f"Pair 2: {s2} → {t2}", r2["path"], r2["metrics"], "secondary"), unsafe_allow_html=True)
    with tabs[3]:
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
                st.plotly_chart(network_figure(go, graph, "Original route", original["path"], blocked_edges=blocked, primary_label="Original", show_edge_labels=True), use_container_width=True)
                st.markdown(route_card_html("Original", original["path"], original["metrics"], "primary"), unsafe_allow_html=True)
            with right:
                st.plotly_chart(network_figure(go, closure_graph, "Rerouted after closure", rerouted["path"], blocked_edges=list(blocked)+closure, primary_label="Rerouted", show_edge_labels=True), use_container_width=True)
                st.markdown(route_card_html("Rerouted", rerouted["path"], rerouted["metrics"], "secondary"), unsafe_allow_html=True)
            o, r = original["metrics"], rerouted["metrics"]
            comparison = pd.DataFrame([
                ["Original", path_to_string(original["path"]), o["distance"], o["time"], o["cost"]],
                ["Rerouted", path_to_string(rerouted["path"]), r["distance"], r["time"], r["cost"]],
                ["Delta", "", format_delta(r["distance"], o["distance"], " km"), format_delta(r["time"], o["time"], " min"), format_delta(r["cost"], o["cost"], " AED")],
            ], columns=["Case", "Path", "Distance", "Time", "Cost"])
            st.dataframe(comparison, use_container_width=True, hide_index=True)

def page_floyd(st: Any, go: Any, pd: Any, graph: WaselGraph) -> None:
    st.markdown(section_header_html("Floyd-Warshall All-Pairs Shortest Paths", "Offline all-pairs route intelligence for hub transfer decisions and proposed corridor analysis.", "Task Area A / Q3"), unsafe_allow_html=True)
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
    st.markdown(section_header_html("BFS and DFS Traversal", "Reachability and fewest-stop reasoning from the Deira hub default start node.", "Task Area A / Q7"), unsafe_allow_html=True)
    start = st.selectbox("Start node", graph.nodes, index=graph.nodes.index("H3"))
    bfs_result = graph.bfs(start)
    dfs_result = graph.dfs(start)
    tab1, tab2 = st.tabs(["🎬 BFS simulator", "🎬 DFS simulator"])
    with tab1:
        left, right = st.columns([2, 1])
        bfs_step = right.slider("BFS step", 0, len(bfs_result["trace"]) - 1, len(bfs_result["trace"]) - 1)
        bfs_play = right.button("▶ Play BFS animation")
        fig_slot = left.empty()
        info_slot = left.empty()
        def draw_bfs(i: int) -> None:
            row = bfs_result["trace"][i]
            fig_slot.plotly_chart(network_figure(go, graph, f"BFS step {i+1}: visit {row['current']}", visited=row["visited"], current=row["current"], blocked_edges=blocked, show_edge_labels=False), use_container_width=True)
            info_slot.markdown(f"<div class='route-card'><div class='route-card-title'>BFS queue state</div><div><b>Visited:</b> {' → '.join(row['visited'])}<br><b>Added this step:</b> {', '.join(row['added']) or '-'}<br><b>Queue:</b> {', '.join(row['queue']) or 'Empty'}</div></div>", unsafe_allow_html=True)
        if bfs_play:
            for i in range(len(bfs_result["trace"])):
                draw_bfs(i)
                time.sleep(st.session_state.get("anim_speed", 0.55))
        else:
            draw_bfs(bfs_step)
        right.dataframe(pd.DataFrame([{"Node": k, "Parent": v or "-"} for k, v in bfs_result["parent"].items()]), hide_index=True, use_container_width=True)
    with tab2:
        left, right = st.columns([2, 1])
        dfs_step = right.slider("DFS step", 1, len(dfs_result["order"]), len(dfs_result["order"]))
        dfs_play = right.button("▶ Play DFS animation")
        fig_slot = left.empty()
        info_slot = left.empty()
        def draw_dfs(i: int) -> None:
            visited = dfs_result["order"][:i]
            current = visited[-1] if visited else None
            fig_slot.plotly_chart(network_figure(go, graph, f"DFS visit order after {i} step(s)", visited=visited, current=current, blocked_edges=blocked), use_container_width=True)
            info_slot.markdown(f"<div class='route-card'><div class='route-card-title'>DFS progress</div><div><b>Visited order:</b> {' → '.join(visited) or '-'}<br><b>Current node:</b> {current or '-'}</div></div>", unsafe_allow_html=True)
        if dfs_play:
            for i in range(1, len(dfs_result["order"]) + 1):
                draw_dfs(i)
                time.sleep(st.session_state.get("anim_speed", 0.55))
        else:
            draw_dfs(dfs_step)
        right.dataframe(pd.DataFrame([{"Node": k, "Parent": v or "-"} for k, v in dfs_result["parent"].items()]), hide_index=True, use_container_width=True)
    if not bfs_result["reachable_all"]:
        st.warning(f"Starting from {start}, only {len(bfs_result['order'])} of {len(graph.nodes)} nodes are reachable. This is a key finding for Q7.")

def page_mst(st: Any, go: Any, pd: Any, graph: WaselGraph, blocked: List[Tuple[str, str]]) -> None:
    st.markdown(section_header_html("Minimum Spanning Tree / Forest", "Cost-minimizing tracking-network design using Kruskal and Prim while respecting the supplied disconnected graph.", "Task Area A / Q4"), unsafe_allow_html=True)
    result = graph.kruskal_mst()
    st.plotly_chart(network_figure(go, graph, "Kruskal Minimum Spanning Forest", mst_edges=result["edges"], blocked_edges=blocked, show_edge_labels=True), use_container_width=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Selected edges", len(result["edges"]))
    c2.metric("Total cost", f"AED {result['total']:.1f}K")
    c3.metric("Components", len(result["components"]))
    if not result["is_spanning_tree"]:
        st.warning("Because the provided graph is disconnected, the mathematically correct output is a Minimum Spanning Forest. A true MST over all 15 nodes would require at least one new bridge edge between components.")
    tab1, tab2 = st.tabs(["🎬 Kruskal trace", "🎬 Prim from H2"])
    edge_lookup = {normalized_edge(e.source, e.target): e for e in graph.edges}
    with tab1:
        left, right = st.columns([2, 1])
        step = right.slider("Kruskal step", 1, len(result["trace"]), len(result["trace"]))
        play = right.button("▶ Play Kruskal animation")
        fig_slot = left.empty()
        info_slot = left.empty()
        def draw_kruskal(i: int) -> None:
            rows = result["trace"][:i]
            chosen = []
            current_edge = None
            for row in rows:
                u, v = row["edge"].split("-")
                current_edge = (u, v)
                if row["action"] == "ADDED":
                    edge = edge_lookup.get(normalized_edge(u, v))
                    if edge:
                        chosen.append(edge)
            row = rows[-1]
            fig_slot.plotly_chart(network_figure(go, graph, f"Kruskal step {i}: {row['action']} {row['edge']}", mst_edges=chosen, blocked_edges=blocked, show_edge_labels=True, temporary_edge=current_edge), use_container_width=True)
            info_slot.markdown(f"<div class='route-card'><div class='route-card-title'>Current decision</div><div><b>Edge:</b> {row['edge']}<br><b>Action:</b> {row['action']}<br><b>Reason:</b> {row['reason']}<br><b>Running total:</b> AED {row['running_total']:.1f}K</div></div>", unsafe_allow_html=True)
        if play:
            for i in range(1, len(result["trace"]) + 1):
                draw_kruskal(i)
                time.sleep(st.session_state.get("anim_speed", 0.55))
        else:
            draw_kruskal(step)
        right.dataframe(pd.DataFrame(result["trace"]), use_container_width=True, hide_index=True)
    with tab2:
        start_node = st.selectbox("Start", graph.nodes, index=graph.nodes.index("H2"), key="prim_start")
        prim = graph.prim_mst(start_node)
        left, right = st.columns([2, 1])
        step = right.slider("Prim step", 1, max(1, len(prim["trace"])), max(1, len(prim["trace"])))
        play = right.button("▶ Play Prim animation")
        fig_slot = left.empty()
        info_slot = left.empty()
        def draw_prim(i: int) -> None:
            rows = prim["trace"][:i]
            chosen = []
            current_edge = None
            for row in rows:
                u, v = row["edge"].split("-")
                current_edge = (u, v)
                edge = edge_lookup.get(normalized_edge(u, v))
                if edge:
                    chosen.append(edge)
            row = rows[-1]
            fig_slot.plotly_chart(network_figure(go, graph, f"Prim step {i}: add {row['edge']}", mst_edges=chosen, blocked_edges=blocked, show_edge_labels=True, temporary_edge=current_edge), use_container_width=True)
            info_slot.markdown(f"<div class='route-card'><div class='route-card-title'>Prim growth</div><div><b>Edge added:</b> {row['edge']}<br><b>Road:</b> {row['road']}<br><b>Running total:</b> AED {row['running_total']:.1f}K</div></div>", unsafe_allow_html=True)
        if prim["trace"]:
            if play:
                for i in range(1, len(prim["trace"]) + 1):
                    draw_prim(i)
                    time.sleep(st.session_state.get("anim_speed", 0.55))
            else:
                draw_prim(step)
        right.dataframe(pd.DataFrame(prim["trace"]), use_container_width=True, hide_index=True)
        if not prim["is_complete"]:
            st.info(f"Prim starting at {start_node} covers {len(prim['visited'])} nodes in its connected component. Run Kruskal for the full spanning forest across disconnected components.")

def page_trees(st: Any, go: Any, pd: Any) -> None:
    st.markdown(section_header_html("BST and AVL Tree Indexing", "Order lookup structures, traversal outputs, deletion, and AVL balance logic.", "Task Area B / Q8-Q11"), unsafe_allow_html=True)
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
    st.markdown(section_header_html("Order Pipeline Data Structures", "Professional simulations for route mutation, rotating rider assignment, priority dispatch, and lifecycle undo.", "Task Area C / Q12-Q15"), unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["🎬 Doubly linked route", "🎬 Circular rider list", "🎬 Priority queue", "🎬 Stack lifecycle"])
    with tab1:
        stages = []
        route = DoublyLinkedList()
        for stop in [("Dubai Marina Hub", "ORD001", "10:15"), ("JLT", "ORD002", "10:30"), ("Downtown Dubai", "ORD003", "10:50"), ("Business Bay", "ORD004", "11:05"), ("Deira", "ORD005", "11:25"), ("Silicon Oasis", "ORD006", "11:50")]:
            route.append(*stop)
        stages.append(("Initial route", route.display_forward(), "Original 6-stop delivery plan"))
        route.insert_after("ORD003", "Al Quoz (Urgent)", "ORD_URGENT", "10:55")
        stages.append(("Urgent insertion", route.display_forward(), "New urgent stop inserted after ORD003"))
        route.delete_by_order_id("ORD005")
        stages.append(("Cancellation complete", route.display_forward(), "Cancelled order ORD005 removed from the route"))
        left, right = st.columns([2, 1])
        stage_idx = right.slider("Route stage", 0, len(stages) - 1, len(stages) - 1)
        play = right.button("▶ Play route simulation")
        fig = left.empty()
        def draw_route(i: int) -> None:
            title, rows, desc = stages[i]
            fig.markdown(f"<div class='route-card route-primary'><div class='route-card-title'>{title}</div><div>{desc}</div></div>", unsafe_allow_html=True)
            left.dataframe(route_to_dataframe(pd, rows), use_container_width=True, hide_index=True)
        if play:
            for i in range(len(stages)):
                draw_route(i)
                time.sleep(st.session_state.get("anim_speed", 0.55))
        else:
            draw_route(stage_idx)
        right.markdown("<div class='note'><b>Backed by a real DoublyLinkedList class:</b> insertion and deletion relink nodes instead of using Python list insert/pop operations.</div>", unsafe_allow_html=True)
    with tab2:
        riders = CircularLinkedList()
        for i in range(1, 9):
            riders.add_rider(f"Rider {i}")
        assignments = []
        rosters = []
        for order in range(1, 12):
            assignments.append((order, riders.assign_next_order(), "Before break"))
            rosters.append((order, list(riders.display_roster())))
        riders.remove_rider("Rider 4")
        for order in range(12, 21):
            assignments.append((order, riders.assign_next_order(), "After Rider 4 break"))
            rosters.append((order, list(riders.display_roster())))
        left, right = st.columns([2, 1])
        step = right.slider("Assignment step", 1, len(assignments), len(assignments))
        play = right.button("▶ Play rider rotation")
        table_slot = left.empty()
        note_slot = left.empty()
        def draw_assign(i: int) -> None:
            partial = assignments[:i]
            current = partial[-1]
            table_slot.dataframe(pd.DataFrame(partial, columns=["Order", "Assigned Rider", "Phase"]), use_container_width=True, hide_index=True)
            roster = rosters[i-1][1]
            note_slot.markdown(f"<div class='route-card'><div class='route-card-title'>Current assignment</div><div><b>Order:</b> {current[0]}<br><b>Assigned rider:</b> {current[1]}<br><b>Roster:</b> {', '.join(roster)}</div></div>", unsafe_allow_html=True)
        if play:
            for i in range(1, len(assignments)+1):
                draw_assign(i)
                time.sleep(st.session_state.get("anim_speed", 0.45))
        else:
            draw_assign(step)
    with tab3:
        orders = [("Order A", 3), ("Order B", 1), ("Order C", 4), ("Order D", 2), ("Order E", 1), ("Order F", 5), ("Order G", 2), ("Order H", 3), ("Order I", 1), ("Order J", 4)]
        pq = MinHeap()
        snapshots = []
        for name, priority in orders:
            pq.push(priority, name)
            queue_view = [(item[2], item[0], item[1] + 1) for item in pq.display()]
            snapshots.append((f"Enqueue {name}", queue_view.copy()))
        while pq:
            popped = pq.pop()
            queue_view = [(item[2], item[0], item[1] + 1) for item in pq.display()]
            snapshots.append((f"Dequeue {popped[2]}", queue_view.copy()))
        left, right = st.columns([2, 1])
        step = right.slider("Heap simulation step", 1, len(snapshots), len(snapshots))
        play = right.button("▶ Play heap simulation")
        table_slot = left.empty()
        note_slot = left.empty()
        def draw_heap(i: int) -> None:
            action, queue_view = snapshots[i-1]
            table_slot.dataframe(pd.DataFrame(queue_view, columns=["Order", "Priority", "Arrival #"]), use_container_width=True, hide_index=True)
            note_slot.markdown(f"<div class='route-card'><div class='route-card-title'>Heap state</div><div><b>Action:</b> {action}<br><b>Items currently in heap:</b> {len(queue_view)}</div></div>", unsafe_allow_html=True)
        if play:
            for i in range(1, len(snapshots)+1):
                draw_heap(i)
                time.sleep(st.session_state.get("anim_speed", 0.4))
        else:
            draw_heap(step)
        st.caption("FIFO tie-breaking is preserved by the internal arrival counter in the custom MinHeap implementation.")
    with tab4:
        lifecycle = Stack()
        lifecycle_rows = []
        for status in ["Received", "Confirmed", "Preparing", "Dispatched", "In Transit", "Delivered"]:
            lifecycle.push(status)
            lifecycle_rows.append((status, " → ".join(lifecycle.display_top_first())))
        error_demo = Stack()
        for status in ["Received", "Confirmed", "Preparing", "Dispatched"]:
            error_demo.push(status)
        before = error_demo.display_top_first()
        error_demo.pop()
        after = error_demo.display_top_first()
        left, right = st.columns([2, 1])
        step = right.slider("Lifecycle step", 1, len(lifecycle_rows), len(lifecycle_rows))
        play = right.button("▶ Play lifecycle simulation")
        frame_slot = left.empty()
        def draw_stack(i: int) -> None:
            partial = lifecycle_rows[:i]
            frame_slot.dataframe(pd.DataFrame(partial, columns=["Action pushed", "Stack top → bottom"]), use_container_width=True, hide_index=True)
        if play:
            for i in range(1, len(lifecycle_rows)+1):
                draw_stack(i)
                time.sleep(st.session_state.get("anim_speed", 0.45))
        else:
            draw_stack(step)
        l, r = st.columns(2)
        l.markdown(metric_card_html("Dispatched", "Erroneous top status", "Before undo", "⚠️", "warn"), unsafe_allow_html=True)
        r.markdown(metric_card_html("Preparing", "Restored top status", "After pop() undo", "↩️", "ok"), unsafe_allow_html=True)
        st.write("Before undo:", before)
        st.write("After undo:", after)

def page_sorting(st: Any, go: Any, px: Any, pd: Any) -> None:
    st.markdown(section_header_html("Sorting, Searching, and Divide-and-Conquer", "Manifest sorting, exact Q19 lookup dataset, and peak-hour detection for Ramadan-style load.", "Task Area D / Q18-Q22"), unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🎬 Sort manifest", "🎬 Search order ID", "🎬 Peak hour"])
    sample = [("JLT",3), ("Deira",1), ("Marina",4), ("JLT",1), ("Deira",2), ("Marina",2), ("Silicon",5), ("Deira",3), ("JLT",2), ("Marina",1), ("Silicon",1), ("Deira",4), ("Silicon",3), ("JLT",5), ("Marina",3)]
    with tab1:
        ms_sorted, ms_count, ms_steps = merge_sort(sample)
        qs_sorted, qs_count, qs_steps = quick_sort(sample)
        c1, c2 = st.columns(2)
        c1.dataframe(pd.DataFrame(ms_sorted, columns=["Zone", "Priority"]), hide_index=True, use_container_width=True)
        c2.dataframe(pd.DataFrame(qs_sorted, columns=["Zone", "Priority"]), hide_index=True, use_container_width=True)
        m1, m2 = st.columns(2)
        m1.metric("Merge comparisons", ms_count)
        m2.metric("Quick comparisons", qs_count)
        with st.expander("Merge first 3 recursion levels"):
            st.write("\n".join(ms_steps))
        with st.expander("Quick first 2 partition levels"):
            st.write("\n".join(qs_steps))
    with tab2:
        ids = list(range(10001, 11001))
        target = st.number_input("Order ID", min_value=10001, max_value=11000, value=10347)
        b_idx, b_comp, b_trace = binary_search(ids, int(target))
        l_idx, l_comp = linear_search(ids, int(target))
        st.table(pd.DataFrame([["Binary", b_idx, b_comp], ["Linear", l_idx, l_comp]], columns=["Method", "Index", "Comparisons"]))
        step = st.slider("Binary search step", 1, len(b_trace), len(b_trace))
        st.dataframe(pd.DataFrame(b_trace[:step], columns=["Low", "Mid", "High", "Mid Value"]), hide_index=True, use_container_width=True)
    with tab3:
        default_orders = [80, 55, 40, 30, 25, 20, 35, 60, 120, 210, 280, 330, 300, 260, 240, 290, 410, 520, 610, 480, 360, 250, 180, 120]
        top = peak_hour_divide_conquer(default_orders, 3)
        step = st.slider("Peak-hour reveal", 1, 24, 24)
        df = pd.DataFrame({"Hour": list(range(24)), "Orders": default_orders})
        fig = px.bar(df.iloc[:step], x="Hour", y="Orders", title="Ramadan-style hourly order volume")
        fig.update_layout(height=420, plot_bgcolor="#F8FAFC", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.write("Top peak hours:", top)

def main() -> None:
    st, go, px, pd = require_ui_libraries()
    style_app(st)
    with st.sidebar:
        st.markdown("## 🚚 WaselX DSA")
        st.caption("Professional cleaned prototype · Phase 3 UI")
        section = st.radio("Navigate", [
            "Overview", "Network", "Pathfinder", "Floyd-Warshall", "BFS/DFS", "MST", "BST/AVL", "Pipeline DS", "Sorting/Search/Peak"
        ])
        edge_labels = {f"{u}-{v} ({road})": (u, v) for u, v, road, *_ in EDGES}
        selected = st.multiselect("Global road closures", list(edge_labels.keys()))
        blocked = [edge_labels[label] for label in selected]
        st.session_state["anim_speed"] = st.slider("Animation speed (sec)", min_value=0.15, max_value=1.20, value=0.45, step=0.05)
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
