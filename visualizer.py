"""
Visual representation of the Mark and Sweep algorithm using graphviz
"""

from typing import Optional, TYPE_CHECKING

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    Digraph = None  # Type placeholder
    print("Note: graphviz not installed. Install with: pip install graphviz")

from mark_and_sweep import MarkAndSweepGC, ManagedObject, ObjectState


class GCVisualizer:
    """Visualize the garbage collection process"""
    
    def __init__(self, gc: MarkAndSweepGC):
        self.gc = gc
        
        if not GRAPHVIZ_AVAILABLE:
            print("⚠️  Graphviz visualization not available")
    
    def create_graph(self, title: str = "Object Graph", phase: str = ""):
        """Create a visual graph of the current object state"""
        if not GRAPHVIZ_AVAILABLE:
            return None
            
        dot = Digraph(comment=title)
        dot.attr(rankdir='LR', label=f'{title}\n{phase}', fontsize='16', labelloc='t')
        
        # Add nodes for all objects
        for obj in self.gc.all_objects:
            # Determine node color based on state and root status
            if obj in self.gc.roots:
                color = 'gold'
                shape = 'doubleoctagon'
            elif obj.state == ObjectState.MARKED:
                color = 'lightgreen'
                shape = 'box'
            elif obj.state == ObjectState.UNMARKED:
                color = 'lightcoral'
                shape = 'box'
            else:  # COLLECTED
                color = 'gray'
                shape = 'box'
            
            label = f"{obj.name}\nID: {obj.id}\n{obj.state.value}"
            dot.node(str(obj.id), label, 
                    style='filled', 
                    fillcolor=color,
                    shape=shape,
                    fontname='Arial')
        
        # Add edges for references
        for obj in self.gc.all_objects:
            for ref in obj.references:
                dot.edge(str(obj.id), str(ref.id))
        
        return dot
    
    def save_graph(self, filename: str, title: str = "Object Graph", phase: str = "") -> bool:
        """Save the graph to a file"""
        if not GRAPHVIZ_AVAILABLE:
            print("Cannot save graph: graphviz not available")
            return False
            
        dot = self.create_graph(title, phase)
        if dot:
            try:
                dot.render(filename, format='png', cleanup=True)
                print(f"📊 Graph saved to {filename}.png")
                return True
            except Exception as e:
                print(f"Error saving graph: {e}")
                return False
        return False
    
    def visualize_gc_cycle(self, output_prefix: str = "gc_cycle"):
        """Visualize a complete GC cycle with before, mark, and after states"""
        if not GRAPHVIZ_AVAILABLE:
            print("Visualization not available")
            return
        
        # Before GC
        self.save_graph(f"{output_prefix}_1_before", 
                       "Mark & Sweep GC", 
                       "Before Collection")
        
        # Run mark phase
        self.gc.mark_phase()
        self.save_graph(f"{output_prefix}_2_marked", 
                       "Mark & Sweep GC", 
                       "After Mark Phase (Green = Reachable, Red = Garbage)")
        
        # Run sweep phase
        self.gc.sweep_phase()
        self.save_graph(f"{output_prefix}_3_after", 
                       "Mark & Sweep GC", 
                       "After Sweep Phase (Garbage Collected)")
        
        print(f"\n✅ Visualization complete! Check {output_prefix}_*.png files")


def print_ascii_visualization(gc: MarkAndSweepGC, phase: str = ""):
    """Print ASCII art visualization of the object graph"""
    print(f"\n{'='*70}")
    print(f"ASCII VISUALIZATION - {phase}")
    print('='*70)
    
    if not gc.all_objects:
        print("(no objects)")
        return
    
    # Print legend
    print("\nLegend:")
    print("  🌳 = Root object")
    print("  ✓  = Marked (reachable)")
    print("  ✗  = Unmarked (garbage)")
    print("  →  = Reference")
    print()
    
    # Print each object and its references
    for obj in sorted(gc.all_objects, key=lambda x: x.id):
        # Status symbols
        root = "🌳" if obj in gc.roots else "  "
        mark = "✓" if obj.state == ObjectState.MARKED else "✗"
        
        # Basic info
        print(f"{root} [{mark}] Object {obj.id}: {obj.name}")
        
        # Show references
        if obj.references:
            for ref in obj.references:
                ref_mark = "✓" if ref.state == ObjectState.MARKED else "✗"
                print(f"       → [{ref_mark}] Object {ref.id}: {ref.name}")
    
    print('='*70)
