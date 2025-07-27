"""
Sample Computer Science Questions for Setwise Quiz Generator

Covers algorithms, data structures, and programming concepts.
Usage: setwise generate --questions-file computer_science_questions.py
"""

# Multiple Choice Questions - Computer Science
mcq = [
    {
        "question": r"What is the time complexity of binary search on a sorted array of size $n$?",
        "options": [
            r"$O(1)$",
            r"$O(\log n)$", 
            r"$O(n)$",
            r"$O(n \log n)$",
            r"$O(n^2)$"
        ],
        "answer": r"$O(\log n)$",
        "marks": 2
    },
    {
        "question": r"Which data structure follows the Last-In-First-Out (LIFO) principle?",
        "options": [
            r"Queue",
            r"Stack",
            r"Linked List", 
            r"Binary Tree",
            r"Hash Table"
        ],
        "answer": r"Stack",
        "marks": 1
    },
    {
        "question": r"In object-oriented programming, what does polymorphism allow?",
        "options": [
            r"Multiple inheritance only",
            r"Dynamic method binding and method overriding",
            r"Private variable access",
            r"Automatic memory management",
            r"Compile-time error checking"
        ],
        "answer": r"Dynamic method binding and method overriding",
        "marks": 2
    },
    {
        "question": r"What is the worst-case time complexity of quicksort?",
        "options": [
            r"$O(n)$",
            r"$O(n \log n)$",
            r"$O(n^2)$",
            r"$O(2^n)$",
            r"$O(n!)$"
        ],
        "answer": r"$O(n^2)$",
        "marks": 2
    },
    {
        "question": r"Which of the following is NOT a characteristic of a good hash function?",
        "options": [
            r"Uniform distribution of hash values",
            r"Deterministic output",
            r"Fast computation",
            r"Always produces the same output size",
            r"Reversible (can retrieve input from output)"
        ],
        "answer": r"Reversible (can retrieve input from output)",
        "marks": 2
    }
]

# Subjective Questions - Computer Science
subjective = [
    {
        "question": r"""Analyze the following recursive algorithm for computing Fibonacci numbers:

\begin{verbatim}
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
\end{verbatim}

\textbf{a)} Trace the execution for \texttt{fibonacci(4)} showing all recursive calls. \textbf{[4 marks]}

\textbf{b)} Determine the time complexity using recurrence relations. \textbf{[3 marks]}

\textbf{c)} Suggest an optimization and analyze its time complexity. \textbf{[3 marks]}""",
        "answer": r"""a) fibonacci(4) calls:
   - fibonacci(3) and fibonacci(2)
   - fibonacci(3) calls fibonacci(2) and fibonacci(1)
   - fibonacci(2) calls fibonacci(1) and fibonacci(0)
   Total: 9 function calls

b) Recurrence: $T(n) = T(n-1) + T(n-2) + O(1)$
   This gives $T(n) = O(\phi^n)$ where $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$

c) Dynamic programming optimization:
   Store computed values in array/memoization
   Time complexity: $O(n)$, Space: $O(n)$""",
        "marks": 10
    },
    {
        "template": r"""Design and analyze a hash table implementation.

You need to implement a hash table with {{ size }} buckets using {{ method }} for collision resolution.

\textbf{a)} Describe how the {{ method }} method works. \textbf{[3 marks]}

\textbf{b)} What is the expected time complexity for search operations? \textbf{[2 marks]}

\textbf{c)} Under what conditions might performance degrade to $O(n)$? \textbf{[3 marks]}

\textbf{d)} Suggest one improvement to maintain good performance. \textbf{[2 marks]}""",
        "variables": [
            {
                "size": 10, "method": "chaining",
                "answer": "a) Chaining: Each bucket contains a linked list of elements that hash to same value; b) Expected O(1) with good hash function and load factor; c) Poor hash function causing clustering, high load factor; d) Dynamic resizing when load factor exceeds threshold"
            },
            {
                "size": 16, "method": "open addressing", 
                "answer": "a) Open addressing: When collision occurs, probe for next available slot using linear/quadratic probing; b) Expected O(1) with low load factor; c) High load factor causing many collisions and long probe sequences; d) Double hashing or Robin Hood hashing"
            }
        ],
        "marks": 10
    },
    {
        "template": r"""Consider the following graph problem:

Given an undirected graph with {{ vertices }} vertices, you need to find {{ problem_type }}.

\textbf{a)} Which algorithm would you use and why? \textbf{[3 marks]}

\textbf{b)} What is the time complexity of your chosen algorithm? \textbf{[2 marks]}

\textbf{c)} Trace through the algorithm execution on a simple example. \textbf{[4 marks]}

\textbf{d)} What data structures are required for implementation? \textbf{[2 marks]}""",
        "variables": [
            {
                "vertices": 6, "problem_type": "the shortest path between two specific vertices",
                "answer": "a) BFS for unweighted or Dijkstra for weighted graphs - guarantees shortest path; b) O(V+E) for BFS, O((V+E)logV) for Dijkstra; c) BFS: queue-based level traversal maintaining distances; d) Queue, visited array, distance array, adjacency list"
            },
            {
                "vertices": 8, "problem_type": "a minimum spanning tree",
                "answer": "a) Kruskal's or Prim's algorithm - both find MST optimally; b) O(ElogE) for Kruskal, O(VlogV + E) for Prim with priority queue; c) Kruskal: sort edges, use union-find to avoid cycles; d) Union-find structure, edge list sorted by weight"
            }
        ],
        "marks": 11
    },
    {
        "question": r"""Compare and contrast different sorting algorithms.

Complete the following table and provide explanations:

\begin{center}
\begin{tabular}{|l|c|c|c|c|}
\hline
\textbf{Algorithm} & \textbf{Best Case} & \textbf{Average Case} & \textbf{Worst Case} & \textbf{Space} \\
\hline
Bubble Sort & & & & \\
\hline
Merge Sort & & & & \\
\hline
Quick Sort & & & & \\
\hline
Heap Sort & & & & \\
\hline
\end{tabular}
\end{center}

\textbf{a)} Fill in the time complexities for each algorithm. \textbf{[4 marks]}

\textbf{b)} Explain why merge sort is considered stable while quick sort is not. \textbf{[3 marks]}

\textbf{c)} In what scenario would you choose heap sort over merge sort? \textbf{[2 marks]}""",
        "answer": r"""a) Time complexities:
   Bubble Sort: O(n), O(n²), O(n²), O(1)
   Merge Sort: O(n log n), O(n log n), O(n log n), O(n)
   Quick Sort: O(n log n), O(n log n), O(n²), O(log n)
   Heap Sort: O(n log n), O(n log n), O(n log n), O(1)

b) Merge sort preserves relative order of equal elements during merge operation. Quick sort may change relative positions during partitioning.

c) Choose heap sort when memory is limited (O(1) space) and consistent O(n log n) performance is needed.""",
        "marks": 9
    }
]