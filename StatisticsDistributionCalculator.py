import sys
from fractions import Fraction
import math
import operator as op
from functools import reduce
import ast
import json

NormalDistCurve = {
    -3.4 : 0.0003, -3.41 : 0.0003, -3.42 : 0.0003, -3.43 : 0.0003, -3.44 : 0.0003, -3.45 : 0.0003, -3.46 : 0.0003, -3.47 : 0.0003, -3.48 : 0.0003, -3.49 : 0.0002, 
    -3.3 : 0.0005, -3.31 : 0.0005, -3.32 : 0.0005, -3.33 : 0.0004, -3.34 : 0.0004, -3.35 : 0.0004, -3.36 : 0.0004, -3.37 : 0.0004, -3.38 : 0.0004, -3.39 : 0.0003, 
    -3.2 : 0.0007, -3.21 : 0.0007, -3.22 : 0.0006, -3.23 : 0.0006, -3.24 : 0.0006, -3.25 : 0.0006, -3.26 : 0.0006, -3.27 : 0.0005, -3.28 : 0.0005, -3.29 : 0.0005, 
    -3.1 : 0.0010, -3.11 : 0.0009, -3.12 : 0.0009, -3.13 : 0.0009, -3.14 : 0.0008, -3.15 : 0.0008, -3.16 : 0.0008, -3.17 : 0.0008, -3.18 : 0.0007, -3.19 : 0.0007, 
    -3.0 : 0.0013, -3.01 : 0.0013, -3.02 : 0.0013, -3.03 : 0.0012, -3.04 : 0.0012, -3.05 : 0.0011, -3.06 : 0.0011, -3.07 : 0.0011, -3.08 : 0.0010, -3.09 : 0.0010, 
    -2.9 : 0.0019, -2.91 : 0.0018, -2.92 : 0.0018, -2.93 : 0.0017, -2.94 : 0.0016, -2.95 : 0.0016, -2.96 : 0.0015, -2.97 : 0.0015, -2.98 : 0.0014, -2.99 : 0.0014, 
    -2.8 : 0.0026, -2.81 : 0.0025, -2.82 : 0.0024, -2.83 : 0.0023, -2.84 : 0.0023, -2.85 : 0.0022, -2.86 : 0.0021, -2.87 : 0.0021, -2.88 : 0.0020, -2.89 : 0.0019, 
    -2.7 : 0.0035, -2.71 : 0.0034, -2.72 : 0.0033, -2.73 : 0.0032, -2.74 : 0.0031, -2.75 : 0.0030, -2.76 : 0.0029, -2.77 : 0.0028, -2.78 : 0.0027, -2.79 : 0.0026, 
    -2.6 : 0.0047, -2.61 : 0.0045, -2.62 : 0.0044, -2.63 : 0.0043, -2.64 : 0.0041, -2.65 : 0.0040, -2.66 : 0.0039, -2.67 : 0.0038, -2.68 : 0.0037, -2.69 : 0.0036, 
    -2.5 : 0.0062, -2.51 : 0.0060, -2.52 : 0.0059, -2.53 : 0.0057, -2.54 : 0.0055, -2.55 : 0.0054, -2.56 : 0.0052, -2.57 : 0.0051, -2.58 : 0.0049, -2.59 : 0.0048, 
    -2.4 : 0.0082, -2.41 : 0.0080, -2.42 : 0.0078, -2.43 : 0.0075, -2.44 : 0.0073, -2.45 : 0.0071, -2.46 : 0.0069, -2.47 : 0.0068, -2.48 : 0.0066, -2.49 : 0.0064, 
    -2.3 : 0.0107, -2.31 : 0.0104, -2.32 : 0.0102, -2.33 : 0.0099, -2.34 : 0.0096, -2.35 : 0.0094, -2.36 : 0.0091, -2.37 : 0.0089, -2.38 : 0.0087, -2.39 : 0.0084, 
    -2.2 : 0.0139, -2.21 : 0.0136, -2.22 : 0.0132, -2.23 : 0.0129, -2.24 : 0.0125, -2.25 : 0.0122, -2.26 : 0.0119, -2.27 : 0.0116, -2.28 : 0.0113, -2.29 : 0.0110, 
    -2.1 : 0.0179, -2.11 : 0.0174, -2.12 : 0.0170, -2.13 : 0.0166, -2.14 : 0.0162, -2.15 : 0.0158, -2.16 : 0.0154, -2.17 : 0.0150, -2.18 : 0.0146, -2.19 : 0.0143, 
    -2.0 : 0.0228, -2.01 : 0.0222, -2.02 : 0.0217, -2.03 : 0.0212, -2.04 : 0.0207, -2.05 : 0.0202, -2.06 : 0.0197, -2.07 : 0.0192, -2.08 : 0.0188, -2.09 : 0.0183, 
    -1.9 : 0.0287, -1.91 : 0.0281, -1.92 : 0.0274, -1.93 : 0.0268, -1.94 : 0.0262, -1.95 : 0.0256, -1.96 : 0.0250, -1.97 : 0.0244, -1.98 : 0.0239, -1.99 : 0.0233, 
    -1.8 : 0.0359, -1.81 : 0.0351, -1.82 : 0.0344, -1.83 : 0.0336, -1.84 : 0.0329, -1.85 : 0.0322, -1.86 : 0.0314, -1.87 : 0.0307, -1.88 : 0.0301, -1.89 : 0.0294, 
    -1.7 : 0.0446, -1.71 : 0.0436, -1.72 : 0.0427, -1.73 : 0.0418, -1.74 : 0.0409, -1.75 : 0.0401, -1.76 : 0.0392, -1.77 : 0.0384, -1.78 : 0.0375, -1.79 : 0.0367, 
    -1.6 : 0.0548, -1.61 : 0.0537, -1.62 : 0.0526, -1.63 : 0.0516, -1.64 : 0.0505, -1.65 : 0.0495, -1.66 : 0.0485, -1.67 : 0.0475, -1.68 : 0.0465, -1.69 : 0.0455, 
    -1.5 : 0.0668, -1.51 : 0.0655, -1.52 : 0.0643, -1.53 : 0.0630, -1.54 : 0.0618, -1.55 : 0.0606, -1.56 : 0.0594, -1.57 : 0.0582, -1.58 : 0.0571, -1.59 : 0.0559, 
    -1.4 : 0.0808, -1.41 : 0.0793, -1.42 : 0.0778, -1.43 : 0.0764, -1.44 : 0.0749, -1.45 : 0.0735, -1.46 : 0.0721, -1.47 : 0.0708, -1.48 : 0.0694, -1.49 : 0.0681, 
    -1.3 : 0.0968, -1.31 : 0.0951, -1.32 : 0.0934, -1.33 : 0.0918, -1.34 : 0.0901, -1.35 : 0.0885, -1.36 : 0.0869, -1.37 : 0.0853, -1.38 : 0.0838, -1.39 : 0.0823, 
    -1.2 : 0.1151, -1.21 : 0.1131, -1.22 : 0.1112, -1.23 : 0.1093, -1.24 : 0.1075, -1.25 : 0.1056, -1.26 : 0.1038, -1.27 : 0.1020, -1.28 : 0.1003, -1.29 : 0.0985, 
    -1.1 : 0.1357, -1.11 : 0.1335, -1.12 : 0.1314, -1.13 : 0.1292, -1.14 : 0.1271, -1.15 : 0.1251, -1.16 : 0.1230, -1.17 : 0.1210, -1.18 : 0.1190, -1.19 : 0.1170, 
    -1.0 : 0.1587, -1.01 : 0.1562, -1.02 : 0.1539, -1.03 : 0.1515, -1.04 : 0.1492, -1.05 : 0.1469, -1.06 : 0.1446, -1.07 : 0.1423, -1.08 : 0.1401, -1.09 : 0.1379, 
    -0.9 : 0.1841, -0.91 : 0.1814, -0.92 : 0.1788, -0.93 : 0.1762, -0.94 : 0.1736, -0.95 : 0.1711, -0.96 : 0.1685, -0.97 : 0.1660, -0.98 : 0.1635, -0.99 : 0.1611, 
    -0.8 : 0.2119, -0.81 : 0.2090, -0.82 : 0.2061, -0.83 : 0.2033, -0.84 : 0.2005, -0.85 : 0.1977, -0.86 : 0.1949, -0.87 : 0.1922, -0.88 : 0.1894, -0.89 : 0.1867, 
    -0.7 : 0.2420, -0.71 : 0.2389, -0.72 : 0.2358, -0.73 : 0.2327, -0.74 : 0.2296, -0.75 : 0.2266, -0.76 : 0.2236, -0.77 : 0.2206, -0.78 : 0.2177, -0.79 : 0.2148, 
    -0.6 : 0.2743, -0.61 : 0.2709, -0.62 : 0.2676, -0.63 : 0.2643, -0.64 : 0.2611, -0.65 : 0.2578, -0.66 : 0.2546, -0.67 : 0.2514, -0.68 : 0.2483, -0.69 : 0.2451, 
    -0.5 : 0.3085, -0.51 : 0.3050, -0.52 : 0.3015, -0.53 : 0.2981, -0.54 : 0.2946, -0.55 : 0.2912, -0.56 : 0.2877, -0.57 : 0.2843, -0.58 : 0.2810, -0.59 : 0.2776, 
    -0.4 : 0.3446, -0.41 : 0.3409, -0.42 : 0.3372, -0.43 : 0.3336, -0.44 : 0.3300, -0.45 : 0.3264, -0.46 : 0.3228, -0.47 : 0.3192, -0.48 : 0.3156, -0.49 : 0.3121, 
    -0.3 : 0.3821, -0.31 : 0.3783, -0.32 : 0.3745, -0.33 : 0.3707, -0.34 : 0.3669, -0.35 : 0.3632, -0.36 : 0.3594, -0.37 : 0.3557, -0.38 : 0.3520, -0.39 : 0.3483, 
    -0.2 : 0.4207, -0.21 : 0.4168, -0.22 : 0.4129, -0.23 : 0.4090, -0.24 : 0.4052, -0.25 : 0.4013, -0.26 : 0.3974, -0.27 : 0.3936, -0.28 : 0.3897, -0.29 : 0.3859, 
    -0.1 : 0.4602, -0.11 : 0.4562, -0.12 : 0.4522, -0.13 : 0.4483, -0.14 : 0.4443, -0.15 : 0.4404, -0.16 : 0.4364, -0.17 : 0.4325, -0.18 : 0.4286, -0.19 : 0.4247, 
    0.0 : 0.5000, -0.01 : 0.4960, -0.02 : 0.4920, -0.03 : 0.4880, -0.04 : 0.4840, -0.05 : 0.4801, -0.06 : 0.4761, -0.07 : 0.4721, -0.08 : 0.4681, -0.09 : 0.4641,
                  0.01 : 0.5040, 0.02 : 0.5080, 0.03 : 0.5120, 0.04 : 0.5160, 0.05 : 0.5199, 0.06 : 0.5239, 0.07 : 0.5279, 0.08 : 0.5319, 0.09 : 0.5359, 
    0.1 : 0.5398, 0.11 : 0.5438, 0.12 : 0.5478, 0.13 : 0.5517, 0.14 : 0.5557, 0.15 : 0.5596, 0.16 : 0.5636, 0.17 : 0.5675, 0.18 : 0.5714, 0.19 : 0.5753, 
    0.2 : 0.5793, 0.21 : 0.5832, 0.22 : 0.5871, 0.23 : 0.5910, 0.24 : 0.5948, 0.25 : 0.5987, 0.26 : 0.6026, 0.27 : 0.6064, 0.28 : 0.6103, 0.29 : 0.6141, 
    0.3 : 0.6179, 0.31 : 0.6217, 0.32 : 0.6255, 0.33 : 0.6293, 0.34 : 0.6331, 0.35 : 0.6368, 0.36 : 0.6406, 0.37 : 0.6443, 0.38 : 0.6480, 0.39 : 0.6517, 
    0.4 : 0.6554, 0.41 : 0.6591, 0.42 : 0.6628, 0.43 : 0.6664, 0.44 : 0.6700, 0.45 : 0.6736, 0.46 : 0.6772, 0.47 : 0.6808, 0.48 : 0.6844, 0.49 : 0.6879, 
    0.5 : 0.6915, 0.51 : 0.6950, 0.52 : 0.6985, 0.53 : 0.7019, 0.54 : 0.7054, 0.55 : 0.7088, 0.56 : 0.7123, 0.57 : 0.7157, 0.58 : 0.7190, 0.59 : 0.7224, 
    0.6 : 0.7257, 0.61 : 0.7291, 0.62 : 0.7324, 0.63 : 0.7357, 0.64 : 0.7389, 0.65 : 0.7422, 0.66 : 0.7454, 0.67 : 0.7486, 0.68 : 0.7517, 0.69 : 0.7549, 
    0.7 : 0.7580, 0.71 : 0.7611, 0.72 : 0.7642, 0.73 : 0.7673, 0.74 : 0.7704, 0.75 : 0.7734, 0.76 : 0.7764, 0.77 : 0.7794, 0.78 : 0.7823, 0.79 : 0.7852, 
    0.8 : 0.7881, 0.81 : 0.7910, 0.82 : 0.7939, 0.83 : 0.7967, 0.84 : 0.7995, 0.85 : 0.8023, 0.86 : 0.8051, 0.87 : 0.8078, 0.88 : 0.8106, 0.89 : 0.8133, 
    0.9 : 0.8159, 0.91 : 0.8186, 0.92 : 0.8212, 0.93 : 0.8238, 0.94 : 0.8264, 0.95 : 0.8289, 0.96 : 0.8315, 0.97 : 0.8340, 0.98 : 0.8365, 0.99 : 0.8389, 
    1.0 : 0.8413, 1.01 : 0.8438, 1.02 : 0.8461, 1.03 : 0.8485, 1.04 : 0.8508, 1.05 : 0.8531, 1.06 : 0.8554, 1.07 : 0.8577, 1.08 : 0.8599, 1.09 : 0.8621, 
    1.1 : 0.8643, 1.11 : 0.8665, 1.12 : 0.8686, 1.13 : 0.8708, 1.14 : 0.8729, 1.15 : 0.8749, 1.16 : 0.8770, 1.17 : 0.8790, 1.18 : 0.8810, 1.19 : 0.8830, 
    1.2 : 0.8849, 1.21 : 0.8869, 1.22 : 0.8888, 1.23 : 0.8907, 1.24 : 0.8925, 1.25 : 0.8944, 1.26 : 0.8962, 1.27 : 0.8980, 1.28 : 0.8997, 1.29 : 0.9015, 
    1.3 : 0.9032, 1.31 : 0.9049, 1.32 : 0.9066, 1.33 : 0.9082, 1.34 : 0.9099, 1.35 : 0.9115, 1.36 : 0.9131, 1.37 : 0.9147, 1.38 : 0.9162, 1.39 : 0.9177, 
    1.4 : 0.9192, 1.41 : 0.9207, 1.42 : 0.9222, 1.43 : 0.9236, 1.44 : 0.9251, 1.45 : 0.9265, 1.46 : 0.9279, 1.47 : 0.9292, 1.48 : 0.9306, 1.49 : 0.9319, 
    1.5 : 0.9332, 1.51 : 0.9345, 1.52 : 0.9357, 1.53 : 0.9370, 1.54 : 0.9382, 1.55 : 0.9394, 1.56 : 0.9406, 1.57 : 0.9418, 1.58 : 0.9429, 1.59 : 0.9441, 
    1.6 : 0.9452, 1.61 : 0.9463, 1.62 : 0.9474, 1.63 : 0.9484, 1.64 : 0.9495, 1.65 : 0.9505, 1.66 : 0.9515, 1.67 : 0.9525, 1.68 : 0.9535, 1.69 : 0.9545, 
    1.7 : 0.9554, 1.71 : 0.9564, 1.72 : 0.9573, 1.73 : 0.9582, 1.74 : 0.9591, 1.75 : 0.9599, 1.76 : 0.9608, 1.77 : 0.9616, 1.78 : 0.9625, 1.79 : 0.9633, 
    1.8 : 0.9641, 1.81 : 0.9649, 1.82 : 0.9656, 1.83 : 0.9664, 1.84 : 0.9671, 1.85 : 0.9678, 1.86 : 0.9686, 1.87 : 0.9693, 1.88 : 0.9699, 1.89 : 0.9706, 
    1.9 : 0.9713, 1.91 : 0.9719, 1.92 : 0.9726, 1.93 : 0.9732, 1.94 : 0.9738, 1.95 : 0.9744, 1.96 : 0.9750, 1.97 : 0.9756, 1.98 : 0.9761, 1.99 : 0.9767, 
    2.0 : 0.9772, 2.01 : 0.9778, 2.02 : 0.9783, 2.03 : 0.9788, 2.04 : 0.9793, 2.05 : 0.9798, 2.06 : 0.9803, 2.07 : 0.9808, 2.08 : 0.9812, 2.09 : 0.9817, 
    2.1 : 0.9821, 2.11 : 0.9826, 2.12 : 0.9830, 2.13 : 0.9834, 2.14 : 0.9838, 2.15 : 0.9842, 2.16 : 0.9846, 2.17 : 0.9850, 2.18 : 0.9854, 2.19 : 0.9857, 
    2.2 : 0.9861, 2.21 : 0.9864, 2.22 : 0.9868, 2.23 : 0.9871, 2.24 : 0.9875, 2.25 : 0.9878, 2.26 : 0.9881, 2.27 : 0.9884, 2.28 : 0.9887, 2.29 : 0.9890, 
    2.3 : 0.9893, 2.31 : 0.9896, 2.32 : 0.9898, 2.33 : 0.9901, 2.34 : 0.9904, 2.35 : 0.9906, 2.36 : 0.9909, 2.37 : 0.9911, 2.38 : 0.9913, 2.39 : 0.9916, 
    2.4 : 0.9918, 2.41 : 0.9920, 2.42 : 0.9922, 2.43 : 0.9925, 2.44 : 0.9927, 2.45 : 0.9929, 2.46 : 0.9931, 2.47 : 0.9932, 2.48 : 0.9934, 2.49 : 0.9936, 
    2.5 : 0.9938, 2.51 : 0.9940, 2.52 : 0.9941, 2.53 : 0.9943, 2.54 : 0.9945, 2.55 : 0.9946, 2.56 : 0.9948, 2.57 : 0.9949, 2.58 : 0.9951, 2.59 : 0.9952, 
    2.6 : 0.9953, 2.61 : 0.9955, 2.62 : 0.9956, 2.63 : 0.9957, 2.64 : 0.9959, 2.65 : 0.9960, 2.66 : 0.9961, 2.67 : 0.9962, 2.68 : 0.9963, 2.69 : 0.9964, 
    2.7 : 0.9965, 2.71 : 0.9966, 2.72 : 0.9967, 2.73 : 0.9968, 2.74 : 0.9969, 2.75 : 0.9970, 2.76 : 0.9971, 2.77 : 0.9972, 2.78 : 0.9973, 2.79 : 0.9974, 
    2.8 : 0.9974, 2.81 : 0.9975, 2.82 : 0.9976, 2.83 : 0.9977, 2.84 : 0.9977, 2.85 : 0.9978, 2.86 : 0.9979, 2.87 : 0.9979, 2.88 : 0.9980, 2.89 : 0.9981, 
    2.9 : 0.9981, 2.91 : 0.9982, 2.92 : 0.9982, 2.93 : 0.9983, 2.94 : 0.9984, 2.95 : 0.9984, 2.96 : 0.9985, 2.97 : 0.9985, 2.98 : 0.9986, 2.99 : 0.9986, 
    3.0 : 0.9987, 3.01 : 0.9987, 3.02 : 0.9987, 3.03 : 0.9988, 3.04 : 0.9988, 3.05 : 0.9989, 3.06 : 0.9989, 3.07 : 0.9989, 3.08 : 0.9990, 3.09 : 0.9990, 
    3.1 : 0.9990, 3.11 : 0.9991, 3.12 : 0.9991, 3.13 : 0.9991, 3.14 : 0.9992, 3.15 : 0.9992, 3.16 : 0.9992, 3.17 : 0.9992, 3.18 : 0.9993, 3.19 : 0.9993, 
    3.2 : 0.9993, 3.21 : 0.9993, 3.22 : 0.9994, 3.23 : 0.9994, 3.24 : 0.9994, 3.25 : 0.9994, 3.26 : 0.9994, 3.27 : 0.9995, 3.28 : 0.9995, 3.29 : 0.9995, 
    3.3 : 0.9995, 3.31 : 0.9995, 3.32 : 0.9995, 3.33 : 0.9996, 3.34 : 0.9996, 3.35 : 0.9996, 3.36 : 0.9996, 3.37 : 0.9996, 3.38 : 0.9996, 3.39 : 0.9997, 
    3.4 : 0.9997, 3.41 : 0.9997, 3.42 : 0.9997, 3.43 : 0.9997, 3.44 : 0.9997, 3.45 : 0.9997, 3.46 : 0.9997, 3.47 : 0.9997, 3.48 : 0.9997, 3.49 : 0.9998,
}

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

