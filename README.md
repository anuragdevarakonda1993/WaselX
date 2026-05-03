# 🚚 WaselX Express — DSA Visualizer

**MAIB Final Project** | Interactive Data Structures & Algorithms

## Deploy to Streamlit Cloud

1. Push **all three files** to the **root** of your GitHub repo:
   ```
   final.py
   requirements.txt
   README.md
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Set **Main file path** to `final.py`
4. Click **Deploy** — Streamlit will auto-install packages from `requirements.txt`

## Run Locally

```bash
pip install -r requirements.txt
streamlit run final.py
```

## Features
- 🗺️ Network Explorer (UAE delivery graph)
- 🔵 Dijkstra's Pathfinder (animated)
- 🌊 BFS / DFS Traversal
- 🌲 Kruskal's MST
- 🌳 BST & AVL Tree
- 📋 Priority Queue Simulator
- 🔗 Linked List Simulator
- 📊 Sorting Benchmark
- 🔍 Binary Search Demo

## Dependencies
| Package | Version |
|---------|---------|
| streamlit | ≥ 1.32.0 |
| plotly | ≥ 5.18.0 |
| networkx | ≥ 3.2.0 |
