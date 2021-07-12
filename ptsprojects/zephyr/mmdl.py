#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

"""MMDL test cases"""

try:
    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp
    from ptsprojects.zephyr.ztestcase import ZTestCase, ZTestCaseSlave

except ImportError:  # running this module as script
    import sys
    import os
    # to be able to locate the following imports
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")

    from ptsprojects.testcase import TestCase, TestCmd, TestFunc, \
        TestFuncCleanUp
    from ptsprojects.zephyr.ztestcase import ZTestCase, ZTestCaseSlave


from pybtp import defs, btp
from pybtp.types import MeshVals
from ptsprojects.stack import get_stack
from ptsprojects.stack import SynchPoint
from wid import mmdl_wid_hdl
from uuid import uuid4
from binascii import hexlify
import random
from time import sleep


device_uuid = hexlify(uuid4().bytes)
device_uuid2 = hexlify(uuid4().bytes)


def set_pixits(ptses):
    """Setup MMDL profile PIXITS for workspace. Those values are used for test
    case if not updated within test case.

    PIXITS always should be updated accordingly to project and newest version of
    PTS.

    pts -- Instance of PyPTS"""

    pts = ptses[0]

    pts.set_pixit("MMDL", "TSPX_bd_addr_iut", "DEADBEEFDEAD")
    pts.set_pixit("MMDL", "TSPX_time_guard", "300000")
    pts.set_pixit("MMDL", "TSPX_use_implicit_send", "TRUE")
    pts.set_pixit("MMDL", "TSPX_tester_database_file",
                  "C:\Program Files\Bluetooth SIG\Bluetooth PTS\Data\SIGDatabase\PTS_SMPP_db.xml")
    pts.set_pixit("MMDL", "TSPX_mtu_size", "23")
    pts.set_pixit("MMDL", "TSPX_delete_link_key", "TRUE")
    pts.set_pixit("MMDL", "TSPX_delete_ltk", "TRUE")
    pts.set_pixit("MMDL", "TSPX_security_enabled", "FALSE")
    pts.set_pixit("MMDL", "TSPX_iut_setup_att_over_br_edr", "FALSE")
    pts.set_pixit("MMDL", "TSPX_scan_interval", "30")
    pts.set_pixit("MMDL", "TSPX_scan_window", "30")
    pts.set_pixit("MMDL", "TSPX_scan_filter", "00")
    pts.set_pixit("MMDL", "TSPX_advertising_interval_min", "160")
    pts.set_pixit("MMDL", "TSPX_advertising_interval_max", "160")
    pts.set_pixit("MMDL", "TSPX_tester_OOB_information", "F87F")
    pts.set_pixit("MMDL", "TSPX_device_uuid", device_uuid)
    pts.set_pixit("MMDL", "TSPX_device_uuid2", device_uuid2)
    pts.set_pixit("MMDL", "TSPX_use_pb_gatt_bearer", "FALSE")
    pts.set_pixit("MMDL", "TSPX_iut_comp_data_page", "0")
    pts.set_pixit("MMDL", "TSPX_OOB_state_change", "FALSE")
    pts.set_pixit("MMDL", "TSPX_sensor_property_ids", "0069,0010,FFF0")
    pts.set_pixit("MMDL", "TSPX_enable_IUT_provisioner", "FALSE")
    pts.set_pixit("MMDL", "TSPX_cadence_property_IDs", "0069,0010,FFF0")