class Uniform():
    def __init__(self):         pass
    def solve(self, x, k):      return (1 / k)
    def solveWork(self, x, k):  return "(1 / "+str(k)+") = "
    def mean(self, x, k):
        a = 0
        for i in x:     a += i
        return (a / k)
    def variance(self, x, k):
        m = self.mean(x, k)
        n = 0
        for i in x:     n += ((i - m) * (i - m))
        return (n / k)

class Binomial():
    def __init__(self):             pass
    def solve(self, x, n, p):       return (ncr(n, x) * (p)**x * (1-p)**(n-x))
    def solveWork(self, x, n, p):   return "[ C("+str(n)+", "+str(x)+") * "+str(p)+"^"+str(x)+" * "+"(1-"+str(p)+")^"+"("+str(n)+"-"+str(x)+") ] + \t||| "+str(self.solve(x, n, p))
    def mean(self, x, n, p):        return (n * p)
    def variance(self, x, n, p):    return (n * p * (1 - p))

class NegativeBinomial():
    def __init__(self):             pass
    def solve(self, x, r, p):       return ncr(x-1, r-1) * ((1-p)**(x-r)) * (p**r) 
    def solveWork(self, x, r, p):   return "[ C("+str(x)+"-1, "+str(r)+"-1) * ((1-"+str(p)+")^("+str(x)+"-"+str(r)+")) * ("+str(p)+"^"+str(r)+") ] + \t||| "+str(self.solve(x, r, p)) 
    def mean(self, x, r, p):        return (r / p)
    def variance(self, x, r, p):    return ( (r * (1 - p)) / (p ** 2) )

