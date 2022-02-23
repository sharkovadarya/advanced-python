import os
import sys

import numpy as np
import matrix_easy
import matrix_medium


# in lieu of appropriate methods which are supposed to be implemented in medium task. this is for the simple task
def matrix_to_lines(m):
    return [" ".join([str(x) for x in row]) + "\n" for row in m.values]


def check_and_write_res(res, expected, filenames, path, write_func):
    for i in range(len(res)):
        if res[i].values == expected[i].tolist():
            with open(os.path.join(path, filenames[i]), "w+") as f:
                write_func(res[i], f)
        else:
            raise RuntimeError("Incorrect computation results")


def compute_and_write_res_easy(res_path_easy, res_path_medium):
    a_values = np.random.randint(0, 10, (10, 10))
    b_values = np.random.randint(0, 10, (10, 10))

    a_matrix_easy = matrix_easy.Matrix(a_values.tolist())
    b_matrix_easy = matrix_easy.Matrix(b_values.tolist())

    sum_matrix_easy = a_matrix_easy + b_matrix_easy
    mul_elem_matrix_easy = a_matrix_easy * b_matrix_easy
    mul_matrix_easy = a_matrix_easy @ b_matrix_easy

    a_matrix_medium = matrix_medium.Matrix(a_values.tolist())
    b_matrix_medium = matrix_medium.Matrix(b_values.tolist())

    sum_matrix_medium = a_matrix_medium + b_matrix_medium
    mul_elem_matrix_medium = a_matrix_medium * b_matrix_medium
    mul_matrix_medium = a_matrix_medium @ b_matrix_medium

    a_np = np.array(a_values)
    b_np = np.array(b_values)

    sum_np = a_np + b_np
    mul_elem_np = a_np * b_np
    mul_np = a_np @ b_np

    expected = [sum_np, mul_elem_np, mul_np]
    filenames = ["matrix+.txt", "matrix*.txt", "matrix@.txt"]
    check_and_write_res([sum_matrix_easy, mul_elem_matrix_easy, mul_matrix_easy], expected, filenames, res_path_easy,
                        lambda m, f: f.writelines(matrix_to_lines(m)))
    check_and_write_res([sum_matrix_medium, mul_elem_matrix_medium, mul_matrix_medium], expected, filenames,
                        res_path_medium, lambda m, f: m.write_to_file(f))


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        compute_and_write_res_easy(sys.argv[1], sys.argv[2])
    else:
        print("Provide artifact paths as an argument.")
