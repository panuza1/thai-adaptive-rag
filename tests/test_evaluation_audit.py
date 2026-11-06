import pytest

from src.audit_retrieval import audit
from src.core import metrics


def sample():
    queries = [{'id': 'q', 'split': 'test', 'group': 'article', 'relevant': ['d1']}]
    documents = [{'id': 'd1'}, {'id': 'd2'}]
    rankings = {'B1': ['d2'], 'B2': ['d1'], 'B3': ['d1'], 'P1:none': ['d2']}
    rows = []
    for system, ranking in rankings.items():
        rows.append({'query_id': 'q', 'group': 'article', 'system': system, 'repeat': 0,
                     'ranking': ranking, 'retrieval_seconds': {'B1': .01, 'B2': .02, 'B3': 1, 'P1:none': .2}[system],
                     **metrics(ranking, {'d1'}, 1)})
    return queries, documents, ['q'], rows, {'k': 1, 'repeats': 1}


def test_audit_validates_qrels_and_cost_oracle():
    result = audit(*sample())
    assert result['validated_primary_rows'] == 4
    assert result['gold_chunks_per_query'] == {1: 1}
    assert result['recall_at_5_is_binary_on_this_sample']
    assert result['oracle']['best_static_per_query_ndcg'] == 1
    assert result['oracle']['cheapest_static_selection_counts'] == {'B2': 1}
    assert result['shared_recall_failures'] == 0


def test_audit_rejects_incorrect_stored_metrics():
    queries, documents, frozen, rows, config = sample()
    rows[0]['recall'] = 1
    with pytest.raises(ValueError, match='score does not match'):
        audit(queries, documents, frozen, rows, config)


def test_multigold_recall_is_not_binary():
    queries, documents, frozen, rows, config = sample()
    queries[0]['relevant'] = ['d1', 'd2']
    for row in rows:
        row.update(metrics(row['ranking'], {'d1', 'd2'}, 1))
    result = audit(queries, documents, frozen, rows, config)
    assert not result['recall_at_5_is_binary_on_this_sample']
    assert result['gold_chunks_per_query'] == {2: 1}
    assert result['oracle']['best_static_per_query_recall'] == .5