class Hypergeometric():
    def __init__(self):             pass
    def solve(self, x, N, n, k):    return ( ( ncr(k, x) * ncr(N-k, n-x) ) / ncr(N, n) )
    def solveWork(self, x, N, n,k): return "( C("+str(k)+", "+str(x)+") * C("+str(N)+"-"+str(k)+", "+str(n)+"-"+str(x)+") ) / C("+str(N)+", "+str(n)+") ) = "
    def mean(self, x, N, n, k):     return ((n * k) / N)
    def variance(self, x, N, n, k): return ( ((N-n)/(N-1)) * n * (k / N) * (1 - (k / N)) )

class Multinomial():
    def __init__(self):             pass
    def solve(self, n, y, p):
        if len(y) != len(p):        return -1
        d = math.factorial(n) 
        for i in range(len(p)):     d = d * ( p[i]**y[i] )
        n = 1
        for i in range(len(y)):     n = n * ( math.factorial(y[i]) )
        if n == 0:                  return -2
        return (d / n)
    def mean(self, n, y, p, i):
        if len(y) != len(p):        return -1
        if len(y) < i:              return -2
        return (n * p[i-1])
    def variance(self, n, y, p, i):
        if len(y) != len(p):        return -1
        if len(y) < i:              return -2
        return (n * p[i-1] * (1 - p[i-1]))

