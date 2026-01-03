"""
Unit tests for the Mark and Sweep Garbage Collector
Run with: pytest test_mark_and_sweep.py
"""

import pytest
from mark_and_sweep import MarkAndSweepGC, ManagedObject, ObjectState


class TestManagedObject:
    """Test the ManagedObject class"""
    
    def test_object_creation(self):
        obj = ManagedObject("test", {"key": "value"})
        assert obj.name == "test"
        assert obj.data == {"key": "value"}
        assert obj.state == ObjectState.UNMARKED
        assert len(obj.references) == 0
    
    def test_add_reference(self):
        obj1 = ManagedObject("obj1")
        obj2 = ManagedObject("obj2")
        
        obj1.add_reference(obj2)
        assert obj2 in obj1.references
        assert len(obj1.references) == 1
        
        # Adding same reference again should not duplicate
        obj1.add_reference(obj2)
        assert len(obj1.references) == 1
    
    def test_remove_reference(self):
        obj1 = ManagedObject("obj1")
        obj2 = ManagedObject("obj2")
        
        obj1.add_reference(obj2)
        obj1.remove_reference(obj2)
        assert obj2 not in obj1.references
        assert len(obj1.references) == 0


class TestMarkAndSweepGC:
    """Test the Mark and Sweep Garbage Collector"""
    
    def test_allocate(self):
        gc = MarkAndSweepGC()
        obj = gc.allocate("test")
        
        assert obj in gc.all_objects
        assert obj.name == "test"
    
    def test_add_remove_root(self):
        gc = MarkAndSweepGC()
        obj = gc.allocate("root")
        
        gc.add_root(obj)
        assert obj in gc.roots
        
        gc.remove_root(obj)
        assert obj not in gc.roots
    
    def test_simple_garbage_collection(self):
        """Test basic GC: reachable vs unreachable objects"""
        gc = MarkAndSweepGC()
        
        # Create reachable object
        root = gc.allocate("root")
        gc.add_root(root)
        
        reachable = gc.allocate("reachable")
        root.add_reference(reachable)
        
        # Create unreachable object
        garbage = gc.allocate("garbage")
        
        # Before GC: 3 objects
        assert len(gc.all_objects) == 3
        
        # Run GC
        stats = gc.collect()
        
        # After GC: 2 objects (garbage collected)
        assert len(gc.all_objects) == 2
        assert stats['collected_objects'] == 1
        assert garbage not in gc.all_objects
        assert root in gc.all_objects
        assert reachable in gc.all_objects
    
    def test_circular_reference_collection(self):
        """Test that circular references are collected when unreachable"""
        gc = MarkAndSweepGC()
        
        # Create circular reference
        objA = gc.allocate("A")
        objB = gc.allocate("B")
        objC = gc.allocate("C")
        
        objA.add_reference(objB)
        objB.add_reference(objC)
        objC.add_reference(objA)  # Circular
        
        # All should be collected (no roots)
        stats = gc.collect()
        
        assert stats['collected_objects'] == 3
        assert len(gc.all_objects) == 0
    
    def test_circular_reference_preservation(self):
        """Test that circular references are kept when reachable"""
        gc = MarkAndSweepGC()
        
        # Create circular reference with root
        objA = gc.allocate("A")
        objB = gc.allocate("B")
        objC = gc.allocate("C")
        
        objA.add_reference(objB)
        objB.add_reference(objC)
        objC.add_reference(objA)  # Circular
        
        # Add root
        gc.add_root(objA)
        
        # All should be kept (reachable from root)
        stats = gc.collect()
        
        assert stats['collected_objects'] == 0
        assert len(gc.all_objects) == 3
    
    def test_mark_phase(self):
        """Test the mark phase independently"""
        gc = MarkAndSweepGC()
        
        root = gc.allocate("root")
        gc.add_root(root)
        
        child1 = gc.allocate("child1")
        child2 = gc.allocate("child2")
        root.add_reference(child1)
        root.add_reference(child2)
        
        garbage = gc.allocate("garbage")
        
        # Run mark phase
        marked_count = gc.mark_phase()
        
        assert marked_count == 3  # root, child1, child2
        assert root.state == ObjectState.MARKED
        assert child1.state == ObjectState.MARKED
        assert child2.state == ObjectState.MARKED
        assert garbage.state == ObjectState.UNMARKED
    
    def test_multiple_roots(self):
        """Test GC with multiple root objects"""
        gc = MarkAndSweepGC()
        
        root1 = gc.allocate("root1")
        root2 = gc.allocate("root2")
        gc.add_root(root1)
        gc.add_root(root2)
        
        obj1 = gc.allocate("obj1")
        obj2 = gc.allocate("obj2")
        root1.add_reference(obj1)
        root2.add_reference(obj2)
        
        garbage = gc.allocate("garbage")
        
        stats = gc.collect()
        
        assert stats['collected_objects'] == 1
        assert garbage not in gc.all_objects
        assert len(gc.all_objects) == 4  # 2 roots + 2 children
    
    def test_deep_reference_chain(self):
        """Test GC with deep reference chains"""
        gc = MarkAndSweepGC()
        
        root = gc.allocate("root")
        gc.add_root(root)
        
        # Create chain: root -> obj1 -> obj2 -> obj3 -> obj4
        current = root
        for i in range(1, 5):
            obj = gc.allocate(f"obj{i}")
            current.add_reference(obj)
            current = obj
        
        garbage = gc.allocate("garbage")
        
        stats = gc.collect()
        
        assert stats['collected_objects'] == 1
        assert len(gc.all_objects) == 5  # root + 4 chain objects
    
    def test_stats_tracking(self):
        """Test statistics tracking"""
        gc = MarkAndSweepGC()
        
        root = gc.allocate("root")
        gc.add_root(root)
        
        garbage1 = gc.allocate("garbage1")
        garbage2 = gc.allocate("garbage2")
        
        gc.collect()
        
        stats = gc.get_stats()
        assert stats['total_objects'] == 1
        assert stats['root_objects'] == 1
        assert stats['total_collected'] == 2
        assert stats['collection_cycles'] == 1


class TestRealWorldScenarios:
    """Test real-world usage scenarios"""
    
    def test_web_request_simulation(self):
        """Simulate HTTP request handling"""
        gc = MarkAndSweepGC()
        
        # Application (persistent)
        app = gc.allocate("app")
        gc.add_root(app)
        
        db_pool = gc.allocate("db_pool")
        app.add_reference(db_pool)
        
        # Request 1
        req1 = gc.allocate("request1")
        gc.add_root(req1)
        session1 = gc.allocate("session1")
        req1.add_reference(session1)
        req1.add_reference(db_pool)
        
        # Request 2
        req2 = gc.allocate("request2")
        gc.add_root(req2)
        session2 = gc.allocate("session2")
        req2.add_reference(session2)
        req2.add_reference(db_pool)
        
        assert len(gc.all_objects) == 6
        
        # Complete request 1
        gc.remove_root(req1)
        gc.collect()
        
        # req1 and session1 collected
        assert len(gc.all_objects) == 4
        
        # Complete request 2
        gc.remove_root(req2)
        gc.collect()
        
        # req2 and session2 collected, app and db_pool remain
        assert len(gc.all_objects) == 2
        assert app in gc.all_objects
        assert db_pool in gc.all_objects


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
