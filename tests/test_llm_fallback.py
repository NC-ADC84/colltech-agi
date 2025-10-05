from colltech_agi_enhanced_backend import LLMIntegration


def test_llm_fallback_local_unreachable():
    # Use provider=local but assume no local server running; ensure fallback contains success=False and error_code
    llm = LLMIntegration(api_key=None, provider='local')
    res = llm.generate_response("Hello world", personality='lyra')
    assert isinstance(res.get('success'), bool)
    assert res.get('success') is False
    assert res.get('error_code') == 'llm_api_error'