class Poisson():
    def __init__(self):             self.e = 2.718281828
    def solve(self, x, u, t):       return ( ( (self.e**(-(u*t))) * ((u*t)**x) ) / (math.factorial(x)) )

class Normal():
    def __init__(self):                     self.e = 2.718281828
    def solve(self, x, u, sd):              return ( ( 1 / (sd * ( math.sqrt(2 * math.pi) ) ) ) * self.e ** ( -0.5 * ( ( (x - u) / (sd) ) ** 2 ) ) )
    def lessthan(self, x, u, sd):           return "P(Z < "+str(self.getZValue(x, u, sd))+") = " 
    def lessthanValue(self, x, u, sd):      return (NormalDistCurve[self.getZValue(x, u, sd)])
    def greaterthan(self, x, u, sd):        return "P(Z > "+str(self.getZValue(x, u, sd))+") = 1 - P(Z < "+str(self.getZValue(x, u, sd))+") = " 
    def greaterthanValue(self, x, u, sd):   return (1 - (NormalDistCurve[self.getZValue(x, u, sd)]))
    def getZValue(self, x, u, sd):          return round(( (x - u) / sd ), 2) 
    def findZValue(self, area):
        answer = []
        for i in NormalDistCurve:
            if NormalDistCurve[i] == area:  answer.append(i)
        return answer

