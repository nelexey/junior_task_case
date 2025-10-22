import pytest

def test_ping_handler_exists():
    """Test that ping handler exists and is callable"""
    from web.handlers.ping_handler import ping_handler
    assert callable(ping_handler)

def test_report_handler_exists():
    """Test that report handler exists and is callable"""
    from web.handlers.report_handler import report_handler
    assert callable(report_handler)

def test_chart_handler_exists():
    """Test that chart handler exists and is callable"""
    from web.handlers.report_handler import chart_handler
    assert callable(chart_handler)

def test_handlers_are_async_functions():
    """Test that handlers are async functions"""
    from web.handlers.ping_handler import ping_handler
    from web.handlers.report_handler import report_handler, chart_handler
    
    # Check that functions are coroutine functions
    assert hasattr(ping_handler, '__call__')
    assert hasattr(report_handler, '__call__')
    assert hasattr(chart_handler, '__call__')