"""
Mark and Sweep Garbage Collection Algorithm Implementation

This module demonstrates a real-life implementation of the Mark and Sweep 
garbage collection algorithm, showing how automatic memory management works.
"""

from typing import Set, List, Optional, Any
from enum import Enum


class ObjectState(Enum):
    """State of an object in the garbage collector"""
    UNMARKED = "unmarked"
    MARKED = "marked"
    COLLECTED = "collected"


class ManagedObject:
    """Represents an object managed by the garbage collector"""
    
    _id_counter = 0
    
    def __init__(self, name: str, data: Any = None):
        ManagedObject._id_counter += 1
        self.id = ManagedObject._id_counter
        self.name = name
        self.data = data
        self.references: List['ManagedObject'] = []
        self.state = ObjectState.UNMARKED
        
    def add_reference(self, obj: 'ManagedObject') -> None:
        """Add a reference to another object"""
        if obj not in self.references:
            self.references.append(obj)
            
    def remove_reference(self, obj: 'ManagedObject') -> None:
        """Remove a reference to another object"""
        if obj in self.references:
            self.references.remove(obj)
    
    def __repr__(self) -> str:
        return f"Object({self.id}: {self.name}, refs={len(self.references)}, state={self.state.value})"


class MarkAndSweepGC:
    """
    Mark and Sweep Garbage Collector
    
    The algorithm works in two phases:
    1. Mark Phase: Starting from root objects, mark all reachable objects
    2. Sweep Phase: Delete all unmarked objects (garbage)
    """
    
    def __init__(self):
        self.all_objects: Set[ManagedObject] = set()
        self.roots: Set[ManagedObject] = set()
        self.collected_count = 0
        self.collection_history: List[dict] = []
        
    def allocate(self, name: str, data: Any = None) -> ManagedObject:
        """Allocate a new object"""
        obj = ManagedObject(name, data)
        self.all_objects.add(obj)
        print(f"📦 Allocated: {obj}")
        return obj
    
    def add_root(self, obj: ManagedObject) -> None:
        """Add an object as a root (e.g., global variable, stack variable)"""
        self.roots.add(obj)
        print(f"🌳 Added root: {obj}")
        
    def remove_root(self, obj: ManagedObject) -> None:
        """Remove an object from roots"""
        if obj in self.roots:
            self.roots.remove(obj)
            print(f"🔻 Removed root: {obj}")
    
    def mark(self, obj: ManagedObject) -> None:
        """
        Mark phase: Recursively mark an object and all objects it references
        """
        # If already marked, skip to avoid infinite loops
        if obj.state == ObjectState.MARKED:
            return
            
        # Mark this object
        obj.state = ObjectState.MARKED
        print(f"  ✓ Marked: {obj}")
        
        # Recursively mark all referenced objects
        for ref in obj.references:
            self.mark(ref)
    
    def mark_phase(self) -> int:
        """
        Mark all reachable objects starting from roots
        Returns the number of objects marked
        """
        print("\n🔍 MARK PHASE - Starting from roots...")
        marked_count = 0
        
        # Reset all objects to unmarked
        for obj in self.all_objects:
            obj.state = ObjectState.UNMARKED
        
        # Mark all objects reachable from roots
        for root in self.roots:
            self.mark(root)
        
        # Count marked objects
        for obj in self.all_objects:
            if obj.state == ObjectState.MARKED:
                marked_count += 1
                
        print(f"✓ Mark phase complete: {marked_count} objects marked as reachable")
        return marked_count
    
    def sweep_phase(self) -> int:
        """
        Sweep phase: Remove all unmarked objects (garbage)
        Returns the number of objects collected
        """
        print("\n🧹 SWEEP PHASE - Collecting garbage...")
        collected = []
        
        # Find all unmarked objects (garbage)
        for obj in list(self.all_objects):
            if obj.state == ObjectState.UNMARKED:
                collected.append(obj)
                obj.state = ObjectState.COLLECTED
                print(f"  🗑️  Collected: {obj}")
        
        # Remove collected objects from the set
        for obj in collected:
            self.all_objects.remove(obj)
            
        self.collected_count += len(collected)
        print(f"✓ Sweep phase complete: {len(collected)} objects collected")
        return len(collected)
    
    def collect(self) -> dict:
        """
        Run a complete garbage collection cycle
        Returns statistics about the collection
        """
        print("\n" + "="*60)
        print("🚮 GARBAGE COLLECTION CYCLE STARTED")
        print("="*60)
        
        initial_count = len(self.all_objects)
        print(f"Total objects before GC: {initial_count}")
        print(f"Root objects: {len(self.roots)}")
        
        # Mark phase
        marked_count = self.mark_phase()
        
        # Sweep phase
        collected = self.sweep_phase()
        
        final_count = len(self.all_objects)
        
        stats = {
            'initial_objects': initial_count,
            'marked_objects': marked_count,
            'collected_objects': collected,
            'final_objects': final_count,
            'roots': len(self.roots)
        }
        
        self.collection_history.append(stats)
        
        print("\n" + "="*60)
        print(f"🎯 GC COMPLETE: {collected} objects freed, {final_count} objects remaining")
        print("="*60 + "\n")
        
        return stats
    
    def get_stats(self) -> dict:
        """Get current garbage collector statistics"""
        return {
            'total_objects': len(self.all_objects),
            'root_objects': len(self.roots),
            'total_collected': self.collected_count,
            'collection_cycles': len(self.collection_history)
        }
    
    def print_object_graph(self) -> None:
        """Print the current object graph"""
        print("\n📊 OBJECT GRAPH:")
        print("-" * 60)
        
        if not self.all_objects:
            print("  (empty)")
            return
            
        for obj in sorted(self.all_objects, key=lambda x: x.id):
            root_marker = "🌳" if obj in self.roots else "  "
            refs = ", ".join([f"#{ref.id}" for ref in obj.references])
            refs_str = f" -> [{refs}]" if refs else ""
            print(f"  {root_marker} #{obj.id}: {obj.name} [{obj.state.value}]{refs_str}")
        
        print("-" * 60)
