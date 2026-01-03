"""
Demo Examples for Mark and Sweep Garbage Collection

This file contains various scenarios demonstrating how the garbage collector works.
"""

from mark_and_sweep import MarkAndSweepGC, ManagedObject
from visualizer import GCVisualizer, print_ascii_visualization


def demo_basic_gc():
    """Basic demonstration of mark and sweep"""
    print("\n" + "🎬 " + "="*68)
    print("DEMO 1: Basic Garbage Collection")
    print("="*70)
    print("Scenario: Creating objects with some becoming unreachable\n")
    
    gc = MarkAndSweepGC()
    
    # Create some objects
    obj1 = gc.allocate("Main", {"type": "main object"})
    obj2 = gc.allocate("Helper", {"type": "helper"})
    obj3 = gc.allocate("Orphan", {"type": "will be garbage"})
    obj4 = gc.allocate("Child", {"type": "child object"})
    
    # Set up references
    obj1.add_reference(obj2)  # Main -> Helper
    obj2.add_reference(obj4)  # Helper -> Child
    
    # obj3 has no references - it's an orphan
    
    # Add root
    gc.add_root(obj1)
    
    # Show object graph
    gc.print_object_graph()
    print_ascii_visualization(gc, "Before GC")
    
    # Run garbage collection
    stats = gc.collect()
    
    # Show results
    gc.print_object_graph()
    print(f"\n📈 Stats: {stats}")
    

def demo_circular_references():
    """Demonstrate handling of circular references"""
    print("\n" + "🎬 " + "="*68)
    print("DEMO 2: Circular References")
    print("="*70)
    print("Scenario: Objects with circular references (A->B->C->A)\n")
    
    gc = MarkAndSweepGC()
    
    # Create circular reference
    objA = gc.allocate("Node-A")
    objB = gc.allocate("Node-B")
    objC = gc.allocate("Node-C")
    
    # Create circle: A -> B -> C -> A
    objA.add_reference(objB)
    objB.add_reference(objC)
    objC.add_reference(objA)
    
    # Create a root that references the circle
    root = gc.allocate("Root")
    root.add_reference(objA)
    gc.add_root(root)
    
    gc.print_object_graph()
    print("\n💡 Note: Circular references exist (A->B->C->A)")
    print("Running GC - should keep all objects (reachable from root)...")
    
    gc.collect()
    gc.print_object_graph()
    
    # Now remove root reference
    print("\n🔻 Removing root reference to the circle...")
    root.remove_reference(objA)
    
    gc.print_object_graph()
    print("\nRunning GC again - should collect the entire circle...")
    
    gc.collect()
    gc.print_object_graph()


def demo_multiple_roots():
    """Demonstrate multiple root objects"""
    print("\n" + "🎬 " + "="*68)
    print("DEMO 3: Multiple Root Objects")
    print("="*70)
    print("Scenario: Multiple root objects (like multiple stack frames)\n")
    
    gc = MarkAndSweepGC()
    
    # Simulate multiple roots (e.g., different stack frames)
    root1 = gc.allocate("StackFrame-1")
    root2 = gc.allocate("StackFrame-2")
    gc.add_root(root1)
    gc.add_root(root2)
    
    # Each root has its own object graph
    obj1a = gc.allocate("Frame1-ObjA")
    obj1b = gc.allocate("Frame1-ObjB")
    root1.add_reference(obj1a)
    obj1a.add_reference(obj1b)
    
    obj2a = gc.allocate("Frame2-ObjA")
    obj2b = gc.allocate("Frame2-ObjB")
    root2.add_reference(obj2a)
    obj2a.add_reference(obj2b)
    
    # Some orphaned objects
    orphan1 = gc.allocate("Orphan-1")
    orphan2 = gc.allocate("Orphan-2")
    
    gc.print_object_graph()
    print("\n💡 Note: Two separate object trees from two roots")
    print("Running GC - should only collect orphans...")
    
    gc.collect()
    gc.print_object_graph()


def demo_progressive_cleanup():
    """Demonstrate progressive cleanup as roots are removed"""
    print("\n" + "🎬 " + "="*68)
    print("DEMO 4: Progressive Cleanup")
    print("="*70)
    print("Scenario: Gradually removing roots and watching garbage accumulate\n")
    
    gc = MarkAndSweepGC()
    
    # Create a tree structure
    root = gc.allocate("Root")
    gc.add_root(root)
    
    branch1 = gc.allocate("Branch-1")
    branch2 = gc.allocate("Branch-2")
    root.add_reference(branch1)
    root.add_reference(branch2)
    
    leaf1a = gc.allocate("Leaf-1A")
    leaf1b = gc.allocate("Leaf-1B")
    branch1.add_reference(leaf1a)
    branch1.add_reference(leaf1b)
    
    leaf2a = gc.allocate("Leaf-2A")
    leaf2b = gc.allocate("Leaf-2B")
    branch2.add_reference(leaf2a)
    branch2.add_reference(leaf2b)
    
    gc.print_object_graph()
    
    # First GC - everything is reachable
    print("\n1️⃣ First GC - all objects reachable:")
    gc.collect()
    
    # Remove reference to branch1
    print("\n🔻 Removing reference to Branch-1...")
    root.remove_reference(branch1)
    gc.print_object_graph()
    
    print("\n2️⃣ Second GC - Branch-1 and its leaves should be collected:")
    gc.collect()
    
    # Remove reference to branch2
    print("\n🔻 Removing reference to Branch-2...")
    root.remove_reference(branch2)
    gc.print_object_graph()
    
    print("\n3️⃣ Third GC - Branch-2 and its leaves should be collected:")
    gc.collect()
    
    # Remove root
    print("\n🔻 Removing root...")
    gc.remove_root(root)
    gc.print_object_graph()
    
    print("\n4️⃣ Fourth GC - Root should be collected (no roots left):")
    gc.collect()
    
    print(f"\n📊 Final stats: {gc.get_stats()}")


