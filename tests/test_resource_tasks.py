import os
import unittest
import urlparse
import ujson

from resource_test_base import ResourcesTestCase, app
from pyhaukka.worker import process_trial

class TasksTestCase(ResourcesTestCase):
    ct_url = 'https://clinicaltrials.gov/show/NCT02034110?displayxml=true'
    def test_post_tasks(self):
        with app.test_client() as c:
            rv = c.post('/tasks', data={'url':self.ct_url})
            loc = rv.headers['Location']
            assert loc is not None
            id = os.path.basename(urlparse.urlparse(loc).path)
            assert id is not None
            t = process_trial.AsyncResult(id)
            assert t is not None
            assert t.state in ['PENDING', 'FAILURE', 'SUCCESS']
            print t.state

    def test_get_task(self):
        t = process_trial.delay(self.ct_url)
        id = t.id
        with app.test_client() as c:
            rv = c.get('/tasks/' + id)
            assert rv is not None
            self.check_content_type(rv.headers)
            data = ujson.loads(rv.data)
            assert data is not None
            assert data['state'] in ['PENDING', 'FAILURE', 'SUCCESS']
            assert data['status'] is not None
            print data['state']
            print data['status']

if __name__ == '__main__':
    unittest.main()
