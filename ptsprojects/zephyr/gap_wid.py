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

import logging
import sys
from pybtp import btp
from pybtp.types import Prop, Perm, UUID, AdType, UriScheme, bdaddr_reverse
import re
import struct
from ptsprojects.stack import get_stack
from binascii import hexlify
from time import sleep

log = logging.debug


def gap_wid_hdl(wid, description, test_case_name):
    log("%s, %r, %r, %s", gap_wid_hdl.__name__, wid, description,
        test_case_name)
    module = sys.modules[__name__]

    try:
        handler = getattr(module, "hdl_wid_%d" % wid)
        return handler(description)
    except AttributeError as e:
        logging.exception(e)


# wid handlers section begin
def hdl_wid_4(desc):
    sleep(10)  # Give some time to discover devices
    btp.gap_stop_discov()
    return btp.check_discov_results()


def hdl_wid_5(desc):
    stack = get_stack()

    btp.gap_set_nonconn()
    btp.gap_set_nondiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad, sd=stack.gap.sd)
    return True


def hdl_wid_10(desc):
    btp.gap_stop_discov()
    return btp.check_discov_results(discovered=True)


def hdl_wid_11(desc):
    btp.gap_stop_discov()
    return btp.check_discov_results(discovered=False)


def hdl_wid_12(desc):
    btp.gap_start_discov(type='passive', mode='observe')
    return True


def hdl_wid_13(desc):
    btp.gap_start_discov(mode='limited')
    return True


def hdl_wid_14(desc):
    btp.gap_stop_discov()
    return btp.check_discov_results(discovered=True)


def hdl_wid_20(desc):
    btp.gap_set_nonconn()
    return True


def hdl_wid_21(desc):
    stack = get_stack()

    btp.gap_set_conn()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_23(desc):
    btp.gap_start_discov()
    return True


def hdl_wid_24(desc):
    stack = get_stack()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_25(desc):
    stack = get_stack()

    if stack.gap.flags:
        stack.gap.ad[AdType.flags] = stack.gap.flags

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_26(desc):
    stack = get_stack()

    stack.gap.ad[AdType.manufacturer_data] = stack.gap.manufacturer_data

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_27(desc):
    stack = get_stack()

    stack.gap.ad[AdType.tx_power] = '00'

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_29(desc):
    stack = get_stack()

    stack.gap.ad[AdType.slave_conn_interval_range] = 'ffffffff'

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_35(desc):
    stack = get_stack()

    if stack.gap.svcs:
        stack.gap.ad[AdType.uuid16_some] = stack.gap.svcs

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_40(desc):
    btp.gap_conn()
    return True


def hdl_wid_46(desc):
    return True


def hdl_wid_44(desc):
    btp.gap_disconn()
    return True


def hdl_wid_47(desc):
    stack = get_stack()

    btp.gap_set_nonconn()
    btp.gap_set_nondiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_49(desc):
    stack = get_stack()

    btp.gap_set_limdiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_50(desc):
    stack = get_stack()

    btp.gap_set_limdiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_51(desc):
    stack = get_stack()

    btp.gap_set_nonconn()
    btp.gap_set_gendiscov()
    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_52(desc):
    stack = get_stack()

    btp.gap_adv_off()
    btp.gap_set_conn()
    btp.gap_set_gendiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_53(desc):
    hdl_wid_51(desc)
    return True


def hdl_wid_54(desc):
    stack = get_stack()

    btp.gap_set_nonconn()
    btp.gap_set_gendiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True

def hdl_wid_55(desc):
    stack = get_stack()

    btp.gap_set_limdiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_56(desc):
    stack = get_stack()

    stack.gap.ad[AdType.uuid16_svc_solicit] = stack.gap.svc_data

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_57(desc):
    stack = get_stack()

    if stack.gap.svc_data:
        stack.gap.ad[AdType.uuid16_svc_data] = stack.gap.svc_data

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_59(desc):
    stack = get_stack()

    btp.gap_set_nonconn()
    btp.gap_set_limdiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_72(desc):
    stack = get_stack()

    btp.gap_set_nondiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_74(desc):
    hdl_wid_72(desc)
    return True


def hdl_wid_75(desc):
    stack = get_stack()

    btp.gap_set_gendiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_76(desc):
    hdl_wid_55(desc)
    return True


def hdl_wid_77(desc):
    btp.gap_disconn()
    return True


def hdl_wid_78(desc):
    btp.gap_conn()
    return True


def hdl_wid_79(desc):
    return hdl_wid_80(desc)