def demo_real_world_scenario():
    """Simulate a real-world scenario like a web server handling requests"""
    print("\n" + "🎬 " + "="*68)
    print("DEMO 5: Real-World Scenario - Web Server Requests")
    print("="*70)
    print("Scenario: Simulating HTTP request processing with temporary objects\n")
    
    gc = MarkAndSweepGC()
    
    # Application root (always alive)
    app = gc.allocate("WebApplication", {"port": 8080})
    gc.add_root(app)
    
    # Database connection pool (persistent)
    db_pool = gc.allocate("DatabasePool", {"connections": 10})
    app.add_reference(db_pool)
    
    print("🌐 Web server started with database pool")
    gc.print_object_graph()
    
    # Simulate Request 1
    print("\n📨 Processing Request 1...")
    req1 = gc.allocate("Request-1", {"path": "/api/users"})
    gc.add_root(req1)  # Active request
    
    session1 = gc.allocate("Session-1", {"user_id": 123})
    req1.add_reference(session1)
    
    response1 = gc.allocate("Response-1", {"status": 200})
    req1.add_reference(response1)
    
    # Request uses DB connection
    req1.add_reference(db_pool)
    
    gc.print_object_graph()
    
    # Simulate Request 2
    print("\n📨 Processing Request 2...")
    req2 = gc.allocate("Request-2", {"path": "/api/posts"})
    gc.add_root(req2)  # Another active request
    
    session2 = gc.allocate("Session-2", {"user_id": 456})
    req2.add_reference(session2)
    
    response2 = gc.allocate("Response-2", {"status": 200})
    req2.add_reference(response2)
    
    req2.add_reference(db_pool)
    
    gc.print_object_graph()
    
    # Complete Request 1
    print("\n✅ Request 1 completed, cleaning up...")
    gc.remove_root(req1)
    
    print("\n🧹 Running GC after Request 1 completed:")
    gc.collect()
    gc.print_object_graph()
    
    # Complete Request 2
    print("\n✅ Request 2 completed, cleaning up...")
    gc.remove_root(req2)
    
    print("\n🧹 Running GC after Request 2 completed:")
    gc.collect()
    gc.print_object_graph()
    
    print("\n💡 Note: Application and DatabasePool remain (still rooted)")
    print(f"📊 Total GC stats: {gc.get_stats()}")


def demo_with_visualization():
    """Create a visual demonstration (requires graphviz)"""
    print("\n" + "🎬 " + "="*68)
    print("DEMO 6: Visual Demonstration (if graphviz is installed)")
    print("="*70)
    
    gc = MarkAndSweepGC()
    visualizer = GCVisualizer(gc)
    
    # Create object graph
    root = gc.allocate("Root")
    gc.add_root(root)
    
    reachable1 = gc.allocate("Reachable-1")
    reachable2 = gc.allocate("Reachable-2")
    garbage1 = gc.allocate("Garbage-1")
    garbage2 = gc.allocate("Garbage-2")
    
    root.add_reference(reachable1)
    reachable1.add_reference(reachable2)
    
    # garbage1 and garbage2 are not referenced
    
    print("Creating visualizations...")
    visualizer.visualize_gc_cycle("demo_visualization")
    
    gc.print_object_graph()


def run_all_demos():
    """Run all demonstration scenarios"""
    demo_basic_gc()
    input("\n Press Enter to continue to next demo...")
    
    demo_circular_references()
    input("\nPress Enter to continue to next demo...")
    
    demo_multiple_roots()
    input("\nPress Enter to continue to next demo...")
    
    demo_progressive_cleanup()
    input("\nPress Enter to continue to next demo...")
    
    demo_real_world_scenario()
    input("\nPress Enter to continue to next demo...")
    
    demo_with_visualization()
    
    print("\n" + "="*70)
    print("🎉 All demos completed!")
    print("="*70)


if __name__ == "__main__":
    import sys
    
    demos = {
        '1': ('Basic GC', demo_basic_gc),
        '2': ('Circular References', demo_circular_references),
        '3': ('Multiple Roots', demo_multiple_roots),
        '4': ('Progressive Cleanup', demo_progressive_cleanup),
        '5': ('Real-World Scenario', demo_real_world_scenario),
        '6': ('Visualization', demo_with_visualization),
        'all': ('All Demos', run_all_demos)
    }
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice in demos:
            demos[choice][1]()
        else:
            print(f"Unknown demo: {choice}")
            print("Available demos:", ', '.join(demos.keys()))
    else:
        print("\n🎯 Mark and Sweep GC - Demo Menu")
        print("="*70)
        for key, (name, _) in demos.items():
            print(f"  {key}. {name}")
        print("="*70)
        print("\nRun with: python demo.py <number>")
        print("Example: python demo.py 1\n")
        
        # Run all demos interactively
        run_all_demos()
