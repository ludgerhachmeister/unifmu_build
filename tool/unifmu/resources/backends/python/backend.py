import json
import logging
import os
import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from pathlib import Path
import base64
from schemas.unifmu_fmi2_pb2 import Fmi2Command, Fmi2Return

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)

try:
    import zmq
except ImportError:
    logger.fatal(
        "unable to import the python library 'zmq' required by the schemaless backend. "
        "please ensure that the library is present in the python environment launching the script. "
        "the missing dependencies can be installed using 'python -m pip install unifmu[python-backend]'"
    )
    sys.exit(-1)

from fmi2 import Fmi2FMU
from model import Model


if __name__ == "__main__":

    # initializing message queue
    context = zmq.Context()

    socket = context.socket(zmq.REQ)

    dispatcher_endpoint = os.environ["UNIFMU_DISPATCHER_ENDPOINT"]

    logger.info(f"dispatcher endpoint received: {dispatcher_endpoint}")

    socket.connect(dispatcher_endpoint)

    ret = Fmi2Return()
    ret.Fmi2ExtHandshakeReturn.SetInParent()
    state = ret.SerializeToString()
    socket.send(state)

    # create slave object then use model description to create a mapping between fmi value references and attribute names of FMU

    reference_to_attr = {}
    with open(Path.cwd().parent / "modelDescription.xml") as f:
        for v in ET.parse(f).find("ModelVariables"):
            reference_to_attr[int(v.attrib["valueReference"])] = v.attrib["name"]

    slave: Fmi2FMU = Model(reference_to_attr)

    command = Fmi2Command()
    result = Fmi2Return()

    # event loop
    while True:

        result.Clear()

        logger.info(f"slave waiting for command")

        msg = socket.recv()
        command.ParseFromString(msg)

        logger.info(f"received command {command}")

        group = command.WhichOneof("command")

        data = getattr(command, command.WhichOneof("command"))

        if group == "Fmi2SetupExperiment":
            start_time = data.start_time
            stop_time = data.stop_time if data.has_stop_time else None
            tolerance = data.tolerance if data.has_tolerance else None
            result.Fmi2StatusReturn.status = slave.setup_experiment(
                start_time, stop_time, tolerance
            )
        elif group == "Fmi2DoStep":
            result.Fmi2StatusReturn.status = slave.do_step(
                data.current_time, data.step_size, data.no_step_prior
            )
        elif group == "Fmi2EnterInitializationMode":
            result.Fmi2StatusReturn.status = slave.enter_initialization_mode()
        elif group == "Fmi2ExitInitializationMode":
            result.Fmi2StatusReturn.status = slave.exit_initialization_mode()
        elif group == "Fmi2ExtSerializeSlave":
            (status, state) = slave.serialize()
            result.Fmi2ExtSerializeSlaveReturn.status = status
            result.Fmi2ExtSerializeSlaveReturn.state = state
        elif group == "Fmi2ExtDeserializeSlave":
            state = command.Fmi2ExtDeserializeSlave.state
            result.Fmi2StatusReturn.status = slave.deserialize(state)
        elif group == "Fmi2GetReal":
            status, values = slave.get_xxx(command.Fmi2GetReal.references)
            result.Fmi2GetRealReturn.status = status
            result.Fmi2GetRealReturn.values[:] = values
        elif group == "Fmi2GetInteger":
            status, values = slave.get_xxx(command.Fmi2GetInteger.references)
            result.Fmi2GetIntegerReturn.status = status
            result.Fmi2GetIntegerReturn.values[:] = values
        elif group == "Fmi2GetBoolean":
            status, values = slave.get_xxx(command.Fmi2GetBoolean.references)
            result.Fmi2GetBooleanReturn.status = status
            result.Fmi2GetBooleanReturn.values[:] = values
        elif group == "Fmi2GetString":
            status, values = slave.get_xxx(command.Fmi2GetString.references)
            result.Fmi2GetStringReturn.status = status
            result.Fmi2GetStringReturn.values[:] = values
        elif group == "Fmi2SetReal":
            status = slave.set_xxx(
                command.Fmi2SetReal.references, command.Fmi2SetReal.values
            )
            result.Fmi2StatusReturn.status = status
        elif group == "Fmi2SetInteger":
            status = slave.set_xxx(
                command.Fmi2SetInteger.references, command.Fmi2SetInteger.values
            )
            result.Fmi2StatusReturn.status = status
        elif group == "Fmi2SetBoolean":
            status = slave.set_xxx(
                command.Fmi2SetBoolean.references, command.Fmi2SetBoolean.values
            )
            result.Fmi2StatusReturn.status = status
        elif group == "Fmi2SetString":
            status = slave.set_xxx(
                command.Fmi2SetString.references, command.Fmi2SetString.values
            )
            result.Fmi2StatusReturn.status = status
        elif group == "Fmi2Terminate":
            result.Fmi2StatusReturn.status = slave.terminate()
        elif group == "Fmi2Reset":
            result.Fmi2StatusReturn.status = slave.reset()
        elif group == "Fmi2FreeInstance":
            logger.error(f"Fmi2FreeInstance received, shutting down")
            result.Fmi2StatusReturn.status = (
                0  # TODO Fmi2FreeInstance should not return a value
            )
            state = result.SerializeToString()

            socket.send(state)
            sys.exit(0)
        else:
            logger.error(f"unrecognized command '{group}' received, shutting down")
            sys.exit(-1)

        state = result.SerializeToString()
        socket.send(state)
