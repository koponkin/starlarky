import tempfile
from subprocess import PIPE, STDOUT, check_output, CalledProcessError

RUNNER_EXECUATBLE = 'larky-runner'
LOG_PARAM = '-l'
INPUT_PARAM = '-i'
OUTPUT_PARAM = '-o'
SCRIPT_PARAM = '-s'


def evaluate(script, input_data: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w+') as output_file, \
            tempfile.NamedTemporaryFile(mode='w+') as input_file, \
            tempfile.NamedTemporaryFile(mode='w+') as log_file:
        input_file.write(input_data)
        input_file.flush()
        __evaluate(script, input_file.name, output_file.name, log_file.name)
        print(log_file.read())
        return output_file.read()


def __evaluate(script, input_path, output_path, log_path):
    try:
        check_output([RUNNER_EXECUATBLE,
                      INPUT_PARAM, input_path,
                      OUTPUT_PARAM, output_path,
                      SCRIPT_PARAM, script,
                      LOG_PARAM, log_path], stderr=STDOUT)
    except CalledProcessError as e:
        raise FailedEvaluation(f'Starlark evaluation failed. \nOutput: {e.output}') from e


class FailedEvaluation(Exception):
    pass