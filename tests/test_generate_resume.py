import json
import pytest
from src.generate import completed_keys


def test_resume_preserves_completed_evidence_and_rejects_changes(tmp_path):
    target=tmp_path/'generation.jsonl'
    config={'model':'fixed'}
    (tmp_path/'generator_config.json').write_text(json.dumps(config))
    row={'query_id':'q','system':'B1','ranking':['d']}
    target.write_text(json.dumps(row)+'\n')
    assert completed_keys(target,[row],config)=={('q','B1')}
    with pytest.raises(ValueError):completed_keys(target,[row],{'model':'changed'})
    with pytest.raises(ValueError):completed_keys(target,[dict(row,ranking=['other'])],config)
    target.write_text((json.dumps(row)+'\n')*2)
    with pytest.raises(ValueError):completed_keys(target,[row],config)
