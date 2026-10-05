import json
import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request


def invalid_response(error, status):
    response_body = {
        'error': error,
    }
    return request.make_json_response(response_body, status)


def valid_response(data, status, pagination_info):
    response_body = {
        'message': "success",
        'data': data
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):
    @http.route("/api/property", methods=["GET"], auth="none", type="http", csrf=False)
    def property_api_endpoint(self):
        print("successfully")

    @http.route("/v1/property", methods=["POST"], auth="none", type="http", csrf=False)
    def property_api_endpoint_post(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("name"):
            return request.make_json_response({
                "error": " must by create your name",
            })
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return valid_response({
                    "message": "Property created",
                    "id": res.id,
                    "name": res.name,
                }, status=200)
        except Exception as error:

            return request.make_json_response({
                "error": " Property not created",
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], auth="none", type="http", csrf=False)
    def property_api_endpoint_put(self, property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        property_id.write(vals)

        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            property_id.write(vals)
            if property_id:
                return valid_response({
                    "message": "Property updated",
                    "updated": vals
                }, status=200)
            else:
                return request.make_json_response({
                    'error': " his id is not fiend yuo must by change id",
                }, status=400)
        except Exception as error:
            return request.make_json_response({
                "error": " his id is not fiend",
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], auth="none", type="http", csrf=False)
    def property_api_endpoint_get(self, property_id):

        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": " his id is not fiend yuo must by change id",
                }, status=400)
            return valid_response({
                "name": property_id.name,
                "id": property_id.id,
                "description": property_id.description,
                "bedrooms": property_id.bedrooms,
                "owner_id": property_id.owner_id.id,
                "owner": property_id.owner_id.name,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": " his id is not fiend yuo must by change id",
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], auth="none", type="http", csrf=False)
    def property_api_endpoint_delete(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": " his id is not fiend yuo must by change id"

                }, status=400)

            property_id.unlink()
            return valid_response({
                "message": "Property deleted",
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": " his id is not fiend yuo must by change id"
            }, status=400)

    @http.route("/v1/property", methods=["GET"], auth="none", type="http", csrf=False)
    def property_api_endpoint_set_data(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            page = offset = None
            limit = 3
            if params:
                if params.get('page'):
                    page = int(params.get('page')[0])
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
            if page:
                offset = (page * limit) - limit
            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]
            res = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id desc')
            print("DEBUG >>> limit:", limit, "offset:", offset, "len(res):", len(res))
            res_count = request.env['property'].sudo().search_count(property_domain)
            if not res:
                return request.make_json_response({
                    "error": "no data found",
                }, status=400)
            return valid_response([{
                "name": property_id.name,
                "id": property_id.id,
                "description": property_id.description,
                "bedrooms": property_id.bedrooms,
                "owner_id": property_id.owner_id.id,
                "owner": property_id.owner_id.name,
            } for property_id in res], pagination_info={
                'page': page if page else 1,
                'limit': limit,
                'count': res_count,
                'pages': math.ceil(res_count / limit) if limit else 1,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": " don't have data"
            }, status=400)