def test_cases(ptses):
    """Returns a list of MMDL test cases
    pts -- Instance of PyPTS"""

    pts = ptses[0]

    stack = get_stack()

    out_actions = [defs.MESH_OUT_DISPLAY_NUMBER,
                   defs.MESH_OUT_DISPLAY_STRING,
                   defs.MESH_OUT_DISPLAY_NUMBER | defs.MESH_OUT_DISPLAY_STRING]
    in_actions = [defs.MESH_IN_ENTER_NUMBER,
                  defs.MESH_IN_ENTER_STRING,
                  defs.MESH_IN_ENTER_NUMBER | defs.MESH_IN_ENTER_STRING]

    oob = 16 * '0'
    out_size = random.randint(0, 2)
    rand_out_actions = random.choice(out_actions) if out_size else 0
    in_size = random.randint(0, 2)
    rand_in_actions = random.choice(in_actions) if in_size else 0
    crpl_size = 10  # Maximum capacity of the replay protection list

    stack.gap_init()
    stack.mesh_init(device_uuid, oob, out_size, rand_out_actions, in_size,
                    rand_in_actions, crpl_size)

    pre_conditions = [
        TestFunc(btp.core_reg_svc_gap),
        TestFunc(btp.core_reg_svc_mesh),
        TestFunc(btp.core_reg_svc_mmdl),
        TestFunc(btp.gap_read_ctrl_info),
        TestFunc(lambda: pts.update_pixit_param(
            "MMDL", "TSPX_bd_addr_iut",
            stack.gap.iut_addr_get_str()))]

    test_cases = [
        ZTestCase("MMDL", "MMDL/SR-CL/COMP/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GOO/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GOO/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GOO/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GOO/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GLV/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLV/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLV/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLV/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLV/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLV/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLV/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GDTT/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GDTT/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GPOO/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPOO/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPOO/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPOO/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GPOOS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPOOS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GPL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPL/BV-15-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GPLS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPLS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GPLS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GBAT/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GLOC/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLOC/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GLOCS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GLOCS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GUP/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GUP/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GUP/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GUP/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GAP/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GAP/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GAP/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GAP/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GAP/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GMP/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GMP/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GMP/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GMP/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/GMP/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/GCP/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/SNR/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BI-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BI-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNR/BI-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BI-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SNRS/BI-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/TIM/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/TIM/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/TIM/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/TIMS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/TIMS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/TIMS/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/TIMS/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/TIMS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LLN/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-15-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-16-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-17-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-18-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLN/BV-19-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LLNS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLNS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLNS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LLC/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLC/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LLCS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLCS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LLCS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/MLTEL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/MLTEL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),


        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYL/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LXYS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LXYS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSL/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LHSLH/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLH/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLH/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLH/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LHSLSA/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLSA/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLSA/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLSA/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LHSLSE/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLSE/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LHSLSE/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LCTL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTL/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LCTLT/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTLT/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTLT/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTLT/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/LCTLS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTLS/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTLS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/LCTLS/BI-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/SCE/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SCE/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SCE/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/SCES/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SCES/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/SCH/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SCH/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/SR/SCHS/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/SR/SCHS/BI-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GOO/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GOO/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GOO/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GOO/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GOO/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GOO/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GOO/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GLV/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLV/BV-15-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GDTT/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GDTT/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GDTT/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GPOO/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPOO/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPOO/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GPL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPL/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GBAT/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GLOC/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLOC/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLOC/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLOC/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLOC/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GLOC/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/GPR/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/GPR/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/SNR/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SNR/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/TIM/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/TIM/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/TIM/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/TIM/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/TIM/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/TIM/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/TIM/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/TIM/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/LLN/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-15-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-16-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-17-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-18-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-19-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-20-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLN/BV-21-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/LLC/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-15-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LLC/BV-16-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-15-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-16-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-17-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-18-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-19-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LCTL/BV-20-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/SCE/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCE/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LXYL/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-05-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-06-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-07-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-08-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-09-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-10-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-11-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-12-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-13-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-14-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-15-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-16-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-17-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-18-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-19-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-20-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-21-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-22-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-23-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-24-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-25-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-26-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-27-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/LHSL/BV-28-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),

        ZTestCase("MMDL", "MMDL/CL/SCH/BV-01-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCH/BV-02-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCH/BV-03-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
        ZTestCase("MMDL", "MMDL/CL/SCH/BV-04-C", cmds=pre_conditions,
                  generic_wid_hdl=mmdl_wid_hdl),
    ]

    return test_cases


def main():
    """Main."""
    import ptsprojects.zephyr.iutctl as iutctl

    class pts:
        pass

    pts.q_bd_addr = "AB:CD:EF:12:34:56"

    iutctl.init_stub()

    test_cases_ = test_cases(pts)

    for test_case in test_cases_:
        print()
        print(test_case)

        if test_case.edit1_wids:
            print(("edit1_wids: %r" % test_case.edit1_wids))

        if test_case.verify_wids:
            print(("verify_wids: %r" % test_case.verify_wids))

        for index, cmd in enumerate(test_case.cmds):
            print(("%d) %s" % (index, cmd)))


if __name__ == "__main__":
    main()