#! /usr/bin/env python

from flask_restful import Api, Resource

class Example(Resource):
    
    def get(self):
        """ An example restful api, always return status success
        ---
        parameters: []
        definitions:
            Status:
                type: object
                properties:
                    status:
                        type: string
        responses:
            200:
                description: Simple HTTP return
                schema:
                    $ref: '#/definitions/Status'
                examples:
                    status: 'success'
        """

        return {'status': 'success'}, 200
