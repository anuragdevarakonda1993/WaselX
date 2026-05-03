"""
WaselX Express — Interactive DSA Visualizer
MAIB Final Project | Data Structures & Algorithms
Upload this single file to GitHub and connect to Streamlit Cloud.

Requirements (requirements.txt):
    streamlit>=1.32.0
    plotly>=5.18.0
    networkx>=3.2.0
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import heapq
import time
import random
from collections import deque
import math

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WaselX Express — DSA Visualizer",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #0f1c2e; }
  [data-testid="stSidebar"] * { color: #e0eaf8 !important; }
  .main-title {
    background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
    padding: 24px 32px; border-radius: 12px; margin-bottom: 20px;
    color: white; text-align: center;
  }
  .metric-card {
    background: linear-gradient(135deg, #1F4E79, #2E75B6);
    border-radius: 10px; padding: 16px; color: white; text-align: center;
    margin: 4px;
  }
  .metric-card h2 { margin: 0; font-size: 2rem; }
  .metric-card p  { margin: 4px 0 0; opacity: 0.85; font-size: 0.85rem; }
  .step-box {
    background: #f0f6ff; border-left: 4px solid #2E75B6;
    border-radius: 6px; padding: 10px 14px; margin: 6px 0;
    font-family: monospace; font-size: 0.88rem;
  }
  .highlight-box {
    background: #e8f4e8; border-left: 4px solid #28a745;
    border-radius: 6px; padding: 10px 14px; margin: 6px 0;
  }
  .warn-box {
    background: #fff8e1; border-left: 4px solid #ffc107;
    border-radius: 6px; padding: 10px 14px; margin: 6px 0;
  }
  div[data-testid="stTabs"] button { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════
NODES = ['H1','H2','H3','H4','H5','H6','H7','D1','D2','D3','D4','D5','D6','D7','D8']

NODE_INFO = {
    'H1': ('Dubai Marina Hub',       'Hub',           'Dubai',     450, 25.0807, 55.1332),
    'H2': ('Business Bay Hub',       'Hub',           'Dubai',     520, 25.1851, 55.2795),
    'H3': ('Deira Hub',              'Hub',           'Dubai',     380, 25.2697, 55.3095),
    'H4': ('JLT Hub',                'Hub',           'Dubai',     290, 25.0657, 55.1453),
    'H5': ('Abu Dhabi Corniche Hub', 'Hub',           'Abu Dhabi', 410, 24.4667, 54.3667),
    'H6': ('Khalifa City Hub',       'Hub',           'Abu Dhabi', 310, 24.4215, 54.4860),
    'H7': ('Sharjah Al Nahda Hub',   'Hub',           'Sharjah',   340, 25.3283, 55.4119),
    'D1': ('Downtown Dubai',         'Delivery Zone', 'Dubai',     280, 25.1972, 55.2744),
    'D2': ('Al Quoz Industrial',     'Delivery Zone', 'Dubai',     150, 25.1380, 55.2220),
    'D3': ('Jumeirah',               'Delivery Zone', 'Dubai',     200, 25.1298, 55.1882),
    'D4': ('Silicon Oasis',          'Delivery Zone', 'Dubai',     180, 25.1190, 55.3796),
    'D5': ('Ajman City Centre',      'Delivery Zone', 'Ajman',     130, 25.4106, 55.4354),
    'D6': ('Yas Island',             'Delivery Zone', 'Abu Dhabi', 160, 24.4674, 54.6074),
    'D7': ('Al Reem Island',         'Delivery Zone', 'Abu Dhabi', 220, 24.4972, 54.4034),
    'D8': ('Muwaileh (Univ. City)',  'Delivery Zone', 'Sharjah',   190, 25.3170, 55.5040),
}

EDGES = [
    ('H1','H4','Sheikh Zayed Rd',    5, 10, 3.5),
    ('H1','D3','Jumeirah Beach Rd',  4, 12, 3.0),
    ('H1','D1','Al Khail Rd',        8, 15, 5.5),
    ('H4','D2','Hessa St',           6, 14, 4.0),
    ('H4','H2','Sheikh Zayed Rd',    7, 13, 5.0),
    ('H2','D1','Financial Centre Rd',3,  8, 2.5),
    ('H2','H3','Al Maktoum Bridge',  9, 18, 6.0),
    ('H3','D4','Dubai-Al Ain Rd',   12, 22, 8.0),
    ('H3','H7','Emirates Rd',       15, 25,10.0),
    ('H7','D8','University Rd',      4,  8, 3.0),
    ('H7','D5','Sheikh Mohammed Rd',10, 18, 7.0),
    ('D1','D3','2nd December St',    5, 11, 3.5),
    ('D1','D2','Al Khail Rd',        6, 13, 4.0),
    ('D2','D4','Hatta Rd',          10, 20, 7.0),
    ('H5','D7','Corniche Rd',        6, 12, 4.0),
    ('H5','H6','Abu Dhabi Ring Rd', 14, 20, 9.0),
    ('H6','D6','Yas Connector',      8, 15, 5.5),
    ('D6','D7','Al Saadiyat Bridge', 7, 13, 5.0),
    ('H5','D6','Island Bypass',     12, 22, 8.0),
    ('D4','D8','Academic City Rd',  18, 30,12.0),
    ('H3','D2','Al Asayel St',       8, 16, 5.5),
    ('H1','H2','Happiness St',      10, 18, 7.0),
    ('D5','D8','Sharjah Ring Rd',    8, 15, 5.5),
    ('H6','D7','Reem Bridge',       10, 18, 7.0),
]

# UAE-style coordinate positions (lon, lat scaled for visual layout)
POS = {n: (NODE_INFO[n][5], NODE_INFO[n][4]) for n in NODES}

EMIRATE_COLORS = {'Dubai':'#2E75B6','Abu Dhabi':'#C55A11','Sharjah':'#375623','Ajman':'#7030A0'}
NODE_COLORS = {n: EMIRATE_COLORS.get(NODE_INFO[n][2], '#888') for n in NODES}

TEAM_MEMBERS = [
    "Anurag Devarakonda", "Anish Borkar", "Nandana Santhosh",
    "Neha Thapa", "Sarth Malankar",
]

# ═══════════════════════════════════════════════════════════════════════════
# FROM-SCRATCH DATA STRUCTURES (Assignment requires no heapq/deque as primary)
# ═══════════════════════════════════════════════════════════════════════════

class MinHeap:
    """Min-Heap Priority Queue — implemented from scratch (Q14 requirement)."""
    def __init__(self):
        self._heap = []
        self._counter = 0

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i] < self._heap[parent]:
                self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._heap)
        while True:
            smallest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest != i:
                self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
                i = smallest
            else:
                break

    def push(self, priority, name):
        entry = (priority, self._counter, name)
        self._counter += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)
        return entry

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty heap")
        root = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(0)
        return root

    def peek(self):
        if not self._heap:
            return None
        return self._heap[0]

    def __len__(self):
        return len(self._heap)

    def __bool__(self):
        return len(self._heap) > 0

    def as_list(self):
        return list(self._heap)

    def sorted_view(self):
        return sorted(self._heap)


class DLLNode:
    """Node for Doubly Linked List (Q12 requirement)."""
    def __init__(self, stop_name, order_id, eta):
        self.stop_name = stop_name
        self.order_id = order_id
        self.eta = eta
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly Linked List — from scratch (Q12 requirement)."""
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, stop_name, order_id, eta):
        node = DLLNode(stop_name, order_id, eta)
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node

    def insert_after(self, target_order_id, stop_name, order_id, eta):
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

    def insert_at(self, index, stop_name, order_id, eta):
        if index <= 0:
            new_node = DLLNode(stop_name, order_id, eta)
            new_node.next = self.head
            if self.head:
                self.head.prev = new_node
            self.head = new_node
            if not self.tail:
                self.tail = new_node
            self._size += 1
            return new_node
        cur = self.head
        for _ in range(index - 1):
            if cur is None:
                break
            cur = cur.next
        if cur is None:
            return self.append(stop_name, order_id, eta)
        return self.insert_after(cur.order_id, stop_name, order_id, eta)

    def delete_by_order_id(self, order_id):
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
                self._size -= 1
                return cur
            cur = cur.next
        return None

    def delete_at(self, index):
        cur = self.head
        for _ in range(index):
            if cur is None:
                return None
            cur = cur.next
        if cur is None:
            return None
        return self.delete_by_order_id(cur.order_id)

    def move_first_to_end(self):
        if self._size <= 1:
            return
        node = self.head
        self.head = node.next
        self.head.prev = None
        node.prev = self.tail
        node.next = None
        self.tail.next = node
        self.tail = node

    def display_forward(self):
        result = []
        cur = self.head
        while cur:
            result.append((cur.stop_name, cur.order_id, cur.eta))
            cur = cur.next
        return result

    def display_reverse(self):
        result = []
        cur = self.tail
        while cur:
            result.append((cur.stop_name, cur.order_id, cur.eta))
            cur = cur.prev
        return result

    def __len__(self):
        return self._size


class CLLNode:
    """Node for Circular Linked List (Q13 requirement)."""
    def __init__(self, rider_name):
        self.rider_name = rider_name
        self.next = None


class CircularLinkedList:
    """Circular Linked List — round-robin rider assignment (Q13 requirement)."""
    def __init__(self):
        self.tail = None
        self._size = 0
        self._current = None

    def add_rider(self, name):
        node = CLLNode(name)
        if not self.tail:
            node.next = node
            self.tail = node
            self._current = node
        else:
            node.next = self.tail.next
            self.tail.next = node
            self.tail = node
        self._size += 1

    def remove_rider(self, name):
        if not self.tail:
            return False
        if self._size == 1 and self.tail.rider_name == name:
            self.tail = None
            self._current = None
            self._size = 0
            return True
        prev, cur = self.tail, self.tail.next
        for _ in range(self._size):
            if cur.rider_name == name:
                prev.next = cur.next
                if cur == self.tail:
                    self.tail = prev
                if cur == self._current:
                    self._current = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def assign_next_order(self):
        if not self._current:
            return None
        rider = self._current.rider_name
        self._current = self._current.next
        return rider

    def display_roster(self):
        if not self.tail:
            return []
        result = []
        cur = self.tail.next
        for _ in range(self._size):
            result.append(cur.rider_name)
            cur = cur.next
        return result


class Stack:
    """Stack — order lifecycle tracking (Q15 requirement)."""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            return None
        return self._items[-1]

    def display(self):
        return list(reversed(self._items))

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return len(self._items) > 0

    def as_list(self):
        return list(self._items)