class Exponential():
    def __init__(self):                     self.e = 2.718281828
    def solveX(self, x, b):                 return ( self.e ** ( -x / b ) )    
    def solveXWork(self, x, b):             return "P(T > "+str(x)+") = ∫("+str(x)+"->∞) (1/"+str(b)+") * e^(-x/"+str(b)+") dx \n = e^(-"+str(x)+"/"+str(b)+") \n = "  
    def solveY(self, x, l):                 return ( self.e ** ( -x * l ) )    
    def solveYWork(self, x, l):             return "P(T > "+str(x)+") = ∫("+str(x)+"->∞) ("+str(l)+") * e^(-x*"+str(l)+") dx \n = e^(-"+str(x)+"*"+str(l)+") \n = "  

class Gamma():
    def __init__(self):                     self.e = 2.718281828
    def solve(self, x, a, b):               return self.integrate(0, x, a, b, 0.001)
    def solveWork(self, x, a, b):           return "= P(X <= "+str(x)+") \n = F*("+str(x)+"; α="+str(a)+", β="+str(b)+") \n = "
    def solveBetween(self, x1, x2, a, b):   
        num1 = self.solve(x2, a, b)     
        num2 = self.solve(x1, a, b)     
        return (num1 - num2)
    def solveBetweenWork(self, x1, x2, a, b):   
        num1 = self.solve(x2, a, b)     
        num2 = self.solve(x1, a, b)     
        string = "= P("+str(x1)+" <= X <= "+str(x2)+") \n = F*("+str(x2)+"; α="+str(a)+", β="+str(b)+") - F*("+str(x1)+"; α="+str(a)+", β="+str(b)+") \n "
        string += "= "+str(num1)+" - "+str(num2)+" \n = "
        return string
    def integrate(self, x1, x2, a, b, dx=0.01):
        i = x1; s = 0
        while i <= x2:
            s += self.function(i, a, b)*dx
            i += dx
        return s
    def function(self, i, a, b):            return ( 1 / ( math.factorial(a-1) * ( b**a ) ) ) * ( i ** (a-1) ) * ( self.e**(-i / b) )

