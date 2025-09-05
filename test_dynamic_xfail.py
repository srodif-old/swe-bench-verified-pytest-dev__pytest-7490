"""Test for the dynamic xfail marker issue"""

def test_dynamic_xfail_marker_in_test_function(testdir):
    """Test that dynamically adding xfail marker during test execution works"""
    testdir.makepyfile(test_foo="""
        import pytest

        def test_xfail_test(request):
            mark = pytest.mark.xfail(reason="xfail")
            request.node.add_marker(mark)
            assert 0
    """)

    result = testdir.runpytest("-rsx")
    result.assert_outcomes(skipped=1, failed=0)
    # Should be marked as xfail, not failed
    assert "XFAIL" in result.stdout.str()


def test_dynamic_xfail_marker_in_fixture(testdir):
    """Test that dynamically adding xfail marker in fixture works"""
    testdir.makepyfile(test_foo="""
        import pytest

        @pytest.fixture
        def add_xfail_marker(request):
            mark = pytest.mark.xfail(reason="xfail from fixture") 
            request.node.add_marker(mark)

        def test_xfail_test(add_xfail_marker):
            assert 0
    """)

    result = testdir.runpytest("-rsx")
    result.assert_outcomes(skipped=1, failed=0)
    assert "XFAIL" in result.stdout.str()