def hdl_wid_80(desc):
    stack = get_stack()

    btp.gap_adv_off()
    btp.gap_set_nonconn()
    btp.gap_set_nondiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_82(desc):
    return True

def hdl_wid_83(desc):
    return True

def hdl_wid_84(desc):
    return True

def hdl_wid_85(desc):
    return True


def hdl_wid_90(desc):
    stack = get_stack()

    btp.gap_adv_off()
    btp.gap_set_conn()
    btp.gap_set_gendiscov()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_91(desc):
    stack = get_stack()

    btp.gap_set_conn()

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_100(desc):
    btp.gap_pair()
    return True


def hdl_wid_104(desc):
    return True


def hdl_wid_106(desc):
    btp.gap_pair()
    return True


def hdl_wid_108(desc):
    btp.gap_pair()
    return True


def hdl_wid_112(desc):
    bd_addr = btp.pts_addr_get()
    bd_addr_type = btp.pts_addr_type_get()

    handle = btp.parse_handle_description(desc)
    if not handle:
        return False

    btp.gattc_read(bd_addr_type, bd_addr, handle)
    # PTS doesn't respond to read req if we do not respond to this WID
    # btp.gattc_read_rsp()
    return True


def hdl_wid_114(desc):
    return True


def hdl_wid_118(desc):
    return True


def hdl_wid_120(desc):
    return True


def hdl_wid_121(desc):
    btp.gap_set_limdiscov()
    btp.gap_set_nonconn()

    return True


def hdl_wid_122(desc):
    btp.gap_set_nonconn()
    btp.gap_set_gendiscov()

    return True


def hdl_wid_124(desc):
    return True


def hdl_wid_125(desc):
    match = re.findall(r'(0[xX])?([0-9a-fA-F]{4})', desc)
    handle = match[0][1]

    bd_addr = btp.pts_addr_get()
    bd_addr_type = btp.pts_addr_type_get()
    btp.gattc_signed_write(bd_addr_type, bd_addr, handle, "01")

    return True


def hdl_wid_127(desc):
    btp.gap_conn_param_update(btp.pts_addr_get(), btp.pts_addr_type_get(),
                              720, 864, 0, 400)
    return True


def hdl_wid_130(desc):
    return btp.gatts_verify_write_fail(desc)


def hdl_wid_137(desc):
    return btp.gatts_verify_write_fail(desc)


def hdl_wid_135(desc):
    btp.gap_unpair()
    return True


def hdl_wid_136(desc):
    btp.core_reg_svc_gatt()
    btp.gatts_add_svc(0, UUID.VND16_1)
    btp.gatts_add_char(0, Prop.read | Prop.auth_swrite,
                       Perm.read | Perm.write_authn, UUID.VND16_2)
    btp.gatts_set_val(0, '01')
    btp.gatts_start_server()
    return True


def hdl_wid_138(desc):
    btp.gap_start_discov(transport='le', type='active', mode='observe')
    sleep(10)  # Give some time to discover devices
    btp.gap_stop_discov()
    return btp.check_discov_results()


def hdl_wid_139(desc):
    bd_addr = btp.pts_addr_get()
    bd_addr_type = btp.pts_addr_type_get()

    attrs = btp.gatts_get_attrs(type_uuid='2803')
    for attr in attrs:
        if not attr:
            continue

        (handle, permission, type_uuid) = attr
        data = btp.gatts_get_attr_val(bd_addr_type, bd_addr, handle)
        if not data:
            continue

        (att_rsp, val_len, val) = data

        hdr = '<BH'
        hdr_len = struct.calcsize(hdr)
        uuid_len = val_len - hdr_len

        (props, handle, chrc_uuid) = struct.unpack("<BH%ds" % uuid_len, val)
        chrc_value_attr = btp.gatts_get_attrs(start_handle=handle,
                                              end_handle=handle)
        if not chrc_value_attr:
            continue

        (handle, permission, type_uuid) = chrc_value_attr[0]
        if permission & Perm.read_authn:
            return format(handle, 'x').zfill(4)

    return False


def hdl_wid_141(desc):
    return btp.gatts_verify_write_success(desc)


def hdl_wid_142(desc):
    btp.gap_conn()
    return True


def hdl_wid_143(desc):
    logging.debug("No API to: 'Inform about lost bond'")
    return True