class Distribution():
    def __init__(self): 
        self.u = Uniform()
        self.b = Binomial()
        self.nb = NegativeBinomial()
        self.h = Hypergeometric()
        self.m = Multinomial()
        self.p = Poisson()
        self.n = Normal()
        self.e = Exponential()
        self.g = Gamma()
        self.help  = "-u  Uniform            |  [1,2,3,...k] | k \n"
        self.help += "-b  Binomial b(x;n,p)  |  x | n | p  OR  [x...] | [n...] | p   \n"
        self.help += "-nb Negative Binomial  |  x | r | p  OR  [x...] | [r...] | p   \n"
        self.help += "-h  Hypergeometric     |  x | N | n | k                    | h(x;N,n,k)    \n"
        self.help += "-m  Multinomial        |  n | [y1,y2,...,yk] | [p1,p2,...,pk] | i    \n"
        self.help += "-p  Poisson p(x;μ,t)   |  x | μ | t  OR  [x...] | μ | t   \n"
        self.help += "-n  Normal             |  x | μ | σ  OR  [x1,x2] | μ | σ   | -solve -lessthan -greaterthan    \n"
        self.help += "-e  Exponential        |  x | β                            | -x     -y   \n"
        self.help += "-g  Gamma              |  x | α | β  OR  x1 | x2 | α | β     \n"
        self.help += "-f     Fraction        |  Makes result a fraction   \n"
        self.help += "-round <SINGLE_DIGIT>  |  Rounds the result to the near SINGLE_DIGIT   \n"
        self.help += "-solve Sovle           |  -u  -b  -nb  -h  -m  -n     \n"
        self.help += "-mean  Mean E[x]       |  -u  -b  -nb  -h  -m     \n"
        self.help += "-var   Variance        |  -u  -b  -nb  -h  -m     \n"
        self.help += "-help                  |  This help text  \n"
        self.help += "exit   ==> exit        |     \n"
    def run(self):
        command = ""
        print(self.help)
        while (command.lower() != "exit"):
            command = input("\nEnter : ")
            answerText = ""            
            print(answerText, self.runCommand(command))
    def runCommand(self, command):
        answerText = ""
        answer = 0
        try:
            if "-help" in command:  print(self.help)
            elif "-u" in command:   
                c = self.removefromString(command, ["-u", "-solve", "-mean", "-var", "-f"])
                arr = c.split("|")
                if len(arr) != 2:   answer = "Cannot find list and number '[1,2,...,k] | k'"
                else:
                    l = json.loads(arr[0])
                    n = float(arr[1])
                    if "-solve" in command:     answer = self.u.solve(l, n)     ;   answerText = self.u.solveWork(1, n)
                    elif "-mean" in command:    answer = self.u.mean(l, n)
                    elif "-var" in command:     answer = self.u.variance(l, n)
            elif "-b" in command:   
                c = self.removefromString(command, ["-b", "-solve", "-mean", "-var", "-f"])
                arr = c.split("|")
                if len(arr) != 3:   answer = "Cannot find 3 numbers 'x | n | p'"
                else:
                    xa = []
                    na = []
                    try:    xa.append(int(arr[0]))
                    except: xa = json.loads(arr[0])
                    try:    na.append(int(arr[1]))
                    except: na = json.loads(arr[1])
                    p = float(arr[2])
                    for x in xa:
                        for n in na:
                            if "-solve" in command:     answer += self.b.solve(x, n, p)     ;   answerText += self.b.solveWork(x, n, p) + "\n "
                            elif "-mean" in command:    answer += self.b.mean(x, n, p)
                            elif "-var" in command:     answer += self.b.variance(x, n, p)
                    answerText += "= "
            elif "-nb" in command:  
                c = self.removefromString(command, ["-nb", "-solve", "-mean", "-var", "-f"])
                arr = c.split("|")
                if len(arr) != 3:   answer = "Cannot find 3 numbers 'x | r | p'"
                else:
                    xa = []
                    ra = []
                    try:    xa.append(int(arr[0]))
                    except: xa = json.loads(arr[0])
                    try:    ra.append(int(arr[1]))
                    except: ra = json.loads(arr[1])
                    p = float(arr[2])
                    for x in xa:
                        for r in ra:
                            if "-solve" in command:     answer += self.nb.solve(x, r, p)    ;   answerText += self.nb.solveWork(x, r, p) + "\n "
                            elif "-mean" in command:    answer += self.nb.mean(x, r, p)
                            elif "-var" in command:     answer += self.nb.variance(x, r, p)
                    answerText += "= "
            elif "-h" in command:   
                c = self.removefromString(command, ["-h", "-solve", "-mean", "-var", "-f"])
                arr = c.split("|")
                if len(arr) != 4:   answer = "Cannot find 4 numbers 'x | N | n | k'"
                else:
                    x = int(arr[0])
                    N = int(arr[1])
                    n = int(arr[2])
                    k = int(arr[3])
                    if "-solve" in command:     answer = self.h.solve(x, N, n, k)       ;   answerText = self.h.solveWork(x, N, n, k)  
                    elif "-mean" in command:    answer = self.h.mean(x, N, n, k)
                    elif "-var" in command:     answer = self.h.variance(x, N, n, k)
            elif "-m" in command:   
                c = self.removefromString(command, ["-mean", "-solve", "-m", "-var", "-f"])
                arr = c.split("|")
                if len(arr) < 3:   answer = "Cannot find numbers and 2 lists 'n | [y1,y2,...,yk] | [p1,p2,...,pk] | i'"
                else:
                    n = int(arr[0])
                    y = json.loads(arr[1])
                    p = json.loads(arr[2])
                    i = 1
                    if len(arr) == 4:   i = int(arr[3])
                    if "-solve" in command:     answer = self.m.solve(n, y, p)
                    elif "-mean" in command:    answer = self.m.mean(n, y, p, i)
                    elif "-var" in command:     answer = self.m.variance(n, y, p, i)
            elif "-p" in command:   
                c = self.removefromString(command, ["-mean", "-solve", "-p", "-var", "-f"])
                arr = c.split("|")
                if len(arr) < 3:   answer = "Cannot find 3 numbers 'x | u | t'  OR  '[x...] | u | t' "
                else:
                    xa = []
                    try:    xa.append(int(arr[0]))
                    except: xa = json.loads(arr[0])
                    # x = int(arr[0])
                    u = float(arr[1])
                    t = float(arr[2])
                    for x in xa:
                        answer += self.p.solve(x, u, t)
            elif "-n" in command:   
                c = self.removefromString(command, ["-n", "-solve", "-mean", "-var", "-f", "-lessthan", "-greaterthan"])
                arr = c.split("|")
                if len(arr) == 1:
                    answer = self.n.findZValue(float(arr[0]))
                elif len(arr) < 3:   answer = "Cannot find number 'z' OR 3 numbers 'x | μ | σ' OR ranged '[n1, n2] | μ | σ'"
                elif len(arr) == 3:
                    xa = []
                    try:    xa.append(float(arr[0]))
                    except: xa = json.loads(arr[0])
                    # x = float(arr[0])
                    u = float(arr[1])
                    sd = float(arr[2])
                    if len(xa) == 1:
                        if "-solve" in command:         answer = self.n.solve(xa[0], u, sd)         
                        elif "-lessthan" in command:    answer = self.n.lessthanValue(xa[0], u, sd)     ;   answerText = self.n.lessthan(xa[0], u, sd)
                        elif "-greaterthan" in command: answer = self.n.greaterthanValue(xa[0], u, sd)  ;   answerText = self.n.greaterthan(xa[0], u, sd)
                    elif len(xa) == 2:
                        # if "-inside" in command:        
                        val1 = self.n.lessthanValue(xa[1], u, sd)
                        val2 = self.n.lessthanValue(xa[0], u, sd)
                        ans = self.n.lessthanValue(xa[1], u, sd) - self.n.lessthanValue(xa[0], u, sd)
                        answerText = "P(Z < "+str(self.n.getZValue(xa[1], u, sd))+") - P(Z < "+str(self.n.getZValue(xa[0], u, sd))+") = "
                        answerText += str(val1) + " - " + str(val2) + " = " 
                        answer = (ans)
                        # if "-outside" in command:       answer = self.n.greaterthan(x, u, sd)
                    else: answer = "Passed in more than 2 values for range"
            elif "-e" in command:
                c = self.removefromString(command, ["-e", "-solve", "-mean", "-var", "-f", "-lessthan", "-greaterthan", "-x", "-y"])
                arr = c.split("|")
                if len(arr) == 2:
                    x = float(arr[0])
                    b = float(arr[1])
                    if "-x" in command:     answer = self.e.solveX(x, b)    ;   answerText = self.e.solveXWork(x, b)
                    elif "-y" in command:   answer = self.e.solveY(x, b)    ;   answerText = self.e.solveYWork(x, b)
                    else:                   answer = "-x or -y not specified"
                else:       answer = "Cannot find numbers 'x | β'"
            elif "-g" in command:
                c = self.removefromString(command, ["-g", "-solve", "-mean", "-var", "-f", "-lessthan", "-greaterthan"])
                arr = c.split("|")
                if len(arr) == 3:
                    x = float(arr[0])
                    a = float(arr[1])
                    b = float(arr[2])
                    answer = self.g.solve(x, a, b)
                    answerText = self.g.solveWork(x, a, b)
                elif len(arr) == 4:     
                    x1 = float(arr[0])
                    x2 = float(arr[1])
                    a = float(arr[2])
                    b = float(arr[3])
                    answer = self.g.solveBetween(x1, x2, a, b)
                    answerText = self.g.solveBetweenWork(x1, x2, a, b)
                else:       answer = "Cannot find numbers 'x | α | β'  OR  'x1 | x2 | α | β'"
            if "-round" in command: 
                index = command.find('-round')
                if index != -1: 
                    roundNum = int((command[index+6:])[:2])
                    answer = round(answer, roundNum)
            if "-f" in command:     answer = str(Fraction(answer))  
        except Exception as e: print("Error : ",e)
        return str(answerText)+str(answer)
    def removefromString(self, string, arr):
        for i in arr:   string = string.replace(i, "")
        index = string.find('-round')
        if index != -1: string = string[:index] + string[index+8:]
        return string.strip()

