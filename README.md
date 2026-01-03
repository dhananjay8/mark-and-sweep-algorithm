# Mark and Sweep Garbage Collection Algorithm

A real-life implementation of the **Mark and Sweep** garbage collection algorithm in Python, demonstrating how automatic memory management works in modern programming languages.

## 🎯 What is Mark and Sweep?

Mark and Sweep is a classic garbage collection algorithm that reclaims memory from objects that are no longer reachable from the program's root set. It works in two phases:

1. **Mark Phase**: Starting from root objects (global variables, stack variables), traverse and mark all reachable objects
2. **Sweep Phase**: Scan through all allocated objects and collect (free) those that weren't marked

This algorithm can handle **circular references** - a scenario where reference counting fails.

## ✨ Features

- ✅ Full implementation of Mark and Sweep algorithm
- ✅ Object reference tracking
- ✅ Root set management (simulating stack/global variables)
- ✅ Circular reference detection and handling
- ✅ Detailed logging and statistics
- ✅ ASCII visualization of object graphs
- ✅ Graphical visualization (optional, requires graphviz)
- ✅ Multiple real-world demo scenarios

## 📋 Requirements

### Basic Usage

```bash
Python 3.7+
```

### Optional (for graphical visualization)

```bash
pip install graphviz
```

You'll also need the graphviz system package:

