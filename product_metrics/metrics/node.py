from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI
from collections import Counter


class NodeMetric(BaseType):
    NODE_TYPES = [("Regular Nodes", 74, "node"),
                  ("Cloud Nodes", 75, "cloud_node"),
                  ("Fast Nodes", 76, 'fast_node'),
                  ("Partner Nodes", 77, 'partner_node'),
                  ("Instance Nodes", 78, 'node_instance')]

    NODE_VERSIONS = [('Node 2.15', 80, '215'),
                     ('Node 2.16', 81, '216'),
                     ('Node 2.18', 82, '218'),
                     ('Node 3.0', 83, '30'),
                     ('Node 3.2', 84, '32')]

    def get_nodes(self):
        all_nodes = []
        for client in MetricHelper().real_clients:
            i = 0
            while True:
                nodes = WallarmAPI().node_api.get_nodes(
                    {'filter[clientid]': client.id, 'limit': 1000, 'offset': i*1000})
                all_nodes += nodes
                i += 1
                if len(nodes) < 1000:
                    break

        return all_nodes

    def get_types(self, nodes):
        types = []
        for node in nodes:
            types.append(node.type)

        count_types = dict(Counter(types))

        count_instance_nodes = 0
        for client in MetricHelper().real_clients:
            i = 0
            while True:
                instance_nodes = WallarmAPI().node_api.get_instance_nodes(
                    {'filter[clientid]': client.id, 'limit': 1000, 'offset': i*1000})
                count_instance_nodes += len(instance_nodes)
                i += 1
                if len(instance_nodes) < 1000:
                    break

        count_types.update({'node_instance': count_instance_nodes})
        return count_types

    def get_versions(self, nodes):
        versions = []
        for node in nodes:
            version = node.node_env_params['packages']
            if 'ruby-proton' in version:
                versions.append(version['ruby-proton']['current'])

        major_versions = [v.split('.')[0]+v.split('.')[1] for v in versions]
        return dict(Counter(major_versions))

    class CountTotalNodes(BaseMetric):
        def __init__(self, nodes):
            super().__init__("Total nodes (except node_instance)", 73)
            self.nodes = nodes

        def value(self) -> int:
            return len(self.nodes)

    class CountActiveNodes(BaseMetric):
        def __init__(self, nodes):
            super().__init__("Active nodes", 79)
            self.nodes = nodes

        def value(self) -> int:
            active_nodes = 0
            for node in self.nodes:
                if node.active:
                    active_nodes += 1
            return active_nodes

    class CountNodesByType(BaseMetric):
        def __init__(self, types, name, row, node_type) -> None:
            super().__init__(name, row)
            self.node_type = node_type
            self.types = types

        def value(self) -> int:
            if self.node_type in self.types:
                return self.types[self.node_type]
            else:
                return 0

    class CountNodesByVersion(BaseMetric):
        def __init__(self, versions, name, row, node_version) -> None:
            super().__init__(name, row)
            self.node_version = node_version
            self.versions = versions

        def value(self) -> int:
            if self.node_version in self.versions:
                return self.versions[self.node_version]
            else:
                return 0

    def collect_metrics(self) -> list:
        nodes = self.get_nodes()
        types = self.get_types(nodes)
        versions = self.get_versions(nodes)

        return [self.CountNodesByVersion(versions, *t) for t in self.NODE_VERSIONS] + [
            self.CountTotalNodes(nodes), self.CountActiveNodes(nodes)] + [
            self.CountNodesByType(types, *t) for t in self.NODE_TYPES]
