# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Collects fault metrics from UCS
from collections import defaultdict
from prometheus_client import Gauge

ucs_faults_total = Gauge('ucs_faults_total', 'Faults', ['domain', 'type', 'description', 'dn', 'code', 'cause'])

# Cleared 	= 0
# Informational = 1
# Minor 	= 2
# Warning	= 3
# Major 	= 4
# Critical	= 5

class Faults:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        faults = stats['FaultInst']
        metrics = defaultdict(list)

        for fault in faults:
            state = 0
            if fault.severity == 'info':
            	state = 1
            if fault.severity == 'minor':
            	state = 2
            if fault.severity == 'warning':
            	state = 3
            if fault.severity == 'major':
            	state = 4
            if fault.severity == 'critical':
            	state = 5
            labels = {'domain': self.domain, 'type': fault.type, 'description': fault.descr, 'dn': fault.dn, 'code': fault.code, 'cause': fault.cause }
            ucs_faults_total.labels(**labels).set(state)
        return
