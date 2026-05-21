# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal computer science knowledge repository containing algorithm implementations, system design patterns, AI/deep learning notes, design patterns, and development references. It's organized by topic rather than being a traditional software project.

## Directory Structure

| Directory | Content |
|-----------|---------|
| `algo/` | Algorithm implementations organized by category |
| `algo/basics/` | Fundamental algorithms: prefix sum, binary search, difference arrays, quick select, binary lifting |
| `algo/data_structure/` | Data structures: union-find, linked list, stack, Fenwick tree, segment tree |
| `algo/graph/` | Graph algorithms: Dijkstra, Floyd, BFS, bipartite graph, MST |
| `algo/math/` | Math utilities: modular arithmetic, bit operations, Catalan numbers, combinatorics |
| `algo/greedy/` | Greedy algorithm patterns |
| `algo/dp/` | Dynamic programming patterns: LIS, LCS, knapsack (01/complete/multiple), tree DP, digit DP, state machine, prefix-sum optimized DP |
| `algo/string/` | String algorithms: KMP, trie |
| `system_design/` | System design implementations: consistent hashing, autocomplete, rate limiter, distributed ID generation, KV store, short URL, news feed, notification system, crawler system, user expansion, chat system, cloud drive, video sharing |
| `ai/` | AI/ML notes and neural network implementations |
| `ai/NNDL/` | Neural network code from "Neural Networks and Deep Learning" course |
| `design_patterns/` | GoF design patterns in Python (creational, behavioral, structural) |
| `devops/` | Docker, Kubernetes, and Terraform notes (markdown) |
| `web/` | FastAPI examples and JavaScript reference |

## Development

There is **no build system, test framework, or package manager** configured. This repository consists of standalone Python scripts and Markdown notes.

### Running code

Individual Python files can be run directly:

```bash
python algo/basics/prefix_sum_前缀和.py
python system_design/限流器.py
```

### Adding new content

- Algorithm files follow the naming convention `topic_中文描述.py` or `topic_english.py`
- Place algorithms in the appropriate subdirectory under `algo/` based on category
- System design implementations go in `system_design/` (can use subdirectories for larger systems)
- Design patterns follow the GoF categorization under `design_patterns/`

## Code Style

- Python files are reference implementations/snippets, not full applications
- Chinese characters are commonly used in file names and comments
- Code is written for Python 3 (uses modern features like type hints in some files)
- Files often contain both standalone code snippets and class-based implementations

## External References

This repository draws inspiration from several sources listed in README.md: OI-WIKI, LeetCode, codeforces-go, ac-library-python, python-patterns, FastAPI docs, Coursera Deep Learning specialization, and zh.javascript.info.