# ═══════════════════════════════════════════════════════════════════════════
# GRAPH CLASS
# ═══════════════════════════════════════════════════════════════════════════
class WaselGraph:
    def __init__(self, blocked_edges=None):
        self.nodes = NODES
        self.idx = {n: i for i, n in enumerate(NODES)}
        self.adj = {n: [] for n in NODES}
        self.blocked = set(blocked_edges or [])
        for u, v, road, d, t, c in EDGES:
            key = tuple(sorted([u, v]))
            if key not in self.blocked:
                self.adj[u].append((v, d, t, c, road))
                self.adj[v].append((u, d, t, c, road))

    def dijkstra_animated(self, src, dst, weight='dist'):
        """Returns list of animation frames for Dijkstra's."""
        wi = {'dist': 1, 'time': 2, 'cost': 3}[weight]
        n = len(self.nodes)
        dist = {nd: float('inf') for nd in self.nodes}
        prev = {nd: None for nd in self.nodes}
        dist[src] = 0
        heap = [(0, src)]
        visited = set()
        frames = []  # each frame: (visited_set, dist_dict, current_node, relaxed_edge)

        frames.append({
            'visited': set(), 'dist': dict(dist), 'current': src,
            'relaxed': None, 'prev': dict(prev),
            'msg': f"Start: Initialize all distances to ∞, set dist[{src}] = 0"
        })

        while heap:
            d, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            frames.append({
                'visited': set(visited), 'dist': dict(dist), 'current': u,
                'relaxed': None, 'prev': dict(prev),
                'msg': f"Visit {u} ({NODE_INFO[u][0]}) — current shortest dist = {d:.1f}"
            })
            if u == dst:
                break
            for v, ed, et, ec, road in self.adj[u]:
                if v in visited:
                    continue
                w = [ed, ed, et, ec][wi]
                nd = dist[u] + w
                if nd < dist[v]:
                    old = dist[v]
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))
                    frames.append({
                        'visited': set(visited), 'dist': dict(dist), 'current': u,
                        'relaxed': (u, v), 'prev': dict(prev),
                        'msg': f"Relax edge {u}→{v} via {road}: {old:.0f} → {nd:.1f} {'✓ IMPROVED' if old != float('inf') else '✓ FOUND'}"
                    })

        # Reconstruct path
        path = []
        cur = dst
        while cur:
            path.append(cur)
            cur = prev[cur]
        path.reverse()

        return frames, path, dist[dst], prev

    def bfs_animated(self, src):
        frames = []
        visited = []
        parent = {src: None}
        queue = deque([src])
        seen = {src}
        frames.append({'visited': [], 'queue': [src], 'current': src,
                       'msg': f"BFS Start from {src}. Queue: [{src}]"})
        while queue:
            node = queue.popleft()
            visited.append(node)
            neighbors_added = []
            for nb, *_ in self.adj[node]:
                if nb not in seen:
                    seen.add(nb)
                    parent[nb] = node
                    queue.append(nb)
                    neighbors_added.append(nb)
            frames.append({
                'visited': list(visited), 'queue': list(queue), 'current': node,
                'parent': dict(parent),
                'msg': f"Visit {node} → Added to queue: {neighbors_added or 'none (all neighbors visited)'}"
            })
        return frames, visited, parent

    def kruskal_animated(self):
        parent = {n: n for n in self.nodes}
        rank   = {n: 0 for n in self.nodes}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            px, py = find(x), find(y)
            if px == py: return False
            if rank[px] < rank[py]: px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]: rank[px] += 1
            return True

        sorted_edges = sorted(EDGES, key=lambda e: e[5])
        frames = []
        mst = []
        total = 0
        frames.append({'mst': [], 'rejected': [], 'current': None, 'total': 0,
                       'msg': "Sort all edges by cost. Start adding smallest edges..."})
        for u, v, road, d, t, c in sorted_edges:
            key = tuple(sorted([u, v]))
            if key in self.blocked:
                continue
            if union(u, v):
                mst.append((u, v, road, d, t, c))
                total += c
                frames.append({'mst': list(mst), 'rejected': [], 'current': (u, v),
                               'total': total,
                               'msg': f"✓ ADD {u}↔{v} ({road}, AED {c}k) — MST total: AED {total:.1f}k"})
            else:
                frames.append({'mst': list(mst), 'rejected': [(u, v)], 'current': (u, v),
                               'total': total,
                               'msg': f"✗ REJECT {u}↔{v} ({road}) — would create a cycle"})
        return frames, mst, total

    def floyd_warshall(self, node_subset=None, weight='time'):
        """Floyd-Warshall all-pairs shortest paths (Q3 requirement)."""
        wi = {'dist': 1, 'time': 2, 'cost': 3}[weight]
        nodes = node_subset or self.nodes
        n = len(nodes)
        idx = {nd: i for i, nd in enumerate(nodes)}
        INF = float('inf')
        dist = [[INF] * n for _ in range(n)]
        nxt = [[None] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, road, d, t, c in EDGES:
            if u in idx and v in idx:
                key = tuple(sorted([u, v]))
                if key not in self.blocked:
                    w = [d, d, t, c][wi]
                    ui, vi = idx[u], idx[v]
                    if w < dist[ui][vi]:
                        dist[ui][vi] = w
                        dist[vi][ui] = w
                        nxt[ui][vi] = v
                        nxt[vi][ui] = u
        init_matrix = [row[:] for row in dist]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]
        return nodes, init_matrix, dist, nxt

    def prim_animated(self, start='H2'):
        """Prim's MST algorithm — animated (Q4c requirement)."""
        frames = []
        mst_edges = []
        in_mst = {start}
        total = 0
        frames.append({'mst': [], 'current': start, 'total': 0,
                       'msg': f"Start Prim's from {start} ({NODE_INFO[start][0]})"})
        while len(in_mst) < len(self.nodes):
            best = None
            for u in in_mst:
                for v, d, t, c, road in self.adj[u]:
                    if v not in in_mst:
                        if best is None or c < best[5]:
                            best = (u, v, road, d, t, c)
            if best is None:
                break
            u, v, road, d, t, c = best
            in_mst.add(v)
            mst_edges.append(best)
            total += c
            frames.append({'mst': list(mst_edges), 'current': v, 'total': total,
                           'msg': f"✓ ADD {u}↔{v} ({road}, AED {c}k) — MST total: AED {total:.1f}k"})
        return frames, mst_edges, total

    def adjacency_matrix(self, weight='dist'):
        """Build adjacency matrix representation (Q1 requirement)."""
        wi = {'dist': 1, 'time': 2, 'cost': 3}[weight]
        n = len(self.nodes)
        INF = float('inf')
        matrix = [[INF] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0
        for u, v, road, d, t, c in EDGES:
            key = tuple(sorted([u, v]))
            if key not in self.blocked:
                w = [d, d, t, c][wi]
                ui, vi = self.idx[u], self.idx[v]
                if w < matrix[ui][vi]:
                    matrix[ui][vi] = w
                    matrix[vi][ui] = w
        return matrix


# ═══════════════════════════════════════════════════════════════════════════
# PLOTLY GRAPH DRAWING HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def base_network_traces(g, highlight_path=None, highlight_edges=None,
                        visited=None, current=None, relaxed_edge=None,
                        mst_edges=None, rejected_edges=None, blocked=None):
    """Returns (edge_traces, node_trace) for a plotly figure."""
    traces = []
    visited = visited or set()
    highlight_path = highlight_path or []
    highlight_edges = highlight_edges or []
    mst_edges = mst_edges or []
    rejected_edges = rejected_edges or []
    blocked = blocked or set()
    path_set = set(zip(highlight_path, highlight_path[1:]))
    path_set |= set(zip(highlight_path[1:], highlight_path))
    mst_set = {(u, v) for u, v, *_ in mst_edges} | {(v, u) for u, v, *_ in mst_edges}
    rejected_set = set(rejected_edges) | {(v, u) for u, v in rejected_edges}

    for u, v, road, d, t, c in EDGES:
        key = tuple(sorted([u, v]))
        x0, y0 = POS[u]
        x1, y1 = POS[v]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2

        if key in blocked:
            color, width, dash = '#ff4444', 2, 'dot'
        elif (u, v) in path_set or (v, u) in path_set:
            color, width, dash = '#ff6b00', 4, 'solid'
        elif (u, v) in mst_set:
            color, width, dash = '#00b050', 3, 'solid'
        elif (u, v) in rejected_set:
            color, width, dash = '#cc0000', 2, 'dash'
        elif relaxed_edge and ((u, v) == relaxed_edge or (v, u) == relaxed_edge):
            color, width, dash = '#ffd700', 3, 'solid'
        else:
            color, width, dash = '#cccccc', 1.2, 'solid'

        traces.append(go.Scatter(
            x=[x0, mx, x1], y=[y0, my, y1],
            mode='lines',
            line=dict(color=color, width=width, dash=dash),
            hoverinfo='text',
            text=f"{u}↔{v} | {road}<br>{d}km | {t}min | AED{c}",
            showlegend=False
        ))

    # Edge weight labels
    for u, v, road, d, t, c in EDGES:
        key = tuple(sorted([u, v]))
        if key in blocked: continue
        x0, y0 = POS[u]; x1, y1 = POS[v]
        traces.append(go.Scatter(
            x=[(x0+x1)/2], y=[(y0+y1)/2],
            mode='text',
            text=[f"{d}km"],
            textfont=dict(size=8, color='#666'),
            hoverinfo='skip', showlegend=False
        ))

    # Nodes
    nx_list, ny_list, nc_list, ns_list, nt_list, nl_list = [], [], [], [], [], []
    for node in NODES:
        x, y = POS[node]
        nx_list.append(x); ny_list.append(y)
        is_hub = NODE_INFO[node][1] == 'Hub'

        if node == current:
            nc_list.append('#ff6b00'); ns_list.append(28)
        elif node in visited:
            nc_list.append('#00b050'); ns_list.append(20)
        elif node in highlight_path:
            nc_list.append('#ff6b00'); ns_list.append(22)
        else:
            nc_list.append(NODE_COLORS[node]); ns_list.append(18 if is_hub else 14)

        info = NODE_INFO[node]
        nt_list.append(f"<b>{node}</b> — {info[0]}<br>Type: {info[1]}<br>Emirate: {info[2]}<br>Daily Orders: {info[3]}")
        nl_list.append(node)

    traces.append(go.Scatter(
        x=nx_list, y=ny_list,
        mode='markers+text',
        marker=dict(size=ns_list, color=nc_list,
                    line=dict(width=2, color='white')),
        text=nl_list,
        textposition='top center',
        textfont=dict(size=10, color='black', family='Arial Black'),
        hovertext=nt_list, hoverinfo='text',
        showlegend=False
    ))
    return traces


def make_figure(traces, title="WaselX Delivery Network"):
    fig = go.Figure(data=traces)
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color='#1F4E79'), x=0.5),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#f8faff',
        paper_bgcolor='white',
        height=480,
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode='closest',
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🚚 WaselX DSA")
    st.markdown("**MAIB Final Project**")
    st.markdown("---")
    section = st.radio("Navigate", [
        "🏠 Overview",
        "🗺️ Network Explorer",
        "🔵 Dijkstra's Pathfinder",
        "📊 Floyd-Warshall",
        "🌊 BFS / DFS Traversal",
        "🌲 Minimum Spanning Tree",
        "🌳 BST & AVL Tree",
        "📋 Priority Queue",
        "🔗 Linked List Simulator",
        "🔄 Circular Linked List",
        "📦 Order Lifecycle Stack",
        "📊 Sorting Benchmark",
        "🔍 Binary Search Demo",
        "⏰ Peak Hour Finder",
    ])
    st.markdown("---")
    st.markdown("**Road Closures**")
    blocked_labels = {f"{u}↔{v} ({road})": tuple(sorted([u, v]))
                      for u, v, road, *_ in EDGES}
    blocked_selections = st.multiselect("Block edges:", list(blocked_labels.keys()))
    blocked_set = {blocked_labels[s] for s in blocked_selections}
    if blocked_set:
        st.warning(f"⚠️ {len(blocked_set)} road(s) closed")
    st.markdown("---")
    st.caption("**Team:** " + " · ".join(TEAM_MEMBERS))

G = WaselGraph(blocked_edges=blocked_set)

