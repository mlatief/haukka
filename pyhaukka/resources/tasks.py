from flask_restful import Resource, reqparse, inputs
from flask import Response

from pyhaukka.worker import process_trial

class Tasks(Resource):
    def post(self):
        from pyhaukka.app import api
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=inputs.url)

        args = parser.parse_args(strict=True)
        url = args.get('url')
        task = process_trial.delay(url)
        task_url = api.url_for(Task, task_id=task.id)
        return Response(status=202, headers={'Location': task_url})

class Task(Resource):
    def get(self, task_id):
        task = process_trial.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'status': str(task.info),  # this is the exception raised
            }

        return response
