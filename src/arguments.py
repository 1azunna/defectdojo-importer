import argparse
from pathlib import Path
from models.common import ImportTypes, SeverityLevel, ReimportConditions


def main_parser():
    """
    The main_parser parses all arguments defined in this function.
    """

    # Create a parent parser with shared arguments (excluding file and import-type)
    parent_parser = argparse.ArgumentParser(
        prog="defectdojo-importer", description="Defect Dojo CI tool for importing scan findings"
    )
    import_args = parent_parser.add_argument_group("Scan Import Configuration")
    import_args.add_argument("-f", "--file", type=Path, help="File to import")
    import_args.add_argument(
        "-t",
        "--import-type",
        type=str,
        default=ImportTypes.FINDINGS.value,
        choices=[import_type.value for import_type in ImportTypes],
        help="Type of import: findings or languages, default is findings.",
    )

    # DefectDojo Configuration Group for parent parser
    dd_config_group = parent_parser.add_argument_group("DefectDojo Configuration")
    dd_config_group.add_argument("--api-url", type=str, help="DefectDojo API URL")
    dd_config_group.add_argument("--api-key", type=str, help="DefectDojo API Key")
    dd_config_group.add_argument("--product-name", type=str, help="Product name")
    dd_config_group.add_argument("--product-type-name", type=str, help="Product type name")
    dd_config_group.add_argument(
        "--critical-product", action="store_true", help="Is product critical?"
    )
    dd_config_group.add_argument("--product-platform", type=str, help="Product platform")

    # Test Configuration Group for parent parser
    test_config_group = parent_parser.add_argument_group("Test Configuration")
    test_config_group.add_argument("--engagement-name", type=str, help="Engagement name")
    test_config_group.add_argument("--test-name", type=str, help="Test name")
    test_config_group.add_argument("--test-type-name", type=str, help="Test type name")
    test_config_group.add_argument("--static-tool", action="store_true", help="Is static tool?")
    test_config_group.add_argument("--dynamic-tool", action="store_true", help="Is dynamic tool?")
    test_config_group.add_argument(
        "--tool-configuration-name", type=str, help="Tool configuration name"
    )
    test_config_group.add_argument(
        "--tool-configuration-params",
        type=str,
        help="Additional tool configuration parameters as comma-separated values. Max of 3 parameters.",
    )

    # Scan Settings Group for parent parser
    scan_settings_group = parent_parser.add_argument_group("Scan Settings")
    scan_settings_group.add_argument(
        "--minimum-severity",
        type=str,
        choices=[severity.value for severity in SeverityLevel],
        help="Minimum severity level",
    )
    scan_settings_group.add_argument(
        "--push-to-jira", action="store_true", default=False, help="Push to Jira?"
    )
    scan_settings_group.add_argument(
        "--close-old-findings", action="store_true", default=True, help="Close old findings?"
    )
    scan_settings_group.add_argument(
        "--reimport",
        action="store_true",
        default=False,
        help="Reimport findings instead of creating a new test",
    )
    scan_settings_group.add_argument(
        "--reimport-condition",
        type=str,
        choices=[condition.value for condition in ReimportConditions],
        help="Condition for reimporting findings",
    )

    # Build/CI Information Group for parent parser
    ci_info_group = parent_parser.add_argument_group("Build/CI Information")
    ci_info_group.add_argument("--build-id", type=str, help="Build ID")
    ci_info_group.add_argument("--commit-hash", type=str, help="Commit hash")
    ci_info_group.add_argument("--branch-tag", type=str, help="Branch or tag")
    ci_info_group.add_argument("--scm-uri", type=str, help="SCM URI")

    # General Options Group for parent parser
    general_group = parent_parser.add_argument_group("General Options")
    general_group.add_argument(
        "-v", "--verbose", dest="debug", action="store_true", help="Enable verbose/debug logging."
    )
    general_group.add_argument(
        "-i", "--insecure", action="store_true", default=False, help="Disable ssl verification."
    )

    # Create a parent parser with shared arguments (excluding subparsers)
    integrations_parent_parser = argparse.ArgumentParser(add_help=False)
    # Copy all arguments from main parser to parent parser (excluding subparsers)
    for action in parent_parser._actions:
        if action.dest not in ["file", "import_type", "product_api_scan", "subcommands"]:
            integrations_parent_parser._add_action(action)
    for group in parent_parser._action_groups:
        if group.title != "Scan Import Configuration":
            integrations_parent_parser._action_groups.append(group)

    # Subparsers for integration
    subparsers = parent_parser.add_subparsers(dest="sub_command", title="Sub-commands", metavar="")
    integration_parser = subparsers.add_parser(
        "integration",
        help="Import findings from supported external integrations",
        parents=[integrations_parent_parser],
        add_help=False,
    )
    integration_subparsers = integration_parser.add_subparsers(
        dest="integration_type", title="Available external integrations options", metavar=""
    )

    dtrack_parser = integration_subparsers.add_parser(
        "dtrack",
        help="Setup and trigger Dependency-Track findings import.",
        parents=[integrations_parent_parser],
        add_help=False,
    )
    # Add dtrack-specific arguments first
    dtrack_parser.add_argument("--dtrack-api-url", type=str, help="Dependency-Track API URL")
    dtrack_parser.add_argument("--dtrack-api-key", type=str, help="Dependency-Track API Key")
    dtrack_parser.add_argument(
        "--dtrack-project-name", type=str, help="Dependency-Track project name"
    )
    dtrack_parser.add_argument(
        "--dtrack-project-version", type=str, help="Dependency-Track project version"
    )
    dtrack_parser.add_argument(
        "--dtrack-reimport", action="store_true", help="Dependency-Track reimport"
    )
    dtrack_parser.add_argument(
        "--dtrack-reactivate", action="store_true", help="Dependency-Track reactivate"
    )

    return parent_parser