# ═══════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
if section == "🏠 Overview":
    st.markdown("""
    <div class="main-title">
      <h1>🚚 WaselX Express</h1>
      <p style="font-size:1.1rem;opacity:0.9">Interactive DSA Visualizer — MAIB Final Project</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in zip([c1,c2,c3,c4],
        ["15","24","3,500","7"],
        ["Network Nodes","Road Edges","Daily Orders","Emirates"]):
        col.markdown(f'<div class="metric-card"><h2>{val}</h2><p>{label}</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🗺️ Full WaselX Delivery Network")
    traces = base_network_traces(G)
    fig = make_figure(traces, "WaselX UAE Delivery Network — All 15 Nodes, 24 Edges")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 The 3 Business Problems")
        st.markdown("""
        | # | Problem | Cost |
        |---|---------|------|
        | 1 | Inefficient routes (+23% distance) | AED 1.2M/yr |
        | 2 | Slow dispatch (8-min manual delay) | 12% complaints |
        | 3 | Poor order lookup (45s avg) | CSAT 3.2/5 |
        """)
    with col2:
        st.subheader("✅ DSA Solutions")
        st.markdown("""
        | Problem | Solution | Savings |
        |---------|----------|---------|
        | Routes | Dijkstra's Algorithm | AED 1.2M/yr |
        | Dispatch | Priority Queue (Min-Heap) | AED 2.4M/yr |
        | Lookup | AVL Tree | CSAT 4.0+ |
        """)

    st.info("👈 Use the sidebar to explore each algorithm interactively!")

# ═══════════════════════════════════════════════════════════════════════════
# NETWORK EXPLORER
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🗺️ Network Explorer":
    st.title("🗺️ Network Explorer")
    st.markdown("Explore the graph representations: Visual Map, Adjacency List, and Adjacency Matrix (Q1 requirement).")

    net_tab1, net_tab2, net_tab3 = st.tabs(["🗺️ Visual Map", "📋 Adjacency List", "🧮 Adjacency Matrix"])

    with net_tab1:
        col1, col2 = st.columns([3, 1])

        with col2:
            st.subheader("Filters")
            show_hubs = st.checkbox("Show Hubs", True)
            show_zones = st.checkbox("Show Delivery Zones", True)
            color_by = st.selectbox("Color by", ["Emirate", "Type", "Daily Orders"])
            selected_node = st.selectbox("Highlight node", ["None"] + NODES)

            st.subheader("Node Info")
            if selected_node != "None":
                info = NODE_INFO[selected_node]
                st.markdown(f"""
                **{selected_node} — {info[0]}**
                - Type: {info[1]}
                - Emirate: {info[2]}
                - Daily Orders: {info[3]}
                - Neighbors: {len(G.adj[selected_node])}
                """)
                nbrs = [(v, d, t, c, r) for v, d, t, c, r in G.adj[selected_node]]
                st.markdown("**Connected to:**")
                for v, d, t, c, r in nbrs:
                    st.markdown(f"→ `{v}` via {r} ({d}km, {t}min)")

        with col1:
            traces = base_network_traces(G,
                highlight_path=[selected_node] if selected_node != "None" else [],
                visited={selected_node} if selected_node != "None" else set())
            fig = make_figure(traces, "WaselX Network — Click nodes for info")
            st.plotly_chart(fig, use_container_width=True)

        # Stats
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            orders_by_emirate = {}
            for n in NODES:
                e = NODE_INFO[n][2]
                orders_by_emirate[e] = orders_by_emirate.get(e, 0) + NODE_INFO[n][3]
            fig_pie = px.pie(values=list(orders_by_emirate.values()),
                             names=list(orders_by_emirate.keys()),
                             title="Daily Orders by Emirate",
                             color_discrete_sequence=['#2E75B6','#C55A11','#375623','#7030A0'])
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            nodes_sorted = sorted(NODES, key=lambda n: NODE_INFO[n][3], reverse=True)
            fig_bar = px.bar(x=nodes_sorted, y=[NODE_INFO[n][3] for n in nodes_sorted],
                             color=[NODE_COLORS[n] for n in nodes_sorted],
                             title="Daily Orders per Node",
                             labels={'x':'Node','y':'Orders'})
            fig_bar.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        with c3:
            edge_costs = [c for _, _, _, _, _, c in EDGES]
            fig_hist = px.histogram(x=edge_costs, nbins=8, title="Edge Cost Distribution (AED)",
                                    color_discrete_sequence=['#2E75B6'])
            fig_hist.update_layout(height=300)
            st.plotly_chart(fig_hist, use_container_width=True)

    with net_tab2:
        st.subheader("Adjacency List Representation")
        st.markdown("Most efficient for WaselX's sparse network (V=15, E=24). Uses only memory proportional to edges `O(V+E)`.")
        for u in NODES:
            neighbors = [f"{v}({d}km)" for v, d, t, c, r in G.adj[u]]
            st.markdown(f"**{u}**: `[{', '.join(neighbors)}]`")

    with net_tab3:
        st.subheader("Adjacency Matrix Representation")
        st.markdown("Allows `O(1)` edge checks, but wastes memory on `INF` for unconnected pairs `O(V²)`.")
        mat_weight = st.selectbox("Weight metric for matrix", ["dist", "time", "cost"], format_func=lambda x: {"dist": "Distance (km)", "time": "Time (min)", "cost": "Cost (AED)"}[x])
        matrix = G.adjacency_matrix(weight=mat_weight)
        
        import pandas as pd
        header = [""] + list(NODES)
        rows = []
        for i, n in enumerate(NODES):
            row = [n] + [f"{matrix[i][j]:.0f}" if matrix[i][j] < float('inf') else "∞" for j in range(len(NODES))]
            rows.append(row)
        
        df_mat = pd.DataFrame(rows, columns=header).set_index("")
        st.dataframe(df_mat, use_container_width=True)

        st.info("💡 **Why Adjacency List is preferred:** The matrix stores 225 entries (most are ∞). The list stores only 48 edge directions. Dijkstra's and BFS algorithms run significantly faster using the Adjacency List on sparse graphs.")

# ═══════════════════════════════════════════════════════════════════════════
# DIJKSTRA
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🔵 Dijkstra's Pathfinder":
    st.title("🔵 Dijkstra's Shortest Path — Step-by-Step Animation")
    st.markdown("Watch Dijkstra's algorithm explore the network in real time, relaxing edges and updating distances.")

    col1, col2, col3, col4 = st.columns(4)
    with col1: src = st.selectbox("Source", NODES, index=0)
    with col2: dst = st.selectbox("Destination", NODES, index=7)
    with col3: weight = st.selectbox("Optimize for", ["dist","time","cost"],
                                      format_func=lambda x: {"dist":"Distance (km)","time":"Time (min)","cost":"Cost (AED)"}[x])
    with col4:
        speed = st.selectbox("Animation Speed", ["Slow","Medium","Fast"],index=1)
        delay = {"Slow":0.9,"Medium":0.45,"Fast":0.15}[speed]

    if src == dst:
        st.warning("Source and destination must be different."); st.stop()

    run = st.button("▶ Run Dijkstra's Animation", type="primary")

    frames, path, best_dist, prev = G.dijkstra_animated(src, dst, weight)

    # Always show final state first
    final_traces = base_network_traces(G, highlight_path=path,
                                        visited=frames[-1]['visited'] if frames else set())
    fig = make_figure(final_traces, f"Dijkstra's: {src} → {dst}  |  Best {weight} = {best_dist:.1f}")
    graph_placeholder = st.empty()
    graph_placeholder.plotly_chart(fig, use_container_width=True)

    col_a, col_b, col_c = st.columns(3)
    w_label = {"dist":"km","time":"min","cost":"AED"}[weight]
    col_a.metric("Optimal Path", " → ".join(path) if path else "No path")
    col_b.metric(f"Best {weight}", f"{best_dist:.1f} {w_label}" if best_dist < float('inf') else "∞")
    col_c.metric("Steps taken", len(frames))

    step_placeholder = st.empty()
    log_placeholder  = st.empty()

    if run:
        logs = []
        for i, frame in enumerate(frames):
            visited  = frame['visited']
            cur      = frame['current']
            relaxed  = frame['relaxed']
            msg      = frame['msg']
            dist_map = frame['dist']

            # Decide what path to highlight so far
            partial_path = []
            if cur in prev or cur == src:
                c = cur
                while c:
                    partial_path.append(c)
                    c = frame['prev'].get(c)
                partial_path.reverse()

            traces = base_network_traces(G,
                highlight_path=partial_path,
                visited=visited,
                current=cur,
                relaxed_edge=relaxed,
                blocked=blocked_set)
            fig_step = make_figure(traces,
                f"Step {i+1}/{len(frames)}: {msg}")
            graph_placeholder.plotly_chart(fig_step, use_container_width=True)

            logs.append(f"**Step {i+1}:** {msg}")
            with log_placeholder.container():
                for log in logs[-6:]:
                    st.markdown(f'<div class="step-box">{log}</div>', unsafe_allow_html=True)

            time.sleep(delay)

        # Final
        final_traces = base_network_traces(G, highlight_path=path, visited=set(NODES))
        fig_final = make_figure(final_traces, f"✅ Done! Optimal {weight} path: {' → '.join(path)}")
        graph_placeholder.plotly_chart(fig_final, use_container_width=True)
        st.success(f"✅ Shortest path found: **{' → '.join(path)}** | {weight}: **{best_dist:.1f} {w_label}**")

    # Complexity
    with st.expander("📚 Algorithm Details & Complexity"):
        st.markdown("""
        **Dijkstra's Algorithm (Min-Heap)**
        
        | Property | Value |
        |----------|-------|
        | Time Complexity | O((V + E) log V) |
        | Space Complexity | O(V) |
        | For WaselX (V=15, E=24) | ~156 operations per query |
        | Supports negative weights? | ❌ No |
        | Best for | Single-source, real-time routing |
        
        **How it works:** Greedily picks the unvisited node with the smallest known distance, 
        then relaxes all its outgoing edges. An orange edge means it was just relaxed (improved).
        Green nodes = already visited with optimal distance confirmed.
        """)

    st.markdown("---")
    st.subheader("🌉 Advanced Path Analysis")
    adv_tab1, adv_tab2 = st.tabs(["🛣️ Dual Path Overlay (Q6d)", "🚧 Road Closure Comparison (Q27d)"])

    with adv_tab1:
        st.markdown("**Compare optimal paths for different metrics simultaneously.**")
        col_m1, col_m2 = st.columns(2)
        with col_m1: metric_1 = st.selectbox("Metric 1 (Blue Path)", ["time", "dist", "cost"], index=0)
        with col_m2: metric_2 = st.selectbox("Metric 2 (Orange Path)", ["cost", "dist", "time"], index=0)

        _, path1, d1, _ = G.dijkstra_animated(src, dst, metric_1)
        _, path2, d2, _ = G.dijkstra_animated(src, dst, metric_2)

        traces = base_network_traces(G)
        
        # Overlay Path 1 (Blue)
        x_p1, y_p1 = [], []
        for i in range(len(path1)-1):
            n1, n2 = path1[i], path1[i+1]
            x_p1.extend([NODE_POS[n1][0], NODE_POS[n2][0], None])
            y_p1.extend([NODE_POS[n1][1], NODE_POS[n2][1], None])
        traces.append(go.Scatter(x=x_p1, y=y_p1, mode='lines', 
                                 line=dict(color='#2E75B6', width=6), opacity=0.7, name=f'Opt by {metric_1}'))

        # Overlay Path 2 (Orange) - offset slightly for visibility
        x_p2, y_p2 = [], []
        for i in range(len(path2)-1):
            n1, n2 = path2[i], path2[i+1]
            x_p2.extend([NODE_POS[n1][0]+0.01, NODE_POS[n2][0]+0.01, None])
            y_p2.extend([NODE_POS[n1][1]-0.01, NODE_POS[n2][1]-0.01, None])
        traces.append(go.Scatter(x=x_p2, y=y_p2, mode='lines', 
                                 line=dict(color='#ff6b00', width=6, dash='dot'), opacity=0.9, name=f'Opt by {metric_2}'))

        fig_dual = make_figure(traces, f"Comparing paths from {src} to {dst}")
        st.plotly_chart(fig_dual, use_container_width=True)
        
        c1, c2 = st.columns(2)
        c1.info(f"**Path 1 ({metric_1}):** {' → '.join(path1)} | {d1:.1f}")
        c2.warning(f"**Path 2 ({metric_2}):** {' → '.join(path2)} | {d2:.1f}")

    with adv_tab2:
        st.markdown("**Simulate a sudden road closure and instantly find the optimal detour.**")
        
        closure_edges = [f"{u} ⇄ {v}" for u, v, _, _, _, _ in EDGES]
        blocked_edge_str = st.selectbox("Select road to block:", ["None"] + closure_edges)
        
        c_left, c_right = st.columns(2)
        
        # Original (Unblocked) Path
        _, path_orig, d_orig, _ = G.dijkstra_animated(src, dst, weight)
        
        if blocked_edge_str == "None":
            st.info("No roads blocked. Standard routing applies.")
            blocked_set_adv = set()
            path_alt, d_alt = path_orig, d_orig
        else:
            u_blk, v_blk = blocked_edge_str.split(" ⇄ ")
            blocked_set_adv = {(u_blk, v_blk), (v_blk, u_blk)}
            
            # Re-run Dijkstra with blocked edge
            _, path_alt, d_alt, _ = G.dijkstra_animated(src, dst, weight, blocked_edges=blocked_set_adv)
            
        with c_left:
            st.markdown("**Original Route:**")
            fig_orig = make_figure(base_network_traces(G, highlight_path=path_orig, blocked=blocked_set_adv), "Before Closure")
            st.plotly_chart(fig_orig, use_container_width=True)
            st.success(f"Cost: {d_orig:.1f} | Path: {' → '.join(path_orig)}")
            
        with c_right:
            st.markdown("**Alternative Route:**")
            fig_alt = make_figure(base_network_traces(G, highlight_path=path_alt, blocked=blocked_set_adv), "After Closure")
            st.plotly_chart(fig_alt, use_container_width=True)
            if not path_alt:
                st.error("No path available!")
            else:
                st.warning(f"Cost: {d_alt:.1f} | Path: {' → '.join(path_alt)}")
        st.code("""
def dijkstra(graph, src, dst, weight='dist'):
    dist = {n: float('inf') for n in graph.nodes}
    dist[src] = 0
    prev = {n: None for n in graph.nodes}
    heap = [(0, src)]
    visited = set()
    
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited: continue
        visited.add(u)
        if u == dst: break
        for v, edge_weight in graph.neighbors(u):
            if dist[u] + edge_weight < dist[v]:
                dist[v] = dist[u] + edge_weight
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    
    # Reconstruct path
    path = []
    cur = dst
    while cur: path.append(cur); cur = prev[cur]
    return list(reversed(path)), dist[dst]
        """, language='python')


# ═══════════════════════════════════════════════════════════════════════════
# FLOYD-WARSHALL
# ═══════════════════════════════════════════════════════════════════════════
elif section == "📊 Floyd-Warshall":
    st.title("📊 Floyd-Warshall — All-Pairs Shortest Paths")
    st.markdown("Compute shortest paths between **all pairs** of hubs simultaneously. O(V³) algorithm ideal for offline analytics.")

    col1, col2 = st.columns(2)
    with col1:
        fw_weight = st.selectbox("Weight metric", ["time", "dist", "cost"],
                                  format_func=lambda x: {"dist": "Distance (km)", "time": "Time (min)", "cost": "Cost (AED)"}[x])
    with col2:
        fw_scope = st.radio("Scope", ["Hubs Only (H1–H7)", "All 15 Nodes"])

    subset = [n for n in NODES if n.startswith('H')] if "Hubs" in fw_scope else None
    nodes_fw, init_mat, final_mat, nxt = G.floyd_warshall(node_subset=subset, weight=fw_weight)

    tab_init, tab_final, tab_analysis = st.tabs(["📋 Initial Matrix", "✅ Final Matrix", "📈 Analysis"])

    w_label = {"dist": "km", "time": "min", "cost": "AED"}[fw_weight]

    with tab_init:
        st.subheader("Initial Distance Matrix (direct edges only)")
        header = [""] + list(nodes_fw)
        rows = []
        for i, n in enumerate(nodes_fw):
            row = [n] + [f"{init_mat[i][j]:.0f}" if init_mat[i][j] < float('inf') else "∞" for j in range(len(nodes_fw))]
            rows.append(row)
        import pandas as pd
        df_init = pd.DataFrame(rows, columns=header).set_index("")
        st.dataframe(df_init, use_container_width=True)

    with tab_final:
        st.subheader(f"Final All-Pairs Shortest {fw_weight.title()} Matrix")
        rows2 = []
        for i, n in enumerate(nodes_fw):
            row = [n] + [f"{final_mat[i][j]:.0f}" if final_mat[i][j] < float('inf') else "∞" for j in range(len(nodes_fw))]
            rows2.append(row)
        df_final = pd.DataFrame(rows2, columns=header).set_index("")
        st.dataframe(df_final, use_container_width=True)

    with tab_analysis:
        st.subheader("Hub Connectivity Analysis")
        idx_fw = {n: i for i, n in enumerate(nodes_fw)}
        INF = float('inf')

        # Find farthest pair
        max_val, max_pair = 0, ("", "")
        for i in range(len(nodes_fw)):
            for j in range(i + 1, len(nodes_fw)):
                if final_mat[i][j] < INF and final_mat[i][j] > max_val:
                    max_val = final_mat[i][j]
                    max_pair = (nodes_fw[i], nodes_fw[j])

        # Find best-connected hub
        best_hub, best_avg = "", INF
        for i, n in enumerate(nodes_fw):
            vals = [final_mat[i][j] for j in range(len(nodes_fw)) if i != j and final_mat[i][j] < INF]
            if vals:
                avg = sum(vals) / len(vals)
                if avg < best_avg:
                    best_avg, best_hub = avg, n

        c1, c2, c3 = st.columns(3)
        c1.metric("Farthest Pair", f"{max_pair[0]}↔{max_pair[1]}", f"{max_val:.0f} {w_label}")
        c2.metric("Best Connected", f"{best_hub}", f"Avg: {best_avg:.1f} {w_label}")
        c3.metric("Matrix Size", f"{len(nodes_fw)}×{len(nodes_fw)}", f"O(V³) = {len(nodes_fw)**3} ops")

        # Disconnected pairs
        disc = [(nodes_fw[i], nodes_fw[j]) for i in range(len(nodes_fw)) for j in range(i+1, len(nodes_fw)) if final_mat[i][j] >= INF]
        if disc:
            st.warning(f"⚠️ {len(disc)} disconnected pair(s) found: {', '.join(f'{a}↔{b}' for a,b in disc[:5])}")

    with st.expander("📚 Floyd-Warshall Details"):
        st.markdown(f"""
        **Floyd-Warshall Algorithm**

        | Property | Value |
        |----------|-------|
        | Time Complexity | O(V³) |
        | Space Complexity | O(V²) |
        | For WaselX Hubs (V=7) | 343 operations |
        | For Full Network (V=15) | 3,375 operations |
        | Best for | All-pairs offline analytics |
        | Supports negative weights? | ✅ Yes (no negative cycles) |

        **When to use:** Nightly batch jobs, SLA modeling, hub connectivity dashboards.
        **When NOT to use:** Real-time single-pair queries (use Dijkstra instead).
        """)


# ═══════════════════════════════════════════════════════════════════════════
# BFS / DFS
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🌊 BFS / DFS Traversal":
    st.title("🌊 BFS / DFS Traversal Animation")

    col1, col2, col3 = st.columns(3)
    with col1: start = st.selectbox("Start Node", NODES, index=2)
    with col2: algo  = st.radio("Algorithm", ["BFS","DFS"])
    with col3: speed = st.selectbox("Speed", ["Slow","Medium","Fast"], index=1)
    delay = {"Slow":0.8,"Medium":0.4,"Fast":0.12}[speed]

    run = st.button(f"▶ Run {algo} Animation", type="primary")
    graph_ph = st.empty()
    log_ph   = st.empty()
    info_ph  = st.empty()

    def dfs_animated(g, src):
        frames, seen = [], set()
        def _dfs(node, depth=0):
            seen.add(node)
            frames.append({'visited': list(seen), 'current': node,
                           'msg': f"Visit {node} ({NODE_INFO[node][0]}) at depth {depth}"})
            for nb, *_ in g.adj[node]:
                if nb not in seen:
                    _dfs(nb, depth+1)
        _dfs(src)
        return frames, list(seen)

    if algo == "BFS":
        frames, order, parent = G.bfs_animated(start)
    else:
        frames, order = dfs_animated(G, start)
        parent = {}

    # Show static final
    traces = base_network_traces(G, visited=set(order), current=start)
    graph_ph.plotly_chart(make_figure(traces, f"{algo} from {start}"), use_container_width=True)

    if run:
        logs = []
        for i, frame in enumerate(frames):
            vis  = set(frame['visited'])
            cur  = frame['current']
            msg  = frame['msg']
            traces = base_network_traces(G, visited=vis, current=cur, blocked=blocked_set)
            graph_ph.plotly_chart(
                make_figure(traces, f"{algo} Step {i+1}/{len(frames)}: {msg}"),
                use_container_width=True)
            logs.append(f"Step {i+1}: {msg}")
            with log_ph.container():
                for log in logs[-5:]:
                    st.markdown(f'<div class="step-box">{log}</div>', unsafe_allow_html=True)
            time.sleep(delay)

        st.success(f"✅ {algo} complete! Visited {len(order)} nodes.")
        info_ph.markdown(f"**Traversal order:** `{'  →  '.join(order)}`")

    with st.expander("📚 BFS vs DFS Explained"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **BFS (Breadth-First Search)**
            - Explores level by level
            - Uses a **Queue** (FIFO)
            - Finds path with fewest hops
            - Time: O(V + E)
            - ✅ Best for: "Fewest stops" delivery
            """)
        with col2:
            st.markdown("""
            **DFS (Depth-First Search)**
            - Explores as deep as possible first
            - Uses a **Stack** (recursion)
            - Does NOT guarantee shortest path
            - Time: O(V + E)
            - ✅ Best for: Checking connectivity
            """)


