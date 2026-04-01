"""Generate the Transit System Simulator PDF report — 8 pages."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Preformatted,
)

# ── Colors — warm, professional, not "AI blue" ──────────────────────
CHARCOAL = HexColor("#2D2D2D")
DARK     = HexColor("#3C3C3C")
WINE     = HexColor("#6B2D5B")
TAUPE    = HexColor("#8C7A6B")
SAND     = HexColor("#F5F0EB")
WHITE    = HexColor("#FFFFFF")
MUTED    = HexColor("#555555")
BORDER   = HexColor("#C4B8AC")

W = 6.5 * inch  # usable width


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "T", parent=base["Title"], fontSize=26, leading=32,
            textColor=CHARCOAL, alignment=TA_CENTER, spaceAfter=4,
        ),
        "sub": ParagraphStyle(
            "Sub", parent=base["Normal"], fontSize=12, leading=16,
            textColor=TAUPE, alignment=TA_CENTER, spaceAfter=4,
        ),
        "author": ParagraphStyle(
            "Au", parent=base["Normal"], fontSize=11, leading=15,
            textColor=MUTED, alignment=TA_CENTER, spaceBefore=14, spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontSize=16, leading=20,
            textColor=CHARCOAL, spaceBefore=14, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontSize=12, leading=15,
            textColor=WINE, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "B", parent=base["Normal"], fontSize=10, leading=14,
            textColor=DARK, spaceAfter=5, alignment=TA_JUSTIFY,
        ),
        "code": ParagraphStyle(
            "C", parent=base["Code"], fontSize=7.5, leading=10,
            textColor=CHARCOAL, backColor=SAND, borderWidth=0.4,
            borderColor=BORDER, borderPadding=5, spaceBefore=3, spaceAfter=6,
            fontName="Courier",
        ),
        "caption": ParagraphStyle(
            "Cap", parent=base["Normal"], fontSize=8.5, leading=11,
            textColor=TAUPE, alignment=TA_CENTER, spaceBefore=2, spaceAfter=8,
            fontName="Helvetica-Oblique",
        ),
    }


def tbl(headers, rows, widths=None):
    """Styled table with warm tones."""
    data = [headers] + rows
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), CHARCOAL),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING",    (0, 0), (-1, 0), 6),
        ("TEXTCOLOR",     (0, 1), (-1, -1), DARK),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8.5),
        ("TOPPADDING",    (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SAND]),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def hr():
    t = Table([[""]], colWidths=[W])
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, TAUPE),
        ("TOPPADDING", (0, 0), (-1, 0), 0),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
    ]))
    return t


def build():
    doc = SimpleDocTemplate(
        "Transit_System_Report.pdf", pagesize=letter,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        leftMargin=1 * inch, rightMargin=1 * inch,
    )
    s = styles()
    story = []

    # ────────────────────────────────────────────────────────────────
    # PAGE 1 — Title
    # ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("Transit System Simulator", s["title"]))
    story.append(hr())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Algorithm Design and Analysis — Final Project", s["sub"],
    ))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("Rohan Sainju", s["author"]))
    story.append(Paragraph("COSC 320.001 — Algorithm Design and Analysis — Spring 2026", s["author"]))
    story.append(Paragraph("March 31, 2026", s["author"]))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph(
        '<link href="https://github.com/rosaiju/transit-system-simulator" '
        'color="#B5451B"><u>'
        'github.com/rosaiju/transit-system-simulator</u></link>',
        s["sub"],
    ))
    story.append(PageBreak())

    # ────────────────────────────────────────────────────────────────
    # PAGE 2 — TOC + Introduction + System Design
    # ────────────────────────────────────────────────────────────────
    story.append(Paragraph("Table of Contents", s["h1"]))
    story.append(hr())
    story.append(Spacer(1, 6))
    toc = [
        ("1.", "System Design & Architecture"),
        ("2.", "Data Structures Used"),
        ("3.", "Graph Operations"),
        ("4.", "Route Finding — DFS & BFS"),
        ("5.", "Shortest Path — Dijkstra's Algorithm"),
        ("6.", "Passenger Simulation & Undo System"),
        ("7.", "Sorting & Searching"),
        ("8.", "Big-O Analysis"),
        ("9.", "Sample Output"),
        ("10.", "Conclusion"),
    ]
    toc_data = [[n, t] for n, t in toc]
    toc_t = Table(toc_data, colWidths=[0.4 * inch, 5 * inch])
    toc_t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("FONTSIZE",  (0, 0), (-1, -1), 10),
        ("FONTNAME",  (0, 0), (0, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, BORDER),
    ]))
    story.append(toc_t)
    story.append(Spacer(1, 14))

    story.append(Paragraph("1. System Design &amp; Architecture", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "The simulator models a city transit network as a weighted undirected "
        "graph. It is built with 10 Python modules, each responsible for one "
        "feature domain:",
        s["body"],
    ))
    story.append(tbl(
        ["File", "Responsibility"],
        [
            ["main.py",          "CLI menu and entry point"],
            ["station.py",       "Station class (ID, name, capacity, queue)"],
            ["graph.py",         "Adjacency list graph — add/remove/display"],
            ["traversal.py",     "DFS (recursive) and BFS (queue-based)"],
            ["shortest_path.py", "Dijkstra's algorithm with path reconstruction"],
            ["passenger.py",     "Queue-based passenger boarding"],
            ["undo_stack.py",    "Stack-based undo history"],
            ["sorting.py",       "Merge Sort and Insertion Sort comparison"],
            ["searching.py",     "Binary Search and Linear Search comparison"],
            ["demo_data.py",     "Sample network (12 stations, 15 connections)"],
        ],
        widths=[1.4 * inch, 5.1 * inch],
    ))
    story.append(Paragraph("Table 1 — Module overview.", s["caption"]))

    story.append(Paragraph("Network Topology", s["h2"]))
    net = (
        "  Station-1 --3-- Station-2 --4-- Station-3\n"
        "      |               |               |\n"
        "      2               5               3\n"
        "      |               |               |\n"
        "  Station-4 --6-- Station-5 --2-- Station-6\n"
        "      |               |               |\n"
        "      4               7               5\n"
        "      |               |               |\n"
        "  Station-7 --3-- Station-8 --4-- Station-9\n"
        "                      |\n"
        "                      6\n"
        "                      |\n"
        "                  Station-10 -3- Station-11 -2- Station-12"
    )
    story.append(Preformatted(net, s["code"]))
    story.append(Paragraph(
        "Figure 1 — 12-station demo network with travel times (minutes).",
        s["caption"],
    ))

    story.append(Paragraph("2. Data Structures Used", s["h1"]))
    story.append(hr())
    story.append(tbl(
        ["Structure", "Usage", "Why"],
        [
            ["Class", "Station",
             "Encapsulates ID, name, capacity, passenger queue."],
            ["Dict (Hash Map)", "Adjacency list / station lookup",
             "O(1) average lookup by station ID."],
            ["List", "Neighbor edges, sorted results",
             "Ordered, indexed access for adjacency entries."],
            ["Deque (Queue)", "BFS frontier, passenger queues",
             "O(1) enqueue/dequeue for FIFO processing."],
            ["Heap (Priority Queue)", "Dijkstra's algorithm",
             "O(log n) extraction of minimum-distance node."],
            ["Stack (List)", "Undo action history",
             "O(1) push/pop for LIFO reversal of actions."],
        ],
        widths=[1.3 * inch, 1.7 * inch, 3.5 * inch],
    ))
    story.append(Paragraph("Table 2 — Data structures and roles.", s["caption"]))

    story.append(Paragraph("Station Class", s["h2"]))
    story.append(Preformatted(
        "class Station:\n"
        "    def __init__(self, station_id, name, capacity):\n"
        "        self.station_id = station_id\n"
        "        self.name = name\n"
        "        self.capacity = capacity\n"
        "        self.passenger_queue = deque()",
        s["code"],
    ))

    story.append(Paragraph("Adjacency List Graph", s["h2"]))
    story.append(Paragraph(
        "The <b>TransitGraph</b> stores two dictionaries: "
        "<font name='Courier' size='9'>stations</font> (ID to Station) and "
        "<font name='Courier' size='9'>adjacency_list</font> "
        "(ID to list of (neighbor_id, weight) tuples). "
        "Space complexity: <b>O(V + E)</b>.",
        s["body"],
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Graph Operations", s["h1"]))
    story.append(hr())
    story.append(tbl(
        ["Operation", "Description", "Time"],
        [
            ["Add Station",      "Insert station into both dicts. Reject duplicates.", "O(1)"],
            ["Remove Station",   "Delete station and all edges referencing it.",       "O(deg v)"],
            ["Add Connection",   "Add weighted undirected edge between two stations.", "O(deg v)"],
            ["Remove Connection","Remove edge from both neighbor lists.",              "O(deg v)"],
            ["Display Network",  "Print all stations with their connections.",         "O(V + E)"],
        ],
        widths=[1.3 * inch, 3.7 * inch, 1.0 * inch],
    ))
    story.append(Paragraph("Table 3 — Graph operations summary.", s["caption"]))
    story.append(PageBreak())

    # ────────────────────────────────────────────────────────────────
    # PAGE 4 — DFS & BFS
    # ────────────────────────────────────────────────────────────────
    story.append(Paragraph("4. Route Finding — DFS &amp; BFS", s["h1"]))
    story.append(hr())

    story.append(Paragraph("Depth-First Search (Recursive)", s["h2"]))
    story.append(Paragraph(
        "DFS explores as deep as possible before backtracking. The "
        "implementation uses <b>recursion</b> — the call stack handles "
        "backtracking automatically.",
        s["body"],
    ))
    story.append(Preformatted(
        "def dfs(graph, start_id, visited=None):\n"
        "    if visited is None:\n"
        "        visited = set()\n"
        "    visited.add(start_id)\n"
        "    result = [start_id]\n"
        "    for neighbor_id, _ in graph.get_neighbors(start_id):\n"
        "        if neighbor_id not in visited:\n"
        "            result.extend(dfs(graph, neighbor_id, visited))\n"
        "    return result",
        s["code"],
    ))

    story.append(Paragraph("Breadth-First Search (Queue-Based)", s["h2"]))
    story.append(Paragraph(
        "BFS explores all neighbors at the current depth before going deeper. "
        "Uses a <b>deque as a FIFO queue</b>.",
        s["body"],
    ))
    story.append(Preformatted(
        "def bfs(graph, start_id):\n"
        "    visited = set()\n"
        "    queue = deque([start_id])\n"
        "    visited.add(start_id)\n"
        "    result = []\n"
        "    while queue:\n"
        "        current_id = queue.popleft()\n"
        "        result.append(current_id)\n"
        "        for neighbor_id, _ in graph.get_neighbors(current_id):\n"
        "            if neighbor_id not in visited:\n"
        "                visited.add(neighbor_id)\n"
        "                queue.append(neighbor_id)\n"
        "    return result",
        s["code"],
    ))

    story.append(Paragraph("DFS vs BFS Comparison", s["h2"]))
    story.append(tbl(
        ["Property", "DFS", "BFS"],
        [
            ["Time",       "O(V + E)",          "O(V + E)"],
            ["Space",      "O(V) call stack",   "O(V) queue"],
            ["Structure",  "Recursion (stack)",  "Queue (deque)"],
            ["Order",      "Deep-first",         "Level-by-level"],
            ["Shortest?",  "No",                 "Yes (unweighted)"],
        ],
        widths=[1.2 * inch, 2.4 * inch, 2.4 * inch],
    ))
    story.append(Paragraph("Table 4 — DFS vs BFS.", s["caption"]))
    story.append(PageBreak())

    # ────────────────────────────────────────────────────────────────
    # PAGE 5 — Dijkstra + Passenger + Undo
    # ────────────────────────────────────────────────────────────────
    story.append(Paragraph("5. Shortest Path — Dijkstra's Algorithm", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Dijkstra's algorithm finds the shortest weighted path using a "
        "<b>min-heap</b> (priority queue). It maintains a distances dict "
        "(initialized to infinity) and a previous dict for path "
        "reconstruction. At each step, the closest unvisited station is "
        "extracted and its neighbors are relaxed.",
        s["body"],
    ))
    story.append(Preformatted(
        "def dijkstra(graph, start_id, end_id):\n"
        "    distances = {sid: float('inf') for sid in graph.stations}\n"
        "    distances[start_id] = 0\n"
        "    previous = {sid: None for sid in graph.stations}\n"
        "    heap = [(0, start_id)]\n"
        "    visited = set()\n"
        "    while heap:\n"
        "        dist, current = heapq.heappop(heap)\n"
        "        if current in visited: continue\n"
        "        visited.add(current)\n"
        "        if current == end_id: break\n"
        "        for neighbor, weight in graph.get_neighbors(current):\n"
        "            new_dist = dist + weight\n"
        "            if new_dist < distances[neighbor]:\n"
        "                distances[neighbor] = new_dist\n"
        "                previous[neighbor] = current\n"
        "                heapq.heappush(heap, (new_dist, neighbor))\n"
        "    # Reconstruct path via previous dict\n"
        "    return distances[end_id], reconstruct(previous, end_id)",
        s["code"],
    ))
    story.append(Paragraph(
        "<b>Time: O((V + E) log V)</b> due to heap operations. "
        "<b>Space: O(V)</b> for distances, previous, heap, and visited set.",
        s["body"],
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "6. Passenger Simulation &amp; Undo System", s["h1"],
    ))
    story.append(hr())

    story.append(Paragraph("Passenger Queue (FIFO)", s["h2"]))
    story.append(Paragraph(
        "Each station has a <font name='Courier' size='9'>deque</font> of "
        "passengers. New arrivals join the back "
        "(<font name='Courier' size='9'>append</font>); boarding removes from "
        "the front (<font name='Courier' size='9'>popleft</font>). "
        "Capacity is enforced — excess passengers are turned away.",
        s["body"],
    ))

    story.append(Paragraph("Undo Stack (LIFO)", s["h2"]))
    story.append(Paragraph(
        "Every user action is pushed onto a stack as a dict with the action "
        "type and data needed for reversal. Calling "
        "<font name='Courier' size='9'>undo()</font> pops the last action and "
        "executes its inverse. Supports unlimited undo depth.",
        s["body"],
    ))
    story.append(tbl(
        ["Action", "Undo Behavior"],
        [
            ["add_station",       "Remove the added station"],
            ["remove_station",    "Re-add station and restore its connections"],
            ["add_connection",    "Remove the added connection"],
            ["remove_connection", "Re-add with original weight"],
            ["add_passengers",    "Remove passengers from back of queue"],
            ["board_passengers",  "Return passengers to front of queue"],
        ],
        widths=[1.6 * inch, 4.9 * inch],
    ))
    story.append(Paragraph("Table 5 — Undo operations.", s["caption"]))
    story.append(PageBreak())

    # ────────────────────────────────────────────────────────────────
    # PAGE 6 — Sorting & Searching
    # ────────────────────────────────────────────────────────────────
    story.append(Paragraph("7. Sorting &amp; Searching", s["h1"]))
    story.append(hr())

    story.append(Paragraph("Merge Sort", s["h2"]))
    story.append(Paragraph(
        "Divide-and-conquer: recursively split the list in half, then merge "
        "sublists in sorted order. Guarantees <b>O(n log n)</b> time in all "
        "cases. Requires <b>O(n)</b> extra space. Returns a new sorted list.",
        s["body"],
    ))

    story.append(Paragraph("Insertion Sort", s["h2"]))
    story.append(Paragraph(
        "Builds the sorted list one element at a time by shifting elements "
        "right until the correct position is found. <b>O(n&sup2;)</b> worst "
        "case, <b>O(n)</b> best case (already sorted). <b>O(1)</b> extra "
        "space. Faster than Merge Sort for small datasets due to low overhead.",
        s["body"],
    ))

    story.append(tbl(
        ["Algorithm", "Best", "Average", "Worst", "Space"],
        [
            ["Merge Sort",     "O(n log n)", "O(n log n)", "O(n log n)", "O(n)"],
            ["Insertion Sort", "O(n)",       "O(n\u00b2)",     "O(n\u00b2)",     "O(1)"],
        ],
        widths=[1.3 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch, 0.9 * inch],
    ))
    story.append(Paragraph("Table 6 — Sorting complexity.", s["caption"]))

    story.append(Paragraph("Binary Search", s["h2"]))
    story.append(Paragraph(
        "Requires sorted input. Repeatedly halves the search interval by "
        "comparing the target to the middle element. "
        "<b>Time: O(log n). Space: O(1).</b>",
        s["body"],
    ))

    story.append(Paragraph("Linear Search", s["h2"]))
    story.append(Paragraph(
        "Scans every element sequentially. No sorted input needed. "
        "<b>Time: O(n). Space: O(1).</b> For repeated lookups on the same "
        "data, sorting once + Binary Search is more efficient.",
        s["body"],
    ))

    story.append(tbl(
        ["Algorithm", "Time", "Space", "Requires Sorted?"],
        [
            ["Binary Search", "O(log n)", "O(1)", "Yes"],
            ["Linear Search", "O(n)",     "O(1)", "No"],
        ],
        widths=[1.4 * inch, 1.2 * inch, 1.0 * inch, 2.4 * inch],
    ))
    story.append(Paragraph("Table 7 — Search comparison.", s["caption"]))
    story.append(PageBreak())

    # ────────────────────────────────────────────────────────────────
    # PAGE 7 — Big-O + Sample Output
    # ────────────────────────────────────────────────────────────────
    story.append(Paragraph("8. Big-O Analysis", s["h1"]))
    story.append(hr())
    story.append(tbl(
        ["Operation", "Time", "Space"],
        [
            ["DFS (recursive)",       "O(V + E)",         "O(V) call stack"],
            ["BFS (queue-based)",     "O(V + E)",         "O(V) queue"],
            ["Dijkstra's Algorithm",  "O((V+E) log V)",   "O(V)"],
            ["Merge Sort",            "O(n log n)",       "O(n)"],
            ["Insertion Sort",        "O(n\u00b2) / O(n) best","O(1)"],
            ["Binary Search",         "O(log n)",         "O(1)"],
            ["Linear Search",         "O(n)",             "O(1)"],
            ["Add / Remove Station",  "O(1) / O(deg v)",  "O(1)"],
            ["Add / Remove Edge",     "O(deg v)",         "O(1)"],
            ["Stack push / pop",      "O(1)",             "O(n) history"],
            ["Queue enq / deq",       "O(1)",             "O(n) passengers"],
        ],
        widths=[1.8 * inch, 1.8 * inch, 2.4 * inch],
    ))
    story.append(Paragraph("Table 8 — Complete Big-O summary.", s["caption"]))

    story.append(Paragraph(
        "The graph uses <b>O(V + E)</b> space overall. The undo stack grows "
        "O(A) where A is the number of user actions. DFS risks O(V) stack "
        "depth on long chains; BFS uses O(V) queue space on star graphs.",
        s["body"],
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("9. Sample Output", s["h1"]))
    story.append(hr())

    story.append(Paragraph("DFS vs BFS from Station-1", s["h2"]))
    story.append(Preformatted(
        "DFS: Station-1 -> 2 -> 3 -> 6 -> 5 -> 4 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12\n"
        "BFS: Station-1 -> 2 -> 4 -> 3 -> 5 -> 7 -> 6 -> 8 -> 9 -> 10 -> 11 -> 12\n"
        "Performance:  DFS = 0.0072 ms  |  BFS = 0.0097 ms",
        s["code"],
    ))

    story.append(Paragraph("Dijkstra: Station-1 to Station-12", s["h2"]))
    story.append(Preformatted(
        "Path: Station-1 --(2)--> 4 --(4)--> 7 --(3)--> 8 --(6)--> 10\n"
        "      --(3)--> 11 --(2)--> 12\n"
        "Total travel time: 20 minutes  |  Stops: 6",
        s["code"],
    ))

    story.append(Paragraph("Sorting Comparison (12 stations)", s["h2"]))
    story.append(Preformatted(
        "Merge Sort     O(n log n)   0.0124 ms\n"
        "Insertion Sort O(n^2)       0.0045 ms\n"
        "(Insertion Sort faster here due to small n — overhead dominates)",
        s["code"],
    ))

    story.append(Paragraph("Passenger Queue &amp; Undo", s["h2"]))
    story.append(Preformatted(
        "> Add 5 passengers to Station-8    -> Added 5 passengers.\n"
        "> Board 3 passengers               -> Boarded: P1, P2, P3\n"
        "> View queue                        -> [P4, P5, P6, P7, P8]\n"
        "> Undo last action                  -> Undid boarding 3 passengers",
        s["code"],
    ))
    story.append(PageBreak())

    # ────────────────────────────────────────────────────────────────
    # PAGE 8 — Conclusion
    # ────────────────────────────────────────────────────────────────
    story.append(Paragraph("10. Conclusion", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "This project demonstrates how fundamental data structures and "
        "algorithms power real-world transit systems. Key takeaways:",
        s["body"],
    ))

    points = [
        "<b>Graph representation matters.</b> The adjacency list is "
        "memory-efficient at O(V + E) and ideal for sparse transit networks.",

        "<b>Algorithm choice depends on the problem.</b> DFS and BFS share "
        "O(V + E) time complexity but serve different purposes — DFS for "
        "deep exploration, BFS for level-order and shortest unweighted paths.",

        "<b>Dijkstra extends BFS to weighted graphs</b> using a priority "
        "queue, achieving O((V + E) log V) time.",

        "<b>Sorting trade-offs are real.</b> Merge Sort guarantees "
        "O(n log n) but Insertion Sort is faster for small or nearly-sorted "
        "data due to lower overhead.",

        "<b>Stacks and queues are essential.</b> The passenger queue "
        "ensures fair FIFO boarding; the undo stack enables LIFO reversal "
        "of any action — both at O(1) per operation.",
    ]
    for p in points:
        story.append(Paragraph(f"\u2022  {p}", s["body"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "The modular design (10 files, each under 200 lines) makes the "
        "simulator extensible for future enhancements such as A* search, "
        "GUI visualization, or schedule-based simulations.",
        s["body"],
    ))

    story.append(Spacer(1, 30))
    story.append(hr())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Submitted by <b>Rohan Sainju</b> — COSC 320.001, Spring 2026",
        s["caption"],
    ))

    # ────────────────────────────────────────────────────────────────
    # APPENDIX — Source Code
    # ────────────────────────────────────────────────────────────────
    source_files = [
        "station.py",
        "graph.py",
        "traversal.py",
        "shortest_path.py",
        "passenger.py",
        "undo_stack.py",
        "sorting.py",
        "searching.py",
        "demo_data.py",
        "main.py",
    ]

    story.append(PageBreak())
    story.append(Paragraph("Appendix — Source Code", s["h1"]))
    story.append(hr())
    story.append(Paragraph(
        "Complete source code for all 10 modules. "
        "Also available at: "
        '<link href="https://github.com/rosaiju/transit-system-simulator" '
        'color="#B5451B"><u>'
        "github.com/rosaiju/transit-system-simulator</u></link>",
        s["body"],
    ))

    for fname in source_files:
        with open(fname, "r") as f:
            code = f.read()
        story.append(Paragraph(fname, s["h2"]))
        story.append(Preformatted(code, s["code"]))

    doc.build(story)
    print("Report generated: Transit_System_Report.pdf")


if __name__ == "__main__":
    build()
