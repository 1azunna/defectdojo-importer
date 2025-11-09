import sys
import logging
from .findings import setup_product_engagement, setup_test, import_findings, integration_findings
from .languages import import_languages
from .validations import validate_config
from arguments import main_parser
from http_client import HttpClient
from defectdojo import DefectDojo
from models.exceptions import ConfigurationError

LOGGER_NAME = "defectdojo_importer"
logging.basicConfig(format="%(levelname)s - %(message)s")
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)
logger.propagate = True


class Importer:
    @staticmethod
    def run(args: list[str]):
        if len(args) == 0:
            main_parser().print_help()
            sys.exit(0)
        else:
            parsed_args = main_parser().parse_args(args)
            try:
                config = validate_config(parsed_args)
            except ConfigurationError as e:
                main_parser().print_help()
                logger.error(f"Configuration error: {e}")
                sys.exit(1)
            client = HttpClient(config.api_url, ssl_verify=parsed_args.insecure, logger=logger)
            defectdojo = DefectDojo(client, config.api_key)
            engagement_config = setup_product_engagement(defectdojo, config)

            if parsed_args.sub_command == "integration":
                match parsed_args.integration_type:
                    case "dtrack":
                        client = HttpClient(
                            str(config.dtrack_api_url),
                            ssl_verify=parsed_args.insecure,
                            logger=logger,
                        )
                integration_findings(
                    client, config, engagement_config["engagement_id"], parsed_args.integration_type
                )

            elif parsed_args.import_type == "findings":
                test_config = setup_test(defectdojo, config, engagement_config)
                import_findings(
                    defectdojo, config, parsed_args.file, test_config, engagement_config
                )
            elif parsed_args.import_type == "languages":
                import_languages(
                    defectdojo, config, engagement_config["product_id"], str(parsed_args.file)
                )