# ═══════════════════════════════════════════════════════════════════════════
# MST
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🌲 Minimum Spanning Tree":
    st.title("🌲 Minimum Spanning Tree — Kruskal's & Prim's")
    st.markdown("Compare two greedy MST algorithms building the cheapest cable network connecting all 15 nodes.")

    mst_tab1, mst_tab2 = st.tabs(["🔷 Kruskal's Algorithm", "🔶 Prim's Algorithm"])

    with mst_tab1:
        speed = st.selectbox("Speed", ["Slow","Medium","Fast"], index=1, key="k_speed")
        delay = {"Slow":0.9,"Medium":0.45,"Fast":0.15}[speed]
        run = st.button("▶ Run Kruskal's Animation", type="primary", key="k_run")

        frames, mst, total = G.kruskal_animated()

        graph_ph = st.empty()
        log_ph   = st.empty()
        metric_ph = st.columns(3)

        traces = base_network_traces(G, mst_edges=mst, blocked=blocked_set)
        graph_ph.plotly_chart(make_figure(traces, f"Kruskal's MST — Total: AED {total:.1f}K"), use_container_width=True)

        metric_ph[0].metric("MST Edges", f"{len(mst)} edges")
        metric_ph[1].metric("Total Cost", f"AED {total:.1f}K")
        metric_ph[2].metric("All-edge Cost", f"AED {sum(c for *_,c in EDGES):.1f}K")

        if run:
            logs = []
            for i, frame in enumerate(frames):
                current_mst = frame['mst']
                rej  = frame.get('rejected', [])
                msg  = frame['msg']

                traces = base_network_traces(G, mst_edges=current_mst,
                    rejected_edges=rej, current=None, blocked=blocked_set)
                graph_ph.plotly_chart(
                    make_figure(traces, f"Kruskal Step {i+1}/{len(frames)}: {msg}"),
                    use_container_width=True)
                logs.append(msg)
                with log_ph.container():
                    for log in logs[-6:]:
                        color = "step-box" if "ADD" in log else "warn-box"
                        st.markdown(f'<div class="{color}">{log}</div>', unsafe_allow_html=True)
                time.sleep(delay)
            st.success(f"✅ Kruskal's MST complete! {len(mst)} edges. Total: AED {total:.1f}K")

        if mst:
            with st.expander("📋 Kruskal's MST Edges"):
                st.table([{"From":u,"To":v,"Road":road,"Dist":f"{d}km","Time":f"{t}min","Cost":f"AED {c}k"} for u,v,road,d,t,c in mst])

    with mst_tab2:
        prim_start = st.selectbox("Start node", NODES, index=NODES.index('H2'), key="p_start")
        p_speed = st.selectbox("Speed", ["Slow","Medium","Fast"], index=1, key="p_speed")
        p_delay = {"Slow":0.9,"Medium":0.45,"Fast":0.15}[p_speed]
        p_run = st.button("▶ Run Prim's Animation", type="primary", key="p_run")

        p_frames, p_mst, p_total = G.prim_animated(start=prim_start)

        p_graph_ph = st.empty()
        p_log_ph   = st.empty()
        p_metric_ph = st.columns(3)

        p_traces = base_network_traces(G, mst_edges=p_mst, blocked=blocked_set)
        p_graph_ph.plotly_chart(make_figure(p_traces, f"Prim's MST from {prim_start} — Total: AED {p_total:.1f}K"), use_container_width=True)

        p_metric_ph[0].metric("MST Edges", f"{len(p_mst)} edges")
        p_metric_ph[1].metric("Total Cost", f"AED {p_total:.1f}K")
        p_metric_ph[2].metric("Kruskal's Cost", f"AED {total:.1f}K", delta="Same ✓" if abs(p_total - total) < 0.01 else f"Δ {p_total - total:.1f}")

        if p_run:
            p_logs = []
            for i, frame in enumerate(p_frames):
                p_cur_mst = frame['mst']
                msg = frame['msg']
                p_traces = base_network_traces(G, mst_edges=p_cur_mst, current=frame.get('current'), blocked=blocked_set)
                p_graph_ph.plotly_chart(
                    make_figure(p_traces, f"Prim Step {i+1}/{len(p_frames)}: {msg}"),
                    use_container_width=True)
                p_logs.append(msg)
                with p_log_ph.container():
                    for log in p_logs[-6:]:
                        color = "step-box" if "ADD" in log else "warn-box"
                        st.markdown(f'<div class="{color}">{log}</div>', unsafe_allow_html=True)
                time.sleep(p_delay)
            st.success(f"✅ Prim's MST complete! {len(p_mst)} edges. Total: AED {p_total:.1f}K")

        if p_mst:
            with st.expander("📋 Prim's MST Edges"):
                st.table([{"From":u,"To":v,"Road":road,"Dist":f"{d}km","Time":f"{t}min","Cost":f"AED {c}k"} for u,v,road,d,t,c in p_mst])

    with st.expander("📚 MST Algorithm Comparison"):
        st.markdown("""
        | Property | Kruskal's | Prim's |
        |----------|-----------|--------|
        | Strategy | Sort all edges, add if no cycle | Grow from start node, add cheapest edge |
        | Time Complexity | O(E log E) | O(E log V) with min-heap |
        | Best for | Sparse graphs | Dense graphs |
        | Uses | Union-Find | Priority Queue |
        | Guarantee | Same total cost | Same total cost |
        | For WaselX (E=24) | Sorts 24 edges | Grows from 1 node |
        """)


