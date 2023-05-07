# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Collects power usage metrics from UCS
from prometheus_client import Gauge
from . import utils as u

ucs_server_temperature = Gauge('ucs_server_temperature',
                         'Temperature Environmental Stats in Celius',
                         ['domain', 'chassis', 'blade', 'type'])

class Temperature:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['ProcessorEnvStats']:
            (_, chassis, blade, _, component, _) = item.dn.split("/")
            cpu_labels = {'domain': self.domain, 'chassis': chassis, 'blade': blade,
                    'type': component}
            ucs_server_temperature.labels(**cpu_labels).set(float(item.temperature))

        for item in stats['ComputeMbTempStats']:
            (_, chassis, blade, _, _) = item.dn.split("/")
            rear_mb_labels = {'domain': self.domain, 'chassis': chassis,
                    'blade': blade, 'type': "motherboard_rear_temperature"}
            front_mb_labels = {'domain': self.domain, 'chassis': chassis,
                    'blade': blade, 'type': "motherboard_front_temperature"}
            ucs_server_temperature.labels(**rear_mb_labels).set(float(item.fm_temp_sen_rear))
            ucs_server_temperature.labels(**front_mb_labels).set(float(item.fm_temp_sen_io))

        for item in stats['EquipmentPsuStats']:
            (_, chassis, component, _) = item.dn.split("/")
            psu_labels = {'domain': self.domain, 'chassis': chassis, 'blade': "",
                    'type': component}
            ucs_server_temperature.labels(**psu_labels).set(float(item.ambient_temp))
