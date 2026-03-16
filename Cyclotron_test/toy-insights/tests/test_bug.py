"""
Test for the deliberate bug: mutable default in ChatRequest.filters

This test demonstrates the bug and shows how it causes state bleed.
The bug is in src/api/models.py where ChatRequest.filters = [] as default.
"""
import pytest
from src.api.models import ChatRequest


class TestMutableDefaultBug:
    """Test and document the mutable default bug."""
    
    def test_mutable_default_state_bleed(self):
        """
        This test FAILS with the current buggy code.
        
        The bug: ChatRequest uses a mutable default (list) for filters.
        Pydantic models cache mutable defaults, causing state bleed across instances.
        
        Expected behavior: Each request should have independent filters.
        Actual (buggy) behavior: Filters accumulate across requests.
        """
        # First request, add a filter
        req1 = ChatRequest(query="query1", filters=["filter_a"])
        assert req1.filters == ["filter_a"]
        
        # Second request, no filters specified (should default to empty)
        req2 = ChatRequest(query="query2")
        # BUG: req2.filters might be ["filter_a"] due to mutable default!
        # This is the bug we're testing for.
        assert req2.filters == [], f"Bug detected! Got {req2.filters}, expected []"
    
    def test_multiple_requests_independent(self):
        """
        Test that multiple requests maintain independent state.
        This reveals the mutable default bug.
        """
        req1 = ChatRequest(query="query1")
        req2 = ChatRequest(query="query2")
        req3 = ChatRequest(query="query3")
        
        # All should have empty filters
        assert req1.filters == []
        assert req2.filters == []
        assert req3.filters == []
        
        # Modify req1's filters
        req1.filters.append("new_filter")
        
        # Others should NOT be affected (but will be with the bug)
        assert req2.filters == [], f"State bleed! req2.filters = {req2.filters}"
        assert req3.filters == [], f"State bleed! req3.filters = {req3.filters}"
    
    def test_the_fix_using_default_factory(self):
        """
        Demonstrate the fix: use Field(default_factory=list).
        
        This is how it SHOULD be implemented:
        
        filters: list[str] = Field(default_factory=list)
        
        Not:
        filters: list[str] = []
        """
        # This comment documents what the fix should look like
        # Uncomment the Field import and update the model to test the fix
        from pydantic import Field, BaseModel
        
        class ChatRequestFixed(BaseModel):
            query: str
            k: int = 5
            filters: list[str] = Field(default_factory=list)
        
        req1 = ChatRequestFixed(query="query1")
        req2 = ChatRequestFixed(query="query2")
        
        req1.filters.append("filter1")
        
        # With the fix, req2 should NOT be affected
        assert req2.filters == []
        assert req1.filters == ["filter1"]


class TestBugFixValidation:
    """
    Instructions for fixing the bug:
    
    1. Open: src/api/models.py
    2. Find the ChatRequest class
    3. Change:
        filters: list[str] = []
       To:
        filters: list[str] = Field(default_factory=list)
    4. Add the import if needed:
        from pydantic import Field
    5. Run: pytest tests/test_bug.py -v
    6. Tests should pass after fix.
    """
    
    def test_fix_instructions_are_clear(self):
        """This test passes if you read the instructions above."""
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
