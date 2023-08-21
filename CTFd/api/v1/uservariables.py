from typing import List

from flask import request
from flask_restx import Namespace, Resource

from CTFd.api.v1.helpers.request import validate_args
from CTFd.api.v1.helpers.schemas import sqlalchemy_to_pydantic
from CTFd.api.v1.schemas import APIDetailedSuccessResponse, APIListSuccessResponse
from CTFd.constants import RawEnum
from CTFd.models import UserVariables, db
from CTFd.schemas.uservariables import UserVariableSchema
from CTFd.utils.decorators import admins_only, during_ctf_time_only
from CTFd.utils.decorators.visibility import check_challenge_visibility
from CTFd.utils.helpers.models import build_model_filters
from CTFd.utils.user import get_current_user, is_admin

uservariables_namespace = Namespace("uservariables", description="Endpoint to retrieve User Variables")

UserVariableModel = sqlalchemy_to_pydantic(UserVariables)


class UserVariableDetailedSuccessResponse(APIDetailedSuccessResponse):
    data: UserVariableModel


class UserVariableListSuccessResponse(APIListSuccessResponse):
    data: List[UserVariableModel]


uservariables_namespace.schema_model(
    "UserVariableDetailedSuccessResponse", UserVariableDetailedSuccessResponse.apidoc()
)

uservariables_namespace.schema_model(
    "UserVariableListSuccessResponse", UserVariableListSuccessResponse.apidoc()
)


@uservariables_namespace.route("")
class UserVariableList(Resource):
    @admins_only
    @uservariables_namespace.doc(
        description="Endpoint to list User Variable objects in bulk",
        responses={
            200: ("Success", "UserVariableListSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    @validate_args(
        {
            "user_id": (int, None),
            "challenge_id": (int, None),
            "variable_name": (str, None),
            "variable_value": (str, None),
            "q": (str, None),
            "field": (
                RawEnum("UserVariableFields", {"user_id": "user_id", "variable_name": "variable_name", "variable_value": "variable_value"}),
                None,
            ),
        },
        location="query",
    )
    def get(self, query_args):
        q = query_args.pop("q", None)
        field = str(query_args.pop("field", None))
        filters = build_model_filters(model=UserVariables,query=q, field=field)

        uservariables = UserVariables.query.filter_by(**query_args).filter(*filters).all()
        response = UserVariableSchema(many=True).dump(uservariables)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        return {"success": True, "data": response.data}

    @admins_only
    @uservariables_namespace.doc(
        description="Endpoint to create a User Variable object",
        responses={
            200: ("Success", "UserVariableDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def post(self):
        req = request.get_json()
        print(req)
        schema = UserVariableSchema()
        response = schema.load(req, session=db.session)
        print(response.data)
        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        db.session.add(response.data)
        db.session.commit()

        response = schema.dump(response.data)

        return {"success": True, "data": response.data}
    
@uservariables_namespace.route("/<uservariable_id>")
class UserVariable(Resource):
    @during_ctf_time_only
    @check_challenge_visibility
    @uservariables_namespace.doc(
        description="Endpoint to get a specific User Variable object",
        responses={
            200: ("Success", "UserVariableDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def get(self, uservariable_id):
        uservariable = UserVariables.query.filter_by(id=uservariable_id).first_or_404()
        schema = UserVariableSchema()
        response = schema.dump(uservariable)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        return {"success": True, "data": response.data}

    @admins_only
    @uservariables_namespace.doc(
        description="Endpoint to edit a specific User Variable object",
        responses={
            200: ("Success", "UserVariableDetailedSuccessResponse"),
            400: (
                "An error occured processing the provided or stored data",
                "APISimpleErrorResponse",
            ),
        },
    )
    def patch(self, uservariable_id):
        uservariable = UserVariables.query.filter_by(id=uservariable_id).first_or_404()
        req = request.get_json()

        schema = UserVariableSchema()
        response = schema.load(req, instance=uservariable, partial=True, session=db.session)

        if response.errors:
            return {"success": False, "errors": response.errors}, 400

        db.session.add(response.data)
        db.session.commit()

        response = schema.dump(response.data)

        return {"success": True, "data": response.data}

    @admins_only
    @uservariables_namespace.doc(
        description="Endpoint to delete a specific User Variable object",
        responses={200: ("Success", "APISimpleSuccessResponse")},
    )
    def delete(self, uservariable_id):
        uservariable = UserVariables.query.filter_by(id=uservariable_id).first_or_404()
        db.session.delete(uservariable)
        db.session.commit()
        db.session.close()

        return {"success": True}