d = Distribution()
if len(sys.argv) > 1:
    command = ""
    for i in sys.argv[1:]:   command += i
    print(d.runCommand(command))
else:
    d.run()

# =======================================================
# EXAMPLE COMMAND LINE INPUTS:
# =======================================================
# For Uniform
# -u -solve [1, 2, 3, 4, 5, 6] | 6                  
# -u -mean [1, 2, 3, 4, 5, 6] | 6
# -u -mean -f [1,2,3,4,5,6] | 6
# -u -var [1,2,3,4,5,6] | 6
# -------------------------------------------------------
# For Binomial
# -b -solve 0 | 3 | 0.25
# -b -mean 0 | 3 | 0.25
# -b -mean -f 0 | 3 | 0.25
# -b -var 0 | 3 | 0.25
# =======================================================


# u = Uniform()
# print(str((u.solve(           [1, 2, 3, 4, 5, 6], 6))))
# print(str(Fraction(u.mean(    [1, 2, 3, 4, 5, 6], 6))))
# print(str((u.variance(        [1, 2, 3, 4, 5, 6], 6))))

# b = Binomial()
# print(str(Fraction(b.solve(       0, 3, 0.25))))
# print(str(Fraction(b.mean(        0, 3, 0.25))))
# print(str(Fraction(b.variance(    0, 3, 0.25))))

# n = NegativeBinomial()
# print(str((n.solve(         8, 3, 0.3))))
# print(str(Fraction(n.mean(  8, 3, 0.3))))
# print(str((n.variance(      8, 3, 0.3))))

# h = Hypergeometric()
# print(str((h.solve(         1, 40, 5, 3))))
# print(str(Fraction(h.mean(  1, 40, 5, 3))))
# print(str((h.variance(      1, 40, 5, 3))))

# m = Multinomial()
# print(str((m.solve(         8, [4, 3, 1], [0.5, 0.3, 0.2] ))))
# print(str(Fraction(m.mean(  8, [4, 3, 1], [0.5, 0.3, 0.2], 1 ))))
# print(str((m.variance(      8, [4, 3, 1], [0.5, 0.3, 0.2], 1 ))))

# p = Poisson()
# print(str((p.solve(  7, 6, 1))))
# print(str((p.solve(  10, 6, 2 ))))


