import pytest
from src.score_answers import score


def test_missing_labels_are_not_success():
    r=score([{'system':'A'}])['A']
    assert r['faithfulness_micro'] is None and r['human_correctness'] is None
    r=score([{'system':'A','supported_claims':2,'unsupported_claims':1}])['A']
    assert r['faithfulness_micro']==pytest.approx(2/3)
    assert r['hallucination_rate_factual_responses']==1
    with pytest.raises(ValueError):score([{'system':'A','supported_claims':-1,'unsupported_claims':0}])


def test_bootstrap_constant_difference():
    from src.analyze import bootstrap
    assert bootstrap([.2,.2,.2],['a','a','b'],n=50)==pytest.approx([.2,.2])


def test_binary_annotation_validation():
    with pytest.raises(ValueError):score([{'system':'A','human_correctness':2}])
