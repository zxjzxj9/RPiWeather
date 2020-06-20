#! /usr/bin/env python

from flask_restful import Api, Resource

class DateWeather(Resource):

    def get(self):
        """ Get the weather from start to end date interval
        ---
        parameters:
            - name: start
              in: body
              description: "weather record starting datetime"
              required: true
              type: string
              format: date-time
            - name: end
              in: body
              description: "weather record ending datetime"
              required: true
              type: string
              format: date-time

        definitions:
            DateWeather:
                type: object
                properties:
                    timestamp:
                        type: array
                        items:
                            type: string
                            format: date-time


        responses:
            200:
                description: Response the weather data from database
                schema:


