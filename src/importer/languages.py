from defectdojo import DefectDojo
from models.config import Config
from common.utils import get_files


def import_languages(defectdojo: DefectDojo, config: Config, product_id: int, filename: str):
    """Import Languages and Lines of Code into DefectDojo API."""

    files = get_files(filename)
    return defectdojo.languages.upload(product_id, files)
