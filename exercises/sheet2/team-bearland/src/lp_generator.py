#!/usr/bin/python3
import gurobipy as gp
import numpy as np
import sys
from gurobipy import GRB

class PointConfig:
    def __init__(self, file_path):
        self.points = np.genfromtxt(file_path, delimiter=' ')
        self.num_points = np.size(self.points) / np.size(self.points[0])
        self.dim = np.size(self.points[0])

    def __repr__(self):
        return "PointConfig()"

    def __str__(self):
        _str = "Point Configuration:\n"
        _str += " - Number of points: {}\n".format(self.num_points)
        _str += " - Point dimension: {}\n".format(self.dim)
        _str += " - Raw points:\n{}\n".format(self.points)
        return _str


class Triangulation:
    def __init__(self, file_path):
        # TODO: should we subtract one so that we can index points directly?
        self.facets = np.genfromtxt(file_path, delimiter=' ')
        self.facets -= 1

    def __repr__(self):
        return "Triangulation()"

    def __str__(self):
        _str = "Facets Configuration:\n"
        _str += " - Facet Indexes:\n{}\n".format(self.facets)
        return _str


def usage():
    print("LP File Generator:")
    print("USAGE: ./lp_generator.py <file.vertices> <file.triangulation>")


def generate_lp(point_config, triangulation):
    print(point_config)
    print(triangulation)
    model = gp.Model('folding')
    # Add Variables: GRB.CONTINUOUS vars are by default [0, \inf)
    y = model.addVars(range(int(point_config.dim)), vtype=GRB.CONTINUOUS,
            name='y')
    w = model.addVars(range(int(point_config.num_points)), vtype=GRB.CONTINUOUS,
            name='w')
    # Add Constrains
    for num, c in enumerate(triangulation.facets):
        facet_ind = set([int(i) for i in c])
        non_facet_ind = set(range(int(point_config.num_points))) - facet_ind 
        print(" -- Constrain for Facet {} -- ".format(num))
        print("Facet: {}\nNon-Facet: {}".format(facet_ind, non_facet_ind))
        # Adding one constrain per vertex in the facet
        for num2, vert in enumerate(facet_ind):
            model.addConstr(gp.quicksum([y[i]*point_config.points[vert][i] 
                                        for i in range(int(point_config.dim))])
                            - w[vert], GRB.EQUAL, 0, "f{}_{}".format(num, num2))
        # Adding one constrain per non-vertex in the facet
        for num2, vert in enumerate(non_facet_ind):
            model.addConstr(gp.quicksum([y[i]*point_config.points[vert][i] 
                                        for i in range(int(point_config.dim))])
                            - w[vert], GRB.LESS_EQUAL, 0, "nf{}_{}".format(num, num2))
    model.write('folding.lp')

if __name__=="__main__":
    if (len(sys.argv) != 3 or sys.argv[1].split('.')[-1] != "vertices"
            or sys.argv[2].split('.')[-1] != "triangulation"):
        usage()
    else:
        point_config = PointConfig(sys.argv[1])
        triangulation = Triangulation(sys.argv[2])
        generate_lp(point_config, triangulation)
        # Optimize
#m.optimize()
#status = m.status
#if status == GRB.UNBOUNDED:
#    print('The model cannot be solved because it is unbounded')
#    exit(0)
#if status == GRB.OPTIMAL:
#    print('The optimal objective is %g' % m.objVal)
#    exit(0)
#if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
#    print('Optimization was stopped with status %d' % status)
#    exit(0)

