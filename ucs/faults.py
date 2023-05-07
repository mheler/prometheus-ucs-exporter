# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Collects fault metrics from UCS
from collections import defaultdict
from prometheus_client import Gauge

ucs_faults_total = Gauge('ucs_faults_total', 'Faults', ['domain', 'type', 'description', 'dn', 'severity', 'code', 'cause'])

class Faults:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        faults = stats['FaultInst']
        metrics = defaultdict(list)

        for fault in faults:
            active = 1
            labels = {'domain': self.domain, 'type': fault.type, 'description': fault.descr, 'dn': fault.dn, 'severity': fault.severity, 'code': fault.code, 'cause': fault.cause }
            ucs_faults_total.labels(**labels).set(active)
        return
