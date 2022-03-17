# from typing import Dict
#
# from project.dao import UserDAO
# from project.exceptions import InvalidCredentials
# from project.services import BaseService
# from project.services.schemas import UserSchema
# from project.utils.jwt_token import JwtToken
# from project.utils.security import compare_passwords
#
#
# class CheckUserCredentialsService(BaseService):
#     def execute(self, email: str, password: str) -> Dict[str, str]:
#         if not (user := UserDAO(self._db_session).get_user_by_email(email)):
#             raise InvalidCredentials
#
#         if not compare_passwords(user.password, password):
#             raise InvalidCredentials
#
#         return JwtToken(UserSchema().dump(user)).get_tokens()