def hdl_wid_144(desc):
    bd_addr = btp.pts_addr_get()
    bd_addr_type = btp.pts_addr_type_get()

    attrs = btp.gatts_get_attrs(type_uuid='2803')
    for attr in attrs:
        if not attr:
            continue

        (handle, permission, type_uuid) = attr
        data = btp.gatts_get_attr_val(bd_addr_type, bd_addr, handle)
        if not data:
            continue

        (att_rsp, val_len, val) = data

        hdr = '<BH'
        hdr_len = struct.calcsize(hdr)
        uuid_len = val_len - hdr_len

        (props, handle, chrc_uuid) = struct.unpack("<BH%ds" % uuid_len, val)
        chrc_value_attr = btp.gatts_get_attrs(start_handle=handle,
                                              end_handle=handle)
        if not chrc_value_attr:
            continue

        (handle, permission, type_uuid) = chrc_value_attr[0]
        if permission & Perm.read_enc:
            return format(handle, 'x').zfill(4)

    return False


def hdl_wid_148(desc):
    btp.gap_conn()
    return not btp.gap_wait_for_connection(10)


def hdl_wid_149(desc):
    stack = get_stack()

    if stack.gap.appearance:
        stack.gap.ad[AdType.gap_appearance] = stack.gap.appearance
    
    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_152(desc):
    stack = get_stack()

    stack.gap.ad[AdType.public_target_addr] = bdaddr_reverse(btp.pts_addr_get())

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_153(desc):
    stack = get_stack()

    stack.gap.ad[AdType.random_target_addr] = bdaddr_reverse(btp.pts_addr_get())

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_154(desc):
    stack = get_stack()

    stack.gap.ad[AdType.advertising_interval] = "0030"

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_155(desc):
    stack = get_stack()

    device_addr = '{:02d}'.format(stack.gap.iut_bd_addr.data["type"]) + \
                  bdaddr_reverse(stack.gap.iut_bd_addr.data["address"])

    stack.gap.ad[AdType.le_bt_device_addr] = device_addr

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_156(desc):
    stack = get_stack()

    stack.gap.ad[AdType.le_role] = '02'

    btp.gap_adv_ind_on(ad=stack.gap.ad)

    return True


def hdl_wid_157(desc):
    btp.gap_start_discov(transport='le', type='active', mode='observe')
    sleep(10)  # Give some time to discover devices
    btp.gap_stop_discov()
    return btp.check_discov_results()


def hdl_wid_158(desc):
    return True


def hdl_wid_161(desc):
    match = re.findall(r'(0[xX])?([0-9a-fA-F]{4})', desc)
    handle = int(match[0][1], 16)

    attr = btp.gatts_get_attrs(handle, handle)
    if not attr:
        return

    (handle, permission, type_uuid) = attr.pop()

    bd_addr = btp.pts_addr_get()
    bd_addr_type = btp.pts_addr_type_get()

    # Check if characteristic has signed write property
    value = btp.gatts_get_attr_val(bd_addr_type, bd_addr, handle - 1)
    if not value:
        return

    (att_rsp, val_len, val) = value

    hdr = '<BH'
    hdr_len = struct.calcsize(hdr)
    uuid_len = val_len - hdr_len

    (properties, value_handle, chrc_uuid) = struct.unpack("<BH%ds" % uuid_len,
                                                          val)

    if properties & Prop.auth_swrite == 0:
        return

    chrc_uuid = btp.btp2uuid(uuid_len, chrc_uuid)

    value = btp.gatts_get_attr_val(bd_addr_type, bd_addr, handle)
    if not value:
        return

    (att_rsp, val_len, val) = value
    return val_len


def hdl_wid_162(desc):
    return True


def hdl_wid_169(desc):
    btp.gap_start_discov(type='active', mode='observe')
    return True


def hdl_wid_173(desc):
    stack = get_stack()

    # Prepare space for URI
    stack.gap.sd.clear()
    stack.gap.sd[AdType.uri] = UriScheme.https + \
                               'github.com/intel/auto-pts'.encode()

    btp.gap_adv_ind_on(sd=stack.gap.sd)

    return True


def hdl_wid_174(desc):
    btp.gap_rpa_conn(desc)
    return True


def hdl_wid_176(desc):
    return True


def hdl_wid_177(desc):
    return True


def hdl_wid_178(desc):
    return True


def hdl_wid_204(desc):
    btp.gap_start_discov(type='passive', mode='observe')
    sleep(10)
    btp.gap_stop_discov()
    return btp.check_discov_results()


def hdl_wid_1002(desc):
    stack = get_stack()
    return stack.gap.get_passkey()


def hdl_wid_2142(desc):
    btp.gap_conn()
    return True

