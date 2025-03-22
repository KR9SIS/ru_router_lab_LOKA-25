"""
Script which calls all attack scripts within vuln_tests
"""

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run


def validate_input(ip: str, test: str, out_file: str) -> tuple[Path, Path | None]:
    """
    Validate the input passed through by args
    """
    if ip.lower() == "localhost":
        ip = "127.0.0.1"
    else:
        ip_lis: list[str] = ip.split(".")
        assert (
            len(ip_lis) == 4
        ), "An IPv4 address must contain 4 numbers seperated by a dot (.). E.g. '127.0.0.1'"
        for num in ip_lis:
            assert (
                num.isnumeric()
            ), "And IPv4 address only contains dots (.) and numbers. E.g. '127.0.0.1'"
        del ip_lis
    assert isinstance(test, str)
    assert isinstance(out_file, str)

    vuln_tests: Path = Path.cwd().joinpath("vuln_tests")
    if test:
        script: Path = vuln_tests.joinpath(test)
        assert (
            script.exists()
        ), "Please input valid filename within vuln_tests. E.g. 'filename.py'"
        return (vuln_tests, script)
    return (vuln_tests, None)


def call_script(script: Path, ip: str):
    """
    Wrapper around subprocess.run to call a given script with an ip address
    """
    return run(
        ["python3", str(script), "-ip", ip],
        check=True,
        capture_output=True,
    ).stdout.decode()


def main(ip: str, test: str, out_file: str):
    """
    Goes into vuln_tests
    Iterates over each script within it or grabs a specific
    one and runs its test
    """
    try:
        (vuln_tests, script) = validate_input(ip, test, out_file)
    except AssertionError as error_note:
        print(error_note)
        return

    if out_file:
        with open(out_file, "w", encoding="utf-8") as file:
            if script:
                print(call_script(script, ip), file=file)
            else:
                for script in vuln_tests.iterdir():
                    if script.suffix == ".py":
                        print(call_script(script, ip), file=file)
        return

    if script:
        print(call_script(script, ip))

        return

    for script in vuln_tests.iterdir():
        if script.suffix == ".py":
            print(call_script(script, ip))

    return


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="main", description="Parser to accept an IP address to test"
    )
    parser.add_argument(
        "-ip",
        action="store",
        type=str,
        default="127.0.0.1",
        required=False,
        help="Use an IP other than localhost",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store",
        type=str,
        default="",
        required=False,
        help="Run specific test",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        default="",
        required=False,
        help="Send test output to file",
    )
    args = parser.parse_args()

    main(args.ip, args.test, args.file)
