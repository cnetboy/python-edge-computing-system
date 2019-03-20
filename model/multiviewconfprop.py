import networkx as nx
from networkx import NetworkXError

import numpy as np


class CameraDetectionInfo():

    def __init__(self, cam, prob, x_mid, y_mid):
        self.cam = cam
        self.prob = prob
        self.x_mid = x_mid
        self.y_mid = y_mid

    def get_cam(self):
        return self.cam

    def get_index(self):
        return self.index

    def get_prob(self):
        return self.prob

    def get_x_mid(self):
        return self.x_mid

    def get_y_mid(self):
        return self.y_mid


class ConfidenceVertex(object):

    def __init__(self, cam, detection_index, prob):
        self.cam = cam
        self.detection_index = detection_index
        self.prob = prob

    def get_cam(self):
        return self.cam

    def get_detection_index(self):
        return self.detection_index

    def get_prob(self):
        return self.prob


def get_detection_infos(cam, predictions):
    detection_infos = list()
    for prediction in predictions:
        xmin = float(prediction['xmin'])
        ymin = float(prediction['ymin'])
        xmax = float(prediction['xmax'])
        ymax = float(prediction['ymax'])
        prob = float(prediction['score'])

        x_mid = (xmax + xmin) / 2
        y_mid = (ymax + ymin) / 2
        detection_infos.append(CameraDetectionInfo(cam, prob, x_mid, y_mid))
    return detection_infos


HOMOGRAPHY = np.array([[1.46400584e+00, -3.66424109e-03,-6.67012133e+01],
                       [2.40077617e-01, 1.27468101e+00, -7.56809029e+01],
                        [6.15150279e-04, 2.49909001e-05, 1.00000000e+00]])
THRESHOLD = 0.1
WIDTH = 640
HEIGHT = 480


def get_corresponding_points(cam1_detection_infos, cam2_detection_infos):
    corresponding_points = list()
    for index_1, info_1 in enumerate(cam1_detection_infos):
        point1 = np.array([[info_1.get_x_mid() * WIDTH], [info_1.get_y_mid() * HEIGHT], [1]])
        expected_point2 = np.matmul(HOMOGRAPHY, point1)
        expected_point2 = expected_point2/expected_point2[2]
        expected_x_threshold = expected_point2[0] * THRESHOLD
        x_max = expected_point2[0] + expected_x_threshold
        x_min = expected_point2[0] - expected_x_threshold
        expected_y_threshold = expected_point2[1] * THRESHOLD
        y_max = expected_point2[1] + expected_y_threshold
        y_min = expected_point2[1] - expected_y_threshold
        for index_2, info_2 in enumerate(cam2_detection_infos):
            x_mid_scaled = info_2.get_x_mid() * WIDTH
            y_mid_scaled = info_2.get_y_mid() * HEIGHT
            if ((x_mid_scaled <= x_max) and (x_mid_scaled >= x_min)) and ((y_mid_scaled <= y_max) and (y_mid_scaled >= y_min)):
                corresponding_points.append((ConfidenceVertex(info_1.get_cam(), index_1, info_1.get_prob()), ConfidenceVertex(info_2.get_cam(), index_2, info_2.get_prob())))
    return corresponding_points


def page_rank(initial_graph, damping_factor=0.85, max_iter=100, tol=1.0e-6, weight='weight'):
    """Return the PageRank of the nodes in the graph.

    PageRank computes a ranking of the nodes in the graph G based on
    the structure of the incoming links. It was originally designed as
    an algorithm to rank web pages.

    Parameters
    ----------
    initial_graph : graph
    A NetworkX graph. Undirected graphs will be converted to a directed
    graph with two directed edges for each undirected edge.

    damping_factor : float, optional
    Damping parameter for PageRank, default=0.85.

    max_iter : integer, optional
    Maximum number of iterations in power method eigenvalue solver.

    tol : float, optional
    Error tolerance used to check convergence in power method solver.

    weight : key, optional
    Edge data key to use as weight. If None weights are set to 1.

    Returns
    -------
    pagerank : dictionary
    Dictionary of nodes with PageRank as value

    Notes
    -----
    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence. The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    The PageRank algorithm was designed for directed graphs but this
    algorithm does not check if the input graph is directed and will
    execute on undirected graphs by converting each edge in the
    directed graph to two edges.


    """
    if len(initial_graph) == 0:
        return {}

    if not initial_graph.is_directed():
        directed_graph = initial_graph.to_directed()
    else:
        directed_graph = initial_graph

    # Create a copy in (right) stochastic form
    stochastic_graph = nx.stochastic_graph(directed_graph, weight=weight)
    number_of_nodes = stochastic_graph.number_of_nodes()

    # Initialize vector values
    total_prob_values = float(sum([node.get_prob() for node in stochastic_graph.nodes()]))
    #personalize_prob = dict((node, node.get_prob() / total_prob_values) for node in stochastic_graph.nodes())
    personalize_prob = dict.fromkeys(stochastic_graph, 1.0 / number_of_nodes)

    # Choose fixed starting vector if not given
    initial_prob = dict((node, node.get_prob() / total_prob_values) for node in stochastic_graph.nodes())
    dangling_weights = personalize_prob
    dangling_nodes = [n for n in stochastic_graph if stochastic_graph.out_degree(n, weight=weight) == 0.0]

    # power iteration: make up to max_iter iterations
    for _ in range(max_iter):
        xlast = initial_prob
        initial_prob = dict.fromkeys(xlast.keys(), 0)
        danglesum = damping_factor * sum(xlast[n] for n in dangling_nodes)
        for n in initial_prob:
            # this matrix multiply looks odd because it is
            # doing a left multiply initial_prob^T=xlast^T*stochastic_graph
            for nbr in stochastic_graph[n]:
                initial_prob[nbr] += damping_factor * xlast[n] * stochastic_graph[n][nbr][weight]
            initial_prob[n] += danglesum * dangling_weights[n] + (1.0 - damping_factor) * personalize_prob[n]

        # check convergence, l1 norm
        err = sum([abs(initial_prob[n] - xlast[n]) for n in initial_prob])
        if err < number_of_nodes * tol:
            return initial_prob
    raise NetworkXError('pagerank: power iteration failed to converge '
                        'in %d iterations.' % max_iter)


# image are actually detection results
def multi_view_predict(init_predictions1, init_predictions2):#, init_predictions3, init_predictions4):
    # get corresponding points
    cam1_detection_info = get_detection_infos(1, init_predictions1)
    cam2_detection_info = get_detection_infos(2, init_predictions2)
   # cam3_detection_info = get_detection_infos(3, init_predictions3)
   # cam4_detection_info = get_detection_infos(3, init_predictions4)

    corresponding_points = get_corresponding_points(cam1_detection_info, cam2_detection_info)

    # Page Rank per corresponding point par
    for points in corresponding_points:
        G = nx.DiGraph()
        G.add_edge(points[0], points[1])
        G.add_edge(points[1], points[0])

        for node in G.nodes():
            print('vector: ' + str(node))
            print('prob: ' + str(node.get_prob()))

        print('page ranking...')

        PR = page_rank(G)
        for key in PR.keys():
            print('vector: ' + str(key))
            print('prob: ' + str(PR[key]))
            if key.get_cam() == 1:
                init_predictions1[key.get_detection_index()]['score'] = PR[key]
            else:
                init_predictions2[key.get_detection_index()]['score'] = PR[key]

    return init_predictions1, init_predictions2, init_predictions2 # They got page ranked yo!