- **macOS**: `brew install graphviz`
- **Ubuntu/Debian**: `sudo apt-get install graphviz`
- **Windows**: Download from [graphviz.org](https://graphviz.org/download/)

## 🚀 Quick Start

### Run All Demos

```bash
python demo.py all
```

### Run Specific Demo

```bash
# Basic garbage collection
python demo.py 1

# Circular references
python demo.py 2

# Multiple roots
python demo.py 3

# Progressive cleanup
python demo.py 4

# Real-world scenario (web server)
python demo.py 5

# Visual demonstration
python demo.py 6
```

## 📚 Usage Examples

### Basic Example

```python
from mark_and_sweep import MarkAndSweepGC

# Create garbage collector
gc = MarkAndSweepGC()

# Allocate objects
obj1 = gc.allocate("Main Object")
obj2 = gc.allocate("Referenced Object")
obj3 = gc.allocate("Orphan Object")  # Will be garbage

# Create references
obj1.add_reference(obj2)

# Set root (like a global variable)
gc.add_root(obj1)

# Print current state
gc.print_object_graph()

# Run garbage collection
stats = gc.collect()

# obj3 will be collected as garbage
print(f"Objects collected: {stats['collected_objects']}")
```

### Handling Circular References

```python
gc = MarkAndSweepGC()

# Create circular reference: A -> B -> C -> A
objA = gc.allocate("Node-A")
objB = gc.allocate("Node-B")
objC = gc.allocate("Node-C")

objA.add_reference(objB)
objB.add_reference(objC)
objC.add_reference(objA)  # Circular!

# If not rooted, all will be collected together
gc.collect()  # Collects all three despite circular refs
```

### Real-World Scenario

```python
gc = MarkAndSweepGC()

# Application root (persists)
app = gc.allocate("WebApp")
gc.add_root(app)

db_pool = gc.allocate("DB Pool")
app.add_reference(db_pool)

# Process request (temporary)
request = gc.allocate("HTTP Request")
gc.add_root(request)
request.add_reference(db_pool)

session = gc.allocate("Session")
request.add_reference(session)

# Request completes
gc.remove_root(request)

# Clean up request and session, keep app and db_pool
gc.collect()
```

## 🏗️ Architecture

### Core Components

#### `ManagedObject`

Represents an object managed by the garbage collector:

- Unique ID
- Name and data
- References to other objects
- State (unmarked/marked/collected)

#### `MarkAndSweepGC`

The garbage collector implementation:

- **`allocate()`**: Create new objects
- **`add_root()`/`remove_root()`**: Manage root set
- **`mark_phase()`**: Mark all reachable objects
- **`sweep_phase()`**: Collect unmarked objects
- **`collect()`**: Run complete GC cycle

#### `GCVisualizer`

Visualization tools:

- ASCII art object graphs
- Graphviz diagrams (if available)
- GC cycle animations

## 📊 Demo Scenarios

### Demo 1: Basic GC

Simple demonstration showing how unreferenced objects are collected.

### Demo 2: Circular References

Shows how Mark and Sweep handles circular references (unlike reference counting).

### Demo 3: Multiple Roots

Demonstrates multiple root objects (like different stack frames).

### Demo 4: Progressive Cleanup

Shows gradual collection as references are removed.

### Demo 5: Real-World Scenario

Simulates a web server processing HTTP requests with temporary objects.

### Demo 6: Visual Demonstration

Creates graphical visualizations of the GC process (requires graphviz).

## 🔍 How It Works

### Mark Phase

```
1. Reset all objects to "unmarked"
2. For each root object:
   a. Mark the object as "reachable"
   b. Recursively mark all referenced objects
3. After marking, reachable objects are marked, garbage is unmarked
```

### Sweep Phase

```
1. Scan all allocated objects
2. If object is unmarked (garbage):
   a. Remove from object set
   b. Free memory
3. Keep marked objects alive
```

### Why It Handles Circular References

Mark and Sweep uses **reachability** from roots, not reference counting:

- Even if A→B→C→A (circular), if none are reachable from roots, all are collected
- Reference counting would fail here (counts never reach zero)

## 📈 Statistics

The GC tracks:

- Total objects allocated
- Objects collected per cycle
- Objects remaining after collection
- Number of GC cycles run
- Collection history

Access with:

```python
stats = gc.get_stats()
print(f"Total collected: {stats['total_collected']}")
```

## 🎨 Visualization

### ASCII Visualization

```
📊 OBJECT GRAPH:
  🌳 #1: Root [marked] -> [#2]
     #2: Child [marked]
     #3: Orphan [unmarked]
```

### Graphical Visualization

When graphviz is installed, you can generate PNG diagrams:

- **Gold double octagon**: Root objects
- **Green boxes**: Marked (reachable) objects
- **Red boxes**: Unmarked (garbage) objects
- **Arrows**: Object references

## 🔬 Educational Value

This implementation teaches:

1. **Memory Management**: How GC works under the hood
2. **Graph Traversal**: Mark phase is a graph DFS/BFS
3. **Reachability Analysis**: Determining live vs dead objects
4. **Algorithm Design**: Two-phase approach to resource management
5. **Real-World Application**: How languages like Java, Python, JavaScript manage memory

## 🆚 Comparison with Reference Counting

| Feature             | Mark & Sweep    | Reference Counting |
| ------------------- | --------------- | ------------------ |
| Circular references | ✅ Handles      | ❌ Fails           |
| Collection timing   | Periodic cycles | Immediate          |
| Memory overhead     | Lower           | Higher (counts)    |
| Pause time          | Longer          | Shorter            |
| Complexity          | O(live objects) | O(operations)      |

## 🛠️ Advanced Usage

### Custom Data

```python
obj = gc.allocate("User", data={
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com"
})
print(obj.data)
```

### Tracking Collections

```python
for cycle in gc.collection_history:
    print(f"Cycle: {cycle['collected_objects']} objects freed")
```

## 🤝 Contributing

This is an educational project. Feel free to:

- Add new demo scenarios
- Improve visualizations
- Add more statistics
- Optimize the algorithm
- Add concurrent GC simulation

## 📝 License

MIT License - Feel free to use for education and learning!

## 🔗 References

- [Garbage Collection Handbook](https://gchandbook.org/)
- [The Garbage Collection Handbook](https://www.cs.kent.ac.uk/people/staff/rej/gcbook/)
- [Python's Garbage Collection](https://docs.python.org/3/library/gc.html)

## 🎓 Learn More

To understand GC algorithms better:

1. Run each demo and observe the output
2. Modify scenarios to create your own object graphs
3. Add print statements to see the mark phase traversal
4. Try implementing optimizations (generational GC, incremental marking)
5. Compare with other GC algorithms (copying, generational, concurrent)

---

**Built with ❤️ for learning and understanding garbage collection**
