""""
SCC Hypervisor Collect CLI Implementation
"""
import argparse
import logging

from scc_hypervisor_collector import __version__ as cli_version
from scc_hypervisor_collector import ConfigManager


def main() -> None:
    """Implements CLI for the scc-hypervisor-gatherer."""

    parser = argparse.ArgumentParser(
        description="Collect configured hypervisor details and upload to "
                    "SUSE Customer Center (SCC)."
    )

    # General purpose options
    parser.add_argument('-V', '--version', action='version',
                        version="%(prog)s " + str(cli_version))

    # Output verbosity control
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-q', '--quiet', action='store_true',
                           help="Decrease output verbosity.")
    verbosity.add_argument('-v', '--verbose', action='store_true',
                           help="Increase output verbosity.")

    # Primary command line options
    parser.add_argument('-c', '--config', default='scchvc.yaml',
                        help="The YAML config file to use.")
    parser.add_argument('--config_dir', '--config-dir',
                        default='~/.config/scc-hypervisor-collector',
                        help="The config directory to check for YAML "
                             "config files.")
    parser.add_argument('-C', '--check', action='store_true',
                        help="Check the configuration data only, "
                             "reporting any errors.")

    args = parser.parse_args()

    if args.quiet:
        log_level = logging.WARN
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)

    cfg_mgr = ConfigManager(config_file=args.config,
                            config_dir=args.config_dir)

    logging.info("ConfigManager: config_data = %s", repr(cfg_mgr.config_data))


__all__ = ['main']