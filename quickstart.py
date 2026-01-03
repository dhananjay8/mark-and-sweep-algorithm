#!/usr/bin/env python3
"""
Quick Start Guide for Mark and Sweep Garbage Collector

This file demonstrates the most common usage patterns.
"""

from mark_and_sweep import MarkAndSweepGC


def main():
    print("="*70)
    print("Mark and Sweep Garbage Collector - Quick Start")
    print("="*70)
    
    # Step 1: Create the garbage collector
    print("\n1️⃣ Creating garbage collector...")
    gc = MarkAndSweepGC()
    
    # Step 2: Allocate some objects
    print("\n2️⃣ Allocating objects...")
    obj_a = gc.allocate("Object-A", data={"value": 100})
    obj_b = gc.allocate("Object-B", data={"value": 200})
    obj_c = gc.allocate("Object-C", data={"value": 300})
    obj_d = gc.allocate("Object-D", data={"value": 400})
    
    # Step 3: Create references between objects
    print("\n3️⃣ Creating object references...")
    obj_a.add_reference(obj_b)  # A -> B
    obj_b.add_reference(obj_c)  # B -> C
    # obj_d is not referenced by anyone
    
    # Step 4: Mark root objects (objects that should stay alive)
    print("\n4️⃣ Setting root objects...")
    gc.add_root(obj_a)  # A is a root (e.g., global variable)
    
    # Step 5: View the object graph
    print("\n5️⃣ Current object graph:")
    gc.print_object_graph()
    
    print("\n💡 Analysis:")
    print("   • Object-A is a root (🌳)")
    print("   • Object-B is reachable from A")
    print("   • Object-C is reachable from B")
    print("   • Object-D is NOT reachable → GARBAGE!")
    
    # Step 6: Run garbage collection
    print("\n6️⃣ Running garbage collection...")
    input("   Press Enter to run GC...")
    
    stats = gc.collect()
    
    # Step 7: View results
    print("\n7️⃣ Object graph after GC:")
    gc.print_object_graph()
    
    print("\n📊 Results:")
    print(f"   • Objects collected: {stats['collected_objects']}")
    print(f"   • Objects remaining: {stats['final_objects']}")
    print(f"   • Object-D was collected as garbage! ✅")
    
    # Step 8: Demonstrate circular reference handling
    print("\n" + "="*70)
    print("Bonus: Circular Reference Handling")
    print("="*70)
    
    print("\n8️⃣ Creating circular references...")
    obj_x = gc.allocate("Object-X")
    obj_y = gc.allocate("Object-Y")
    obj_z = gc.allocate("Object-Z")
    
    obj_x.add_reference(obj_y)
    obj_y.add_reference(obj_z)
    obj_z.add_reference(obj_x)  # Creates circle: X -> Y -> Z -> X
    
    print("\n   Created: X → Y → Z → X (circular!)")
    gc.print_object_graph()
    
    print("\n💡 These objects reference each other in a circle,")
    print("   but they're NOT reachable from any root.")
    print("   Mark & Sweep can collect them! (Reference counting cannot)")
    
    input("\n   Press Enter to collect circular garbage...")
    stats = gc.collect()
    
    print(f"\n   ✅ Collected {stats['collected_objects']} objects despite circular refs!")
    gc.print_object_graph()
    
    # Summary
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    total_stats = gc.get_stats()
    print(f"Total objects currently alive: {total_stats['total_objects']}")
    print(f"Total garbage collected: {total_stats['total_collected']}")
    print(f"GC cycles run: {total_stats['collection_cycles']}")
    
    print("\n✨ Key Takeaways:")
    print("   1. Objects reachable from roots are kept alive")
    print("   2. Unreachable objects are collected as garbage")
    print("   3. Circular references are handled correctly")
    print("   4. The algorithm has two phases: Mark → Sweep")
    
    print("\n📚 Next steps:")
    print("   • Run: python demo.py all     (for all demos)")
    print("   • Run: python interactive.py   (for interactive mode)")
    print("   • Run: python test_mark_and_sweep.py (for tests)")
    print("\n")


if __name__ == "__main__":
    main()