# ═══════════════════════════════════════════════════════════════════════════
# BST & AVL
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🌳 BST & AVL Tree":
    st.title("🌳 Binary Search Tree & AVL Tree")

    tab1, tab2, tab3 = st.tabs(["🌳 Build BST","⚖️ AVL Balancing","🔍 Search Demo"])

    ORDER_IDS = [1045,1023,1078,1012,1034,1056,1089,1005,1020,1067,1050,1098]

    def build_bst(keys):
        """Returns adjacency dict for tree drawing."""
        class Node:
            def __init__(self, k): self.k=k; self.l=None; self.r=None
        root = None
        def ins(node, k):
            if not node: return Node(k)
            if k < node.k: node.l = ins(node.l, k)
            else: node.r = ins(node.r, k)
            return node
        for k in keys: root = ins(root, k)
        return root

    def tree_positions(root):
        """BFS to get (node, x, y, parent) for plotting."""
        if not root: return []
        result = []
        queue = deque([(root, 0, 0, None, 1.0)])
        while queue:
            node, x, y, parent, spread = queue.popleft()
            result.append((node.k, x, y, parent))
            if node.l: queue.append((node.l, x - spread, y - 1, node.k, spread/2))
            if node.r: queue.append((node.r, x + spread, y - 1, node.k, spread/2))
        return result

    def plot_tree(positions, highlight=None, title="BST"):
        fig = go.Figure()
        pos_map = {k: (x, y) for k, x, y, _ in positions}
        for k, x, y, parent in positions:
            if parent is not None:
                px2, py2 = pos_map[parent]
                color = '#ff6b00' if k == highlight or parent == highlight else '#aaaaaa'
                fig.add_trace(go.Scatter(x=[px2,x], y=[py2,y], mode='lines',
                    line=dict(color=color, width=2), showlegend=False, hoverinfo='skip'))
        for k, x, y, parent in positions:
            color = '#ff6b00' if k == highlight else '#2E75B6'
            fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers+text',
                marker=dict(size=36, color=color, line=dict(width=2,color='white')),
                text=[str(k)], textfont=dict(size=10, color='white'),
                textposition='middle center', hoverinfo='text',
                hovertext=f"Order ID: {k}", showlegend=False))
        fig.update_layout(title=title, height=400,
            xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
            yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
            plot_bgcolor='#f8faff', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=40,b=10))
        return fig

    with tab1:
        st.subheader("Build BST from Order IDs")
        custom = st.text_input("Order IDs (comma-separated)", ",".join(map(str,ORDER_IDS)))
        try:
            keys = [int(x.strip()) for x in custom.split(",") if x.strip()]
        except:
            keys = ORDER_IDS

        root = build_bst(keys)
        pos  = tree_positions(root)
        st.plotly_chart(plot_tree(pos, title=f"BST — {len(keys)} Nodes"), use_container_width=True)

        col1, col2, col3 = st.columns(3)
        def inorder(n):
            if not n: return []
            return inorder(n.l) + [n.k] + inorder(n.r)
        def preorder(n):
            if not n: return []
            return [n.k] + preorder(n.l) + preorder(n.r)
        def postorder(n):
            if not n: return []
            return postorder(n.l) + postorder(n.r) + [n.k]
        def height(n):
            if not n: return 0
            return 1 + max(height(n.l), height(n.r))

        col1.metric("Tree Height", height(root))
        col2.metric("Nodes", len(keys))
        col3.metric("Worst-case Search", f"O({height(root)})")

        st.markdown(f"**In-order:** `{inorder(root)}`")
        st.markdown(f"**Pre-order:** `{preorder(root)}`")
        st.markdown(f"**Post-order:** `{postorder(root)}`")

    with tab2:
        st.subheader("AVL Tree Operations & Rotations")
        st.markdown("AVL trees self-balance to guarantee `O(log n)` height. Watch rotations happen as nodes are inserted.")

        avl_case = st.selectbox("Demonstrate Rotation Case:", ["LL (Right Rotation)", "RR (Left Rotation)", "LR (Left-Right Rotation)", "RL (Right-Left Rotation)"])

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Before Rotation (Imbalanced):**")
            if "LL" in avl_case:
                pos_before = [(1012, 0.5, 0, None), (1005, 0.25, -1, 1012), (1003, 0.125, -2, 1005)]
                st.plotly_chart(plot_tree(pos_before, highlight=1012, title="Imbalance at 1012 (LL)"), use_container_width=True)
            elif "RR" in avl_case:
                pos_before = [(1078, 0.5, 0, None), (1089, 0.75, -1, 1078), (1098, 0.875, -2, 1089)]
                st.plotly_chart(plot_tree(pos_before, highlight=1078, title="Imbalance at 1078 (RR)"), use_container_width=True)
            elif "LR" in avl_case:
                pos_before = [(1034, 0.5, 0, None), (1012, 0.25, -1, 1034), (1023, 0.375, -2, 1012)]
                st.plotly_chart(plot_tree(pos_before, highlight=1034, title="Imbalance at 1034 (LR)"), use_container_width=True)
            else: # RL
                pos_before = [(1056, 0.5, 0, None), (1078, 0.75, -1, 1056), (1067, 0.625, -2, 1078)]
                st.plotly_chart(plot_tree(pos_before, highlight=1056, title="Imbalance at 1056 (RL)"), use_container_width=True)
        
        with c2:
            st.markdown("**After Rotation (Balanced):**")
            if "LL" in avl_case:
                pos_after = [(1005, 0.5, 0, None), (1003, 0.25, -1, 1005), (1012, 0.75, -1, 1005)]
                st.plotly_chart(plot_tree(pos_after, title="Single Right Rotation"), use_container_width=True)
                st.info("Fix: Single **Right Rotation** at 1012.")
            elif "RR" in avl_case:
                pos_after = [(1089, 0.5, 0, None), (1078, 0.25, -1, 1089), (1098, 0.75, -1, 1089)]
                st.plotly_chart(plot_tree(pos_after, title="Single Left Rotation"), use_container_width=True)
                st.info("Fix: Single **Left Rotation** at 1078.")
            elif "LR" in avl_case:
                pos_after = [(1023, 0.5, 0, None), (1012, 0.25, -1, 1023), (1034, 0.75, -1, 1023)]
                st.plotly_chart(plot_tree(pos_after, title="Left-Right Rotation"), use_container_width=True)
                st.info("Fix: **Left Rotation** at 1012, then **Right Rotation** at 1034.")
            else: # RL
                pos_after = [(1067, 0.5, 0, None), (1056, 0.25, -1, 1067), (1078, 0.75, -1, 1067)]
                st.plotly_chart(plot_tree(pos_after, title="Right-Left Rotation"), use_container_width=True)
                st.info("Fix: **Right Rotation** at 1078, then **Left Rotation** at 1056.")

        st.markdown("---")
        st.subheader("Height Comparison: BST vs AVL")
        scenarios = {
            "Original order": ORDER_IDS,
            "Sorted (worst case)": sorted(ORDER_IDS),
            "Reverse sorted": sorted(ORDER_IDS, reverse=True),
        }
        heights_bst = {}
        for name, ks in scenarios.items():
            heights_bst[name] = height(build_bst(ks))
        avl_height = math.ceil(math.log2(len(ORDER_IDS)+1))

        fig_comp = go.Figure()
        fig_comp.add_bar(x=list(heights_bst.keys()), y=list(heights_bst.values()),
                         name="BST Height", marker_color='#2E75B6')
        fig_comp.add_bar(x=list(heights_bst.keys()), y=[avl_height]*3,
                         name="AVL Height (guaranteed)", marker_color='#00b050')
        fig_comp.update_layout(barmode='group', title="BST vs AVL Height by Insertion Order",
                                height=300, yaxis_title="Tree Height")
        st.plotly_chart(fig_comp, use_container_width=True)

        st.info("💡 **AVL trees guarantee O(log n) height.** Sorted input makes a plain BST degrade to O(n) (a linked list), which is unacceptable for WaselX's 15,000 orders/day scale.")

    with tab3:
        st.subheader("🔍 Search & Deletion Demo")
        
        c_left, c_right = st.columns(2)
        with c_left:
            target = st.number_input("Search for Order ID", min_value=1000, max_value=9999,
                                      value=1067, step=1)
        with c_right:
            delete_target = st.selectbox("Or Delete Node", [1005, 1012, 1023, 1056, 1078, 1045], index=4)
            del_btn = st.button("🗑️ Delete Node", type="primary")

        root_search = build_bst(ORDER_IDS)
        
        if del_btn:
            st.markdown(f"**Deleting {delete_target}**")
            # Determine deletion case for explanation
            node_to_del = root_search
            while node_to_del and node_to_del.k != delete_target:
                if delete_target < node_to_del.k: node_to_del = node_to_del.l
                else: node_to_del = node_to_del.r
                
            if node_to_del:
                if not node_to_del.l and not node_to_del.r:
                    case = "Leaf node (No children) — simply remove."
                elif node_to_del.l and node_to_del.r:
                    case = "Two children — replace with inorder successor (smallest in right subtree)."
                else:
                    case = "One child — bypass the node."
                st.info(f"**Deletion Case:** {case}")
                
            def delete_node(root, key):
                if not root: return root
                if key < root.k: root.l = delete_node(root.l, key)
                elif key > root.k: root.r = delete_node(root.r, key)
                else:
                    if not root.l: return root.r
                    elif not root.r: return root.l
                    temp = root.r
                    while temp.l: temp = temp.l
                    root.k = temp.k
                    root.r = delete_node(root.r, temp.k)
                return root
            
            root_search = delete_node(root_search, delete_target)
            pos_after = tree_positions(root_search)
            st.plotly_chart(plot_tree(pos_after, title=f"BST after deleting {delete_target}"), use_container_width=True)
            st.success(f"Successfully deleted {delete_target}. Tree structure maintained.")

        else:
            path_search = []
            node = root_search
            found = False
            while node:
                path_search.append(node.k)
                if node.k == target: found = True; break
                elif target < node.k: node = node.l
                else: node = node.r

            pos_search = tree_positions(root_search)
            for k in path_search:
                st.plotly_chart(plot_tree(pos_search, highlight=k,
                    title=f"Searching for {target} — Current: {k} ({'Found! ✅' if k==target else 'Go ' + ('left' if target<k else 'right') + ' ➡'})"),
                    use_container_width=True)
                if k == target: break

            if found:
                st.success(f"✅ Order {target} found! Path: {' → '.join(map(str,path_search))} | Comparisons: {len(path_search)}")
            else:
                st.error(f"❌ Order {target} not in BST. Comparisons made: {len(path_search)}")


