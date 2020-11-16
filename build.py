import argparse
from os import popen, system
from pathlib import Path
import logging
import shutil
from shutil import SameFileError
import subprocess
import os
import sys
from sys import executable, platform
import platform
from tempfile import TemporaryDirectory
from os import makedirs


from unifmu.generate import generate_fmu_from_backend, get_backends


class Chdir:
    def __init__(self, wd):
        wd = Path(wd)
        self.old_wd = Path.cwd()
        self.wd = wd

    def __enter__(self):
        os.chdir(self.wd)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_wd)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__file__)

    parser = argparse.ArgumentParser()

    # ----------- here we resolve file paths -----------------------

    s = platform.system()

    integration_tests_executable = (
        (
            Path("tests/c_tests/build")
            / {
                "Windows": "Debug/integration_tests.exe",
                "Linux": "integration_tests",
                "Darwin": "integration_tests",
            }[s]
        )
        .absolute()
        .__fspath__()
    )
    print(integration_tests_executable)
    binary_basename = "unifmu"

    # note that lib prefix is removed
    input, output = {
        "Linux": (f"lib{binary_basename}.so", f"linux64/{binary_basename}.so"),
        "Windows": (f"{binary_basename}.dll", f"win64/{binary_basename}.dll"),
        "Darwin": (f"lib{binary_basename}.dylib", f"darwin64/{binary_basename}.dylib"),
    }[s]

    wrapper_in = Path(f"wrapper/target/debug/{input}").absolute().__fspath__()
    wrapper_out = Path(
        f"tool/unifmu/resources/common/unifmu_binaries/{output}").absolute()
    makedirs(wrapper_out.parent, exist_ok=True)
    wrapper_out = wrapper_out.__fspath__()

    # -------------- parse args -------------------------

    parser.add_argument(
        "--update-wrapper",
        "-u",
        dest="update_wrapper",
        action="store_true",
        help="updates the shared object inside the example FMUs",
    )

    parser.add_argument(
        "--test-rust",
        dest="test_rust",
        action="store_true",
        help="run rust integration tests",
    )

    parser.add_argument(
        "--test-c", dest="test_c", action="store_true", help="run C integration tests"
    )

    parser.add_argument(
        "--export-examples", dest="export_examples", action="store_true", help="copy example FMUs to the examples directory"
    )

    args = parser.parse_args()

    if args.update_wrapper:

        logger.info("building wrapper")
        with Chdir("wrapper"):
            res = subprocess.Popen(args=["cargo", "build"]).wait()

        if res != 0:
            logger.error("wrapper failed to build")
            sys.exit(-1)

        logger.info(
            f"wrapper was build, copying from '{wrapper_in}' to '{wrapper_out}'"
        )

        try:
            shutil.copy(src=wrapper_in, dst=wrapper_out)
        except SameFileError:
            pass

        logger.info("wrapper updated")

    if args.export_examples:

        for b in get_backends():
            outdir = Path(f"examples/{b}_fmu")
            generate_fmu_from_backend(b, outdir)

    if args.test_rust:
        res = subprocess.Popen(["cargo", "test"]).wait()

        if res != 0:
            logger.error("Rust test failed")
            sys.exit(-1)

    if args.test_c:

        # build tests
        build_dir = Path("tests/c_tests/build")
        build_dir.mkdir(exist_ok=True)

        with Chdir(build_dir):
            logger.info("configuring cmake")
            res = subprocess.Popen(
                args=["cmake", "-DCMAKE_BUILD_TYPE=Debug", ".."]
            ).wait()

            if res != 0:
                logger.error("unable to configure cmake")
                sys.exit(-1)

            logger.info("building tests")
            res = subprocess.Popen(args=["cmake", "--build", "."]).wait()

            if res != 0:
                logger.error("unable to compile C integration tests")
                sys.exit(-1)

        # export test examples into tmp directory and execute tests
        with TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            fmu_path = tmpdir / "python_fmu"
            generate_fmu_from_backend("python", fmu_path)

            resources_uri = (fmu_path / "resources").absolute().as_uri()

            logger.info("running C integration tests")
            res = subprocess.Popen(
                args=[integration_tests_executable,
                      wrapper_out, resources_uri]
            ).wait()

            if res != 0:
                logger.error("C integration tests failed")
                sys.exit(-1)

            logger.info("C integration tests successful")
