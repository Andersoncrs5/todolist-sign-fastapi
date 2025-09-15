from api.utils.res.response_body import ResponseBody
from typing import Final, Dict

RESPONSE_401: Final[Dict] = {
    "description": "Token invalid",
    "model": ResponseBody[None]
}

RESPONSE_404_USER: Final[Dict] = {
    "description": "User not found",
    "model": ResponseBody[None]
}