# ═══════════════════════════════════════════════════════════════════════════
# PRIORITY QUEUE
# ═══════════════════════════════════════════════════════════════════════════
elif section == "📋 Priority Queue":
    st.title("📋 Priority Queue — From-Scratch Min-Heap Dispatch Simulator")
    st.markdown("Simulate WaselX's order dispatch system using a **from-scratch min-heap** (no `heapq`). VIP orders always go first!")

    PRIORITY_NAMES = {1:"🚨 VIP Same-Hour", 2:"⚡ Express (2hr)", 3:"📦 Standard", 4:"🗓 Scheduled", 5:"🐢 Economy"}
    PRIORITY_COLORS = {1:"#cc0000", 2:"#ff6b00", 3:"#2E75B6", 4:"#375623", 5:"#888"}

    tab1, tab2 = st.tabs(["📥 Add Orders","📊 Heap Visualization"])

    if "pq_mh" not in st.session_state:
        st.session_state.pq_mh = MinHeap()
        st.session_state.pq_log = []

    mh = st.session_state.pq_mh

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            order_name = st.text_input("Order ID", f"ORD-{random.randint(100,999)}")
        with col2:
            priority = st.selectbox("Priority", [1,2,3,4,5],
                format_func=lambda x: PRIORITY_NAMES[x])
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Enqueue", type="primary"):
                mh.push(priority, order_name)
                st.session_state.pq_log.append(f"➕ Enqueued: {order_name} [{PRIORITY_NAMES[priority]}]")

        col4, col5 = st.columns(2)
        with col4:
            if st.button("⬇️ Dequeue Next", disabled=not mh):
                p, _, name = mh.pop()
                st.session_state.pq_log.append(f"🚀 Dispatched: {name} [{PRIORITY_NAMES[p]}]")
                st.success(f"Dispatched: **{name}** — {PRIORITY_NAMES[p]}")
        with col5:
            if st.button("🔄 Load Sample Batch"):
                st.session_state.pq_mh = MinHeap()
                mh = st.session_state.pq_mh
                sample = [("A",3),("B",1),("C",4),("D",2),("E",1),("F",5),("G",2),("H",3),("I",1),("J",4)]
                for name, p in sample:
                    mh.push(p, f"Order-{name}")
                st.session_state.pq_log.append("📥 Loaded 10-order sample batch (from-scratch MinHeap)")

        if mh:
            st.markdown("**Current Queue (sorted by priority):**")
            sorted_view = mh.sorted_view()
            for i, (p, cnt, name) in enumerate(sorted_view):
                color = PRIORITY_COLORS[p]
                st.markdown(f"<div style='background:{color}18;border-left:4px solid {color};"
                            f"border-radius:4px;padding:6px 12px;margin:3px 0'>"
                            f"<b>#{i+1}</b> {name} — {PRIORITY_NAMES[p]}</div>",
                            unsafe_allow_html=True)
        else:
            st.info("Queue is empty. Add orders or load sample batch.")

        if st.session_state.pq_log:
            st.markdown("**Dispatch Log:**")
            for log in reversed(st.session_state.pq_log[-8:]):
                st.markdown(f'<div class="step-box">{log}</div>', unsafe_allow_html=True)

        if st.button("🗑 Clear All"):
            st.session_state.pq_mh = MinHeap()
            st.session_state.pq_log = []

    with tab2:
        st.subheader("Min-Heap Tree Visualization (from-scratch)")
        if mh:
            heap_arr = mh.as_list()
            n = len(heap_arr)
            fig_heap = go.Figure()
            positions = {}
            for i in range(n):
                level = int(math.log2(i+1))
                pos_in_level = i - (2**level - 1)
                total_in_level = 2**level
                x = (pos_in_level + 0.5) / total_in_level
                y = -level
                positions[i] = (x, y)
                if i > 0:
                    parent = (i-1)//2
                    px2, py2 = positions[parent]
                    fig_heap.add_trace(go.Scatter(x=[px2,x],y=[py2,y],
                        mode='lines', line=dict(color='#aaa',width=2),
                        showlegend=False, hoverinfo='skip'))

            for i, (p,cnt,name) in enumerate(heap_arr):
                x, y = positions[i]
                color = PRIORITY_COLORS[p]
                fig_heap.add_trace(go.Scatter(x=[x],y=[y],
                    mode='markers+text',
                    marker=dict(size=40,color=color,line=dict(width=2,color='white')),
                    text=[f"P{p}"],
                    textfont=dict(size=11,color='white'),
                    textposition='middle center',
                    hovertext=f"{name}<br>{PRIORITY_NAMES[p]}",
                    hoverinfo='text', showlegend=False))
                fig_heap.add_trace(go.Scatter(x=[x],y=[y-0.18],
                    mode='text', text=[name[:8]],
                    textfont=dict(size=8,color='#333'),
                    showlegend=False, hoverinfo='skip'))

            fig_heap.update_layout(height=max(300, 100*int(math.log2(n+1)+1)),
                xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.05,1.05]),
                yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
                plot_bgcolor='#f8faff', paper_bgcolor='white',
                title="From-Scratch Min-Heap (root = next to dispatch)",
                margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig_heap, use_container_width=True)
            st.caption("✅ This heap uses our **from-scratch MinHeap** class with manual sift_up/sift_down — O(log n) per operation.")
        else:
            st.info("Add orders to see the heap visualization.")

    with st.expander("📚 Min-Heap Implementation Details"):
        st.markdown("""
        **From-Scratch Min-Heap** (no `heapq` library)
        
        | Operation | Complexity | Method |
        |-----------|-----------|--------|
        | Enqueue (push) | O(log n) | Append + sift_up |
        | Dequeue (pop) | O(log n) | Swap root with last + sift_down |
        | Peek | O(1) | Read index 0 |
        | For WaselX (3,500 orders) | log₂(3500) = 12 ops | Sub-millisecond |
        """)
        st.code("""
class MinHeap:
    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i] < self._heap[parent]:
                self._heap[i], self._heap[parent] = (
                    self._heap[parent], self._heap[i])
                i = parent
            else: break

    def _sift_down(self, i):
        n = len(self._heap)
        while True:
            smallest = i
            left, right = 2*i+1, 2*i+2
            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest != i:
                self._heap[i], self._heap[smallest] = (
                    self._heap[smallest], self._heap[i])
                i = smallest
            else: break
        """, language="python")


