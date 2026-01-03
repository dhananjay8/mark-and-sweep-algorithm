#!/usr/bin/env python3
"""
Interactive Mark and Sweep Garbage Collector Demo

This provides an interactive command-line interface to experiment with
the garbage collector in real-time.
"""

from mark_and_sweep import MarkAndSweepGC, ManagedObject
from visualizer import print_ascii_visualization
import cmd
import shlex


class GCShell(cmd.Cmd):
    """Interactive shell for garbage collector experimentation"""
    
    intro = """
╔═══════════════════════════════════════════════════════════════════╗
║   Mark and Sweep Garbage Collector - Interactive Demo            ║
╚═══════════════════════════════════════════════════════════════════╝

Type 'help' to see available commands.
Type 'tutorial' for a guided walkthrough.
    """
    
    prompt = 'gc> '
    
    def __init__(self):
        super().__init__()
        self.gc = MarkAndSweepGC()
        self.objects = {}  # name -> object mapping for easy reference
    
    def do_alloc(self, arg):
        """Allocate a new object: alloc <name> [data]"""
        args = shlex.split(arg)
        if not args:
            print("Usage: alloc <name> [data]")
            return
        
        name = args[0]
        data = args[1] if len(args) > 1 else None
        
        if name in self.objects:
            print(f"❌ Object '{name}' already exists")
            return
        
        obj = self.gc.allocate(name, data)
        self.objects[name] = obj
        print(f"✅ Created object: {obj}")
    
    def do_ref(self, arg):
        """Add reference: ref <from> <to>"""
        args = shlex.split(arg)
        if len(args) != 2:
            print("Usage: ref <from_object> <to_object>")
            return
        
        from_name, to_name = args
        
        if from_name not in self.objects:
            print(f"❌ Object '{from_name}' not found")
            return
        if to_name not in self.objects:
            print(f"❌ Object '{to_name}' not found")
            return
        
        from_obj = self.objects[from_name]
        to_obj = self.objects[to_name]
        
        from_obj.add_reference(to_obj)
        print(f"✅ Added reference: {from_name} → {to_name}")
    
    def do_unref(self, arg):
        """Remove reference: unref <from> <to>"""
        args = shlex.split(arg)
        if len(args) != 2:
            print("Usage: unref <from_object> <to_object>")
            return
        
        from_name, to_name = args
        
        if from_name not in self.objects:
            print(f"❌ Object '{from_name}' not found")
            return
        if to_name not in self.objects:
            print(f"❌ Object '{to_name}' not found")
            return
        
        from_obj = self.objects[from_name]
        to_obj = self.objects[to_name]
        
        from_obj.remove_reference(to_obj)
        print(f"✅ Removed reference: {from_name} ⇸ {to_name}")
    
    def do_root(self, arg):
        """Add object to roots: root <name>"""
        if not arg:
            print("Usage: root <object_name>")
            return
        
        if arg not in self.objects:
            print(f"❌ Object '{arg}' not found")
            return
        
        obj = self.objects[arg]
        self.gc.add_root(obj)
        print(f"✅ Added '{arg}' to roots")
    
    def do_unroot(self, arg):
        """Remove object from roots: unroot <name>"""
        if not arg:
            print("Usage: unroot <object_name>")
            return
        
        if arg not in self.objects:
            print(f"❌ Object '{arg}' not found")
            return
        
        obj = self.objects[arg]
        self.gc.remove_root(obj)
        print(f"✅ Removed '{arg}' from roots")
    
    def do_collect(self, arg):
        """Run garbage collection: collect"""
        print_ascii_visualization(self.gc, "Before GC")
        stats = self.gc.collect()
        
        # Update objects dict to remove collected objects
        collected_names = []
        for name, obj in list(self.objects.items()):
            if obj not in self.gc.all_objects:
                collected_names.append(name)
        
        for name in collected_names:
            del self.objects[name]
        
        print(f"\n📊 Collection Stats:")
        print(f"  - Marked (reachable): {stats['marked_objects']}")
        print(f"  - Collected (garbage): {stats['collected_objects']}")
        print(f"  - Remaining: {stats['final_objects']}")
    
    def do_show(self, arg):
        """Show object graph: show"""
        self.gc.print_object_graph()
        print_ascii_visualization(self.gc, "Current State")
    
    def do_list(self, arg):
        """List all objects: list"""
        if not self.objects:
            print("No objects allocated")
            return
        
        print("\n📦 Objects:")
        for name, obj in sorted(self.objects.items()):
            root_marker = "🌳" if obj in self.gc.roots else "  "
            refs = [n for n, o in self.objects.items() if o in obj.references]
            refs_str = f" → {', '.join(refs)}" if refs else ""
            print(f"  {root_marker} {name}{refs_str}")
    
    def do_stats(self, arg):
        """Show garbage collector statistics: stats"""
        stats = self.gc.get_stats()
        print("\n📈 Garbage Collector Statistics:")
        print(f"  Total objects: {stats['total_objects']}")
        print(f"  Root objects: {stats['root_objects']}")
        print(f"  Total collected: {stats['total_collected']}")
        print(f"  GC cycles run: {stats['collection_cycles']}")
    
    def do_clear(self, arg):
        """Clear all objects and start fresh: clear"""
        self.gc = MarkAndSweepGC()
        self.objects = {}
        print("✅ Cleared all objects")
    
    def do_tutorial(self, arg):
        """Run an interactive tutorial: tutorial"""
        print("\n" + "="*70)
        print("📚 TUTORIAL: Mark and Sweep Garbage Collection")
        print("="*70)
        
        print("\nStep 1: Create some objects")
        print("Command: alloc root")
        input("Press Enter to execute...")
        self.do_alloc("root")
        
        print("\nCommand: alloc child1")
        input("Press Enter...")
        self.do_alloc("child1")
        
        print("\nCommand: alloc child2")
        input("Press Enter...")
        self.do_alloc("child2")
        
        print("\nCommand: alloc orphan")
        input("Press Enter...")
        self.do_alloc("orphan")
        
        print("\nStep 2: Create references")
        print("Command: ref root child1")
        input("Press Enter...")
        self.do_ref("root child1")
        
        print("\nCommand: ref root child2")
        input("Press Enter...")
        self.do_ref("root child2")
        
        print("\nStep 3: Set root object")
        print("Command: root root")
        input("Press Enter...")
        self.do_root("root")
        
        print("\nStep 4: View the object graph")
        print("Command: show")
        input("Press Enter...")
        self.do_show("")
        
        print("\n💡 Notice: 'orphan' has no references and is not rooted")
        print("   It will be collected as garbage!")
        
        print("\nStep 5: Run garbage collection")
        print("Command: collect")
        input("Press Enter...")
        self.do_collect("")
        
        print("\n✅ Tutorial complete!")
        print("Try creating your own object graphs with:")
        print("  - alloc, ref, root, collect")
        print("  - Type 'help' for all commands")
    
    def do_example(self, arg):
        """Load a predefined example: example <name>"""
        examples = {
            'simple': self._example_simple,
            'circular': self._example_circular,
            'tree': self._example_tree,
            'web': self._example_web
        }
        
        if not arg or arg not in examples:
            print("Available examples:")
            print("  simple   - Simple parent-child relationship")
            print("  circular - Circular reference demonstration")
            print("  tree     - Tree structure with branches")
            print("  web      - Web server request simulation")
            print("\nUsage: example <name>")
            return
        
        self.do_clear("")
        examples[arg]()
    
    def _example_simple(self):
        print("Loading simple example...")
        self.do_alloc("parent")
        self.do_alloc("child")
        self.do_alloc("orphan")
        self.do_ref("parent child")
        self.do_root("parent")
        self.do_show("")
    
    def _example_circular(self):
        print("Loading circular reference example...")
        self.do_alloc("A")
        self.do_alloc("B")
        self.do_alloc("C")
        self.do_ref("A B")
        self.do_ref("B C")
        self.do_ref("C A")
        self.do_show("")
        print("\n💡 A→B→C→A forms a circle. Without roots, all will be collected!")
    
    def _example_tree(self):
        print("Loading tree structure example...")
        self.do_alloc("root")
        self.do_alloc("branch1")
        self.do_alloc("branch2")
        self.do_alloc("leaf1a")
        self.do_alloc("leaf1b")
        self.do_alloc("leaf2a")
        self.do_ref("root branch1")
        self.do_ref("root branch2")
        self.do_ref("branch1 leaf1a")
        self.do_ref("branch1 leaf1b")
        self.do_ref("branch2 leaf2a")
        self.do_root("root")
        self.do_show("")
    
    def _example_web(self):
        print("Loading web server example...")
        self.do_alloc("app")
        self.do_alloc("db_pool")
        self.do_alloc("request1")
        self.do_alloc("session1")
        self.do_ref("app db_pool")
        self.do_ref("request1 session1")
        self.do_ref("request1 db_pool")
        self.do_root("app")
        self.do_root("request1")
        self.do_show("")
        print("\n💡 Try: unroot request1, then collect")
    
    def do_quit(self, arg):
        """Exit the interactive shell: quit"""
        print("\n👋 Goodbye!")
        return True
    
    def do_exit(self, arg):
        """Exit the interactive shell: exit"""
        return self.do_quit(arg)
    
    def do_EOF(self, arg):
        """Handle Ctrl+D"""
        print()
        return self.do_quit(arg)


if __name__ == "__main__":
    GCShell().cmdloop()
