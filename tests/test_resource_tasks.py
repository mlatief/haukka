import os
import unittest
import urlparse
import ujson

from resource_test_base import ResourcesTestCase, app
from pyhaukka.worker import process_trial
from httmock import urlmatch, HTTMock

@urlmatch(netloc=r'(.*\.)?clinicaltrials\.gov$')
def ct_gov_mock(url, request):
    xml = file('tests/small_ct.xml').read()
    return xml

@urlmatch(netloc=r'(.*\.)?clinicaltrials\.gov$')
def ct_dummy_mock(url, request):
    xml = "<ct><id_info><nct_id>NCTnnn</nct_id></id_info></ct>"
    return xml


class TasksTestCase(ResourcesTestCase):
    ct_url = 'https://clinicaltrials.gov/show/NCT02034110?displayxml=true'

    def setUp(self):
        super(TasksTestCase, self).setUp()
        from pyhaukka.worker import celery_app
        celery_app.conf.update(CELERY_ALWAYS_EAGER=True, CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)

    def test_post_tasks(self):
        with HTTMock(ct_gov_mock):
            with app.test_client() as c:
                rv = c.post('/tasks', data={'url':self.ct_url})
                loc = rv.headers['Location']
                assert loc is not None
                id = os.path.basename(urlparse.urlparse(loc).path)
                assert id is not None
                t = process_trial.AsyncResult(id)
                assert t is not None
                assert t.state == 'PROGRESS'
                assert t.info.get('status', '') == 'Storing clinical trial'

    def test_get_task(self):
        with HTTMock(ct_dummy_mock):
            t = process_trial.delay(self.ct_url)
            id = t.id
        with app.test_client() as c:
            rv = c.get('/tasks/' + id)
            assert rv is not None
            self.check_content_type(rv.headers)
            data = ujson.loads(rv.data)
            assert data is not None
            assert data['state'] == 'PROGRESS'
            assert data['status'] == 'Storing clinical trial'

if __name__ == '__main__':
    unittest.main()