# ═══════════════════════════════════════════════════════════════════════════
# LINKED LIST
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🔗 Linked List Simulator":
    st.title("🔗 Doubly Linked List — Rider Route Simulator")
    st.markdown("This uses our **from-scratch `DoublyLinkedList` class** to manage rider routes with O(1) insertions.")

    if "dll_obj" not in st.session_state:
        st.session_state.dll_obj = DoublyLinkedList()
        initial_route = [
            ("Dubai Marina Hub", "ORD001", "10:15"),
            ("JLT", "ORD002", "10:30"),
            ("Downtown Dubai", "ORD003", "10:50"),
            ("Business Bay", "ORD004", "11:05"),
            ("Deira", "ORD005", "11:25"),
            ("Silicon Oasis", "ORD006", "11:50"),
        ]
        for stop, oid, eta in initial_route:
            st.session_state.dll_obj.append(stop, oid, eta)
        st.session_state.dll_log = ["Initial route loaded into DoublyLinkedList."]

    dll = st.session_state.dll_obj

    def draw_dll(dll_obj):
        nodes = dll_obj.display_forward()
        if not nodes: return go.Figure()
        fig = go.Figure()
        n = len(nodes)
        for i, (stop, oid, eta) in enumerate(nodes):
            x = i * 2
            color = '#2E75B6' if 'Urgent' not in stop else '#cc0000'
            fig.add_trace(go.Scatter(x=[x],y=[0],
                mode='markers+text',
                marker=dict(size=50,color=color,line=dict(width=2,color='white')),
                text=[oid],textfont=dict(size=8,color='white'),
                textposition='middle center',
                hovertext=f"{stop}<br>{oid}<br>ETA: {eta}",
                hoverinfo='text',showlegend=False))
            fig.add_trace(go.Scatter(x=[x],y=[-0.22],mode='text',
                text=[f"{stop[:12]}...{eta}" if len(stop)>12 else f"{stop}\n{eta}"],
                textfont=dict(size=8,color='#333'),
                showlegend=False,hoverinfo='skip'))
            if i < n-1:
                fig.add_trace(go.Scatter(x=[x+0.3,x+1.7],y=[0,0],
                    mode='lines+text',
                    line=dict(color='#2E75B6',width=2),
                    text=["","⇄"],textposition='middle center',
                    textfont=dict(size=14,color='#2E75B6'),
                    showlegend=False,hoverinfo='skip'))
        fig.update_layout(height=200,
            xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.5,n*2-0.5]),
            yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.6,0.4]),
            plot_bgcolor='#f8faff',paper_bgcolor='white',
            margin=dict(l=10,r=10,t=10,b=10))
        return fig

    st.plotly_chart(draw_dll(dll), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**➕ Insert Urgent Order**")
        nodes_list = dll.display_forward()
        if nodes_list:
            after_target = st.selectbox("Insert after order:", [oid for _, oid, _ in nodes_list])
            new_stop = st.text_input("Stop name", "Al Quoz (Urgent)")
            new_oid  = st.text_input("Order ID", f"ORD-URG-{random.randint(10,99)}")
            new_eta  = st.text_input("ETA", "11:00")
            if st.button("➕ Insert", type="primary"):
                dll.insert_after(after_target, new_stop, new_oid, new_eta)
                st.session_state.dll_log.append(f"Inserted {new_oid} after {after_target} in O(1)")
                st.rerun()

    with col2:
        st.markdown("**🗑 Cancel Order**")
        nodes_list = dll.display_forward()
        if nodes_list:
            cancel_target = st.selectbox("Cancel order:", [oid for _, oid, _ in nodes_list])
            if st.button("🗑 Remove"):
                removed_node = dll.delete_by_order_id(cancel_target)
                if removed_node:
                    st.session_state.dll_log.append(f"Removed {cancel_target} ({removed_node.stop_name}) in O(1)")
                    st.rerun()

    with col3:
        st.markdown("**📋 Route Operations**")
        if st.button("↩ Reset to Default"):
            del st.session_state["dll_obj"]
            st.rerun()
        if st.button("⬆ Move first stop to end"):
            if len(dll) > 1:
                first_oid = dll.head.order_id
                dll.move_first_to_end()
                st.session_state.dll_log.append(f"Moved {first_oid} to end of route in O(1)")
                st.rerun()
        if st.button("⏪ Display Reverse (Audit)"):
            rev = dll.display_reverse()
            st.session_state.dll_log.append(f"Reverse audit: {' -> '.join(oid for _, oid, _ in rev)}")

    st.markdown("**Operation Log:**")
    for log in reversed(st.session_state.dll_log[-5:]):
        st.markdown(f'<div class="step-box">{log}</div>', unsafe_allow_html=True)

    with st.expander("📚 Why Doubly Linked List?"):
        st.markdown("""
        **Doubly Linked List** (Implemented from scratch)
        
        | Operation | Array | Doubly Linked List |
        |-----------|-------|-------------------|
        | Insert mid-route | O(n) — shift all elements | **O(1)** — relink pointers |
        | Delete any stop | O(n) — shift all elements | **O(1)** — relink pointers |
        | Traverse forward | O(n) | O(n) |
        | Traverse backward | O(n) | **O(n) via prev pointers** |
        
        For delivery routes where urgent insertions and cancellations happen frequently, 
        the DLL's O(1) insert/delete far outweighs the O(1) random access of arrays.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# CIRCULAR LINKED LIST
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🔄 Circular Linked List":
    st.title("🔄 Circular Linked List — Round-Robin Rider Assignment")
    st.markdown("Using our **from-scratch `CircularLinkedList`** to fairly distribute orders to riders.")

    if "cll" not in st.session_state:
        st.session_state.cll = CircularLinkedList()
        for i in range(1, 9):
            st.session_state.cll.add_rider(f"Rider {i}")
        st.session_state.cll_log = []
        st.session_state.cll_order_cnt = 1

    cll = st.session_state.cll

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Assign Incoming Orders")
        if st.button("📦 Assign Next Order", type="primary"):
            rider = cll.assign_next_order()
            if rider:
                oid = f"Order {st.session_state.cll_order_cnt}"
                st.session_state.cll_order_cnt += 1
                st.session_state.cll_log.append(f"Assigned {oid} ➔ **{rider}**")
            else:
                st.error("No riders available!")
        
        if st.button("📦 Assign 5 Orders"):
            for _ in range(5):
                rider = cll.assign_next_order()
                if rider:
                    oid = f"Order {st.session_state.cll_order_cnt}"
                    st.session_state.cll_order_cnt += 1
                    st.session_state.cll_log.append(f"Assigned {oid} ➔ **{rider}**")

        st.markdown("**Assignment Log:**")
        for log in reversed(st.session_state.cll_log[-10:]):
            st.markdown(f'<div class="step-box">{log}</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("Manage Riders")
        roster = cll.display_roster()
        st.markdown("**Current Roster (Order of assignment):**")
        for r in roster:
            is_next = cll._current and cll._current.rider_name == r
            if is_next:
                st.markdown(f"🟢 **{r}** (Next)")
            else:
                st.markdown(f"⚪ {r}")
                
        if roster:
            to_remove = st.selectbox("Rider going on break:", roster)
            if st.button("⏸️ Remove Rider"):
                cll.remove_rider(to_remove)
                st.session_state.cll_log.append(f"⏸️ **{to_remove}** went on break (removed from ring)")
                st.rerun()

        if st.button("↩ Reset Demo (8 Riders)"):
            del st.session_state["cll"]
            st.rerun()

    with st.expander("📚 Circular Linked List Details"):
        st.markdown("""
        **Circular Linked List**
        
        - The `tail` node's `next` pointer points back to the `head`
        - Enables infinite traversal without index bounds checking
        - `assign_next_order()` simply reads the current rider and moves the pointer: `current = current.next`
        - Perfect data structure for fair, round-robin resource allocation.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# STACK LIFECYCLE
# ═══════════════════════════════════════════════════════════════════════════
elif section == "📦 Order Lifecycle Stack":
    st.title("📦 Stack — Order Lifecycle Tracking")
    st.markdown("Track an order's lifecycle using a LIFO (Last-In-First-Out) Stack. Allows instant 'Undo' of the last status change.")

    if "stack_obj" not in st.session_state:
        st.session_state.stack_obj = Stack()
        st.session_state.stack_obj.push("Received")

    stack = st.session_state.stack_obj

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Update Status")
        
        current_state = stack.peek()
        st.metric("Current Status", current_state if current_state else "Empty")
        
        next_logical = {"Received": "Confirmed", "Confirmed": "Preparing", 
                        "Preparing": "Dispatched", "Dispatched": "In Transit", 
                        "In Transit": "Delivered", "Delivered": "Done"}
        
        suggested = next_logical.get(current_state, "")
        
        new_status = st.text_input("New Status", value=suggested if suggested != "Done" else "")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬆️ Push Status", type="primary") and new_status:
                stack.push(new_status)
                st.rerun()
        with c2:
            if st.button("⏪ Undo (Pop)", disabled=len(stack)<=1):
                removed = stack.pop()
                st.toast(f"Undid '{removed}'. Reverted to '{stack.peek()}'")
                st.rerun()
                
        if st.button("🗑 Reset Order"):
            st.session_state.stack_obj = Stack()
            st.session_state.stack_obj.push("Received")
            st.rerun()

    with col2:
        st.subheader("Stack Visualizer (LIFO)")
        items = stack.display() # Returns top-to-bottom
        
        for i, item in enumerate(items):
            if i == 0:
                # Top of stack
                st.markdown(f"""
                <div style='background:#2E75B6; color:white; padding:15px; margin:5px 0; border-radius:8px; text-align:center; font-weight:bold; border: 2px solid #1F4E79; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    {item} (TOP)
                </div>
                """, unsafe_allow_html=True)
            else:
                opacity = max(0.4, 1.0 - (i * 0.15))
                st.markdown(f"""
                <div style='background:rgba(46, 117, 182, {opacity}); color:white; padding:10px; margin:5px 10px; border-radius:6px; text-align:center;'>
                    {item}
                </div>
                """, unsafe_allow_html=True)

    with st.expander("📚 Stack Applications"):
        st.markdown("""
        **Stack (LIFO)**
        
        - **Push**: Add new status `O(1)`
        - **Pop**: Remove last status (Undo) `O(1)`
        - **Peek**: Check current status `O(1)`
        
        Used heavily in state machines, browser history, and undo features.
        """)


# ═══════════════════════════════════════════════════════════════════════════
# SORTING BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════
elif section == "📊 Sorting Benchmark":
    st.title("📊 Sorting Algorithm Benchmark")
    st.markdown("Compare Merge Sort vs Quick Sort performance at WaselX scale.")

    def merge_sort(arr):
        if len(arr) <= 1: return arr
        m = len(arr)//2
        l, r = merge_sort(arr[:m]), merge_sort(arr[m:])
        res = []; i = j = 0
        while i < len(l) and j < len(r):
            if l[i] <= r[j]: res.append(l[i]); i+=1
            else: res.append(r[j]); j+=1
        return res + l[i:] + r[j:]

    def quick_sort(arr):
        if len(arr) <= 1: return arr
        pivot = arr[len(arr)//2]
        left   = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right  = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

    tab1, tab2 = st.tabs(["⏱ Performance Chart","🎞 Step-by-Step Visualization"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            sizes = st.multiselect("Dataset sizes",
                [100,500,1000,5000,10000,50000],
                default=[100,500,1000,5000,10000])
            data_type = st.radio("Data distribution",
                ["Random","Sorted (60% pre-sorted)","Reverse sorted","Nearly sorted"])

        with col2:
            runs = st.slider("Runs per size (averaged)", 1, 5, 2)

        if st.button("▶ Run Benchmark", type="primary"):
            ms_times, qs_times = [], []
            progress = st.progress(0)
            total_steps = len(sizes) * runs * 2

            step = 0
            for sz in sizes:
                ms_t, qs_t = [], []
                for _ in range(runs):
                    if data_type == "Random":
                        data = [random.randint(1,100000) for _ in range(sz)]
                    elif data_type == "Sorted (60% pre-sorted)":
                        data = list(range(int(sz*0.6))) + [random.randint(0,sz) for _ in range(sz-int(sz*0.6))]
                    elif data_type == "Reverse sorted":
                        data = list(range(sz, 0, -1))
                    else:
                        data = list(range(sz)); random.shuffle(data[:sz//10])

                    t0 = time.perf_counter()
                    merge_sort(data[:])
                    ms_t.append(time.perf_counter()-t0)
                    step += 1; progress.progress(step/total_steps)

                    t0 = time.perf_counter()
                    import sys; sys.setrecursionlimit(max(10000, sz*2))
                    quick_sort(data[:])
                    qs_t.append(time.perf_counter()-t0)
                    step += 1; progress.progress(step/total_steps)

                ms_times.append(sum(ms_t)/len(ms_t)*1000)
                qs_times.append(sum(qs_t)/len(qs_t)*1000)

            fig = go.Figure()
            fig.add_scatter(x=sizes, y=ms_times, mode='lines+markers',
                name='Merge Sort', line=dict(color='#2E75B6', width=3),
                marker=dict(size=10))
            fig.add_scatter(x=sizes, y=qs_times, mode='lines+markers',
                name='Quick Sort', line=dict(color='#ff6b00', width=3),
                marker=dict(size=10))
            fig.update_layout(title="Merge Sort vs Quick Sort — Execution Time",
                xaxis_title="Dataset Size (n)", yaxis_title="Time (ms)",
                height=400, legend=dict(x=0.02, y=0.98))
            st.plotly_chart(fig, use_container_width=True)

            results = [{"Size":s,"Merge Sort (ms)":f"{ms:.3f}","Quick Sort (ms)":f"{qs:.3f}",
                        "Winner":"Merge Sort" if ms<qs else "Quick Sort"}
                       for s,ms,qs in zip(sizes,ms_times,qs_times)]
            st.table(results)

    with tab2:
        st.subheader("Visualize Sorting Steps (Q18 Dataset)")
        st.markdown("Sorting the specific 15-order subset as required by the assignment:")
        q18_dataset = "1056, 1078, 1023, 1089, 1045, 1012, 1067, 1034, 1098, 1005, 1028, 1082, 1015, 1062, 1073"
        arr_input = st.text_input("Enter numbers (comma-separated)", q18_dataset)
        try:
            arr = [int(x.strip()) for x in arr_input.split(",")]
        except:
            arr = [int(x.strip()) for x in q18_dataset.split(",")]

        sort_algo = st.radio("Algorithm", ["Merge Sort","Bubble Sort (visual)"], horizontal=True)

        def get_bubble_steps(arr):
            arr = arr[:]
            steps = [arr[:]]
            n = len(arr)
            for i in range(n):
                for j in range(n-i-1):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
                        steps.append(arr[:])
            return steps

        def get_merge_levels(arr):
            """Get the merge sort levels for visualization."""
            if len(arr) <= 1: return [[arr]]
            levels = [[arr[:]]]
            def split(a, depth=0):
                if len(a) <= 1: return
                m = len(a)//2
                if depth+1 >= len(levels): levels.append([])
                levels[depth+1].extend([a[:m], a[m:]])
                split(a[:m], depth+1)
                split(a[m:], depth+1)
            split(arr)
            return levels

        if sort_algo == "Bubble Sort (visual)":
            steps = get_bubble_steps(arr)
            step_idx = st.slider("Step", 0, len(steps)-1, 0)
            current = steps[step_idx]
            fig = go.Figure(go.Bar(x=list(range(len(current))), y=current,
                marker_color=['#ff6b00' if i==step_idx%len(current) or i==(step_idx+1)%len(current)
                              else '#2E75B6' for i in range(len(current))]))
            fig.update_layout(title=f"Bubble Sort — Step {step_idx}/{len(steps)-1}",
                height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"Array: {current}")
        else:
            levels = get_merge_levels(arr)
            st.markdown(f"**Merge Sort on:** `{arr}`")
            for i, level in enumerate(levels):
                st.markdown(f"**Level {i} — {len(level)} subarray(s):**")
                cols = st.columns(len(level))
                for col, sub in zip(cols, level):
                    with col:
                        fig = go.Figure(go.Bar(x=list(range(len(sub))), y=sub,
                            marker_color='#2E75B6'))
                        fig.update_layout(height=100, margin=dict(l=2,r=2,t=2,b=2),
                            showlegend=False,
                            xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
                        st.plotly_chart(fig, use_container_width=True)
                        st.caption(f"`{sub}`")


# ═══════════════════════════════════════════════════════════════════════════
# BINARY SEARCH
# ═══════════════════════════════════════════════════════════════════════════
elif section == "🔍 Binary Search Demo":
    st.title("🔍 Binary Search vs Linear Search")
    st.markdown("Watch how binary search eliminates half the search space each step — vs. linear search checking one by one. (Q19 Assignment Dataset: IDs 10001 to 11000)")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dataset:** `[10001, 10002, ..., 11000]` (1,000 orders)")
        arr_size = 1000
        start_id = 10001
        arr = list(range(start_id, start_id + arr_size))
    with col2:
        target = st.number_input("Search target (Q19 target: 10347)", min_value=10001, max_value=11000, value=10347)

    # Binary search steps
    bs_steps = []
    lo, hi = 0, len(arr)-1
    while lo <= hi:
        mid = (lo+hi)//2
        bs_steps.append((lo, mid, hi))
        if arr[mid] == target: break
        elif arr[mid] < target: lo = mid+1
        else: hi = mid-1
    found_bs = arr[bs_steps[-1][1]] == target if bs_steps else False

    # Linear search steps
    target_idx = target - start_id
    ls_comps = target_idx + 1 if 0 <= target_idx < arr_size else arr_size

    step_bs = st.slider("Binary Search Step", 0, len(bs_steps)-1, len(bs_steps)-1) if bs_steps else 0

    if bs_steps:
        lo_s, mid_s, hi_s = bs_steps[step_bs]
        colors_bs = []
        for i in range(arr_size):
            if i == mid_s: colors_bs.append('#ff6b00')
            elif lo_s <= i <= hi_s: colors_bs.append('#2E75B6')
            else: colors_bs.append('#dddddd')

        fig_bs = go.Figure()
        # Sub-sample for visual clarity (Plotly struggles with 1000 thin bars)
        sample_step = max(1, arr_size // 100)
        vis_indices = list(range(0, arr_size, sample_step))
        # Ensure mid_s is in vis_indices
        if mid_s not in vis_indices:
            vis_indices.append(mid_s)
            vis_indices.sort()
            
        vis_x = [arr[i] for i in vis_indices]
        vis_colors = [colors_bs[i] for i in vis_indices]
        
        fig_bs.add_bar(x=vis_x, y=[1]*len(vis_x),
            marker_color=vis_colors,
            hovertext=[f"Value: {v}" for v in vis_x], hoverinfo='text')
        fig_bs.add_vline(x=arr[mid_s], line_color='#ff6b00', line_width=3,
            annotation_text=f"mid={arr[mid_s]}", annotation_position="top")
        fig_bs.update_layout(title=f"Binary Search — Step {step_bs+1}/{len(bs_steps)} | Search space: [{arr[lo_s]}..{arr[hi_s]}] | Checking: {arr[mid_s]}",
            height=220, showlegend=False,
            xaxis_title="Order ID", yaxis=dict(showticklabels=False),
            margin=dict(l=10,r=10,t=50,b=30))
        st.plotly_chart(fig_bs, use_container_width=True)

    # Linear search
    colors_ls = ['#00b050' if i == target_idx else '#ff4444' if i < target_idx else '#dddddd' for i in vis_indices]
    fig_ls = go.Figure()
    fig_ls.add_bar(x=vis_x, y=[1]*len(vis_x), marker_color=colors_ls)
    fig_ls.update_layout(title=f"Linear Search — Checks every element from left | Comparisons: {ls_comps}",
        height=180, showlegend=False,
        xaxis_title="Order ID", yaxis=dict(showticklabels=False),
        margin=dict(l=10,r=10,t=50,b=30))
    st.plotly_chart(fig_ls, use_container_width=True)

    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Binary Search Comparisons", len(bs_steps))
    col2.metric("Linear Search Comparisons", ls_comps)
    col3.metric("Binary Search Faster by", f"{ls_comps - len(bs_steps)}x fewer" if len(bs_steps) > 0 else "N/A")

    # Scale simulation
    st.markdown("---")
    st.subheader("📈 At WaselX Scale — 500 calls/day")
    sizes_demo = [100, 500, 1000, 3500, 10000, 50000]
    bs_comps = [math.ceil(math.log2(n)) for n in sizes_demo]
    ls_comps_demo = [n//2 for n in sizes_demo]  # average case

    fig_scale = go.Figure()
    fig_scale.add_scatter(x=sizes_demo, y=bs_comps, mode='lines+markers',
        name='Binary Search O(log n)', line=dict(color='#00b050', width=3),
        marker=dict(size=10))
    fig_scale.add_scatter(x=sizes_demo, y=ls_comps_demo, mode='lines+markers',
        name='Linear Search O(n)', line=dict(color='#cc0000', width=3),
        marker=dict(size=10))
    fig_scale.update_layout(title="Comparisons vs Array Size — Exponential Divergence",
        xaxis_title="Orders in Database", yaxis_title="Avg Comparisons per Lookup",
        height=350)
    st.plotly_chart(fig_scale, use_container_width=True)

    st.markdown("""
    | Array Size | Binary Search | Linear Search | Daily Saving (500 calls) |
    |------------|--------------|--------------|--------------------------|
    | 100 | 7 | 50 | 21,500 comparisons/day |
    | 3,500 (current) | 12 | 1,750 | 869,000 comparisons/day |
    | 15,000 (scaled) | 14 | 7,500 | 3,743,000 comparisons/day |
    """)

# ═══════════════════════════════════════════════════════════════════════════
# PEAK HOUR D&C
# ═══════════════════════════════════════════════════════════════════════════
elif section == "⏰ Peak Hour Finder":
    st.title("⏰ Peak Hour Finder — Divide & Conquer")
    st.markdown("Analyze 6,000 order timestamps to find the peak activity hour during Ramadan, using a Divide & Conquer approach (Q20 requirement).")

    # Generate synthetic Ramadan data (peak around sunset/Iftar ~18:00)
    @st.cache_data
    def generate_ramadan_data():
        hours = list(range(24))
        # Base volume
        counts = [random.randint(50, 150) for _ in range(24)]
        # Iftar peak
        counts[17] = random.randint(300, 400)
        counts[18] = random.randint(600, 800)
        counts[19] = random.randint(400, 500)
        # Suhoor peak
        counts[3] = random.randint(200, 300)
        counts[4] = random.randint(250, 350)
        
        # Adjust total to exactly 6000
        current_total = sum(counts)
        ratio = 6000 / current_total
        counts = [int(c * ratio) for c in counts]
        diff = 6000 - sum(counts)
        counts[18] += diff
        
        return counts

    hourly_counts = generate_ramadan_data()

    def find_peak_dc(arr, low, high):
        """Divide & Conquer to find a peak (element >= neighbors)."""
        if low == high:
            return low, arr[low]
            
        mid = (low + high) // 2
        
        if (mid == 0 or arr[mid] >= arr[mid-1]) and (mid == len(arr)-1 or arr[mid] >= arr[mid+1]):
            return mid, arr[mid]
            
        if mid > 0 and arr[mid-1] > arr[mid]:
            return find_peak_dc(arr, low, mid - 1)
        else:
            return find_peak_dc(arr, mid + 1, high)

    def find_peak_linear(arr):
        max_val = max(arr)
        max_idx = arr.index(max_val)
        return max_idx, max_val

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Results")
        if st.button("🔍 Find Peak Hour", type="primary"):
            t0 = time.perf_counter()
            dc_idx, dc_val = find_peak_dc(hourly_counts, 0, len(hourly_counts)-1)
            dc_time = time.perf_counter() - t0
            
            t0 = time.perf_counter()
            lin_idx, lin_val = find_peak_linear(hourly_counts)
            lin_time = time.perf_counter() - t0
            
            st.success(f"**Divide & Conquer Found:** Hour {dc_idx}:00 with {dc_val} orders")
            st.info(f"**Linear Search Found:** Hour {lin_idx}:00 with {lin_val} orders")
            
            c1, c2 = st.columns(2)
            c1.metric("D&C Time", f"{dc_time*1000000:.1f} µs")
            c2.metric("Linear Time", f"{lin_time*1000000:.1f} µs")
            
            if dc_val != lin_val:
                st.warning("⚠️ Note: D&C finds *a* local peak, while Linear scan finds the *global* peak. On this bimodal (Iftar/Suhoor) distribution, D&C might lock onto the Suhoor peak if it searches that half first!")

    with col2:
        st.subheader("Order Distribution (6,000 orders)")
        fig = go.Figure()
        colors = ['#2E75B6' if c < 400 else '#ff6b00' for c in hourly_counts]
        fig.add_trace(go.Bar(
            x=[f"{h:02d}:00" for h in range(24)],
            y=hourly_counts,
            marker_color=colors,
            text=hourly_counts,
            textposition='auto'
        ))
        fig.update_layout(
            title="Ramadan Order Volume by Hour",
            xaxis_title="Time of Day",
            yaxis_title="Orders",
            height=300,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📚 D&C vs Linear Search for Peak Finding"):
        st.markdown("""
        | Metric | Divide & Conquer | Linear Scan |
        |--------|-----------------|-------------|
        | Time Complexity | **O(log n)** | O(n) |
        | Space Complexity | O(log n) (call stack) | **O(1)** |
        | Guaranteed Global Max? | ❌ No, finds local peak | ✅ Yes |
        
        **Conclusion for WaselX:** Since there are only 24 hours in a day, `n=24` is extremely small. The overhead of recursion makes D&C effectively slower or equal to a simple O(n) linear scan, and D&C might return the local Suhoor peak instead of the true Iftar peak. **Linear scan is recommended here.**
        """)
