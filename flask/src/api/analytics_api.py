from src.services.analytics_service import Analitics

from flask import Blueprint

bp = Blueprint("analytics", __name__, url_prefix="/analytics")

bp.add_url_rule("/load-data", view_func=Analitics.load_data, methods=["POST"])
