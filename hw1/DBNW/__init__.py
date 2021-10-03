
# import json
# from flask import Flask, request
# # from graphene_schema import schema
# from graphene import Schema

# app = Flask(__name__)

# @app.route('/')
# def graphql():
#     query = request.args.get('query')
#     result = Schema.execute(query)
#     d = json.dumps(result.data)
#     return '{}'.format(d)

#Python HTTP server for GraphQL.

#import graphene_schema 

from flask import Flask
from graphene_schema import schema
from flask_graphql import GraphQLView
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.add_url_rule('/', view_func=GraphQLView.as_view('graphql',
                 schema=schema, graphiql=True))
app.run(debug=True)